"""MatchLens core — offline explainable match-intelligence agent (zero deps).

Agent loop: PERCEIVE -> INDEX -> RETRIEVE -> REASON -> EXPLAIN -> ACT
Reads a match events CSV, computes stats, extracts key moments, runs insight
rules, and generates a cited natural-language recap. No network, no deps.

All user-visible prose goes through i18n.t(lang, ...) so the same analysis
can be rendered in Chinese or English (see --lang).
"""
from __future__ import annotations

import csv

from . import i18n

_SHOT_TYPES = ("GOAL", "OWN_GOAL", "SHOT", "SHOT_ON_TARGET", "PENALTY_MISSED")
_SOT_TYPES = ("GOAL", "SHOT_ON_TARGET")


def _f(x, default=None):
    try:
        return float(str(x).strip().replace(",", ""))
    except (TypeError, ValueError):
        return default


def _minute(x):
    x = str(x).strip()
    if not x:
        return None
    try:
        if "+" in x:
            base, extra = x.split("+", 1)
            return float(base) + float(extra or 0) / 100.0
        return float(x)
    except ValueError:
        return None


def _finding(rule, title, detail, evidence, metric=None):
    return {"rule": rule, "title": title, "detail": detail,
            "evidence": evidence, "metric": metric}


def load_events(path):
    events = []
    with open(path, newline="", encoding="utf-8-sig") as fh:
        for i, row in enumerate(csv.DictReader(fh), start=2):
            events.append({
                "src": path.replace("\\", "/").split("/")[-1],
                "row": i,
                "minute": _minute(row.get("minute")),
                "minute_raw": (row.get("minute") or "").strip(),
                "team": (row.get("team") or "?").strip().upper(),
                "player": (row.get("player") or "").strip(),
                "type": (row.get("event_type") or "").strip().upper(),
                "detail": (row.get("detail") or "").strip(),
                "xg": _f(row.get("xg")),
            })
    events.sort(key=lambda e: (e["minute"] if e["minute"] is not None else 0.0, e["row"]))
    return events


def load_teams(path):
    teams = {}
    with open(path, newline="", encoding="utf-8-sig") as fh:
        for row in csv.DictReader(fh):
            code = (row.get("code") or "").strip().upper()
            if code:
                teams[code] = (row.get("name") or code).strip()
    return teams


def _cite(e):
    tail = f" xG={e['xg']:.2f}" if e["xg"] is not None else ""
    det = f"（{e['detail']}）" if e["detail"] else ""
    return (f"{e['src']} L{e['row']} {e['minute_raw']}' {e['team']} "
            f"{e['type']} {e['player']}{tail}{det}")


def compute_stats(events):
    stats = {}
    for e in events:
        s = stats.setdefault(e["team"], {
            "goals": 0, "shots": 0, "sot": 0, "xg": 0.0,
            "yellow": 0, "red": 0, "subs_in": 0,
            "pens_scored": 0, "pens_missed": 0})
        t = e["type"]
        if t == "GOAL":
            s["goals"] += 1
        if t in _SHOT_TYPES:
            s["shots"] += 1
        if t in _SOT_TYPES:
            s["sot"] += 1
        if t == "YELLOW_CARD":
            s["yellow"] += 1
        if t == "RED_CARD":
            s["red"] += 1
        if t == "SUB_IN":
            s["subs_in"] += 1
        if t == "PENALTY_MISSED":
            s["pens_missed"] += 1
        if t == "GOAL" and ("pen" in e["detail"].lower() or "点球" in e["detail"]):
            s["pens_scored"] += 1
        if e["xg"] is not None:
            s["xg"] += e["xg"]
    return stats


def extract_moments(events, lang="zh"):
    moments = []
    score = {e["team"]: 0 for e in events}
    for e in events:
        if e["type"] == "GOAL":
            score[e["team"]] = score.get(e["team"], 0) + 1
            key = "moment_goal_detail" if e["detail"] else "moment_goal"
            moments.append({
                "minute": e["minute"], "minute_raw": e["minute_raw"],
                "kind": "GOAL", "team": e["team"], "key": True,
                "text": i18n.t(lang, key, player=e["player"], detail=e["detail"]),
                "score": dict(score), "cite": _cite(e)})
        elif e["type"] == "PENALTY_MISSED":
            key = "moment_pen_miss_detail" if e["detail"] else "moment_pen_miss"
            moments.append({
                "minute": e["minute"], "minute_raw": e["minute_raw"],
                "kind": "PEN_MISS", "team": e["team"], "key": True,
                "text": i18n.t(lang, key, player=e["player"], detail=e["detail"]),
                "score": dict(score), "cite": _cite(e)})
        elif e["type"] == "RED_CARD":
            key = "moment_red_detail" if e["detail"] else "moment_red"
            moments.append({
                "minute": e["minute"], "minute_raw": e["minute_raw"],
                "kind": "RED", "team": e["team"], "key": True,
                "text": i18n.t(lang, key, player=e["player"], detail=e["detail"]),
                "score": dict(score), "cite": _cite(e)})
        elif e["type"] == "YELLOW_CARD":
            key = "moment_yellow_detail" if e["detail"] else "moment_yellow"
            moments.append({
                "minute": e["minute"], "minute_raw": e["minute_raw"],
                "kind": "YELLOW", "team": e["team"], "key": False,
                "text": i18n.t(lang, key, player=e["player"], detail=e["detail"]),
                "score": dict(score), "cite": _cite(e)})
    return moments


