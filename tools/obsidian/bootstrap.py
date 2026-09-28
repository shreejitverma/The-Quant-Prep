"""Install the Obsidian community plugins pinned in plugins.lock.json into .obsidian/plugins/.

Plugin bundles are not committed (several exceed the repo's large-file limit); this script
downloads each plugin's release assets for the pinned tag from GitHub, verifies every file
against its sha256 in the lock, and writes it. It is idempotent: a plugin whose installed
tag matches the lock is skipped. Obsidian rewrites installed main.js files (it strips the
source map), so installed copies are tracked by tag, never re-hashed.

Usage (from the repo root):
    python3 tools/obsidian/bootstrap.py            # install or update everything
    python3 tools/obsidian/bootstrap.py --check    # report what would change, exit 1 if anything would
    python3 tools/obsidian/bootstrap.py --only dataview templater-obsidian
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOCK = Path(__file__).with_name("plugins.lock.json")
MARKER = ".installed-tag"
TIMEOUT = 60


class BootstrapError(RuntimeError):
    pass


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "the-quant-prep-bootstrap"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return resp.read()


def install(plugin: dict, plugins_dir: Path) -> str:
    pid, repo, tag, hashes = plugin["id"], plugin["repo"], plugin["tag"], plugin["sha256"]
    target = plugins_dir / pid
    marker = target / MARKER
    if marker.exists() and marker.read_text().strip() == tag:
        return "up-to-date"
    files = {}
    for name, expected in hashes.items():
        data = fetch(f"https://github.com/{repo}/releases/download/{tag}/{name}")
        actual = hashlib.sha256(data).hexdigest()
        if actual != expected:
            raise BootstrapError(f"{pid} {tag} {name}: sha256 {actual} does not match lock {expected}")
        files[name] = data
    target.mkdir(parents=True, exist_ok=True)
    for name, data in files.items():  # write only after every file verified
        (target / name).write_bytes(data)
    marker.write_text(tag + "\n")
    return f"installed {tag}"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--vault", type=Path, default=ROOT, help="vault root (default: repo root)")
    ap.add_argument("--only", nargs="+", metavar="ID", help="limit to these plugin ids")
    ap.add_argument("--check", action="store_true", help="report pending installs without downloading")
    args = ap.parse_args(argv)

    lock = json.loads(LOCK.read_text())
    plugins = [p for p in lock["plugins"] if not args.only or p["id"] in args.only]
    unknown = set(args.only or []) - {p["id"] for p in plugins}
    if unknown:
        print(f"error: not in lock: {', '.join(sorted(unknown))}", file=sys.stderr)
        return 2
    plugins_dir = args.vault / ".obsidian" / "plugins"
    pending, failed = 0, 0
    for p in plugins:
        marker = plugins_dir / p["id"] / MARKER
        current = marker.read_text().strip() if marker.exists() else None
        if args.check:
            if current != p["tag"]:
                pending += 1
                print(f"{p['id']}: {current or 'missing'} -> {p['tag']}")
            continue
        try:
            print(f"{p['id']}: {install(p, plugins_dir)}")
        except (BootstrapError, OSError) as exc:  # keep going, report every failure, exit non-zero
            failed += 1
            print(f"{p['id']}: FAILED {exc}", file=sys.stderr)
    if args.check:
        print(f"check: {pending} plugin(s) to install or update")
        return 1 if pending else 0
    print(f"bootstrap: {len(plugins) - failed} ok, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
