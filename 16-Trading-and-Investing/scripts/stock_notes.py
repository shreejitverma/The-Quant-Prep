"""Shared helpers for the stock-research note pipeline.

Every script that reads or writes ticker notes goes through this module so that:

- frontmatter is edited block by block instead of by ad hoc string splits and regexes,
  which previously dropped keys, duplicated blocks and left `market_data` below the closing fence;
- one ticker map is used everywhere (three diverging copies made non-US fetches fail silently);
- a missing or failed value is written as missing, never as a number such as 0 or None.

Standard library only, so the repo test suite can import it without yfinance installed.
"""

from __future__ import annotations

import re
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
STOCK_ROOT = REPO_ROOT / "16-Trading-and-Investing" / "Investing" / "Stock Research"

# Local ticker (from the note file name) to Yahoo Finance symbol.
# Listings are chosen so that price and financial statements share a currency:
# ADR symbols report USD prices against home-currency statements, which corrupts ratios such as FCF yield.
TICKER_MAP: dict[str, str] = {
    # US share classes
    "BRK.B": "BRK-B",
    "BRK.A": "BRK-A",
    # India (NSE)
    "RELIANCE": "RELIANCE.NS",
    "HDFCBANK": "HDFCBANK.NS",
    "TCS": "TCS.NS",
    "ASIANPAINT": "ASIANPAINT.NS",
    "TITAN": "TITAN.NS",
    "INFY": "INFY.NS",
    "ICICIBANK": "ICICIBANK.NS",
    "BAJFINANCE": "BAJFINANCE.NS",
    "PIDILITIND": "PIDILITIND.NS",
    "NESTLEIND": "NESTLEIND.NS",
    "HINDUNILVR": "HINDUNILVR.NS",
    "MARICO": "MARICO.NS",
    "LT": "LT.NS",
    "SUNPHARMA": "SUNPHARMA.NS",
    # Japan (TSE)
    "7203": "7203.T",
    "6758": "6758.T",
    "6861": "6861.T",
    "7974": "7974.T",
    "6954": "6954.T",
    "9983": "9983.T",
    "4063": "4063.T",
    "6981": "6981.T",
    "7741": "7741.T",
    # Germany (XETRA)
    "RAA": "RAA.DE",
    "SY1": "SY1.DE",
    "FPE3": "FPE3.DE",
    "SRT3": "SRT3.DE",
    "NEM": "NEM.DE",
    "EVD": "EVD.DE",
    "SIX2": "SIX2.DE",
    "AFX": "AFX.DE",
    "SIE": "SIE.DE",
    "SAP": "SAP.DE",
    # Netherlands and Denmark: home listings, not ADRs
    "ASML": "ASML.AS",
    "NVO": "NOVO-B.CO",
    # Brazil (B3)
    "WEGE3": "WEGE3.SA",
    "RADL3": "RADL3.SA",
    "ITUB4": "ITUB4.SA",
    "RENT3": "RENT3.SA",
    "EQTL3": "EQTL3.SA",
    # China and Hong Kong
    "600519": "600519.SS",
    # South Korea and Taiwan
    "005930": "005930.KS",
    "TSM": "2330.TW",
    # South East Asia
    "D05": "D05.SI",
    "BBCA": "BBCA.JK",
    "CPALL": "CPALL.BK",
    "PBBANK": "PBBANK.KL",
    # Sweden
    "INVE.B": "INVE-B.ST",
    "ATCO.A": "ATCO-A.ST",
    "ASSA.B": "ASSA-B.ST",
    "HEXA.B": "HEXA-B.ST",
    # Companies outside the US whose primary or only listing chosen here is a US one
    "MELI": "MELI",
    "SHOP": "SHOP",
    "SE": "SE",
    "NTES": "NTES",
}

# Keys that older writers emitted as body text directly under the closing fence.
MISPLACED_KEYS = ("last_updated", "market_data")

# Reverse DCF assumptions; written next to every solved value so the number is reproducible.
DCF_DISCOUNT_RATE = 0.10
DCF_TERMINAL_GROWTH = 0.03
DCF_YEARS = 10
DCF_GROWTH_LOW = -0.50
DCF_GROWTH_HIGH = 1.00

# FCF yields outside this band are treated as data errors, not valuations: below 0.1% the price
# is over 1000x FCF, the signature of a minor-unit or cross-currency mix-up (INFY's USD ADR price
# against INR statements gave 0.07%), and above 50% the same mix-up runs the other way.
FCF_YIELD_MIN = 0.001
FCF_YIELD_MAX = 0.50

