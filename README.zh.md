# MatchLens — 可解释足球战报智能体（离线 · 零依赖）

[![CI](https://github.com/Zhiyilang/matchlens/actions/workflows/ci.yml/badge.svg)](https://github.com/Zhiyilang/matchlens/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)

粘贴一份比赛事件 CSV，MatchLens 以**可解释智能体**的方式跑完
「感知 → 索引 → 检索 → 推理 → 解释 → 行动」闭环，产出：

- **比分 + xG 对比**（机会质量，而非只看结果）
- **关键节点时间线**（进球/失点/红牌/黄牌，带实时比分）
- **数据洞察**（高效终结/挥霍机会/红牌连锁反应/替补奇兵/阶段压制/纪律数据）
- **自然语言战报**（模板生成，每个数字可溯源）
- **后续分析建议**（分析师视角的下一步）

每条洞察都带**证据引用**（哪个文件、哪一行、第几分钟、哪个球员、xG 多少）。

- **零依赖**：纯 Python 标准库
- **100% 离线**：比赛数据不出本机
- **非黑箱**：规则透明，公式写在 README 里，可手工复核
- **双语输出**：`--lang zh|en`，全部文案经 i18n 层（转播/studio 出海场景）
- **实时播报**：`--live` 按事件流逐条解说，15 分钟 xG 更新 + 半场/全场总结 + 自动战报
- **合成数据**：`--gen SEED` 确定性生成整场合成比赛（扩展评测数据集）

English version: [README.md](README.md)

## 快速开始

```bash
# 批量分析（生成 HTML 报告）
python -m matchlens.cli examples/match_events.csv --teams examples/teams.csv --html report.html

# 实时播报模式（转播风格逐条解说；--delay 控制节奏）
python -m matchlens.cli examples/match_events.csv --teams examples/teams.csv --live --delay 0.05

# 英文输出
python -m matchlens.cli examples/match_events.csv --teams examples/teams.csv --lang en

# 生成一场新的合成比赛（种子 7 确定性可复现）
python -m matchlens.cli --gen 7 --out examples/generated_match.csv --teams-out examples/generated_teams.csv

# 评测
python eval.py
```

事件 CSV 列：`minute,team,player,event_type,detail,xg`
（`minute` 支持 `45+2` 补时写法；`xg` 可留空）
球队 CSV 列：`code,name`

事件类型：`GOAL / SHOT / SHOT_ON_TARGET / PENALTY_MISSED / YELLOW_CARD / RED_CARD / SUB_IN / SUB_OUT`

## 实时播报示例（--live）

```
⚽ 12' 进球！蓝狮足球俱乐部 9 张伟 (助攻来自 7 李雷) （比分 1-0）
⏱ 15-30' xG 更新：蓝狮足球俱乐部 0.35, 红鹰竞技 0.18
⚽ 34' 进球！红鹰竞技 8 迭戈 (点球) （比分 1-1）
🪑 半场结束：1-1 | xG 蓝狮足球俱乐部 0.63, 红鹰竞技 0.97
🟥 67' 红鹰竞技 5 托马什 被红牌罚下！ (两黄变一红)
⚽ 88' 进球！蓝狮足球俱乐部 20 赵蓬 (替补登场10分钟内建功) （比分 3-1）
🏁 全场结束：3-1 | xG 蓝狮足球俱乐部 1.81, 红鹰竞技 1.54 | 射门 蓝狮足球俱乐部 5, 红鹰竞技 4
📝 自动战报：蓝狮足球俱乐部 3-1 红鹰竞技。进球序列：……
```

## 规则与公式（透明可复核）

| 洞察 | 规则 |
|---|---|
| `CLINICAL_FINISHING` | 进球数 − xG ≥ +0.5（终结效率高于机会质量） |
| `WASTEFUL_ATTACK` | 进球数 − xG ≤ −0.5（挥霍机会） |
| `MAN_DOWN_EFFECT` | 红牌前后 15 分钟窗口的本队/对手 xG 变化 |
| `SUB_IMPACT` | 换人后 12 分钟内同队进球 |
| `MOMENTUM_PHASE` | 15 分钟区间 xG 分箱，双方差值 ≥ 0.4 的最大区间 |
| `DISCIPLINE` | 黄/红牌计数汇总 |

射门 = `GOAL/OWN_GOAL/SHOT/SHOT_ON_TARGET/PENALTY_MISSED` 事件数；
射正 = `GOAL/SHOT_ON_TARGET`；xG = 以上事件的 `xg` 求和。

## 智能体闭环

```
PERCEIVE  读取事件流与球队名
INDEX     按分钟排序，建立球员/事件类型/xG 索引
RETRIEVE  统计射门/xG/纪律/换人，执行 5 类洞察规则
REASON    比分走势 + xG 对比，判定比赛形态
EXPLAIN   生成洞察（附证据引用）+ 自然语言战报
ACT       给出后续分析建议
```

## 测试与质量

`python eval.py` → **70 条断言全过**：demo 场解析、i18n 双语对齐、
英文渲染、实时叙事器（比分推进/半场一次/确定性重放）、合成生成器
（同种子字节级一致/可回读分析/事件量合理）、CLI 真子进程
（中/英/实时/生成/HTML/错误退出码）。CI 在 Python 3.10/3.11/3.12 三版本运行。

## 参赛信息

为 **Microsoft × Premier League「Inside the Game: Developer Hackathon」**
（**$50,000 现金奖池**）构建。官方要点：

- **注册截止 2026-10-20 12:00 PT**；构建期 10-06 ~ 10-27；**提交截止 2026-10-27 23:59 PT**；11-10 通知前六名
- 命题：把合成足球数据转化为**可解释的赛事情报、实时叙事与自动战报**（studio/转播/流媒体场景）
- MatchLens 对应：可解释情报（xG + 6 类洞察 + 证据引用）✓、实时叙事（`--live`）✓、
  自动战报（模板化可溯源）✓、多语言（`--lang en`）✓、扩展数据集（`--gen`）✓
- 报名入口：msft.it/6016aY5LY（Innovation Studio 平台）

## 免责声明

本工具基于事件数据生成分析，不构成任何投注建议。

## License

MIT
