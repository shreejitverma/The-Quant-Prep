"""Trading Lab: pure-Python interactive simulation and analytics engines.

Designed for standard-library execution, verifiable quantitative modeling,
and browser-based interactive market experiment playback.
"""

from . import (  # noqa: F401
    event_study,
    fut_desk,
    games,
    journal_stats,
    lob_sim,
    market,
    mm_quote,
    opt_desk,
    overfit_trap,
    port_alloc,
    pos_sizing,
    replay_chart,
)
from .base import LabResult, Param, TradingLabEngine
from .registry import get_engine, list_engines, register

__all__ = [
    "LabResult",
    "Param",
    "TradingLabEngine",
    "get_engine",
    "list_engines",
    "register",
]
