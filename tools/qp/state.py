"""Learner state: topic mastery, card scheduling, drill history and activity.

State is personal, so it lives outside the repo by default
(``$QP_HOME/state.json``, default ``~/.local/share/quant-prep/state.json``).
Point ``QP_HOME`` at a private, backed-up directory to keep it across machines.
Writes are atomic (temp file + rename), so a crash never leaves a torn file.
"""

from __future__ import annotations

import contextlib
import datetime as dt
import json
import os
import shutil
import tempfile
import threading
from dataclasses import dataclass
from pathlib import Path

try:  # POSIX advisory locks; on Windows only the in-process lock applies
    import fcntl
except ImportError:  # pragma: no cover
    fcntl = None

SCHEMA_VERSION = 1
MASTERY_LABELS = ("unseen", "studied", "practiced", "solid", "interview-ready")
GRADES = ("again", "hard", "good", "easy")
MIN_EASE = 1.3
DEFAULT_PROFILE = {"tracks": ["quant-trader", "quant-research", "quant-dev"], "hours_per_week": 10, "new_cards_per_day": 20}


class StateError(RuntimeError):
    pass


def default_home() -> Path:
    env = os.environ.get("QP_HOME")
    if env:
        return Path(env).expanduser()
    base = os.environ.get("XDG_DATA_HOME") or str(Path.home() / ".local" / "share")
    return Path(base) / "quant-prep"


def today() -> dt.date:
    override = os.environ.get("QP_TODAY")  # deterministic tests and time travel
    return dt.date.fromisoformat(override) if override else dt.date.today()


def now_iso() -> str:
    return dt.datetime.now().replace(microsecond=0).isoformat()


def empty_state() -> dict:
    return {"version": SCHEMA_VERSION, "profile": dict(DEFAULT_PROFILE), "topics": {}, "cards": {}, "drills": [], "activity": {}}


@dataclass
class CardSchedule:
    ease: float = 2.5
    interval: int = 0  # days
    reps: int = 0  # consecutive successful reviews
    lapses: int = 0
    due: str = ""  # ISO date; empty means never reviewed (new)
    last: str = ""

    @classmethod
    def from_dict(cls, d: dict) -> CardSchedule:
        return cls(**{k: d[k] for k in ("ease", "interval", "reps", "lapses", "due", "last") if k in d})

    def to_dict(self) -> dict:
        return {
            "ease": round(self.ease, 3),
            "interval": self.interval,
            "reps": self.reps,
            "lapses": self.lapses,
            "due": self.due,
            "last": self.last,
        }


def schedule(card: CardSchedule, grade: str, on: dt.date) -> CardSchedule:
    """SM-2 style scheduling with four Anki-like grades.

    again: lapse, due again today (relearn in the same session), ease -0.2.
    hard:  interval x1.2 (at least 1 day), ease -0.15.
    good:  1 day, then 3 days, then interval x ease.
    easy:  4 days on a new card, otherwise interval x ease x 1.3, ease +0.15.
    """
    if grade not in GRADES:
        raise StateError(f"unknown grade {grade!r}; use one of {', '.join(GRADES)}")
    c = CardSchedule(**card.to_dict())
    if grade == "again":
        c.lapses += 1 if c.reps or c.interval else 0
        c.reps = 0
        c.interval = 0
        c.ease = max(MIN_EASE, c.ease - 0.2)
    elif grade == "hard":
        c.interval = max(1, round(c.interval * 1.2))
        c.ease = max(MIN_EASE, c.ease - 0.15)
        c.reps += 1
    elif grade == "good":
        c.interval = 1 if c.reps == 0 else 3 if c.reps == 1 else max(c.interval + 1, round(c.interval * c.ease))
        c.reps += 1
    else:
        c.interval = 4 if c.reps == 0 else max(c.interval + 1, round(c.interval * c.ease * 1.3))
        c.ease += 0.15
        c.reps += 1
    c.due = (on + dt.timedelta(days=c.interval)).isoformat()
    c.last = on.isoformat()
    return c


