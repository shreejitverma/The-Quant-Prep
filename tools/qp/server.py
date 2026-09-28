"""Local web dashboard: a stdlib HTTP server exposing a JSON API over the same vault and
state file the CLI uses, plus the static single-page app in ``web/``.

Security model: binds to 127.0.0.1 by default; state-changing requests must be JSON
POSTs and are rejected when an ``Origin`` header names a different host (blocks
cross-site requests from other pages open in the browser). Static file serving is
confined to the repo and to an allowlist of extensions.
"""

from __future__ import annotations

import datetime as dt
import json
import mimetypes
import secrets
import threading
import time
import webbrowser
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

from . import drills, planner
from .state import GRADES, MASTERY_LABELS, StateError, Store, today
from .vault import TRACK_LABELS, TRACKS, Note, Vault, load_vault

WEB_DIR = Path(__file__).with_name("web")
FILE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".py", ".cpp", ".hpp", ".h", ".md", ".txt", ".csv", ".ipynb", ".pdf"}
TEXT_EXTS = {".py", ".cpp", ".hpp", ".h", ".md", ".txt", ".csv", ".ipynb"}
VAULT_TTL = 2.0  # seconds; notes are re-read at most this often so edits show up live
MAX_BODY = 64 * 1024
CDN = "https://cdn.jsdelivr.net"
# Scripts only from this server and the pinned (SRI-checked) CDN files; KaTeX needs inline styles and fonts.
CSP = (
    f"default-src 'self'; script-src 'self' {CDN}; style-src 'self' 'unsafe-inline' {CDN}; font-src {CDN}; "
    "img-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'"
)
MAX_GAMES = 64


class ApiError(Exception):
    def __init__(self, status: HTTPStatus, message: str):
        super().__init__(message)
        self.status = status


