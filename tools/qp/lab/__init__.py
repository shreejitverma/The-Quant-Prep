"""Trading Lab: pure-Python interactive simulation and analytics engines.

Designed for standard-library execution, verifiable quantitative modeling,
and browser-based interactive market experiment playback.
"""

from . import lob_sim, pos_sizing  # noqa: F401
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
