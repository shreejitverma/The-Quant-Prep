"""Central registry for Trading Lab engines."""

from __future__ import annotations

from typing import Any

from .base import TradingLabEngine

_REGISTRY: dict[str, TradingLabEngine] = {}


def register(engine: TradingLabEngine) -> None:
    """Register an instantiated Trading Lab engine."""
    _REGISTRY[engine.engine_id] = engine


def get_engine(engine_id: str) -> TradingLabEngine | None:
    """Look up an engine by its unique ID."""
    return _REGISTRY.get(engine_id)


def list_engines() -> list[dict[str, Any]]:
    """Return summary metadata for all registered engines."""
    return [
        {
            "id": eng.engine_id,
            "name": eng.name,
            "asset_class": eng.asset_class,
            "description": eng.description,
            "param_count": len(eng.params),
        }
        for eng in sorted(_REGISTRY.values(), key=lambda e: e.engine_id)
    ]