_TOP_KEY = re.compile(r"^([A-Za-z0-9_]+):(.*)$")
_TICKER = re.compile(r"\(([^)]+)\)")


class NoteFormatError(ValueError):
    """A note cannot be edited safely; the caller must fix it by hand."""


class UnmappedTickerError(LookupError):
    """A non-US note has no Yahoo symbol, so a fetch would hit an unrelated US listing."""


# ---------------------------------------------------------------- tickers


def extract_ticker(filename: str, content: str | None = None) -> str | None:
    """Return the ticker inside the last parentheses of a file name or frontmatter, or None.

    Historical case-study notes such as "Kodak (The Digital Blindness).md" are rejected
    because their parenthetical is a title, not a ticker.
    """
    matches = _TICKER.findall(filename)
    if matches:
        candidate = matches[-1]
        if len(candidate) <= 10 and candidate.upper() == candidate and " " not in candidate:
            return candidate
    if content:
        m = re.search(r"^ticker:\s*([A-Za-z0-9._-]+)", content, flags=re.MULTILINE)
        if m:
            cand = m.group(1).strip()
            if len(cand) <= 10:
                return cand
    return None


def yahoo_symbol(ticker: str) -> str:
    return TICKER_MAP.get(ticker, ticker)


def note_country(path: Path, root: Path | None = None) -> str | None:
    """Country folder of a note laid out as <sector>/<country>/.../<note>.md, or None."""
    parts = path.relative_to(root or STOCK_ROOT).parts
    return parts[1] if len(parts) >= 3 else None


def fetch_symbol(path: Path, ticker: str, root: Path | None = None) -> str:
    """Yahoo symbol to fetch for a note.

    A bare local ticker outside the US folder resolves on Yahoo to whatever US security
    shares the code (NEM is Newmont, not Nemetschek; BBCA is a US ETF), so such tickers
    must be in TICKER_MAP or already carry an exchange suffix such as `.PA`.
    """
    if ticker in TICKER_MAP:
        return TICKER_MAP[ticker]
    if "." in ticker or note_country(path, root) == "US":
        return ticker
    raise UnmappedTickerError(f"{ticker} in {path.name} is outside the US folder and has no TICKER_MAP entry")


def iter_ticker_notes(root: Path = STOCK_ROOT) -> Iterator[tuple[Path, str]]:
    """Yield (path, ticker) for every ticker note, skipping the Historical case files."""
    for path in sorted(root.rglob("*.md")):
        if "Historical" in path.relative_to(root).parts or path.name.startswith("_"):
            continue
        text = path.read_text(encoding="utf-8")
        ticker = extract_ticker(path.name, text)
        if ticker:
            yield path, ticker


# ---------------------------------------------------------------- frontmatter


def split_note(text: str) -> tuple[list[str] | None, str]:
    """Split a note into frontmatter lines (without fences) and body text.

    Returns (None, text) when the note has no frontmatter.
    Raises NoteFormatError when the opening fence is never closed.
    """
    lines = text.split("\n")
    if not lines or lines[0].rstrip() != "---":
        return None, text
    for i in range(1, len(lines)):
        if lines[i].rstrip() == "---":
            return lines[1:i], "\n".join(lines[i + 1 :])
    raise NoteFormatError("frontmatter opening fence is never closed")


def join_note(frontmatter: list[str], body: str) -> str:
    return "---\n" + "\n".join(frontmatter) + "\n---\n" + body


def _is_continuation(line: str) -> bool:
    return line.startswith((" ", "\t", "- "))


def _block_span(lines: list[str], key: str) -> tuple[int, int] | None:
    """Return [start, end) of the top-level block for `key`, or None."""
    for i, line in enumerate(lines):
        m = _TOP_KEY.match(line)
        if m and m.group(1) == key:
            end = i + 1
            while end < len(lines) and _is_continuation(lines[end]):
                end += 1
            return i, end
    return None


def top_level_keys(lines: list[str]) -> list[str]:
    return [m.group(1) for line in lines if (m := _TOP_KEY.match(line))]


def get_block(lines: list[str], key: str) -> list[str] | None:
    span = _block_span(lines, key)
    return None if span is None else lines[span[0] : span[1]]


def set_block(lines: list[str], key: str, block: list[str]) -> list[str]:
    """Replace the block for `key` in place, or append it; returns a new list."""
    if not block or not block[0].startswith(f"{key}:"):
        raise ValueError(f"block must start with '{key}:'")
    span = _block_span(lines, key)
    if span is None:
        return [*lines, *block]
    return [*lines[: span[0]], *block, *lines[span[1] :]]


