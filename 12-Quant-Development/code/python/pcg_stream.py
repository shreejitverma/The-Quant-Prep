"""Seeded draws built from the raw PCG64 bit stream, so quoted values do not move with NumPy releases.

NumPy's NEP 19 fixes the raw output of a bit generator for a given seed, but lets `Generator`
distribution methods (`normal`, `integers`, `choice`, `exponential`, ...) change their algorithms
in feature releases. A script that prints and asserts exact values from seeded draws therefore
derives every draw from `PCG64(seed).random_raw` with the explicit rules below, as note 14 recommends.

* uniform: the top 53 bits of a raw word times 2^-53, on [0, 1).
* integers in [low, high): low + floor(u * (high - low)), exact for spans below 2^53.
* choice: an index drawn by `integers`.
* exponential: -scale * log(1 - u).
* normal: Box-Muller on pairs of uniforms, cosine normals first, then sine normals.

Shared by the section's scripts; it has no main guard, so tools/run_examples.py does not run it.
"""

from __future__ import annotations

import math

import numpy as np


class PcgStream:
    """A sequential stream of draws; each call consumes raw words in order."""

    def __init__(self, seed: int) -> None:
        self._bits = np.random.PCG64(seed)

    def _count(self, size: int | tuple[int, ...] | None) -> int:
        return 1 if size is None else math.prod(size) if isinstance(size, tuple) else size

    def _shape(self, values: np.ndarray, size: int | tuple[int, ...] | None):
        return values[0].item() if size is None else values.reshape(size)

    def _uniforms(self, n: int) -> np.ndarray:
        return (self._bits.random_raw(n) >> np.uint64(11)).astype(np.float64) * 2.0**-53

    def uniform(self, size: int | tuple[int, ...] | None = None):
        return self._shape(self._uniforms(self._count(size)), size)

    def integers(self, low: int, high: int, size: int | tuple[int, ...] | None = None):
        u = self._uniforms(self._count(size))
        return self._shape(low + np.floor(u * (high - low)).astype(np.int64), size)

    def choice(self, values, size: int | tuple[int, ...] | None = None):
        options = np.asarray(values)
        idx = np.floor(self._uniforms(self._count(size)) * len(options)).astype(np.int64)
        return self._shape(options[idx], size)

    def exponential(self, scale: float, size: int | tuple[int, ...] | None = None):
        return self._shape(-scale * np.log(1.0 - self._uniforms(self._count(size))), size)

    def normal(self, loc: float = 0.0, scale: float = 1.0, size: int | tuple[int, ...] | None = None):
        n = self._count(size)
        u = self._uniforms(n + n % 2)
        radius = np.sqrt(-2.0 * np.log(1.0 - u[0::2]))  # 1 - u is in (0, 1], so the log is finite
        angle = 2.0 * math.pi * u[1::2]
        z = np.concatenate([radius * np.cos(angle), radius * np.sin(angle)])[:n]
        return self._shape(z if (loc, scale) == (0.0, 1.0) else loc + scale * z, size)
