"""Case File 09: GameStop, January 2021, every number on the page.

Backs `16-Trading-and-Investing/20-History-and-Events/09-2021-GameStop-Meme-Squeeze-and-DTCC-Margin-Halt.md`.
Independent routes used here:
- price changes are recomputed from the SEC staff report's cited prices in exact decimal arithmetic, and
  its "more than 1,600%" statement is checked against the January 11 close as reported at the time, which
  must also lie below the report's January 11 intraday high;
- the NSCC January 27 margin call is checked to equal the sum of its two cited components;
- the hypothetical dealer hedge uses the closed-form Black-Scholes gamma and is checked against a central
  finite difference of the closed-form delta, and the 1/sqrt(tau) scaling is checked by comparing two
  expiries;
- the re-lending example (short interest above 100%) is run on a share ledger of loan records, and the
  short interest and the shares never sold short are counted from those records.
Every quoted number is printed as ``label = value`` and asserted.
"""

from __future__ import annotations

import math
from decimal import Decimal as D


def approx(label: str, value: float, expected: float, decimals: int) -> None:
    tol = 0.5 * 10.0**-decimals + 1e-12
    assert abs(value - expected) <= tol, f"{label}: computed {value!r}, quoted {expected}"
    print(f"    {label} = {value:.{decimals}f}")


def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def call_delta(s: float, k: float, sigma: float, tau: float) -> float:
    d1 = (math.log(s / k) + 0.5 * sigma**2 * tau) / (sigma * math.sqrt(tau))
    return norm_cdf(d1)


def call_gamma(s: float, k: float, sigma: float, tau: float) -> float:
    d1 = (math.log(s / k) + 0.5 * sigma**2 * tau) / (sigma * math.sqrt(tau))
    return math.exp(-0.5 * d1 * d1) / math.sqrt(2.0 * math.pi) / (s * sigma * math.sqrt(tau))


def prices() -> None:
    print("GME prices (SEC staff report, October 14, 2021)")
    jan12, jan13, jan27, high = D("19.95"), D("31.40"), D("347.51"), D("483.00")
    jan11, jan11_high = D("19.94"), D("20.65")  # close as reported at the time; intraday high from the SEC
    assert jan11 <= jan11_high, "a close cannot exceed the day's intraday high"
    approx("Jan 13 close over Jan 12 close (%)", float((jan13 / jan12 - 1) * 100), 57.39, 2)
    approx("Jan 27 close over Jan 12 close (%)", float((jan27 / jan12 - 1) * 100), 1641.90, 2)
    gain_jan11 = float((jan27 / jan11 - 1) * 100)
    approx("Jan 27 close over Jan 11 close (%)", gain_jan11, 1642.78, 2)
    assert gain_jan11 > 1600, "SEC: more than 1,600% above the January 11 close"
    approx("Jan 28 intraday high over Jan 12 close (%)", float((high / jan12 - 1) * 100), 2321.05, 2)


def nscc() -> None:
    print("NSCC margin, January 27, 2021 ($bn)")
    mtm, special = D("2.1"), D("4.8")
    assert mtm + special == D("6.9"), "intraday calls = mark-to-market + special charge"
    print(f"    intraday margin calls = {mtm + special}")


class ShareLedger:
    """Physical holders of each share and the open stock loans against the float."""

    def __init__(self, float_shares: int) -> None:
        self.holder = {share: f"owner{share}" for share in range(float_shares)}
        self.loans: list[tuple[int, str, str]] = []  # (share, lender, short seller)
        self._next = 0

    def _new_party(self, kind: str) -> str:
        self._next += 1
        return f"{kind}{self._next}"

    def lend_and_short(self, share: int) -> None:
        """The holder lends the share to a short seller, who sells it to a new buyer."""
        lender, seller, buyer = self.holder[share], self._new_party("short"), self._new_party("buyer")
        self.loans.append((share, lender, seller))
        self.holder[share] = buyer

    def short_interest_pct(self) -> float:
        return len(self.loans) / len(self.holder) * 100

    def never_shorted(self) -> int:
        return len(set(self.holder) - {share for share, _, _ in self.loans})


def relending() -> None:
    print("Re-lending ledger: 100-share float")
    one = ShareLedger(100)
    # A lends share 0 to X, X sells it to B; B lends the same share to Y, Y sells it to C.
    one.lend_and_short(0)
    one.lend_and_short(0)
    approx("short interest, one share lent twice (%)", one.short_interest_pct(), 2.0, 0)
    never = one.never_shorted()
    assert never == 99, f"ledger shows {never} shares never sold short"
    print(f"    shares never sold short = {never}")
    whole = ShareLedger(100)
    for _ in range(2):
        for share in range(100):
            whole.lend_and_short(share)
    si = whole.short_interest_pct()
    approx("short interest, every share lent and re-lent once (%)", si, 200.0, 0)
    assert si > 100, "short interest exceeds 100% of the float"
    print(f"    shares owed by short sellers = {len(whole.loans)}, float = {len(whole.holder)}")


def dealer_hedge() -> None:
    print("Hypothetical dealer short 10,000 at-the-money calls, S = K = 40, sigma = 200%")
    n, s, k, sigma = 10_000, 40.0, 40.0, 2.0
    results = {}
    for days, quoted in ((5, 35053), (1, 79006)):
        tau = days / 252
        g = call_gamma(s, k, sigma, tau)
        h = 1e-4
        g_fd = (call_delta(s + h, k, sigma, tau) - call_delta(s - h, k, sigma, tau)) / (2 * h)
        assert abs(g - g_fd) / g < 1e-6, f"gamma {g} vs finite difference {g_fd}"
        shares = n * 100 * g
        results[days] = shares
        approx(f"shares to buy per $1 rise, {days} trading days to expiry", shares, quoted, 0)
    ratio = results[1] / results[5]
    # Near the money gamma scales like 1/sqrt(tau); d1 = sigma*sqrt(tau)/2 adds a small correction.
    assert abs(ratio / math.sqrt(5) - 1) < 0.02, f"ratio {ratio} vs sqrt(5)"
    approx("sqrt(5)", math.sqrt(5), 2.236, 3)
    approx("ratio of 1-day to 5-day hedge", ratio, 2.25, 2)


def main() -> None:
    prices()
    nscc()
    relending()
    dealer_hedge()
    print("all GameStop checks passed")


if __name__ == "__main__":
    main()