def remove_block(lines: list[str], key: str) -> list[str]:
    span = _block_span(lines, key)
    return list(lines) if span is None else [*lines[: span[0]], *lines[span[1] :]]


def block_fields(block: list[str]) -> dict[str, str]:
    """Flatten a nested block into dotted keys: {'returns.cagr_10y': '13.14%'}."""
    fields: dict[str, str] = {}
    stack: list[tuple[int, str]] = []
    for line in block[1:]:
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" "))
        key, _, value = line.strip().partition(":")
        while stack and stack[-1][0] >= indent:
            stack.pop()
        dotted = ".".join([*(name for _, name in stack), key])
        if value.strip():
            fields[dotted] = value.strip()
        else:
            stack.append((indent, key))
    return fields


def relocate_misplaced_blocks(text: str) -> tuple[str, list[str]]:
    """Move `last_updated` and `market_data` blocks from the top of the body into the frontmatter.

    Returns (new_text, moved_keys).
    Raises NoteFormatError if a key exists both above and below the fence, since it is
    then unclear which value is current.
    """
    frontmatter, body = split_note(text)
    if frontmatter is None:
        return text, []
    body_lines = body.split("\n")
    moved: list[str] = []
    i = 0
    while i < len(body_lines):
        line = body_lines[i]
        m = _TOP_KEY.match(line)
        if not m or m.group(1) not in MISPLACED_KEYS:
            break
        key = m.group(1)
        if _block_span(frontmatter, key) is not None:
            raise NoteFormatError(f"'{key}' appears both in the frontmatter and below the closing fence")
        end = i + 1
        while end < len(body_lines) and body_lines[end].startswith((" ", "\t")):
            end += 1
        frontmatter = [*frontmatter, *body_lines[i:end]]
        moved.append(key)
        i = end
    if not moved:
        return text, []
    return join_note(frontmatter, "\n".join(body_lines[i:])), moved


# Known ADRs or cross-border listings where financial statements and market price currencies diverge
KNOWN_CURRENCY_MISMATCHES = {"NTES", "3690.HK", "CSL.AX", "ULVR.L", "INFY"}
CURRENCY_MISMATCH = "currency_mismatch"
MISSING = "N/A"

# Yahoo quotes some listings in a minor unit: GBp is pence, a hundredth of GBP.
CURRENCY_SUBUNITS: dict[str, tuple[str, int]] = {
    "GBp": ("GBP", 100),
    "GBX": ("GBP", 100),
    "ZAc": ("ZAR", 100),
    "ILA": ("ILS", 100),
}


def to_major_unit(amount: float | None, currency: str | None) -> tuple[float | None, str | None]:
    """Convert a minor-unit quote such as 4205.5 GBp to 42.055 GBP; other currencies pass through."""
    if currency not in CURRENCY_SUBUNITS:
        return amount, currency
    major, factor = CURRENCY_SUBUNITS[currency]
    return (None if amount is None else amount / factor), major


def check_currency_guard(financial_currency: str | None, quote_currency: str | None) -> bool:
    """Return True if currencies match or are unknown; False if confirmed mismatch.

    Codes are compared exactly: GBp (pence) and GBP differ by a factor of 100, so callers
    convert minor units with to_major_unit before comparing.
    """
    if not financial_currency or not quote_currency:
        return True
    return financial_currency == quote_currency


def strip_inline_metadata(body: str) -> str:
    """Remove body inline Dataview fields (status:: ..., priority:: ...) that shadow frontmatter."""
    lines = body.split("\n")
    cleaned = [line for line in lines if not re.match(r"^(status|priority)::\s*", line.strip())]
    return "\n".join(cleaned)


# ---------------------------------------------------------------- market data


REQUIRED_MARKET_FIELDS = ("price", "market_cap")
_PLACEHOLDERS = ("None", "null", "")
_ZEROS = ("0", "0.0")


