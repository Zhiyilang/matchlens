"""MatchLens core — offline explainable match-intelligence agent (zero deps).

Agent loop: PERCEIVE -> INDEX -> RETRIEVE -> REASON -> EXPLAIN -> ACT
Reads a match events CSV, computes stats, extracts key moments, runs insight
rules, and generates a cited natural-language recap. No network, no deps.
"""
from __future__ import annotations

import csv

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


def extract_moments(events):
    moments = []
    score = {e["team"]: 0 for e in events}
    for e in events:
        if e["type"] == "GOAL":
            score[e["team"]] = score.get(e["team"], 0) + 1
            moments.append({
                "minute": e["minute"], "minute_raw": e["minute_raw"],
                "kind": "GOAL", "team": e["team"], "key": True,
                "text": f"{e['player']} 进球" + (f"（{e['detail']}）" if e["detail"] else ""),
                "score": dict(score), "cite": _cite(e)})
        elif e["type"] == "PENALTY_MISSED":
            moments.append({
                "minute": e["minute"], "minute_raw": e["minute_raw"],
                "kind": "PEN_MISS", "team": e["team"], "key": True,
                "text": f"{e['player']} 罚失点球（{e['detail']}）" if e["detail"]
                        else f"{e['player']} 罚失点球",
                "score": dict(score), "cite": _cite(e)})
        elif e["type"] == "RED_CARD":
            moments.append({
                "minute": e["minute"], "minute_raw": e["minute_raw"],
                "kind": "RED", "team": e["team"], "key": True,
                "text": f"{e['player']} 被红牌罚下" + (f"（{e['detail']}）" if e["detail"] else ""),
                "score": dict(score), "cite": _cite(e)})
        elif e["type"] == "YELLOW_CARD":
            moments.append({
                "minute": e["minute"], "minute_raw": e["minute_raw"],
                "kind": "YELLOW", "team": e["team"], "key": False,
                "text": f"{e['player']} 黄牌" + (f"（{e['detail']}）" if e["detail"] else ""),
                "score": dict(score), "cite": _cite(e)})
    return moments


