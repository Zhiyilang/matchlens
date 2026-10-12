"""Command line interface.

Usage:
    python -m matchlens.cli events.csv [--teams teams.csv] [--html report.html]
"""
from __future__ import annotations

import argparse
import json
import sys

from . import core
from . import report


def main(argv=None):
    p = argparse.ArgumentParser(
        prog="matchlens",
        description="MatchLens — 离线可解释足球战报智能体（零依赖）")
    p.add_argument("events", help="比赛事件 CSV（minute,team,player,event_type,detail,xg）")
    p.add_argument("--teams", help="球队名 CSV（code,name）")
    p.add_argument("--html", help="输出 HTML 报告路径")
    p.add_argument("--question", help="要回答的问题（可选）")
    p.add_argument("--json", action="store_true", help="同时打印 JSON 结果")
    args = p.parse_args(argv)

    r = core.analyze(args.events, args.teams, args.question)
    names = r["names"]
    stats = r["stats"]

    print("=" * 68)
    print("MatchLens — 可解释足球战报智能体（离线 · 零依赖）")
    print("=" * 68)
    if r["question"]:
        print(f"问题: {r['question']}")
    for name, line in r["steps"]:
        print(f"[{name}] {line}")
    print("-" * 68)

    print("比分与数据:")
    for t in sorted(stats, key=lambda t: -stats[t]["goals"]):
        s = stats[t]
        print(f"  {names.get(t, t)}: {s['goals']} 球 | 射门 {s['shots']} "
              f"(射正 {s['sot']}) | xG {s['xg']:.2f} | "
              f"黄 {s['yellow']} 红 {s['red']} | 点球进 {s['pens_scored']} 失 {s['pens_missed']}")

    print(f"\n关键节点（共 {len(r['moments'])}）:")
    for m in r["moments"]:
        sc = "-".join(str(v) for _, v in
                      sorted(m["score"].items(), key=lambda kv: kv[0]))
        print(f"  {m['minute_raw']:>5}' [{m['kind']:8}] {names.get(m['team'], m['team'])} "
              f"{m['text']}  (比分 {sc})")

    print(f"\n洞察（{len(r['insights'])} 条）:")
    for f in r["insights"]:
        print(f"  * {f['title']}: {f['detail']}")
        for ev in f["evidence"]:
            print(f"      证据: {ev}")

    print(f"\n战报: {r['recap']}")
    print(f"比赛形态: {r['label']}")
    print("\n后续分析建议:")
    for i, a in enumerate(r["next_actions"], 1):
        print(f"  {i}. {a}")
    print("\n免责声明：本工具基于事件数据生成分析，不构成任何投注建议。")

    if args.html:
        report.write_html(r, args.html)
        print(f"\nHTML 报告已生成: {args.html}")
    if args.json:
        print(json.dumps(r, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
