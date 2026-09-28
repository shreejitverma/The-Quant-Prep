"""Euler-Maruyama solver for scalar SDEs dX = a(X, t) dt + b(X, t) dW, with GBM and Vasicek examples.

Run as a script to plot one path of each example; import ``euler_maruyama`` to reuse the solver.
"""

from __future__ import annotations

from collections.abc import Callable

import numpy as np

Coefficient = Callable[[float, float], float]


def euler_maruyama(
    drift: Coefficient, diffusion: Coefficient, x0: float, T: float, dt: float, rng: np.random.Generator | None = None
) -> tuple[np.ndarray, np.ndarray]:
    """Simulate one path on a uniform grid. Strong order 0.5, weak order 1."""
    if T <= 0 or dt <= 0:
        raise ValueError("T and dt must be positive")
    rng = rng or np.random.default_rng()
    n = int(round(T / dt))  # round, not truncate: int(0.3 / 0.1) == 2
    t = np.linspace(0.0, T, n + 1)
    h = T / n
    x = np.empty(n + 1)
    x[0] = x0
    dw = rng.normal(0.0, np.sqrt(h), size=n)
    for i in range(n):
        x[i + 1] = x[i] + drift(x[i], t[i]) * h + diffusion(x[i], t[i]) * dw[i]
    return t, x


def main() -> None:
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(7)
    mu, sigma = 0.1, 0.2  # GBM: dS = mu S dt + sigma S dW
    kappa, theta, sig_vas = 3.0, 0.05, 0.03  # Vasicek: dr = kappa (theta - r) dt + sigma dW

    def gbm_drift(s: float, t: float) -> float:
        return mu * s

    def gbm_diffusion(s: float, t: float) -> float:
        return sigma * s

    def vas_drift(r: float, t: float) -> float:
        return kappa * (theta - r)

    def vas_diffusion(r: float, t: float) -> float:
        return sig_vas

    t_gbm, s_gbm = euler_maruyama(gbm_drift, gbm_diffusion, x0=100, T=1, dt=0.001, rng=rng)
    t_vas, r_vas = euler_maruyama(vas_drift, vas_diffusion, x0=0.02, T=1, dt=0.001, rng=rng)

    fig, ax = plt.subplots(2, 1, figsize=(10, 8))
    ax[0].plot(t_gbm, s_gbm)
    ax[0].set_title("GBM simulation (Euler-Maruyama)")
    ax[0].grid(True)
    ax[1].plot(t_vas, r_vas, color="orange")
    ax[1].set_title("Vasicek simulation (mean reversion)")
    ax[1].grid(True)
    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
