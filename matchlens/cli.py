"""Command line interface.

Usage:
    python -m matchlens.cli events.csv [--teams teams.csv] [--html report.html]
                                     [--lang zh|en] [--live] [--delay 0.2]
    python -m matchlens.cli --gen 7 --out examples/gen.csv \
        [--teams-out examples/gen_teams.csv] [--home-name "..." --away-name "..."]
"""
from __future__ import annotations

import argparse
import json
import sys

from . import core
from . import generate
from . import i18n
from . import live as live_mod
from . import report


def main(argv=None):
    p = argparse.ArgumentParser(
        prog="matchlens",
        description="MatchLens — 离线可解释足球战报智能体（零依赖）/ "
                    "offline explainable match-intelligence agent")
    p.add_argument("events", nargs="?", default=None,
                   help="比赛事件 CSV（minute,team,player,event_type,detail,xg）")
    p.add_argument("--teams", help="球队名 CSV（code,name）")
    p.add_argument("--html", help="输出 HTML 报告路径")
    p.add_argument("--question", help="要回答的问题（可选）")
    p.add_argument("--json", action="store_true", help="同时打印 JSON 结果")
    p.add_argument("--lang", choices=i18n.LANGS, default="zh",
                   help="输出语言 / output language")
    p.add_argument("--live", action="store_true",
                   help="实时模式：按事件流逐条播报 / real-time narration")
    p.add_argument("--delay", type=float, default=0.0,
                   help="实时模式每条事件的播报间隔（秒）/ live pacing seconds")
    # generator mode
    p.add_argument("--gen", type=int, metavar="SEED", default=None,
                   help="生成一场合成比赛（确定性种子）并退出 / generate a synthetic match")
    p.add_argument("--out", help="生成模式的事件 CSV 输出路径")
    p.add_argument("--teams-out", help="生成模式的球队 CSV 输出路径")
    p.add_argument("--home-name", default="Blue Lions FC")
    p.add_argument("--away-name", default="Red Eagles")
    args = p.parse_args(argv)
    lang = args.lang

    # ---- generator mode ----------------------------------------------------
    if args.gen is not None:
        if not args.out:
            p.error("--gen requires --out PATH")
        events = generate.generate_match(seed=args.gen)
        names = {"BL": args.home_name, "RH": args.away_name}
        generate.write_csvs(events, args.out, args.teams_out, names)
        print(f"[gen] seed={args.gen} -> {args.out} ({len(events)} events)")
        if args.teams_out:
            print(f"[gen] teams -> {args.teams_out}")
        return 0

    if not args.events:
        p.error("events CSV is required (or use --gen SEED --out PATH)")

    # ---- live mode -----------------------------------------------------------
    if args.live:
        print(i18n.t(lang, "cli_live_banner"))
        events = core.load_events(args.events)
        names = core.load_teams(args.teams) if args.teams else {}
        narrator = live_mod.LiveNarrator(names, lang)
        narrator.replay(events, on_line=lambda ln: print("  " + ln),
                        delay=args.delay)
        return 0

    # ---- batch analysis ------------------------------------------------------
    r = core.analyze(args.events, args.teams, args.question, lang)
    names = r["names"]
    stats = r["stats"]

    print("=" * 68)
    print(i18n.t(lang, "cli_title"))
    print("=" * 68)
    if r["question"]:
        print(f"{i18n.t(lang, 'cli_question')}: {r['question']}")
    for name, line in r["steps"]:
        print(f"[{name}] {line}")
    print("-" * 68)

    print(f"{i18n.t(lang, 'cli_scoreline')}:")
    for t in sorted(stats, key=lambda t: -stats[t]["goals"]):
        s = stats[t]
        print("  " + i18n.t(lang, "cli_stats_line", name=names.get(t, t),
                            goals=s["goals"], shots=s["shots"], sot=s["sot"],
                            xg=f"{s['xg']:.2f}", yellow=s["yellow"], red=s["red"],
                            ps=s["pens_scored"], pm=s["pens_missed"]))

    print(f"\n{i18n.t(lang, 'cli_moments_header', n=len(r['moments']))}:")
    for m in r["moments"]:
        sc = "-".join(str(v) for _, v in
                      sorted(m["score"].items(), key=lambda kv: kv[0]))
        print(f"  {m['minute_raw']:>5}' [{m['kind']:8}] {names.get(m['team'], m['team'])} "
              f"{m['text']}  (score {sc})")

    print(f"\n{i18n.t(lang, 'cli_insights_header', n=len(r['insights']))}:")
    for f in r["insights"]:
        print(f"  * {f['title']}: {f['detail']}")
        for ev in f["evidence"]:
            print(f"      {i18n.t(lang, 'cli_evidence')}: {ev}")

    print(f"\n{i18n.t(lang, 'cli_recap')}: {r['recap']}")
    print(f"{i18n.t(lang, 'cli_label')}: {r['label']}")
    print(f"\n{i18n.t(lang, 'cli_next')}:")
    for i, a in enumerate(r["next_actions"], 1):
        print(f"  {i}. {a}")
    print("\n" + i18n.t(lang, "cli_disclaimer"))

    if args.html:
        report.write_html(r, args.html, lang)
        print(f"\n{i18n.t(lang, 'cli_html_written')}: {args.html}")
    if args.json:
        print(json.dumps(r, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
