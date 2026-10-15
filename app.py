"""MatchLens web demo — zero-dependency stdlib HTTP server.

Serves a bilingual landing page, the full HTML match report and a captured
live-narration transcript. Reads PORT from the environment, binds 0.0.0.0.

Run:  python app.py            (then open http://localhost:8000)
"""
from __future__ import annotations

import os
import tempfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

from matchlens import core, i18n, live as live_mod, report

HERE = os.path.dirname(os.path.abspath(__file__))
DEMO_EV = os.path.join(HERE, "examples", "match_events.csv")
DEMO_TEAMS = os.path.join(HERE, "examples", "teams.csv")
REPO = "https://github.com/Zhiyilang/matchlens"

STRINGS = {
    "title": {"zh": "MatchLens — 可解释比赛情报智能体",
              "en": "MatchLens — Explainable Match-Intelligence Agent"},
    "hero_sub": {
        "zh": "把比赛事件数据变成说得清的情报、当场能播的叙事。纯 Python 标准库，零依赖，全离线。",
        "en": "Turns match-event data into cited insights and broadcast-ready narrative. Pure stdlib, zero deps, fully offline."},
    "cta_report": {"zh": "查看 HTML 战报报告", "en": "Open HTML match report"},
    "cta_live": {"zh": "观看实时播报实录", "en": "Watch live narration"},
    "cta_repo": {"zh": "GitHub 仓库（MIT）", "en": "GitHub repo (MIT)"},
    "feat_evid": {"zh": "证据可溯源", "en": "Cited evidence"},
    "feat_evid_d": {"zh": "每条洞察精确到文件、行号、分钟与球员，可当场手工复核。",
                    "en": "Every insight cites file, row, minute and player — verifiable by hand."},
    "feat_live": {"zh": "实时播报", "en": "Real-time narration"},
    "feat_live_d": {"zh": "事件流逐条解说：进球播报、15 分钟 xG 更新、半场与全场总结。",
                    "en": "Streams commentary: goal calls, 15-min xG updates, halftime and full-time recaps."},
    "feat_i18n": {"zh": "双语输出", "en": "Bilingual output"},
    "feat_i18n_d": {"zh": "CLI、HTML 报告与播报共用同一 i18n 层，一键切换中英文。",
                    "en": "CLI, HTML report and commentary share one i18n layer."},
    "feat_gen": {"zh": "合成数据扩展", "en": "Synthetic data"},
    "feat_gen_d": {"zh": "确定性种子生成整场新比赛，同一分析闭环直接回读。",
                   "en": "Deterministic seeds manufacture full matches the same loop can read."},
    "live_title": {"zh": "实时播报实录", "en": "Live narration transcript"},
    "live_sub": {"zh": "以下为对示例比赛的完整逐条播报（离线捕获）。",
                 "en": "Full commentary replay for the bundled demo match (captured offline)."},
    "back": {"zh": "← 返回首页", "en": "<- Back to home"},
    "toggle": {"zh": "English", "en": "中文"},
    "footer": {"zh": "MatchLens · agents propose, evidence decides · MIT",
               "en": "MatchLens - agents propose, evidence decides - MIT"},
}


def _s(lang, key):
    return STRINGS[key].get(lang) or STRINGS[key]["zh"]


def _page(lang, body, title):
    other = "en" if lang == "zh" else "zh"
    return """<!DOCTYPE html>
<html lang="%s">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<style>
* { box-sizing: border-box; }
body { font-family: "Segoe UI", "Microsoft YaHei", sans-serif; background: #f4f6fa;
       color: #1f2933; margin: 0; padding: 32px; }
.wrap { max-width: 880px; margin: 0 auto; }
.top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
a.toggle { color: #3b7dd8; text-decoration: none; font-size: 14px; font-weight: 600; }
h1 { font-size: 26px; margin: 0 0 8px; }
.sub { color: #64748b; font-size: 14px; margin-bottom: 28px; }
.cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
         gap: 14px; margin-bottom: 28px; }
.card { background: #fff; border-radius: 14px; padding: 18px;
        box-shadow: 0 1px 3px rgba(15,23,42,.08); }
.card h3 { margin: 0 0 6px; font-size: 15px; }
.card p { margin: 0; color: #64748b; font-size: 13px; line-height: 1.55; }
.cta { display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 24px; }
.cta a { display: inline-block; padding: 10px 20px; border-radius: 999px;
         text-decoration: none; font-size: 14px; font-weight: 600; }
.cta a.primary { background: #3b7dd8; color: #fff; }
.cta a.ghost { background: #fff; color: #3b7dd8; box-shadow: 0 1px 3px rgba(15,23,42,.12); }
.footer { color: #94a3b8; font-size: 12px; margin-top: 32px; text-align: center; }
</style>
</head>
<body>
<div class="wrap">
<div class="top"><strong>MatchLens</strong><a class="toggle" href="?lang=%s">%s</a></div>
%s
<div class="footer">%s</div>
</div>
</body>
</html>""" % (lang, _esc(title), other, _esc(_s(other, "toggle")), body, _esc(_s(lang, "footer")))


