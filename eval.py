"""Reproducible assertions for the bundled demo match.

Run:  python eval.py
Exits non-zero if any assertion fails.
"""
from matchlens import core

r = core.analyze("examples/match_events.csv", "examples/teams.csv",
                 question="这场比赛发生了什么？谁的发挥决定了胜负？")

stats, names = r["stats"], r["names"]
bl, rh = stats["BL"], stats["RH"]
checks = []


def check(name, cond):
    checks.append((name, bool(cond)))


check("比分 3-1 解析正确", bl["goals"] == 3 and rh["goals"] == 1)
check("BL xG ≈ 1.81", abs(bl["xg"] - 1.81) < 0.01)
check("RH xG ≈ 1.54", abs(rh["xg"] - 1.54) < 0.01)
check("射门统计 BL 5 / RH 4", bl["shots"] == 5 and rh["shots"] == 4)
check("补时分钟 45+2 / 90+3 解析", any(m["minute_raw"] == "45+2" for m in r["moments"])
      and any(m["minute_raw"] == "90+3" for m in r["moments"]))
kinds = [m["kind"] for m in r["moments"]]
check("关键节点含进球/失点/红牌",
      kinds.count("GOAL") == 4 and "PEN_MISS" in kinds and "RED" in kinds)
check("比分走势 1-0 -> 1-1 -> 2-1 -> 3-1",
      [tuple(sorted(m["score"].values())) for m in r["moments"] if m["kind"] == "GOAL"]
      == [(0, 1), (1, 1), (1, 2), (1, 3)])
rules = {f["rule"] for f in r["insights"]}
for rule in ("CLINICAL_FINISHING", "WASTEFUL_ATTACK", "MAN_DOWN_EFFECT",
             "SUB_IMPACT", "MOMENTUM_PHASE", "DISCIPLINE"):
    check(f"命中洞察 {rule}", rule in rules)
check("比赛形态：比分悬殊但机会均等", r["label"] == "比分悬殊但机会均等")
check("战报含比分与 xG", "3-1" in r["recap"] and "1.81" in r["recap"])
check("战报提到红牌与替补建功",
      "红牌罚下" in r["recap"] and "替补" in r["recap"])
check("每条洞察都有证据", all(f["evidence"] for f in r["insights"]))
check("智能体闭环 6 步", len(r["steps"]) == 6)
check("后续建议 4 条", len(r["next_actions"]) == 4)

failed = [n for n, ok in checks if not ok]
for n, ok in checks:
    print(f"[{'PASS' if ok else 'FAIL'}] {n}")
print(f"\n{len(checks) - len(failed)}/{len(checks)} passed")
raise SystemExit(1 if failed else 0)