class App:
    """Request-independent application state shared by handler threads."""

    def __init__(self, store: Store, vault_loader=load_vault):
        self.store = store
        self._loader = vault_loader
        self._vault: Vault | None = None
        self._loaded_at = 0.0
        self._lock = threading.Lock()
        self.games: dict[str, drills.MarketMakingGame] = {}

    @property
    def vault(self) -> Vault:
        with self._lock:
            if self._vault is None or time.monotonic() - self._loaded_at > VAULT_TTL:
                self._vault = self._loader()
                self._loaded_at = time.monotonic()
            return self._vault

    # --- views ------------------------------------------------------------
    def topic_row(self, n: Note) -> dict:
        s = self.store
        return {
            "id": n.id,
            "title": n.title,
            "type": n.type,
            "tier": n.tier,
            "status": n.status,
            "tracks": n.tracks,
            "hours": n.est_hours,
            "cards": len(n.cards),
            "prereqs": n.prereqs,
            "path": n.path.as_posix(),
            "mastery": s.mastery(n.id) if n.trackable else None,
            "readiness": round(planner.topic_readiness(s, n), 3) if n.trackable else None,
        }

    def summary(self) -> dict:
        v, s = self.vault, self.store
        tracks = s.profile["tracks"]
        track_rows = []
        for t in TRACKS:
            ts = planner.track_summary(v, s, t)
            track_rows.append(
                {
                    "track": t,
                    "label": TRACK_LABELS[t],
                    "readiness": round(ts.readiness, 3),
                    "solid": ts.solid,
                    "topics": ts.topics,
                    "hours_left": round(ts.hours_left, 1),
                    "active": t in tracks,
                }
            )
        sections = []
        for sec in v.sections:
            topics = [n for n in sec.notes if n.trackable]
            if not topics:
                continue
            sections.append(
                {
                    "folder": sec.folder,
                    "title": sec.title,
                    "topics": len(topics),
                    "written": sum(n.status in ("solid", "canonical") for n in topics),
                    "readiness": round(planner.weighted_readiness(s, topics), 3),
                }
            )
        firms = sorted(
            (
                {"id": f.id, "title": f.title, "type": f.meta.get("firm_type"), "readiness": round(planner.firm_readiness(v, s, f), 3)}
                for f in v.firms()
            ),
            key=lambda r: -r["readiness"],
        )
        start = today() - dt.timedelta(days=181)
        activity = {d: a for d, a in s.data["activity"].items() if d >= start.isoformat()}
        best: dict[str, float] = {}
        for d in s.data["drills"]:
            best[d["mode"]] = max(best.get(d["mode"], d["score"]), d["score"])
        return {
            "today": today().isoformat(),
            "profile": s.profile,
            "streak": s.streak(),
            "tracks": track_rows,
            "counts": planner.counts(v, s, tracks),
            "queue": len(planner.due_cards(v, s, tracks)),
            "next": [{**self.topic_row(n), "blocked_by": b} for n, b in planner.next_topics(v, s, tracks, 6)],
            "sections": sections,
            "firms": firms,
            "activity": activity,
            "best": best,
            "drills": s.data["drills"][-30:],
            "mastery_labels": MASTERY_LABELS,
            "notes": len(v.notes),
            "cards_total": len(v.cards),
        }

    def catalog(self) -> dict:
        v = self.vault
        out = []
        for sec in v.sections:
            out.append(
                {
                    "folder": sec.folder,
                    "title": sec.title,
                    "library": sec.library,
                    "notes": [self.topic_row(n) for n in sec.notes if not n.id.startswith("moc:")],
                    "readme": next((n.id for n in sec.notes if n.id == f"moc:{sec.folder}"), None),
                }
            )
        return {"sections": out, "mastery_labels": MASTERY_LABELS, "tracks": TRACK_LABELS}

    def note(self, nid: str) -> dict:
        v, s = self.vault, self.store
        n = v.notes.get(nid) or v.resolve(nid)
        if n is None:
            raise ApiError(HTTPStatus.NOT_FOUND, f"no note {nid!r}")
        paths = {x.path.as_posix(): x.id for x in v.notes.values()}
        return {
            **self.topic_row(n),
            "meta": n.meta,
            "body": n.body,
            "prereq_rows": [{"id": p, "title": v.notes[p].title if p in v.notes else p, "mastery": s.mastery(p)} for p in n.prereqs],
            "unlocks": [{"id": m.id, "title": m.title} for m in v.notes.values() if n.id in m.prereqs],
            "card_rows": [{"id": c.id, "due": s.card(c.id).due, "interval": s.card(c.id).interval} for c in n.cards],
            "paths": paths,
        }

    def queue(self, limit: int) -> list[dict]:
        v, s = self.vault, self.store
        out = []
        for c in planner.due_cards(v, s, s.profile["tracks"], limit):
            sched = s.card(c.id)
            out.append(
                {
                    "id": c.id,
                    "prompt": c.prompt,
                    "answer": c.answer,
                    "note_id": c.note_id,
                    "note_title": v.notes[c.note_id].title,
                    "new": not sched.due,
                    "interval": sched.interval,
                }
            )
        return out

    def plan(self, hours: float | None, tiers: tuple[str, ...]) -> dict:
        v, s = self.vault, self.store
        h = hours or float(s.profile.get("hours_per_week", 10))
        weeks = planner.weekly_plan(v, s, s.profile["tracks"], h, tiers)
        return {
            "hours_per_week": h,
            "tiers": tiers,
            "total_hours": round(sum(w["hours"] for w in weeks), 1),
            "weeks": [{**w, "hours": round(w["hours"], 1), "topics": [self.topic_row(n) for n in w["topics"]]} for w in weeks],
        }

    def firm(self, fid: str) -> dict:
        v = self.vault
        f = v.notes.get(fid)
        if f is None or f.type != "firm":
            raise ApiError(HTTPStatus.NOT_FOUND, f"no firm {fid!r}")
        focus = planner.firm_focus(v, f)
        return {
            "id": f.id,
            "title": f.title,
            "type": f.meta.get("firm_type"),
            "status": f.status,
            "readiness": round(planner.firm_readiness(v, self.store, f), 3),
            "focus": sorted((self.topic_row(n) for n in focus), key=lambda r: r["readiness"]),
            "body": f.body,
            "path": f.path.as_posix(),
            "paths": {x.path.as_posix(): x.id for x in v.notes.values()},
        }

    # --- drills -----------------------------------------------------------
    def problems(self, mode: str, n: int, seed: int | None) -> list[dict]:
        gen = drills.problems(mode, seed)
        out = []
        for _ in range(n):
            p = next(gen)
            out.append(
                {"text": p.text, "num": p.answer.numerator, "den": p.answer.denominator, "tol": float(p.tolerance), "answer": p.answer_text}
            )
        return out

    def mm_new(self) -> dict:
        if len(self.games) >= MAX_GAMES:
            self.games.pop(next(iter(self.games)))
        gid = secrets.token_hex(8)
        self.games[gid] = drills.MarketMakingGame()
        return {"game": gid, "state": self.games[gid].state()}

    def mm_quote(self, gid: str, bid, ask) -> dict:
        game = self.games.get(gid)
        if game is None:
            raise ApiError(HTTPStatus.NOT_FOUND, "unknown or expired game")
        try:
            event = game.quote(int(bid), int(ask))
        except (TypeError, ValueError) as exc:
            raise ApiError(HTTPStatus.BAD_REQUEST, str(exc)) from exc
        if game.finished:
            s = game.summary()
            self.store.record_drill("mm", s["trades"], s["trades"] - s["informed_trades"], 0, s["pnl"], {"summary": s})
            self.games.pop(gid, None)
        return {"event": event, "state": game.state()}


