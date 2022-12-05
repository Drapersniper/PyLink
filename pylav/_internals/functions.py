from __future__ import annotations

import pathlib
import sys
from typing import TypeVar

T = TypeVar("T")


def _get_path(path: T | pathlib.Path) -> str | T | None:

    return get_true_path(path, fallback=path)


def update_event_loop_policy() -> None:
    if sys.implementation.name == "cpython":
        # Let's not force this dependency, uvloop is much faster on cpython
        try:
            import uvloop  # type: ignore
        except ImportError:
            pass
        else:
            import asyncio

            if not isinstance(asyncio.get_event_loop_policy(), uvloop.EventLoopPolicy):
                asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
