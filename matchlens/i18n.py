"""Bilingual (zh/en) string tables for MatchLens.

Every user-visible sentence lives here so the CLI, HTML report and live
narrator can all switch language with one flag (`--lang`). Adding a language
means adding one dict entry per key — no logic changes.

Convention: templates use {name}-style placeholders; `.format(**kwargs)` fills
them. Both languages must define every key (enforced by eval.py).
"""
from __future__ import annotations

STRINGS: dict[str, dict[str, str]] = {
    # ---- CLI chrome -------------------------------------------------------
    "cli_title": {
        "zh": "MatchLens — 可解释足球战报智能体（离线 · 零依赖）",
        "en": "MatchLens — Explainable Match-Intelligence Agent (offline · zero-dependency)",
    },
    "cli_question": {"zh": "问题", "en": "Question"},
    "cli_scoreline": {"zh": "比分与数据", "en": "Scoreline & stats"},
    "cli_stats_line": {
        "zh": "{name}: {goals} 球 | 射门 {shots} (射正 {sot}) | xG {xg} | "
              "黄 {yellow} 红 {red} | 点球进 {ps} 失 {pm}",
        "en": "{name}: {goals} goals | {shots} shots ({sot} on target) | xG {xg} | "
              "{yellow}Y {red}R | penalties {ps}/{pm}",
    },
    "cli_moments_header": {"zh": "关键节点（共 {n}）", "en": "Key moments ({n})"},
    "cli_insights_header": {"zh": "洞察（{n} 条）", "en": "Insights ({n})"},
    "cli_evidence": {"zh": "证据", "en": "Evidence"},
    "cli_recap": {"zh": "战报", "en": "Recap"},
    "cli_label": {"zh": "比赛形态", "en": "Match shape"},
    "cli_next": {"zh": "后续分析建议", "en": "Next-step analysis"},
    "cli_disclaimer": {
        "zh": "免责声明：本工具基于事件数据生成分析，不构成任何投注建议。",
        "en": "Disclaimer: analysis is generated from event data and is not betting advice.",
    },
    "cli_html_written": {"zh": "HTML 报告已生成", "en": "HTML report written"},
    "cli_live_banner": {
        "zh": "实时模式：按事件流逐条播报（--delay 可控制播报节奏）",
        "en": "LIVE mode: narrating the event stream as it arrives (--delay sets the pace)",
    },

    # ---- moments ----------------------------------------------------------
    "moment_goal": {"zh": "{player} 进球", "en": "{player} scores"},
    "moment_goal_detail": {"zh": "{player} 进球（{detail}）", "en": "{player} scores ({detail})"},
    "moment_pen_miss": {"zh": "{player} 罚失点球", "en": "{player} misses a penalty"},
    "moment_pen_miss_detail": {"zh": "{player} 罚失点球（{detail}）",
                               "en": "{player} misses a penalty ({detail})"},
    "moment_red": {"zh": "{player} 被红牌罚下", "en": "{player} is sent off"},
    "moment_red_detail": {"zh": "{player} 被红牌罚下（{detail}）",
                          "en": "{player} is sent off ({detail})"},
    "moment_yellow": {"zh": "{player} 黄牌", "en": "{player} is booked"},
    "moment_yellow_detail": {"zh": "{player} 黄牌（{detail}）",
                             "en": "{player} is booked ({detail})"},

    # ---- rule titles ------------------------------------------------------
    "rule_clinical": {"zh": "高效终结", "en": "Clinical finishing"},
    "rule_wasteful": {"zh": "挥霍机会", "en": "Wasted chances"},
    "rule_man_down": {"zh": "红牌连锁反应", "en": "Man-down ripple effect"},
    "rule_sub_impact": {"zh": "替补奇兵", "en": "Super-sub impact"},
    "rule_momentum": {"zh": "阶段压制", "en": "Phase dominance"},
    "rule_discipline": {"zh": "纪律数据", "en": "Discipline"},

    # ---- rule details -----------------------------------------------------
    "detail_clinical": {
        "zh": "{name} 打进 {goals} 球但 xG 仅 {xg}（超额 +{diff}）——临门一脚明显高于平均水准。",
        "en": "{name} scored {goals} from xG {xg} (surplus +{diff}) — finishing well above chance quality.",
    },
    "detail_wasteful": {
        "zh": "{name} xG {xg} 却只进 {goals} 球（缺口 {diff}）——机会质量不差，转化率拖后腿。",
        "en": "{name} generated xG {xg} but scored only {goals} (gap {diff}) — chance quality was there, conversion was not.",
    },
    "detail_man_down": {
        "zh": "{name} {minute}' 被罚下后：本队 xG {xb}->{xa}，被对手 xG {ob}->{oa}。",
        "en": "{name}'s {minute}' red card: their xG {xb}->{xa}, the opponent's {ob}->{oa}.",
    },
    "detail_sub_impact": {
        "zh": "{name} 替补 {player} {minute}' 登场，{gminute}' 即取得进球。",
        "en": "{name} sub {player} came on at {minute}' and scored at {gminute}'.",
    },
    "detail_momentum": {
        "zh": "{b}-{be} 分钟区间 {name} xG {xa}，对手 {xb}——该阶段明显占优。",
        "en": "{b}-{be} minute window: {name} xG {xa} vs {xb} — clear dominance.",
    },
    "detail_discipline": {
        "zh": "{parts}（全场共 {y} 黄 {r} 红）。",
        "en": "{parts} ({y}Y {r}R overall).",
    },
    "detail_discipline_part": {
        "zh": "{name} {y} 黄 {r} 红",
        "en": "{name} {y}Y {r}R",
    },

    # ---- match shape ------------------------------------------------------
    "shape_draw": {"zh": "平局收场", "en": "Draw"},
    "shape_one_goal": {"zh": "一击之差", "en": "One-goal margin"},
    "shape_lopsided": {"zh": "比分悬殊但机会均等", "en": "Lopsided scoreline, even chances"},
    "shape_onesided": {"zh": "一边倒", "en": "One-sided dominance"},

    # ---- recap fragments --------------------------------------------------
    "recap_opener": {"zh": "{hi} {hg}-{lg} {lo}。", "en": "{hi} {hg}-{lg} {lo}."},
    "recap_goals_seq": {"zh": "进球序列：{seq}。", "en": "Scoring sequence: {seq}."},
    "recap_goal_item": {"zh": "{minute}' {team} {text}", "en": "{minute}' {team} {text}"},
    "recap_xg_even": {
        "zh": "xG {hx}-{lx}，两队创造的机会几乎均等，比分差距主要来自终结效率。",
        "en": "xG {hx}-{lx}: almost identical chance quality; the margin came from finishing efficiency.",
    },
    "recap_xg_lead": {
        "zh": "xG {hx}-{lx}，{lead} 在机会质量上占优。",
        "en": "xG {hx}-{lx}: {lead} led on chance quality.",
    },
    "recap_red": {
        "zh": "{team} {minute}' 被红牌罚下（{player}），此后长时间少打一人。",
        "en": "{team} went a man down at {minute}' ({player}) for a long stretch.",
    },
    "recap_sub": {
        "zh": "替补 {player} {minute}' 登场，{gminute}' 建功，成为胜负手之一。",
        "en": "Sub {player} ({minute}') scored at {gminute}' — one of the decisive differences.",
    },
    "recap_pen": {
        "zh": "{minute}' {team} 罚失点球（{player}），悬念留到最后。",
        "en": "{team} missed a penalty at {minute}' ({player}) — suspense to the end.",
    },

    # ---- next actions -----------------------------------------------------
    "next_actions": {
        "zh": "把本场射门事件拆到球员维度，做 xG 贡献排名||"
              "对比赛季场均 xG/射门数，判断本场是否属于异常高效/低效||"
              "若有传球与站位数据，补传球网络与助攻链分析||"
              "对红牌、点球等关键节点回放录像，复核判罚与站位选择",
        "en": "Break shots down to player level and rank xG contributions||"
              "Compare against season averages to flag abnormally clinical or wasteful finishing||"
              "With passing and positional data, add pass networks and assist chains||"
              "Replay video at red-card and penalty nodes to review decisions and positioning",
    },

    # ---- live narrator ----------------------------------------------------
    "live_goal": {"zh": "⚽ {minute}' 进球！{team} {player}{detail} （比分 {score}）",
                  "en": "⚽ {minute}' GOAL! {team} {player}{detail} (score {score})"},
    "live_pen_miss": {"zh": "😬 {minute}' {team} {player} 罚失点球！{detail}",
                      "en": "😬 {minute}' {team} {player} misses a penalty!{detail}"},
    "live_red": {"zh": "🟥 {minute}' {team} {player} 被红牌罚下！{detail}",
                 "en": "🟥 {minute}' {team} {player} is sent off!{detail}"},
    "live_yellow": {"zh": "🟨 {minute}' {team} {player} 黄牌{detail}",
                    "en": "🟨 {minute}' {team} {player} booked{detail}"},
    "live_bin": {"zh": "⏱ {b}-{be}' xG 更新：{parts}",
                 "en": "⏱ {b}-{be}' xG update: {parts}"},
    "live_bin_part": {"zh": "{name} {xg}", "en": "{name} {xg}"},
    "live_halftime": {"zh": "🪑 半场结束：{score} | xG {parts}",
                      "en": "🪑 Halftime: {score} | xG {parts}"},
    "live_fulltime": {"zh": "🏁 全场结束：{score} | xG {parts} | 射门 {shots}",
                      "en": "🏁 Full time: {score} | xG {parts} | shots {shots}"},
    "live_auto_recap": {"zh": "📝 自动战报：{recap}", "en": "📝 Auto-recap: {recap}"},
    "live_score_fmt": {"zh": "{a}-{b}", "en": "{a}-{b}"},

    # ---- HTML report ------------------------------------------------------
    "html_title": {"zh": "MatchLens 战报", "en": "MatchLens Report"},
    "html_sub": {
        "zh": "离线 · 零依赖 · 每条洞察均可溯源（文件/行号/分钟/球员）",
        "en": "Offline · zero-dependency · every insight traceable (file/row/minute/player)",
    },
    "html_form": {"zh": "比赛形态", "en": "Match shape"},
    "html_xg": {"zh": "xG 对比", "en": "xG comparison"},
    "html_steps": {"zh": "智能体闭环", "en": "Agent loop"},
    "html_moments": {"zh": "关键节点（{n}）", "en": "Key moments ({n})"},
    "html_insights": {"zh": "洞察（{n}）", "en": "Insights ({n})"},
    "html_recap": {"zh": "自然语言战报", "en": "Natural-language recap"},
    "html_next": {"zh": "后续分析建议", "en": "Next-step analysis"},
    "html_insight_badge": {"zh": "洞察", "en": "Insight"},
    "html_evidence": {"zh": "证据引用", "en": "Evidence citations"},
    "html_foot": {
        "zh": "MatchLens v1.0 · 本报告基于事件数据生成，不构成任何投注建议。",
        "en": "MatchLens v1.0 · generated from event data; not betting advice.",
    },
    "html_badge_goal": {"zh": "进球", "en": "Goal"},
    "html_badge_pen_miss": {"zh": "失点", "en": "Miss"},
    "html_badge_red": {"zh": "红牌", "en": "Red"},
    "html_badge_yellow": {"zh": "黄牌", "en": "Yellow"},

    # ---- agent-loop step descriptions (REASON/EXPLAIN label part) ----------
    "step_reason_label": {"zh": "判定比赛形态：{label}", "en": "match shape: {label}"},
    "step_perceive": {
        "zh": "读取 {n} 个比赛事件 | 球队 {teams}",
        "en": "read {n} match events | teams {teams}",
    },
    "step_index": {
        "zh": "按分钟排序，建立球员/事件类型/xG 索引，识别 {n} 个关键节点",
        "en": "sorted by minute; player/event-type/xG indexes built; {n} key moments identified",
    },
    "step_retrieve": {
        "zh": "统计射门/xG/纪律/换人数据，执行 5 类洞察规则，命中 {n} 条",
        "en": "tallied shots/xG/discipline/subs; ran 5 insight rules; {n} findings",
    },
    "step_reason": {
        "zh": "计算比分走势与 xG 对比，判定比赛形态：{label}",
        "en": "score progression and xG compared; {label}",
    },
    "step_explain": {
        "zh": "生成 {n} 条洞察（每条附证据引用）与自然语言战报",
        "en": "emitted {n} insights (each with evidence citations) and a natural-language recap",
    },
    "step_act": {
        "zh": "给出 {n} 条后续分析建议",
        "en": "produced {n} next-step analysis suggestions",
    },
}

LANGS = ("zh", "en")


def t(lang: str, key: str, **kwargs) -> str:
    """Translate `key` into `lang`, formatting {placeholders} from kwargs."""
    if lang not in STRINGS[key]:
        lang = "zh"
    s = STRINGS[key][lang]
    return s.format(**kwargs) if kwargs else s


def next_actions(lang: str) -> list[str]:
    raw = STRINGS["next_actions"].get(lang) or STRINGS["next_actions"]["zh"]
    return [x.strip() for x in raw.split("||") if x.strip()]
