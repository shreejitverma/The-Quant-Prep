"""CLI dispatcher for the Trading Lab (subcommand `qp lab`).

Usage:
  qp lab list
  qp lab info <engine_id>
  qp lab run <engine_id> [key=val ...]
"""

from __future__ import annotations

import argparse
import sys
from typing import Any

from .registry import get_engine, list_engines


def parse_kwarg(arg_str: str) -> tuple[str, Any]:
    if "=" not in arg_str:
        raise ValueError(f"Argument must be in 'key=value' format, got {arg_str!r}")
    k, _, v = arg_str.partition("=")
    k = k.strip().lstrip("-")
    v = v.strip()
    return k, v


def cmd_lab_list(args: argparse.Namespace) -> int:
    engines = list_engines()
    if not engines:
        print("engines: 0 results")
        return 0
    print(f"engines[{len(engines)}]{{id,name,asset_class,params,description}}:")
    for eng in engines:
        print(f'  {eng["id"]},{eng["name"]},{eng["asset_class"]},{eng["param_count"]},"{eng["description"]}"')
    return 0


def cmd_lab_info(args: argparse.Namespace) -> int:
    engine = get_engine(args.engine_id)
    if not engine:
        print(f"error: unknown engine {args.engine_id!r}", file=sys.stderr)
        return 1

    print(f"engine: {engine.engine_id}")
    print(f"name: {engine.name}")
    print(f"asset_class: {engine.asset_class}")
    print(f"description: {engine.description}")
    if engine.params:
        print(f"params[{len(engine.params)}]{{name,type,default,description}}:")
        for p in engine.params.values():
            print(f'  {p.name},{p.param_type},{p.default},"{p.description}"')
    else:
        print("params: 0 results")
    return 0


def cmd_lab_run(args: argparse.Namespace) -> int:
    engine = get_engine(args.engine_id)
    if not engine:
        print(f"error: unknown engine {args.engine_id!r}", file=sys.stderr)
        return 1

    kwargs: dict[str, Any] = {}
    for item in args.params:
        try:
            k, v = parse_kwarg(item)
            kwargs[k] = v
        except ValueError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2

    try:
        valid_kwargs = engine.validate_params(kwargs)
        result = engine.run(**valid_kwargs)
        store = getattr(args, "store", None)
        if store is None:
            from ..state import Store

            store = Store()
        store.record_lab_run(engine.engine_id, result.metrics)
        print(result.to_toon())
        return 0
    except Exception as exc:
        print(f"error: simulation execution failed: {exc}", file=sys.stderr)
        return 1


def build_lab_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="qp lab", description="Interactive Trading Lab execution engine.")
    sub = p.add_subparsers(dest="lab_cmd")

    sp_list = sub.add_parser("list", help="List all registered simulation engines")
    sp_list.set_defaults(fn=cmd_lab_list)

    sp_info = sub.add_parser("info", help="Show parameters and details for an engine")
    sp_info.add_argument("engine_id", help="Engine identifier, e.g. 'pos_sizing'")
    sp_info.set_defaults(fn=cmd_lab_info)

    sp_run = sub.add_parser("run", help="Run a simulation engine with parameters")
    sp_run.add_argument("engine_id", help="Engine identifier, e.g. 'pos_sizing'")
    sp_run.add_argument("params", nargs="*", help="key=value parameters")
    sp_run.set_defaults(fn=cmd_lab_run)

    return p


def main(argv: list[str] | None = None, store: Any = None) -> int:
    parser = build_lab_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "fn", None):
        parser.print_help()
        return 0
    args.store = store
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