def normalize_market_data(lines: list[str]) -> tuple[list[str], list[str]]:
    """Strip placeholder values from `market_data` and derive data quality from what is left.

    Values of None, null, empty or exactly 0 are fetch failures, so they are removed and listed
    under `missing`; when price is missing, dividend_yield: 0 is treated the same way.
    `missing` keeps earlier entries that are still absent and adds any required field
    (REQUIRED_MARKET_FIELDS) that is not present, so `data_quality: ok` means price and
    market cap are both there and a re-run yields the same block.
    Returns (new_lines, missing_fields).
    """
    block = get_block(lines, "market_data")
    if block is None:
        return lines, []
    entries = []
    for line in block[1:]:
        key, _, value = line.strip().partition(":")
        entries.append((line, key, value.strip()))
    has_price = any(key == "price" and value not in (*_PLACEHOLDERS, *_ZEROS) for _, key, value in entries)

    kept = [block[0]]
    present: set[str] = set()
    earlier: list[str] = []
    stripped: list[str] = []
    for line, key, value in entries:
        if key == "data_quality":
            continue
        if key == "missing":
            earlier.extend(value.split())
            continue
        if value in _PLACEHOLDERS or (value in _ZEROS and (key != "dividend_yield" or not has_price)):
            stripped.append(key)
            continue
        kept.append(line)
        present.add(key)

    missing: list[str] = []
    for key in (*earlier, *stripped, *REQUIRED_MARKET_FIELDS):
        if key not in present and key not in missing:
            missing.append(key)
    kept.append(f"  data_quality: {'missing' if missing else 'ok'}")
    if missing:
        kept.append(f"  missing: {' '.join(missing)}")
    return set_block(lines, "market_data", kept), missing


def drop_foreign_listing_data(lines: list[str], expected_symbol: str) -> tuple[list[str], str | None]:
    """Drop `market_data` values recorded under a symbol other than the one the pipeline fetches.

    `market_data.ticker` is the symbol the values came from; when it differs from
    `expected_symbol` they belong to another security (an ADR or an unrelated US listing),
    so every field is removed and the block is re-labelled with the expected symbol;
    run normalize_market_data afterwards to record what is now missing.
    Returns (new_lines, rejected_symbol or None).
    """
    block = get_block(lines, "market_data")
    if block is None:
        return lines, None
    recorded = block_fields(block).get("ticker")
    if recorded is None or recorded == expected_symbol:
        return lines, None
    return set_block(lines, "market_data", [block[0], f"  ticker: {expected_symbol}"]), recorded


# ---------------------------------------------------------------- reverse DCF


@dataclass(frozen=True)
class ImpliedGrowth:
    """Result of a reverse DCF solve; `rate` is None unless status is 'solved'."""

    status: str
    rate: float | None = None


def dcf_value(fcf_per_share: float, growth: float) -> float:
    """Value per share of `fcf_per_share` growing at `growth` for DCF_YEARS, then at terminal growth."""
    r, tg = DCF_DISCOUNT_RATE, DCF_TERMINAL_GROWTH
    value = 0.0
    cash = fcf_per_share
    for year in range(1, DCF_YEARS + 1):
        cash *= 1 + growth
        value += cash / (1 + r) ** year
    terminal = cash * (1 + tg) / (r - tg)
    return value + terminal / (1 + r) ** DCF_YEARS


def solve_implied_growth(price: float | None, fcf_per_share: float | None) -> ImpliedGrowth:
    """Growth rate the market price implies under the module's DCF assumptions.

    The DCF value is strictly increasing in growth, so bisection is exact to tolerance.
    Out-of-range and undefined cases return a status instead of a fake number.
    """
    if price is None or price <= 0:
        return ImpliedGrowth("missing_price")
    if fcf_per_share is None:
        return ImpliedGrowth("missing_fcf")
    if fcf_per_share <= 0:
        return ImpliedGrowth("non_positive_fcf")
    lo, hi = DCF_GROWTH_LOW, DCF_GROWTH_HIGH
    if dcf_value(fcf_per_share, lo) >= price:
        return ImpliedGrowth("below_search_range")
    if dcf_value(fcf_per_share, hi) < price:
        return ImpliedGrowth("above_search_range")
    for _ in range(200):
        mid = (lo + hi) / 2
        if dcf_value(fcf_per_share, mid) < price:
            lo = mid
        else:
            hi = mid
        if hi - lo < 1e-9:
            break
    return ImpliedGrowth("solved", hi)


def parse_percent(value: str | None) -> float | None:
    """Parse '2.86%' to 0.0286; None for missing or non-numeric placeholders."""
    if value is None:
        return None
    raw = value.strip().rstrip("%").strip()
    try:
        return float(raw) / 100
    except ValueError:
        return None