class Store:
    """Owner of the state file, safe across threads and processes.

    Every mutation is a transaction: take the in-process lock and an exclusive
    ``fcntl`` lock on ``state.lock``, re-read the file if another process changed it,
    apply the change, then write atomically (temp file, fsync, rename, directory fsync,
    previous version kept as ``state.json.bak``). So ``qp serve`` and a terminal
    ``qp review`` can run at once without losing each other's updates.
    Long-lived readers (the server) call ``refresh()`` before reading.
    """

    def __init__(self, home: Path | None = None):
        self.home = home or default_home()
        self.path = self.home / "state.json"
        self.lock = threading.RLock()
        self._stamp: tuple | None = None
        self.data = self._load()

    def _file_stamp(self) -> tuple | None:
        try:
            st = self.path.stat()
        except FileNotFoundError:
            return None
        return (st.st_ino, st.st_mtime_ns, st.st_size)

    def _load(self) -> dict:
        self._stamp = self._file_stamp()
        if self._stamp is None:
            return empty_state()
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise StateError(f"{self.path} is not valid JSON ({exc}); restore state.json.bak or move it aside") from exc
        if data.get("version") != SCHEMA_VERSION:
            raise StateError(f"{self.path} has schema version {data.get('version')!r}, expected {SCHEMA_VERSION}")
        base = empty_state()
        base.update(data)
        base["profile"] = {**DEFAULT_PROFILE, **data.get("profile", {})}
        return base

    def refresh(self) -> None:
        """Reload if another process rewrote the file since we last read or wrote it."""
        with self.lock:
            if self._file_stamp() != self._stamp:
                self.data = self._load()

    @contextlib.contextmanager
    def _transaction(self):
        with self.lock:
            self.home.mkdir(parents=True, exist_ok=True)
            with open(self.home / "state.lock", "a+") as lockfile:
                if fcntl is not None:
                    fcntl.flock(lockfile.fileno(), fcntl.LOCK_EX)
                try:
                    self.refresh()
                    yield self.data
                    self._write()
                finally:
                    if fcntl is not None:
                        fcntl.flock(lockfile.fileno(), fcntl.LOCK_UN)

    def _write(self) -> None:
        fd, tmp = tempfile.mkstemp(dir=self.home, prefix=".state.", suffix=".json")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                json.dump(self.data, fh, indent=1, sort_keys=True)
                fh.write("\n")
                fh.flush()
                os.fsync(fh.fileno())
            if self.path.exists():
                shutil.copy2(self.path, self.path.with_suffix(".json.bak"))
            os.replace(tmp, self.path)
        except BaseException:
            Path(tmp).unlink(missing_ok=True)
            raise
        dir_fd = os.open(self.home, os.O_RDONLY)
        try:
            os.fsync(dir_fd)
        finally:
            os.close(dir_fd)
        self._stamp = self._file_stamp()

    def save(self) -> None:
        """Persist the in-memory state as it is (used after direct edits in tests and tools)."""
        with self.lock:
            self.home.mkdir(parents=True, exist_ok=True)
            self._write()

    # profile -------------------------------------------------------------
    @property
    def profile(self) -> dict:
        return self.data["profile"]

    def set_profile(self, **values) -> None:
        hours = values.get("hours_per_week")
        if hours is not None and not (isinstance(hours, (int, float)) and 0 < hours <= 100):
            raise StateError("hours_per_week must be in (0, 100]")
        new_cards = values.get("new_cards_per_day")
        if new_cards is not None and not (isinstance(new_cards, int) and 0 <= new_cards <= 1000):
            raise StateError("new_cards_per_day must be an integer in [0, 1000]")
        with self._transaction() as data:
            data["profile"].update({k: v for k, v in values.items() if v is not None})

    # topics --------------------------------------------------------------
    def mastery(self, topic_id: str) -> int:
        return int(self.data["topics"].get(topic_id, {}).get("mastery", 0))

    def set_mastery(self, topic_id: str, level: int) -> None:
        if not 0 <= level < len(MASTERY_LABELS):
            raise StateError(f"mastery must be 0-{len(MASTERY_LABELS) - 1}")
        with self._transaction() as data:
            entry = data["topics"].setdefault(topic_id, {"mastery": 0, "history": []})
            entry["mastery"] = level
            entry["updated"] = today().isoformat()
            entry["history"].append([today().isoformat(), level])
            self._bump("marks")

    # cards ---------------------------------------------------------------
    def card(self, card_id: str) -> CardSchedule:
        raw = self.data["cards"].get(card_id)
        return CardSchedule.from_dict(raw) if raw else CardSchedule()

    def grade(self, card_id: str, grade: str) -> CardSchedule:
        if grade not in GRADES:
            raise StateError(f"unknown grade {grade!r}; use one of {', '.join(GRADES)}")
        with self._transaction() as data:
            new = schedule(self.card(card_id), grade, today())
            first = data["cards"].get(card_id, {}).get("first") or today().isoformat()
            data["cards"][card_id] = {**new.to_dict(), "first": first}
            self._bump("reviews")
        return new

    def new_cards_seen_today(self) -> int:
        t = today().isoformat()
        with self.lock:
            return sum(1 for c in self.data["cards"].values() if c.get("first") == t)

    # drills --------------------------------------------------------------
    def record_drill(self, mode: str, attempts: int, correct: int, seconds: float, score: float, extra: dict | None = None) -> dict:
        row = {
            "mode": mode,
            "at": now_iso(),
            "attempts": attempts,
            "correct": correct,
            "seconds": round(seconds, 1),
            "score": round(score, 2),
            **(extra or {}),
        }
        with self._transaction() as data:
            data["drills"].append(row)
            self._bump("drills")
        return row

    # activity ------------------------------------------------------------
    def _bump(self, kind: str) -> None:
        day = self.data["activity"].setdefault(today().isoformat(), {})
        day[kind] = day.get(kind, 0) + 1

    def streak(self) -> int:
        with self.lock:
            days = set(self.data["activity"])
        d = today()
        if d.isoformat() not in days:
            d -= dt.timedelta(days=1)  # the streak survives until today ends
        n = 0
        while d.isoformat() in days:
            n += 1
            d -= dt.timedelta(days=1)
        return n
