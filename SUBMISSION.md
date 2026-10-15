# MatchLens — Microsoft × Premier League "Inside the Game" 申报物料

> 赛事：Microsoft × Premier League「Inside the Game: Developer Hackathon」
> 奖池：**$50,000 现金**（现金 + 球票等）；前六名 11-10 通知
> 平台：Innovation Studio（注册后邮件邀请）· 注册入口 msft.it/6016aY5LY

## ⏰ 时间线（北京）

| 节点 | 时间 |
|---|---|
| **注册截止** | **2026-10-20 12:00 PT ≈ 北京 10-21 03:00** |
| 提交截止 | 2026-10-27 23:59 PT ≈ 北京 10-28 14:59 |
| 前六名通知 | 2026-11-10 |

## 用户必须做的（按序）

1. **10-20 12:00 PT 前**：msft.it/6016aY5LY 用 Microsoft 账号注册（免费，全球开放；政府雇员需自查单位政策）
2. 等 Innovation Studio 平台邀请邮件，建项目
3. 关联公开仓库 https://github.com/Zhiyilang/matchlens
4. 录 <5min 演示视频（分镜见 DEMO_SCRIPT.md），上传 YouTube（可设为 Unlisted）
5. 10-27 23:59 PT 前在平台提交

## 平台字段填写（可直接复制）

**Project name**: MatchLens — Explainable Match-Intelligence Agent

**Tagline**: Offline, zero-dependency agent that turns match-event data into cited insights, real-time bilingual narration, and automated recaps.

**Description**（粘贴）:

> MatchLens is an explainable match-intelligence agent built for the Inside
> the Game brief: it transforms match-event data into explainable insights,
> real-time narratives, and automated recaps for studio, broadcast and
> streaming scenarios.
>
> Feed it a match-events CSV (or generate a synthetic match with one flag) and
> a six-stage agent loop — PERCEIVE → INDEX → RETRIEVE → REASON → EXPLAIN →
> ACT — produces: a scoreline and xG comparison; a key-moment timeline with
> running score; six families of data insights (clinical finishing, wasted
> chances, man-down ripple effect, super-sub impact, phase dominance,
> discipline); and a natural-language recap. Every insight carries an evidence
> citation down to the file, row, minute and player, so a studio analyst can
> verify any claim in seconds.
>
> `--live` replays an event stream as broadcast-style commentary with
> 15-minute xG updates, halftime/full-time summaries and an auto-recap.
> `--lang en|zh` renders the entire output bilingually for international
> audiences. `--gen SEED` deterministically manufactures additional synthetic
> matches to expand evaluation datasets. Pure Python standard library, 100%
> offline, MIT-licensed, 70-assertion eval suite green on Python 3.10/3.11/3.12.

**GitHub repo**: https://github.com/Zhiyilang/matchlens

**Demo video**: （录好后贴 YouTube 链接）

## 评分映射（brief 六条 → MatchLens 功能）

| 官方 brief | MatchLens 对应 | 演示位置 |
|---|---|---|
| Analyze match events in real time | `--live` 事件流播报 + 15 分钟 xG 更新 + 半/全场总结 | 视频 0:40-1:40 |
| Generate stories, highlights, and recaps | 自动战报（模板化、数字全溯源）+ 关键节点时间线 | 视频 1:40-2:20 |
| Explain key moments and tactical patterns | 6 类洞察规则 + 证据引用（文件/行号/分钟/球员） | 视频 2:20-3:00 |
| Expand datasets for AI and analytics | `--gen SEED` 合成比赛生成器（确定性、可回读分析） | 视频 3:00-3:30 |
| Deliver insights in multiple languages | `--lang zh\|en` 全文案 i18n 层 | 视频 3:30-4:00 |
| Personalized experiences for studios/fans | HTML 报告（比分板/xG 条形/时间线/洞察卡） | 视频 4:00-4:40 |

## 差异化卖点（评委视角）

1. **可解释是硬约束，不是口号**：每条洞察带证据引用，公式全写进 README，可手工复核——直接回应 brief 的 "explainable"。
2. **零依赖 + 全离线**：纯标准库，转播现场弱网/内网环境直接跑，不需要任何云账号。
3. **双语开箱即用**：i18n 层覆盖 CLI/HTML/实时播报全部文案，出海场景即切即用。
4. **工程质量可见**：70 断言 eval + 三版本 CI 绿徽标 + 生成器字节级确定性测试。

## 风险与规避

- **不需要 Azure/Copilot 也能交**：brief 说 "strongest submissions will leverage GitHub Copilot / Foundry / Azure"（最强提交会用到），非硬性；若评委追问，可强调"离线优先"是与云端方案互补的定位（转播现场/内网）。
- **视频必须 <5min**：分镜已按 4:40 设计，留 20 秒余量。
- **注册是硬门槛**：10-20 12:00 PT 截止，错过即出局——优先于其他一切。
