"""Self-contained HTML report (inline CSS, no external assets)."""
from __future__ import annotations

import html

from . import i18n

_CSS = """
* { box-sizing: border-box; }
body { font-family: "Segoe UI", "Microsoft YaHei", sans-serif; background: #f4f6fa;
       color: #1f2933; margin: 0; padding: 32px; }
.wrap { max-width: 880px; margin: 0 auto; }
h1 { font-size: 24px; margin: 0 0 4px; }
.sub { color: #64748b; font-size: 13px; margin-bottom: 24px; }
.scoreboard { background: #fff; border-radius: 14px; padding: 24px;
              box-shadow: 0 1px 3px rgba(15,23,42,.08); margin-bottom: 20px; }
.score-line { display: flex; align-items: center; justify-content: center;
              gap: 18px; font-size: 30px; font-weight: 700; }
.score-line .team { flex: 1; text-align: center; font-size: 17px; }
.score-line .num { font-size: 40px; color: #1f2933; }
.score-line .vs { color: #94a3b8; font-size: 15px; }
.form { text-align: center; margin-top: 10px; }
.form span { display: inline-block; padding: 3px 14px; border-radius: 999px;
             background: #eef2ff; color: #3b7dd8; font-size: 13px; font-weight: 600; }
.xg-row { display: flex; align-items: center; gap: 10px; margin-top: 8px;
          font-size: 13px; }
.xg-row .lab { width: 110px; text-align: right; color: #64748b;
               white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.xg-row .bar-bg { flex: 1; background: #eef2f7; border-radius: 6px; height: 16px; }
.xg-row .bar { height: 16px; border-radius: 6px; }
.xg-row .val { width: 56px; font-weight: 700; }
table { width: 100%; border-collapse: collapse; background: #fff; border-radius: 12px;
        overflow: hidden; box-shadow: 0 1px 3px rgba(15,23,42,.08); margin-bottom: 20px; }
td { padding: 9px 14px; font-size: 13px; border-bottom: 1px solid #eef2f7;
     vertical-align: top; }
tr:last-child td { border-bottom: none; }
.st { font-weight: 700; color: #3b7dd8; white-space: nowrap; width: 90px; }
h2 { font-size: 17px; margin: 26px 0 12px; }
.timeline { background: #fff; border-radius: 12px; padding: 8px 20px;
            box-shadow: 0 1px 3px rgba(15,23,42,.08); }
.tl-item { display: flex; gap: 14px; padding: 11px 0;
           border-bottom: 1px solid #eef2f7; align-items: baseline; }
.tl-item:last-child { border-bottom: none; }
.tl-min { font-family: Consolas, monospace; font-weight: 700; color: #3b7dd8;
          min-width: 46px; }
.tl-badge { font-size: 11px; font-weight: 700; color: #fff; padding: 1px 8px;
            border-radius: 999px; }
.tl-team { color: #64748b; font-size: 12px; min-width: 86px; }
.tl-text { flex: 1; font-size: 13.5px; }
.tl-score { font-family: Consolas, monospace; font-size: 12px; color: #94a3b8; }
.card { background: #fff; border-radius: 12px; padding: 18px 20px; margin-bottom: 14px;
        box-shadow: 0 1px 3px rgba(15,23,42,.08); border-left: 4px solid #cbd5e1; }
.card-head { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }
.sev { color: #fff; font-size: 11px; font-weight: 700; padding: 2px 10px;
       border-radius: 999px; }
.title { font-size: 15px; font-weight: 700; }
.detail { font-size: 13.5px; line-height: 1.6; margin: 0 0 10px; }
.lbl { font-size: 11px; font-weight: 700; color: #64748b; letter-spacing: .05em;
       margin: 8px 0 4px; }
ul.ev { margin: 0 0 6px; padding-left: 18px; }
ul.ev li { font-family: Consolas, monospace; font-size: 12px; color: #475569;
           line-height: 1.7; word-break: break-all; }
.recap { background: #fff; border-radius: 12px; padding: 20px 22px;
         box-shadow: 0 1px 3px rgba(15,23,42,.08); font-size: 14px;
         line-height: 1.9; }
.actions { background: #fff; border-radius: 12px; padding: 18px 22px;
           box-shadow: 0 1px 3px rgba(15,23,42,.08); }
.actions ol { margin: 0; padding-left: 20px; }
.actions li { font-size: 13.5px; line-height: 1.8; }
.foot { margin-top: 28px; font-size: 12px; color: #94a3b8; }
"""