def run_rules(events, stats, names):
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
                    "CLINICAL_FINISHING", "高效终结",
                    f"{names.get(t, t)} 打进 {s['goals']} 球但 xG 仅 {s['xg']:.2f}"
                    f"（超额 +{diff:.2f}）——临门一脚明显高于平均水准。", ev, diff))
            elif diff <= -0.5:
                out.append(_finding(
                    "WASTEFUL_ATTACK", "挥霍机会",
                    f"{names.get(t, t)} xG {s['xg']:.2f} 却只进 {s['goals']} 球"
                    f"（缺口 {diff:.2f}）——机会质量不差，转化率拖后腿。", ev, diff))

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
            "MAN_DOWN_EFFECT", "红牌连锁反应",
            f"{names.get(r['team'], r['team'])} {r['minute_raw']}' 被罚下后："
            f"本队 xG {xf_b:.2f}->{xf_a:.2f}，被对手 xG {xa_b:.2f}->{xa_a:.2f}。",
            [_cite(r)] + [_cite(e) for e in after][:4],
            xf_a + xa_a))

    # R3 substitute impact --------------------------------------------------------
    for i, e in enumerate(events):
        if e["type"] == "SUB_IN":
            for x in events[i + 1:]:
                if (x["team"] == e["team"] and x["type"] == "GOAL"
                        and (x["minute"] or 0) - (e["minute"] or 0) <= 12):
                    out.append(_finding(
                        "SUB_IMPACT", "替补奇兵",
                        f"{names.get(e['team'], e['team'])} 替补 {e['player']} "
                        f"{e['minute_raw']}' 登场，{x['minute_raw']}' 即取得进球。",
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
            "MOMENTUM_PHASE", "阶段压制",
            f"{best_b}-{best_b + 15} 分钟区间 {names.get(best_lead, best_lead)} "
            f"xG {d[best_lead]:.2f}，对手 {d[other]:.2f}——该阶段明显占优。",
            [_cite(e) for e in events
             if e["xg"] is not None
             and int(min(e["minute"] or 0.0, 89.99) // 15) * 15 == best_b][:5],
            best_diff))

    # R5 discipline ------------------------------------------------------------------
    y = sum(s["yellow"] for s in stats.values())
    r_ = sum(s["red"] for s in stats.values())
    if y or r_:
        parts = [f"{names.get(t, t)} {stats[t]['yellow']} 黄 {stats[t]['red']} 红"
                 for t in teams]
        out.append(_finding(
            "DISCIPLINE", "纪律数据",
            "；".join(parts) + f"（全场共 {y} 黄 {r_} 红）。",
            [_cite(e) for e in events
             if e["type"] in ("YELLOW_CARD", "RED_CARD")][:5],
            float(y + r_ * 2)))
    return out


def competitiveness(stats):
    ts = sorted(stats, key=lambda t: (-stats[t]["goals"], t))
    gd = abs(stats[ts[0]]["goals"] - stats[ts[1]]["goals"])
    xd = abs(stats[ts[0]]["xg"] - stats[ts[1]]["xg"])
    if gd == 0:
        return "平局收场"
    if gd == 1:
        return "一击之差"
    if xd <= 0.5:
        return "比分悬殊但机会均等"
    return "一边倒"


def build_recap(events, stats, names, moments):
    teams = sorted(stats, key=lambda t: (-stats[t]["goals"], -stats[t]["xg"], t))
    hi, lo = teams[0], teams[1]
    hs, ls = stats[hi], stats[lo]
    parts = [f"{names.get(hi, hi)} {hs['goals']}-{ls['goals']} {names.get(lo, lo)}。"]
    goals = [m for m in moments if m["kind"] == "GOAL"]
    if goals:
        seq = "；".join(
            f"{m['minute_raw']}' {names.get(m['team'], m['team'])} {m['text']}"
            for m in goals)
        parts.append(f"进球序列：{seq}。")
    xd = abs(hs["xg"] - ls["xg"])
    if xd <= 0.5:
        parts.append(f"xG {hs['xg']:.2f}-{ls['xg']:.2f}，两队创造的机会几乎均等，"
                     "比分差距主要来自终结效率。")
    else:
        lead = hi if hs["xg"] >= ls["xg"] else lo
        parts.append(f"xG {hs['xg']:.2f}-{ls['xg']:.2f}，"
                     f"{names.get(lead, lead)} 在机会质量上占优。")
    reds = [e for e in events if e["type"] == "RED_CARD"]
    if reds:
        r = reds[0]
        parts.append(f"{names.get(r['team'], r['team'])} {r['minute_raw']}' "
                     f"被红牌罚下（{r['player']}），此后长时间少打一人。")
    for i, e in enumerate(events):
        if e["type"] == "SUB_IN":
            for x in events[i + 1:]:
                if (x["team"] == e["team"] and x["type"] == "GOAL"
                        and (x["minute"] or 0) - (e["minute"] or 0) <= 12):
                    parts.append(f"替补 {e['player']} {e['minute_raw']}' 登场，"
                                 f"{x['minute_raw']}' 建功，成为胜负手之一。")
                    break
    pens = [e for e in events if e["type"] == "PENALTY_MISSED"]
    if pens:
        p = pens[0]
        parts.append(f"{p['minute_raw']}' {names.get(p['team'], p['team'])} "
                     f"罚失点球（{p['player']}），悬念留到最后。")
    return "".join(parts)


NEXT_ACTIONS = [
    "把本场射门事件拆到球员维度，做 xG 贡献排名",
    "对比赛季场均 xG/射门数，判断本场是否属于异常高效/低效",
    "若有传球与站位数据，补传球网络与助攻链分析",
    "对红牌、点球等关键节点回放录像，复核判罚与站位选择",
]


def analyze(events_path, teams_path=None, question=None):
    events = load_events(events_path)
    names = load_teams(teams_path) if teams_path else {}
    stats = compute_stats(events)
    moments = extract_moments(events)
    insights = run_rules(events, stats, names)
    label = competitiveness(stats)
    recap = build_recap(events, stats, names, moments)

    steps = [
        ("PERCEIVE", f"读取 {len(events)} 个比赛事件 | 球队 "
                     f"{', '.join(names.get(t, t) for t in sorted(stats))}"),
        ("INDEX", f"按分钟排序，建立球员/事件类型/xG 索引，"
                  f"识别 {len(moments)} 个关键节点"),
        ("RETRIEVE", f"统计射门/xG/纪律/换人数据，执行 5 类洞察规则，"
                     f"命中 {len(insights)} 条"),
        ("REASON", f"计算比分走势与 xG 对比，判定比赛形态：{label}"),
        ("EXPLAIN", f"生成 {len(insights)} 条洞察（每条附证据引用）"
                    "与自然语言战报"),
        ("ACT", f"给出 {len(NEXT_ACTIONS)} 条后续分析建议"),
    ]

    return {"question": question, "events": len(events), "stats": stats,
            "names": names, "moments": moments, "insights": insights,
            "label": label, "recap": recap, "steps": steps,
            "next_actions": NEXT_ACTIONS}
