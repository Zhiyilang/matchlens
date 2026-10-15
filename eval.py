"""Reproducible assertions for MatchLens.

Run:  python eval.py
Exits non-zero if any assertion fails.

Covers: demo-match analysis (19 original checks), i18n parity, English
rendering, the live narrator, the synthetic generator, and the CLI end-to-end
via real subprocesses.
"""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from matchlens import core, generate, i18n, live as live_mod, report  # noqa: E402

PY = sys.executable
DEMO_EV = os.path.join(HERE, "examples", "match_events.csv")
DEMO_TEAMS = os.path.join(HERE, "examples", "teams.csv")

checks = []


def check(name, cond):
    checks.append((name, bool(cond)))


# ===========================================================================
# 1. demo match analysis (original 19)
# ===========================================================================
r = core.analyze(DEMO_EV, DEMO_TEAMS,
                 question="这场比赛发生了什么？谁的发挥决定了胜负？")
stats, names = r["stats"], r["names"]
bl, rh = stats["BL"], stats["RH"]

check("比分 3-1 解析正确", bl["goals"] == 3 and rh["goals"] == 1)
check("BL xG ≈ 1.81", abs(bl["xg"] - 1.81) < 0.01)
check("RH xG ≈ 1.54", abs(rh["xg"] - 1.54) < 0.01)
check("射门统计 BL 5 / RH 4", bl["shots"] == 5 and rh["shots"] == 4)
check("补时分钟 45+2 / 90+3 解析",
      any(m["minute_raw"] == "45+2" for m in r["moments"])
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
check("战报提到红牌与替补建功", "红牌罚下" in r["recap"] and "替补" in r["recap"])
check("每条洞察都有证据", all(f["evidence"] for f in r["insights"]))
check("智能体闭环 6 步", len(r["steps"]) == 6)
check("后续建议 4 条", len(r["next_actions"]) == 4)

# ===========================================================================
# 2. i18n parity — every key defined and non-empty in both languages
# ===========================================================================
bad = []
for key, table in i18n.STRINGS.items():
    for lang in ("zh", "en"):
        v = table.get(lang)
        if not v or not str(v).strip():
            bad.append(f"{key}.{lang}")
check(f"i18n 全键双语非空（{len(i18n.STRINGS)} 键）", not bad)
check("i18n next_actions 双语各 4 条",
      len(i18n.next_actions("zh")) == 4 and len(i18n.next_actions("en")) == 4)

# ===========================================================================
# 3. English rendering of the same demo match
# ===========================================================================
r_en = core.analyze(DEMO_EV, DEMO_TEAMS, lang="en")
check("EN 标签：一边倒类英文形态", r_en["label"] == "Lopsided scoreline, even chances")
check("EN 战报含比分与 xG", "3-1" in r_en["recap"] and "1.81" in r_en["recap"])
check("EN 战报含 Scoring sequence", "Scoring sequence" in r_en["recap"])
check("EN 关键时刻为 scores", any("scores" in m["text"] for m in r_en["moments"]))
check("EN 洞察标题英文", all(f["title"].isascii() for f in r_en["insights"]))
check("EN 下一步建议英文", all(a.isascii() for a in r_en["next_actions"]))
check("ZH/EN 洞察条数一致", len(r_en["insights"]) == len(r["insights"]))
check("ZH/EN 关键时刻条数一致", len(r_en["moments"]) == len(r["moments"]))

# ===========================================================================
# 4. live narrator (real-time narrative)
# ===========================================================================
events = core.load_events(DEMO_EV)
names_live = core.load_teams(DEMO_TEAMS)
nar = live_mod.LiveNarrator(names_live, "zh")
lines = nar.replay(events)
joined = "\n".join(lines)
check("实时：出进球播报", any("进球！" in ln for ln in lines))
check("实时：比分随进球推进", any("（比分 1-0）" in ln for ln in lines)
      and any("（比分 3-1）" in ln for ln in lines))
check("实时：半场总结恰好一次", sum("半场结束" in ln for ln in lines) == 1)
check("实时：全场总结一次", sum("全场结束" in ln for ln in lines) == 1)
check("实时：含自动战报", any("自动战报" in ln for ln in lines))
check("实时：含 15 分钟 xG 更新", any("xG 更新" in ln for ln in lines))
check("实时：红牌播报", any("红牌罚下" in ln for ln in lines))

nar_en = live_mod.LiveNarrator(names_live, "en")
lines_en = nar_en.replay(events)
check("实时 EN：GOAL 播报", any("GOAL!" in ln for ln in lines_en))
check("实时 EN：Full time 总结", any("Full time" in ln for ln in lines_en))
check("实时 EN：Auto-recap", any("Auto-recap" in ln for ln in lines_en))
check("实时 ZH/EN 行数一致", len(lines_en) == len(lines))

# determinism: same feed -> same output
nar2 = live_mod.LiveNarrator(names_live, "zh")
check("实时：确定性重放", nar2.replay(events) == lines)

# narrator tracks score independently of core
check("实时：终场比分与批量一致",
      nar.score.get("BL") == bl["goals"] and nar.score.get("RH") == rh["goals"])

# ===========================================================================
# 5. synthetic generator
# ===========================================================================
g1 = generate.generate_match(seed=7)
g2 = generate.generate_match(seed=7)
check("生成器：同种子确定性", g1 == g2)
check("生成器：不同种子不同", generate.generate_match(seed=8) != g1)
check("生成器：事件量合理（>=30）", len(g1) >= 30)
check("生成器：分钟不超 90", all(e["minute"] <= 90.0 for e in g1))
check("生成器：xG 在 [0,1]", all(e["xg"] is None or 0.0 <= e["xg"] <= 1.0 for e in g1))
check("生成器：两队都有事件",
      {e["team"] for e in g1} >= {"BL", "RH"})
check("生成器：有进球", any(e["type"] == "GOAL" for e in g1))
check("生成器：有射门", sum(1 for e in g1 if e["type"] in core._SHOT_TYPES) >= 8)

with tempfile.TemporaryDirectory() as td:
    ev_path = os.path.join(td, "gen.csv")
    tm_path = os.path.join(td, "teams.csv")
    generate.write_csvs(g1, ev_path, tm_path, {"BL": "Blue Lions FC", "RH": "Red Eagles"})
    check("生成器：CSV 可被 load_events 解析",
          len(core.load_events(ev_path)) == len(g1))
    check("生成器：teams CSV 可解析",
          core.load_teams(tm_path).get("BL") == "Blue Lions FC")
    rg = core.analyze(ev_path, tm_path)
    check("生成器：合成场可全量分析", rg["events"] == len(g1))
    check("生成器：合成场产出洞察", len(rg["insights"]) >= 1)
    # determinism at the file level
    ev_path2 = os.path.join(td, "gen2.csv")
    generate.write_csvs(generate.generate_match(seed=7), ev_path2)
    with open(ev_path, encoding="utf-8") as f1, open(ev_path2, encoding="utf-8") as f2:
        check("生成器：同种子 CSV 字节一致", f1.read() == f2.read())

    # =========================================================================
    # 6. HTML report (both languages)
    # =========================================================================
    hp = os.path.join(td, "r.html")
    report.write_html(r, hp, "zh")
    with open(hp, encoding="utf-8") as fh:
        doc_zh = fh.read()
    check("HTML 中文版含战报标题", "自然语言战报" in doc_zh and "MatchLens" in doc_zh)
    report.write_html(r_en, os.path.join(td, "r_en.html"), "en")
    with open(os.path.join(td, "r_en.html"), encoding="utf-8") as fh:
        doc_en = fh.read()
    check("HTML 英文版含 Recap 标题", "Natural-language recap" in doc_en)
    check("HTML 英文版无中文标题泄漏", "自然语言战报" not in doc_en)
    check("HTML 转义防注入", "<script>" not in doc_zh)

    # =========================================================================
    # 7. CLI end-to-end (real subprocesses)
    # =========================================================================
    p = subprocess.run([PY, "-m", "matchlens.cli", DEMO_EV, "--teams", DEMO_TEAMS],
                       capture_output=True, text=True, timeout=30, cwd=HERE)
    check("CLI 默认中文退出 0", p.returncode == 0)
    check("CLI 中文输出含进球与战报", "进球" in p.stdout and "战报" in p.stdout)

    p_en = subprocess.run([PY, "-m", "matchlens.cli", DEMO_EV, "--teams", DEMO_TEAMS,
                           "--lang", "en"], capture_output=True, text=True,
                          timeout=30, cwd=HERE)
    check("CLI --lang en 退出 0", p_en.returncode == 0)
    check("CLI 英文输出含 Recap 与 GOAL", "Recap" in p_en.stdout and "GOAL" in p_en.stdout)
    check("CLI 英文输出无中文标题", "自然语言战报" not in p_en.stdout)

    p_live = subprocess.run([PY, "-m", "matchlens.cli", DEMO_EV, "--teams", DEMO_TEAMS,
                             "--live", "--lang", "en"], capture_output=True, text=True,
                            timeout=30, cwd=HERE)
    check("CLI --live 退出 0", p_live.returncode == 0)
    check("CLI --live 有 GOAL 播报与全场总结",
          "GOAL!" in p_live.stdout and "Full time" in p_live.stdout)

    p_gen = subprocess.run([PY, "-m", "matchlens.cli", "--gen", "42",
                            "--out", os.path.join(td, "cli_gen.csv"),
                            "--teams-out", os.path.join(td, "cli_gen_teams.csv")],
                           capture_output=True, text=True, timeout=30, cwd=HERE)
    check("CLI --gen 退出 0", p_gen.returncode == 0)
    check("CLI --gen 落盘可分析",
          os.path.exists(os.path.join(td, "cli_gen.csv"))
          and core.analyze(os.path.join(td, "cli_gen.csv"))["events"] > 0)

    p_bad = subprocess.run([PY, "-m", "matchlens.cli"],
                           capture_output=True, text=True, timeout=30, cwd=HERE)
    check("CLI 无参数报错退出非 0", p_bad.returncode != 0)

    p_html = subprocess.run([PY, "-m", "matchlens.cli", DEMO_EV, "--teams", DEMO_TEAMS,
                             "--lang", "en", "--html", os.path.join(td, "cli.html")],
                            capture_output=True, text=True, timeout=30, cwd=HERE)
    check("CLI --html 生成英文报告",
          p_html.returncode == 0 and os.path.exists(os.path.join(td, "cli.html")))

# ===========================================================================
# web demo: real HTTP server, bilingual pages
# ===========================================================================
import threading  # noqa: E402
import urllib.error  # noqa: E402
import urllib.request  # noqa: E402
from http.server import ThreadingHTTPServer  # noqa: E402

import app as app_mod  # noqa: E402

_srv = ThreadingHTTPServer(("127.0.0.1", 0), app_mod.Handler)
_port = _srv.server_address[1]
_t = threading.Thread(target=_srv.serve_forever, daemon=True)
_t.start()
try:
    def _get(path):
        try:
            with urllib.request.urlopen("http://127.0.0.1:%d%s" % (_port, path), timeout=10) as r:
                return r.status, r.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            return e.code, e.read().decode("utf-8", "replace")

    code, home_zh = _get("/")
    check("web / 返回 200", code == 200)
    check("web / 含标题与行动按钮", "MatchLens" in home_zh and "/report" in home_zh)
    code, home_en = _get("/?lang=en")
    check("web /?lang=en 英文界面", code == 200 and "Explainable Match-Intelligence" in home_en)
    code, home_bad = _get("/?lang=fr")
    check("web 坏 lang 回退中文", code == 200 and "可解释比赛情报智能体" in home_bad)
    code, rep_en = _get("/report?lang=en")
    check("web /report 英文报告", code == 200 and "MatchLens" in rep_en and "xG" in rep_en)
    code, rep_zh = _get("/report?lang=zh")
    check("web /report 中文报告", code == 200 and "MatchLens" in rep_zh)
    code, live_zh = _get("/live?lang=zh")
    check("web /live 播报实录非空", code == 200 and len(live_zh) > 2000)
    code, hz = _get("/healthz")
    check("web /healthz", code == 200 and hz.strip() == "ok")
    code, _ = _get("/nope")
    check("web 404 处理", code == 404)
finally:
    _srv.shutdown()

# ===========================================================================
failed = [n for n, ok in checks if not ok]
for n, ok in checks:
    print(f"[{'PASS' if ok else 'FAIL'}] {n}")
print(f"\n{len(checks) - len(failed)}/{len(checks)} passed")
if failed:
    print("FAILED:", "; ".join(failed))
raise SystemExit(1 if failed else 0)