def run_rules(events, stats, names, lang="zh"):
    out = []
    teams = sorted(stats)

    # R1 finishing efficiency --------------------------------------------------
    for t in teams:
        s = stats[t]
        if s["shots"] >= 3:
            diff = s["goals"] - s["xg"]
            ev = [_cite(e) for e in events
                  if e["team"] == t and e["type"] in _SHOT_TYPES][:5]
            if diff >= 0.5:
                out.append(_finding(
                    "CLINICAL_FINISHING", i18n.t(lang, "rule_clinical"),
                    i18n.t(lang, "detail_clinical", name=names.get(t, t),
                           goals=s["goals"], xg=f"{s['xg']:.2f}", diff=f"{diff:.2f}"),
                    ev, diff))
            elif diff <= -0.5:
                out.append(_finding(
                    "WASTEFUL_ATTACK", i18n.t(lang, "rule_wasteful"),
                    i18n.t(lang, "detail_wasteful", name=names.get(t, t),
                           goals=s["goals"], xg=f"{s['xg']:.2f}", diff=f"{diff:.2f}"),
                    ev, diff))

    # R2 man-down effect after a red card ---------------------------------------
    reds = [e for e in events if e["type"] == "RED_CARD"]
    if reds:
        r = reds[0]
        m = r["minute"] or 0.0
        after = [e for e in events if (e["minute"] or 0) > m and e["xg"] is not None]
        before = [e for e in events if (e["minute"] or 0) <= m and e["xg"] is not None]
        xf_a = sum(e["xg"] for e in after if e["team"] == r["team"])
        xa_a = sum(e["xg"] for e in after if e["team"] != r["team"])
        xf_b = sum(e["xg"] for e in before if e["team"] == r["team"])
        xa_b = sum(e["xg"] for e in before if e["team"] != r["team"])
        out.append(_finding(
            "MAN_DOWN_EFFECT", i18n.t(lang, "rule_man_down"),
            i18n.t(lang, "detail_man_down", name=names.get(r["team"], r["team"]),
                   minute=r["minute_raw"], xb=f"{xf_b:.2f}", xa=f"{xf_a:.2f}",
                   ob=f"{xa_b:.2f}", oa=f"{xa_a:.2f}"),
            [_cite(r)] + [_cite(e) for e in after][:4],
            xf_a + xa_a))

    # R3 substitute impact --------------------------------------------------------
    for i, e in enumerate(events):
        if e["type"] == "SUB_IN":
            for x in events[i + 1:]:
                if (x["team"] == e["team"] and x["type"] == "GOAL"
                        and (x["minute"] or 0) - (e["minute"] or 0) <= 12):
                    out.append(_finding(
                        "SUB_IMPACT", i18n.t(lang, "rule_sub_impact"),
                        i18n.t(lang, "detail_sub_impact", name=names.get(e["team"], e["team"]),
                               player=e["player"], minute=e["minute_raw"],
                               gminute=x["minute_raw"]),
                        [_cite(e), _cite(x)],
                        (x["minute"] or 0) - (e["minute"] or 0)))
                    break

    # R4 momentum phase (15-minute xG bins) ----------------------------------------
    bins = {}
    for e in events:
        if e["xg"] is None:
            continue
        b = int(min(e["minute"] or 0.0, 89.99) // 15) * 15
        bins.setdefault(b, {}).setdefault(e["team"], 0.0)
        bins[b][e["team"]] += e["xg"]
    best_b, best_diff, best_lead = None, 0.0, None
    for b, d in bins.items():
        ts = sorted(d)
        if len(ts) == 2:
            diff = abs(d[ts[0]] - d[ts[1]])
            if diff > best_diff:
                best_b, best_diff, best_lead = b, diff, max(ts, key=lambda t: d[t])
    if best_b is not None and best_diff >= 0.4:
        d = bins[best_b]
        other = [t for t in sorted(d) if t != best_lead][0]
        out.append(_finding(
            "MOMENTUM_PHASE", i18n.t(lang, "rule_momentum"),
            i18n.t(lang, "detail_momentum", b=best_b, be=best_b + 15,
                   name=names.get(best_lead, best_lead), xa=f"{d[best_lead]:.2f}",
                   xb=f"{d[other]:.2f}"),
            [_cite(e) for e in events
             if e["xg"] is not None
             and int(min(e["minute"] or 0.0, 89.99) // 15) * 15 == best_b][:5],
            best_diff))

    # R5 discipline ------------------------------------------------------------------
    y = sum(s["yellow"] for s in stats.values())
    r_ = sum(s["red"] for s in stats.values())
    if y or r_:
        parts = "；".join(
            i18n.t(lang, "detail_discipline_part", name=names.get(t, t),
                   y=stats[t]["yellow"], r=stats[t]["red"])
            for t in teams)
        out.append(_finding(
            "DISCIPLINE", i18n.t(lang, "rule_discipline"),
            i18n.t(lang, "detail_discipline", parts=parts, y=y, r=r_),
            [_cite(e) for e in events
             if e["type"] in ("YELLOW_CARD", "RED_CARD")][:5],
            float(y + r_ * 2)))
    return out


def competitiveness(stats, lang="zh"):
    ts = sorted(stats, key=lambda t: (-stats[t]["goals"], t))
    gd = abs(stats[ts[0]]["goals"] - stats[ts[1]]["goals"])
    xd = abs(stats[ts[0]]["xg"] - stats[ts[1]]["xg"])
    if gd == 0:
        return i18n.t(lang, "shape_draw")
    if gd == 1:
        return i18n.t(lang, "shape_one_goal")
    if xd <= 0.5:
        return i18n.t(lang, "shape_lopsided")
    return i18n.t(lang, "shape_onesided")


def build_recap(events, stats, names, moments, lang="zh"):
    teams = sorted(stats, key=lambda t: (-stats[t]["goals"], -stats[t]["xg"], t))
    hi, lo = teams[0], teams[1]
    hs, ls = stats[hi], stats[lo]
    parts = [i18n.t(lang, "recap_opener", hi=names.get(hi, hi), hg=hs["goals"],
                    lg=ls["goals"], lo=names.get(lo, lo))]
    goals = [m for m in moments if m["kind"] == "GOAL"]
    if goals:
        seq = "；".join(
            i18n.t(lang, "recap_goal_item", minute=m["minute_raw"],
                   team=names.get(m["team"], m["team"]), text=m["text"])
            for m in goals)
        parts.append(i18n.t(lang, "recap_goals_seq", seq=seq))
    xd = abs(hs["xg"] - ls["xg"])
    if xd <= 0.5:
        parts.append(i18n.t(lang, "recap_xg_even", hx=f"{hs['xg']:.2f}",
                            lx=f"{ls['xg']:.2f}"))
    else:
        lead = hi if hs["xg"] >= ls["xg"] else lo
        parts.append(i18n.t(lang, "recap_xg_lead", hx=f"{hs['xg']:.2f}",
                            lx=f"{ls['xg']:.2f}", lead=names.get(lead, lead)))
    reds = [e for e in events if e["type"] == "RED_CARD"]
    if reds:
        r = reds[0]
        parts.append(i18n.t(lang, "recap_red", team=names.get(r["team"], r["team"]),
                            minute=r["minute_raw"], player=r["player"]))
    for i, e in enumerate(events):
        if e["type"] == "SUB_IN":
            for x in events[i + 1:]:
                if (x["team"] == e["team"] and x["type"] == "GOAL"
                        and (x["minute"] or 0) - (e["minute"] or 0) <= 12):
                    parts.append(i18n.t(lang, "recap_sub", player=e["player"],
                                        minute=e["minute_raw"],
                                        gminute=x["minute_raw"]))
                    break
    pens = [e for e in events if e["type"] == "PENALTY_MISSED"]
    if pens:
        p = pens[0]
        parts.append(i18n.t(lang, "recap_pen", minute=p["minute_raw"],
                            team=names.get(p["team"], p["team"]), player=p["player"]))
    return "".join(parts)


def analyze(events_path, teams_path=None, question=None, lang="zh"):
    events = load_events(events_path)
    names = load_teams(teams_path) if teams_path else {}
    stats = compute_stats(events)
    moments = extract_moments(events, lang)
    insights = run_rules(events, stats, names, lang)
    label = competitiveness(stats, lang)
    recap = build_recap(events, stats, names, moments, lang)
    nexts = i18n.next_actions(lang)

    steps = [
        ("PERCEIVE", i18n.t(lang, "step_perceive", n=len(events),
                            teams=", ".join(names.get(t, t) for t in sorted(stats)))),
        ("INDEX", i18n.t(lang, "step_index", n=len(moments))),
        ("RETRIEVE", i18n.t(lang, "step_retrieve", n=len(insights))),
        ("REASON", i18n.t(lang, "step_reason", label=label)),
        ("EXPLAIN", i18n.t(lang, "step_explain", n=len(insights))),
        ("ACT", i18n.t(lang, "step_act", n=len(nexts))),
    ]

    return {"question": question, "events": len(events), "stats": stats,
            "names": names, "moments": moments, "insights": insights,
            "label": label, "recap": recap, "steps": steps,
            "next_actions": nexts, "lang": lang}
