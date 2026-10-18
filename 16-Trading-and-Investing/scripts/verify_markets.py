"""Forwarding entrypoint for verify_markets.py."""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from tools.qp.verify_markets import main

if __name__ == "__main__":
    sys.exit(main())
