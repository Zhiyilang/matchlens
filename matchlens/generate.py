"""Synthetic match-event generator — "expand datasets for AI and analytics".

The Microsoft x Premier League brief supplies synthetic, football-realistic
data. MatchLens ships with one hand-authored demo match; this module can
manufacture unlimited additional matches (deterministic per seed) so analysts
can stress-test insight rules across many games.

Model (all seeded, all offline):
- shots arrive in a non-homogeneous Poisson-ish stream, more likely as the
  match progresses and slightly more for the "home" side
- each shot gets an xG by zone (close range > penalty > header > long range)
- a goal is scored with probability xG (so xG totals stay realistic)
- cards, subs and the occasional missed penalty round out the event mix
"""
from __future__ import annotations

import csv
import random

EVENT_HEADER = ["minute", "team", "player", "event_type", "detail", "xg"]

_ZONES = [
    # (weight, detail, xg_lo, xg_hi)
    (10, "inside box", 0.10, 0.45),
    (14, "inside box", 0.05, 0.20),
    (10, "header", 0.05, 0.25),
    (12, "long range", 0.02, 0.08),
    (6, "penalty", 0.72, 0.80),
    (8, "counter attack", 0.15, 0.50),
]
_CARD_DETAILS = ["late challenge", "tactical foul", "dissent", "reckless tackle"]
_SUB_MINUTES = (55, 80)


def _xg_for_zone(rng):
    w, detail, lo, hi = rng.choices(
        _ZONES, weights=[z[0] for z in _ZONES], k=1)[0]
    return detail, round(rng.uniform(lo, hi), 2)


def generate_match(seed=1, home="BL", away="RH", n_players=11):
    """Return a deterministic list of event dicts for one synthetic match."""
    rng = random.Random(seed)
    events = []
    minute = 1.0
    while minute < 90.0:
        # gap between events shrinks slightly as the match goes on
        gap = rng.uniform(1.0, 5.0) * (1.0 - 0.25 * (minute / 90.0))
        minute = min(90.0, minute + gap)
        m_raw = f"{int(minute)}"
        team = home if rng.random() < 0.53 else away
        player = f"No.{rng.randint(1, n_players)}"

        r = rng.random()
        if r < 0.10:  # card
            etype = "RED_CARD" if rng.random() < 0.12 else "YELLOW_CARD"
            events.append({"minute": minute, "minute_raw": m_raw, "team": team,
                           "player": player, "type": etype,
                           "detail": rng.choice(_CARD_DETAILS), "xg": None})
        elif r < 0.20:  # substitution
            events.append({"minute": minute, "minute_raw": m_raw, "team": team,
                           "player": player, "type": "SUB_IN",
                           "detail": rng.choice(["tactical", "injury", "fresh legs"]),
                           "xg": None})
        elif r < 0.23 and minute > 20:  # occasional penalty
            xg = round(rng.uniform(0.72, 0.80), 2)
            if rng.random() < xg:
                events.append({"minute": minute, "minute_raw": m_raw, "team": team,
                               "player": player, "type": "GOAL",
                               "detail": "penalty", "xg": xg})
            else:
                events.append({"minute": minute, "minute_raw": m_raw, "team": team,
                               "player": player, "type": "PENALTY_MISSED",
                               "detail": rng.choice(["saved", "off the post", "over the bar"]),
                               "xg": xg})
        else:  # open-play shot
            zone, xg = _xg_for_zone(rng)
            scored = rng.random() < xg
            events.append({"minute": minute, "minute_raw": m_raw, "team": team,
                           "player": player,
                           "type": "GOAL" if scored else (
                               "SHOT_ON_TARGET" if rng.random() < 0.45 else "SHOT"),
                           "detail": zone, "xg": xg})
    events.sort(key=lambda e: e["minute"])
    return events


def write_csvs(events, events_path, teams_path=None, names=None):
    """Write the events CSV (and optional teams CSV) in MatchLens' schema."""
    with open(events_path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(EVENT_HEADER)
        for e in events:
            w.writerow([e["minute_raw"], e["team"], e["player"], e["type"],
                        e["detail"], "" if e["xg"] is None else e["xg"]])
    if teams_path and names:
        with open(teams_path, "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["code", "name"])
            for code, name in names.items():
                w.writerow([code, name])
    return events_path