def make_handler(app: App, allowed_origins: set[str]):
    allowed_hosts = {o.split("://", 1)[1] for o in allowed_origins}

    class Handler(BaseHTTPRequestHandler):
        server_version = "qp"

        def log_message(self, fmt, *args):  # quiet by default; errors still surface as JSON
            pass

        # --- plumbing -----------------------------------------------------
        def send_json(self, payload, status: HTTPStatus = HTTPStatus.OK) -> None:
            body = json.dumps(payload).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def send_file(self, path: Path, ctype: str | None = None) -> None:
            data = path.read_bytes()
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", ctype or mimetypes.guess_type(path.name)[0] or "application/octet-stream")
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "no-cache")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            self.wfile.write(data)

        def end_headers(self) -> None:
            self.send_header("Content-Security-Policy", CSP)
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            super().end_headers()

        def check_host(self) -> None:
            # Blocks DNS rebinding: a hostile page resolving its own name to 127.0.0.1 sends its own Host.
            if self.headers.get("Host") not in allowed_hosts:
                raise ApiError(HTTPStatus.FORBIDDEN, "unexpected Host header")

        def read_json(self) -> dict:
            origin = self.headers.get("Origin")
            if origin and origin not in allowed_origins:
                raise ApiError(HTTPStatus.FORBIDDEN, "cross-origin request refused")
            if self.headers.get("Sec-Fetch-Site") == "cross-site":
                raise ApiError(HTTPStatus.FORBIDDEN, "cross-site request refused")
            mime = (self.headers.get("Content-Type") or "").split(";", 1)[0].strip().lower()
            if mime != "application/json":
                raise ApiError(HTTPStatus.UNSUPPORTED_MEDIA_TYPE, "send application/json")
            length = int(self.headers.get("Content-Length") or 0)
            if length > MAX_BODY:
                raise ApiError(HTTPStatus.REQUEST_ENTITY_TOO_LARGE, "request too large")
            try:
                data = json.loads(self.rfile.read(length) or b"{}")
            except json.JSONDecodeError as exc:
                raise ApiError(HTTPStatus.BAD_REQUEST, f"invalid JSON: {exc}") from exc
            if not isinstance(data, dict):
                raise ApiError(HTTPStatus.BAD_REQUEST, "expected a JSON object")
            return data

        def dispatch(self, method: str) -> None:
            url = urlparse(self.path)
            q = {k: v[-1] for k, v in parse_qs(url.query).items()}
            try:
                self.check_host()
                # One request at a time against the store: local single-user app, and it rules out
                # races between concurrent grades, summaries and game quotes. Pick up edits made by
                # other processes (a terminal `qp review`) before handling the request.
                with app.store.lock:
                    app.store.refresh()
                    if method == "GET":
                        self.get(url.path, q)
                    else:
                        self.post(url.path, self.read_json())
            except ApiError as exc:
                self.send_json({"error": str(exc)}, exc.status)
            except StateError as exc:
                self.send_json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)
            except BrokenPipeError:
                pass
            except Exception as exc:  # surface, never swallow: the UI shows the message
                self.send_json({"error": f"internal error: {type(exc).__name__}: {exc}"}, HTTPStatus.INTERNAL_SERVER_ERROR)
                raise

        def do_GET(self):
            self.dispatch("GET")

        def do_POST(self):
            self.dispatch("POST")

        # --- routes -------------------------------------------------------
        def get(self, path: str, q: dict) -> None:
            if path.startswith("/api/"):
                parts = path[5:].split("/", 1)
                route, arg = parts[0], unquote(parts[1]) if len(parts) > 1 else ""
                if route == "summary":
                    return self.send_json(app.summary())
                if route == "catalog":
                    return self.send_json(app.catalog())
                if route == "note" and arg:
                    return self.send_json(app.note(arg))
                if route == "queue":
                    return self.send_json(app.queue(int(q.get("limit", 50))))
                if route == "plan":
                    tiers = (
                        ("core",)
                        if q.get("tiers") == "core"
                        else ("core", "advanced")
                        if q.get("tiers") == "no-senior"
                        else ("core", "advanced", "senior")
                    )
                    return self.send_json(app.plan(float(q["hours"]) if q.get("hours") else None, tiers))
                if route == "firm" and arg:
                    return self.send_json(app.firm(arg))
                if route == "problems":
                    mode = q.get("mode", "arith")
                    if mode not in drills.GENERATORS:
                        raise ApiError(HTTPStatus.BAD_REQUEST, f"unknown mode {mode!r}")
                    n = max(1, min(int(q.get("n", 200)), 1000))
                    return self.send_json(app.problems(mode, n, int(q["seed"]) if q.get("seed") else None))
                raise ApiError(HTTPStatus.NOT_FOUND, f"no route {path}")
            if path.startswith("/files/"):
                return self.serve_repo_file(unquote(path[len("/files/") :]))
            name = "index.html" if path in ("/", "/index.html") else path.lstrip("/")
            target = (WEB_DIR / name).resolve()
            if target.parent != WEB_DIR.resolve() or not target.is_file():
                raise ApiError(HTTPStatus.NOT_FOUND, "not found")
            return self.send_file(target)

        def serve_repo_file(self, rel: str) -> None:
            root = app.vault.root.resolve()
            target = (root / rel).resolve()
            if root not in target.parents or target.suffix.lower() not in FILE_EXTS or not target.is_file():
                raise ApiError(HTTPStatus.NOT_FOUND, "not found")
            ctype = "text/plain; charset=utf-8" if target.suffix.lower() in TEXT_EXTS else None
            return self.send_file(target, ctype)

        def post(self, path: str, body: dict) -> None:
            if path == "/api/mark":
                note = app.vault.notes.get(str(body.get("id")))
                if note is None or not note.trackable:
                    raise ApiError(HTTPStatus.NOT_FOUND, "no such topic")
                app.store.set_mastery(note.id, int(body.get("level", -1)))
                return self.send_json(app.topic_row(note))
            if path == "/api/grade":
                cid, grade = str(body.get("card")), str(body.get("grade"))
                if cid not in app.vault.cards:
                    raise ApiError(HTTPStatus.NOT_FOUND, "no such card")
                if grade not in GRADES:
                    raise ApiError(HTTPStatus.BAD_REQUEST, f"grade must be one of {GRADES}")
                return self.send_json(app.store.grade(cid, grade).to_dict())
            if path == "/api/profile":
                tracks = body.get("tracks")
                if tracks is not None and (not isinstance(tracks, list) or not tracks or any(t not in TRACKS for t in tracks)):
                    raise ApiError(HTTPStatus.BAD_REQUEST, f"tracks must be a non-empty subset of {TRACKS}")
                hours = body.get("hours_per_week")
                if hours is not None and not (isinstance(hours, (int, float)) and 0 < hours <= 100):
                    raise ApiError(HTTPStatus.BAD_REQUEST, "hours_per_week must be in (0, 100]")
                app.store.set_profile(tracks=tracks, hours_per_week=hours)
                return self.send_json(app.store.profile)
            if path == "/api/drill":
                mode = str(body.get("mode"))
                if mode not in drills.GENERATORS:
                    raise ApiError(HTTPStatus.BAD_REQUEST, "unknown drill mode")
                attempts, correct = int(body.get("attempts", 0)), int(body.get("correct", 0))
                if not 0 <= correct <= attempts <= 10_000:
                    raise ApiError(HTTPStatus.BAD_REQUEST, "inconsistent drill counts")
                return self.send_json(app.store.record_drill(mode, attempts, correct, float(body.get("seconds", 0)), correct))
            if path == "/api/mm/new":
                return self.send_json(app.mm_new())
            if path == "/api/mm/quote":
                return self.send_json(app.mm_quote(str(body.get("game")), body.get("bid"), body.get("ask")))
            raise ApiError(HTTPStatus.NOT_FOUND, f"no route {path}")

    return Handler


def serve(store: Store, host: str = "127.0.0.1", port: int = 8765, open_browser: bool = False) -> None:
    app = App(store)
    origins = {f"http://{host}:{port}", f"http://localhost:{port}", f"http://127.0.0.1:{port}"}
    httpd = ThreadingHTTPServer((host, port), make_handler(app, origins))
    url = f"http://{'127.0.0.1' if host in ('0.0.0.0', '') else host}:{port}/"
    print(f"qp: dashboard at {url} (state {store.path}); Ctrl-C to stop")
    if open_browser:
        threading.Timer(0.5, webbrowser.open, args=(url,)).start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print()
    finally:
        httpd.server_close()
