"""Progress analytics: readiness scores, next topics, weekly plans and the review queue.

Every score here is a transparent formula over the vault and the state file, so a
number shown on the dashboard can always be explained:

- topic readiness = mastery / 4 when the topic has no cards, otherwise
  0.5 * mastery / 4 + 0.5 * card maturity, where card maturity is the mean over
  its cards of min(interval / 21 days, 1) (0 for unseen cards).
- track or firm readiness = mean topic readiness weighted by est_hours * tier weight.
"""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass

from .state import Store, today
from .vault import TIERS, Card, Note, Vault

TIER_WEIGHT = {"core": 1.0, "advanced": 0.6, "senior": 0.4}
MATURE_DAYS = 21
SOLID = 3  # mastery level at which a topic counts as learned


def card_maturity(store: Store, cards: list[Card]) -> float | None:
    if not cards:
        return None
    return sum(min(store.card(c.id).interval / MATURE_DAYS, 1.0) for c in cards) / len(cards)


def topic_readiness(store: Store, note: Note) -> float:
    base = store.mastery(note.id) / 4
    maturity = card_maturity(store, note.cards)
    return base if maturity is None else 0.5 * base + 0.5 * maturity


def weight(note: Note) -> float:
    return max(note.est_hours, 1.0) * TIER_WEIGHT.get(note.tier, 1.0)


def weighted_readiness(store: Store, notes: list[Note]) -> float:
    total = sum(weight(n) for n in notes)
    return sum(weight(n) * topic_readiness(store, n) for n in notes) / total if total else 0.0


@dataclass
class TrackSummary:
    track: str
    topics: int
    solid: int
    readiness: float
    hours_left: float


def remaining_hours(store: Store, note: Note) -> float:
    return note.est_hours * max(0, SOLID - store.mastery(note.id)) / SOLID


def track_summary(vault: Vault, store: Store, track: str) -> TrackSummary:
    topics = vault.topics([track])
    return TrackSummary(
        track,
        len(topics),
        sum(store.mastery(t.id) >= SOLID for t in topics),
        weighted_readiness(store, topics),
        sum(remaining_hours(store, t) for t in topics),
    )


def firm_focus(vault: Vault, firm: Note) -> list[Note]:
    ids = firm.meta.get("focus") or []
    focus = [vault.notes[i] for i in ids if i in vault.notes and vault.notes[i].trackable]
    return focus or vault.topics(firm.tracks)


def firm_readiness(vault: Vault, store: Store, firm: Note) -> float:
    return weighted_readiness(store, firm_focus(vault, firm))


def blockers(vault: Vault, store: Store, note: Note) -> list[str]:
    """Prerequisites not yet at 'practiced' (mastery 2)."""
    return [p for p in note.prereqs if p in vault.notes and store.mastery(p) < 2]


def _priority(note: Note) -> tuple:
    return (TIERS.index(note.tier) if note.tier in TIERS else 9, note.section, note.order)


def next_topics(vault: Vault, store: Store, tracks: list[str], limit: int = 5) -> list[tuple[Note, list[str]]]:
    """Unlearned topics, unblocked first, then by tier and syllabus order."""
    open_ = [n for n in vault.topics(tracks) if store.mastery(n.id) < SOLID]
    ranked = sorted(open_, key=lambda n: (bool(blockers(vault, store, n)), store.mastery(n.id) == 0, _priority(n)))
    return [(n, blockers(vault, store, n)) for n in ranked[:limit]]


def study_order(vault: Vault, store: Store, tracks: list[str], tiers: tuple[str, ...] = TIERS) -> list[Note]:
    """Topological order of unlearned topics for the tracks, pulling in unlearned prerequisites
    from other tracks. Ties break by tier, then syllabus order."""
    wanted: dict[str, Note] = {}
    stack = [n for n in vault.topics(tracks) if n.tier in tiers and store.mastery(n.id) < SOLID]
    while stack:
        n = stack.pop()
        if n.id in wanted:
            continue
        wanted[n.id] = n
        stack.extend(vault.notes[p] for p in n.prereqs if p in vault.notes and vault.notes[p].trackable and store.mastery(p) < SOLID)
    indeg = {i: 0 for i in wanted}
    children: dict[str, list[str]] = {i: [] for i in wanted}
    for n in wanted.values():
        for p in n.prereqs:
            if p in wanted:
                indeg[n.id] += 1
                children[p].append(n.id)
    ready = sorted((wanted[i] for i, d in indeg.items() if d == 0), key=_priority)
    order: list[Note] = []
    while ready:
        n = ready.pop(0)
        order.append(n)
        for c in children[n.id]:
            indeg[c] -= 1
            if indeg[c] == 0:
                ready.append(wanted[c])
        ready.sort(key=_priority)
    if len(order) != len(wanted):  # a cycle; qp check reports it, keep the plan usable
        order += sorted((n for n in wanted.values() if n not in order), key=_priority)
    return order


def weekly_plan(
    vault: Vault, store: Store, tracks: list[str], hours_per_week: float, tiers: tuple[str, ...] = TIERS, start: dt.date | None = None
) -> list[dict]:
    if hours_per_week <= 0:
        raise ValueError("hours_per_week must be positive")
    start = start or today()
    weeks: list[dict] = []
    current: dict | None = None
    for note in study_order(vault, store, tracks, tiers):
        hours = max(remaining_hours(store, note), 0.5)
        if current is None or (current["hours"] + hours > hours_per_week and current["topics"]):
            current = {"week": len(weeks) + 1, "starts": (start + dt.timedelta(weeks=len(weeks))).isoformat(), "hours": 0.0, "topics": []}
            weeks.append(current)
        current["topics"].append(note)
        current["hours"] += hours
    return weeks


def due_cards(vault: Vault, store: Store, tracks: list[str] | None = None, limit: int | None = None) -> list[Card]:
    """Review cards due today (oldest first), then new cards up to the daily new-card budget,
    in syllabus order. Cards belong to the profile's tracks via their note."""
    t = today().isoformat()
    due, new = [], []
    for note in vault.topics(tracks):
        for card in note.cards:
            sched = store.card(card.id)
            if not sched.due:
                new.append(card)
            elif sched.due <= t:
                due.append((sched.due, card))
    due.sort(key=lambda x: x[0])
    budget = max(0, int(store.profile.get("new_cards_per_day", 20)) - store.new_cards_seen_today())
    out = [c for _, c in due] + new[:budget]
    return out[:limit] if limit else out


def counts(vault: Vault, store: Store, tracks: list[str] | None = None) -> dict:
    t = today().isoformat()
    cards = [c for n in vault.topics(tracks) for c in n.cards]
    seen = [store.card(c.id) for c in cards if store.card(c.id).due]
    return {
        "cards": len(cards),
        "cards_seen": len(seen),
        "cards_due": sum(1 for s in seen if s.due <= t),
        "cards_mature": sum(1 for s in seen if s.interval >= MATURE_DAYS),
    }