def implied_growth_from_fcf_yield(fcf_yield: float | None, ticker: str | None = None) -> ImpliedGrowth:
    """Reverse DCF on a yield basis: price / FCF per share equals 1 / FCF yield.

    A stored yield of exactly 0 means the fetch had no FCF, not that FCF is zero.
    A positive yield outside [FCF_YIELD_MIN, FCF_YIELD_MAX] returns `implausible_fcf_yield`.
    """
    if ticker and ticker in KNOWN_CURRENCY_MISMATCHES:
        return ImpliedGrowth("currency_mismatch")
    if fcf_yield is None or fcf_yield == 0:
        return ImpliedGrowth("missing_fcf")
    if fcf_yield < 0:
        return ImpliedGrowth("non_positive_fcf")
    if not FCF_YIELD_MIN <= fcf_yield <= FCF_YIELD_MAX:
        return ImpliedGrowth("implausible_fcf_yield")
    return solve_implied_growth(1.0 / fcf_yield, 1.0)


def implied_growth_from_stored_yield(stored: str | None, ticker: str | None = None) -> ImpliedGrowth:
    """Reverse DCF from a stored `valuation.fcf_yield` string such as '2.86%', 'N/A' or 'currency_mismatch'."""
    if stored == CURRENCY_MISMATCH:
        return ImpliedGrowth(CURRENCY_MISMATCH)
    return implied_growth_from_fcf_yield(parse_percent(stored), ticker=ticker)


def format_rate(rate: float) -> str:
    """Format a growth rate as a percentage with one decimal, never as -0.0%."""
    text = f"{rate * 100:.1f}"
    return f"{'0.0' if text == '-0.0' else text}%"


def implied_growth_lines(result: ImpliedGrowth, basis: str | None = None) -> list[str]:
    """The three value_metrics lines that record a reverse DCF result."""
    rate = "n/a" if result.rate is None else format_rate(result.rate)
    if basis is None:
        basis = (
            f"fcf_yield r={DCF_DISCOUNT_RATE:.0%} terminal={DCF_TERMINAL_GROWTH:.0%} "
            f"years={DCF_YEARS} range={DCF_GROWTH_LOW:.0%} to {DCF_GROWTH_HIGH:.0%}"
        )
    return [
        f"  implied_growth_rate: {rate}",
        f"  implied_growth_status: {result.status}",
        f"  implied_growth_basis: {basis}",
    ]


def replace_implied_growth(lines: list[str], result: ImpliedGrowth, basis: str | None = None) -> list[str]:
    """Shared helper to replace implied growth fields inside value_metrics block."""
    block = get_block(lines, "value_metrics")
    if block is None:
        return lines
    stale = ("implied_growth_rate:", "implied_growth_status:", "implied_growth_basis:")
    body = [line for line in block[1:] if not line.strip().startswith(stale)]
    new_block = [block[0], *implied_growth_lines(result, basis), *body]
    return set_block(lines, "value_metrics", new_block)


def apply_implied_growth(lines: list[str], ticker: str | None = None) -> tuple[list[str], ImpliedGrowth | None]:
    """Recompute implied growth inside `value_metrics` from its own `valuation.fcf_yield`."""
    block = get_block(lines, "value_metrics")
    if block is None:
        return lines, None
    result = implied_growth_from_stored_yield(block_fields(block).get("valuation.fcf_yield"), ticker=ticker)
    return replace_implied_growth(lines, result), result


def format_ratio(value: float | None) -> str:
    """Format a ratio such as D/E or PEG; None and exact zero are missing, as legacy writers stored failures as 0."""
    if value is None or value == 0:
        return MISSING
    return f"{value:.2f}" if abs(value) >= 0.005 else f"{value:.2g}"


def normalize_value_metrics(lines: list[str], ticker: str | None = None) -> list[str]:
    """Replace legacy placeholder zeros in `value_metrics` with N/A and apply the currency guard.

    A D/E or PEG of exactly 0 and an FCF yield of exactly 0% were written for failed fetches.
    An FCF yield for a ticker in KNOWN_CURRENCY_MISMATCHES divides home-currency cash flow by a
    foreign-currency market cap, so it is replaced with `currency_mismatch`.
    """
    block = get_block(lines, "value_metrics")
    if block is None:
        return lines
    new_block = [block[0]]
    for line in block[1:]:
        indent = line[: len(line) - len(line.lstrip(" "))]
        key, _, value = line.strip().partition(":")
        value = value.strip()
        if key in ("debt_to_equity", "peg_ratio") and value in ("0", "0.0", "0.00"):
            line = f"{indent}{key}: {MISSING}"
        elif key == "fcf_yield":
            if ticker in KNOWN_CURRENCY_MISMATCHES:
                line = f"{indent}{key}: {CURRENCY_MISMATCH}"
            elif value in ("0%", "0.0%", "0.00%"):
                line = f"{indent}{key}: {MISSING}"
        new_block.append(line)
    return set_block(lines, "value_metrics", new_block)