_BADGE_COLOR = {"GOAL": "#2e9e5b", "PEN_MISS": "#d64545",
                "RED": "#b91c1c", "YELLOW": "#d98e04"}
_COLORS = {"BL": "#3b7dd8", "RH": "#d64545"}


def _esc(x):
    return html.escape(str(x))


def write_html(result: dict, path: str, lang: str = "zh") -> None:
    names, stats = result["names"], result["stats"]
    teams = sorted(stats, key=lambda t: -stats[t]["goals"])
    max_xg = max((s["xg"] for s in stats.values()), default=1.0) or 1.0

    score_html = "".join(
        f"<div class='team'>{_esc(names.get(t, t))}</div>"
        f"<div class='num'>{stats[t]['goals']}</div>"
        + ("<div class='vs'>VS</div>" if i == 0 and len(teams) == 2 else "")
        for i, t in enumerate(teams))

    xg_rows = "".join(
        f"<div class='xg-row'><div class='lab'>{_esc(names.get(t, t))}</div>"
        f"<div class='bar-bg'><div class='bar' style='width:"
        f"{stats[t]['xg'] / max_xg * 100:.0f}%;background:{_COLORS.get(t, '#3b7dd8')}'>"
        f"</div></div><div class='val'>{stats[t]['xg']:.2f}</div></div>"
        for t in teams)

    timeline = "".join(
        "<div class='tl-item'>"
        f"<div class='tl-min'>{m['minute_raw']}'</div>"
        f"<div class='tl-badge' style='background:{_BADGE_COLOR.get(m['kind'], '#666')}'>"
        f"{i18n.t(lang, 'html_badge_' + m['kind'].lower())}</div>"
        f"<div class='tl-team'>{_esc(names.get(m['team'], m['team']))}</div>"
        f"<div class='tl-text'>{_esc(m['text'])}</div>"
        "<div class='tl-score'>"
        + "-".join(str(v) for _, v in sorted(m["score"].items()))
        + "</div></div>"
        for m in result["moments"])

    cards = "".join(
        "<div class='card'>"
        f"<div class='card-head'><span class='sev' style='background:#3b7dd8'>"
        f"{i18n.t(lang, 'html_insight_badge')}</span>"
        f"<span class='title'>{_esc(f['title'])}</span></div>"
        f"<p class='detail'>{_esc(f['detail'])}</p>"
        f"<div class='lbl'>{i18n.t(lang, 'html_evidence')}</div>"
        f"<ul class='ev'>{''.join(f'<li>{_esc(e)}</li>' for e in f['evidence'])}</ul>"
        "</div>"
        for f in result["insights"])

    steps = "".join(
        f"<tr><td class='st'>{_esc(n)}</td><td>{_esc(l)}</td></tr>"
        for n, l in result["steps"])
    actions = "".join(f"<li>{_esc(a)}</li>" for a in result["next_actions"])

    doc = f"""<!DOCTYPE html>
<html lang="{'zh-CN' if lang == 'zh' else 'en'}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{i18n.t(lang, 'html_title')}</title>
<style>{_CSS}</style>
</head>
<body>
<div class="wrap">
  <h1>{i18n.t(lang, 'html_title')}</h1>
  <div class="sub">{i18n.t(lang, 'html_sub')}</div>
  <div class="scoreboard">
    <div class="score-line">{score_html}</div>
    <div class="form"><span>{i18n.t(lang, 'html_form')}: {_esc(result['label'])}</span></div>
    <h2 style="margin-top:18px">{i18n.t(lang, 'html_xg')}</h2>
    {xg_rows}
  </div>
  <h2>{i18n.t(lang, 'html_steps')}</h2>
  <table>{steps}</table>
  <h2>{i18n.t(lang, 'html_moments', n=len(result['moments']))}</h2>
  <div class="timeline">{timeline}</div>
  <h2>{i18n.t(lang, 'html_insights', n=len(result['insights']))}</h2>
  {cards}
  <h2>{i18n.t(lang, 'html_recap')}</h2>
  <div class="recap">{_esc(result['recap'])}</div>
  <h2>{i18n.t(lang, 'html_next')}</h2>
  <div class="actions"><ol>{actions}</ol></div>
  <div class="foot">{i18n.t(lang, 'html_foot')}</div>
</div>
</body>
</html>
"""
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(doc)