def _esc(x):
    return (str(x).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def landing(lang):
    body = """
<h1>%s</h1>
<p class="sub">%s</p>
<div class="cta">
<a class="primary" href="/report?lang=%s">%s</a>
<a class="ghost" href="/live?lang=%s">%s</a>
<a class="ghost" href="%s">%s</a>
</div>
<div class="cards">
<div class="card"><h3>%s</h3><p>%s</p></div>
<div class="card"><h3>%s</h3><p>%s</p></div>
<div class="card"><h3>%s</h3><p>%s</p></div>
<div class="card"><h3>%s</h3><p>%s</p></div>
</div>""" % (
        _esc(_s(lang, "title")), _esc(_s(lang, "hero_sub")), lang,
        _esc(_s(lang, "cta_report")), lang, _esc(_s(lang, "cta_live")),
        REPO, _esc(_s(lang, "cta_repo")),
        _esc(_s(lang, "feat_evid")), _esc(_s(lang, "feat_evid_d")),
        _esc(_s(lang, "feat_live")), _esc(_s(lang, "feat_live_d")),
        _esc(_s(lang, "feat_i18n")), _esc(_s(lang, "feat_i18n_d")),
        _esc(_s(lang, "feat_gen")), _esc(_s(lang, "feat_gen_d")),
    )
    return _page(lang, body, _s(lang, "title"))


def report_page(lang):
    result = core.analyze(DEMO_EV, DEMO_TEAMS, lang=lang)
    fd, path = tempfile.mkstemp(suffix=".html")
    os.close(fd)
    try:
        report.write_html(result, path, lang=lang)
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    finally:
        os.unlink(path)


def live_page(lang):
    events = core.load_events(DEMO_EV)
    teams = core.load_teams(DEMO_TEAMS)
    names = dict(teams)
    narrator = live_mod.LiveNarrator(names=names, lang=lang)
    lines = []
    narrator.replay(events, on_line=lines.append, delay=0.0)
    body = "<h1>%s</h1><p class=\"sub\">%s</p>" % (
        _esc(_s(lang, "live_title")), _esc(_s(lang, "live_sub")))
    body += "<div class=\"card\" style=\"background:#fff;border-radius:14px;padding:18px;box-shadow:0 1px 3px rgba(15,23,42,.08)\">"
    for ln in lines:
        body += "<p style=\"margin:6px 0;font-size:14px;line-height:1.5\">%s</p>" % _esc(ln)
    body += "</div><p style=\"margin-top:18px\"><a href=\"/?lang=%s\" style=\"color:#3b7dd8\">%s</a></p>" % (
        lang, _esc(_s(lang, "back")))
    return _page(lang, body, _s(lang, "live_title"))


class Handler(BaseHTTPRequestHandler):
    server_version = "MatchLens/1.1"

    def log_message(self, fmt, *args):  # keep test output clean
        pass

    def _send(self, code, text, ctype="text/html; charset=utf-8"):
        data = text.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        parsed = urlparse(self.path)
        qs = parse_qs(parsed.query)
        lang = qs.get("lang", ["zh"])[0]
        if lang not in i18n.LANGS:
            lang = "zh"
        if parsed.path in ("/", "/index.html"):
            self._send(200, landing(lang))
        elif parsed.path == "/report":
            self._send(200, report_page(lang))
        elif parsed.path == "/live":
            self._send(200, live_page(lang))
        elif parsed.path == "/healthz":
            self._send(200, "ok", "text/plain; charset=utf-8")
        else:
            self._send(404, "not found", "text/plain; charset=utf-8")


def main():
    port = int(os.environ.get("PORT", "8000"))
    httpd = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    print("MatchLens web demo on http://0.0.0.0:%d" % port)
    httpd.serve_forever()


if __name__ == "__main__":
    main()
