# MatchLens — Microsoft × Premier League "Inside the Game" 申报物料

> 赛事：Microsoft × Premier League「Inside the Game: Developer Hackathon」
> 规则原文：https://aka.ms/insidethegame/rules（已逐条核录）
> 平台：Innovation Studio（注册后邮件邀请）· 注册入口 msft.it/6016aY5LY

## ⏰ 时间线（北京）

| 节点 | 时间 |
|---|---|
| **注册截止** | **2026-10-20 12:00 PT ≈ 北京 10-21 03:00（硬门槛，错过出局）** |
| 黑客周期 | 2026-10-06 → 10-27 23:59 PT（**已开始**） |
| 提交截止 | 2026-10-27 23:59 PT ≈ 北京 10-28 14:59 |
| 前六名通知 | 2026-11-10 |

## 💰 奖项（官方规则原文，非笼统"$50k"）

| 奖项 | 现金（e-Gift Card 均分给队员） | 另含 |
|---|---|---|
| Grand Prize 第一名 | **$4,000** | 英超数字门票 ARV $1,000 + 商店券 $50 + 官方社交特写 |
| Grand Prize 第二名 | **$2,500** | 同上 |
| Best Use of Microsoft Foundry | **$1,500** | 商店券 + 特写 |
| Best Enterprise Solution | **$1,500** | 同上 |
| Best Multi-Agent System | **$1,500** | 同上 |
| Best Azure Cloud Native Integration | **$1,500** | 同上 |

现金合计 $12,500；全队 ARV $14,800–$59,200。**一个项目最多拿 1 个大奖 + 1 个类别奖。**

## ⚖️ 评审标准（Stage 2 五项各 20%，等权重）

1. **Technological Implementation** — 合成数据创建的创造性与质量；hero technologies（Foundry / Agent Framework / Azure MCP / Copilot Agent Mode / Fabric / GitHub SDK / Azure AI）利用度；代码结构、文档、可维护性
2. **Agentic Design & Innovation** — 智能体模式创造性；编排/MCP/多智能体协作
3. **Real-World Impact & Applicability** — 问题重要性；可部署性
4. **User Experience & Presentation** — UX 直观性；视频传达力；前后端均衡
5. **Adherence to Hackathon Category** — 类别契合度
（平分时先比第 1 项。Stage 1 为通过制：主题契合 + 合理应用赛事技术。）

## ✅ 资格核对（官方排除项逐条过）

| 项 | 状态 |
|---|---|
| 禁赛地区（Brazil/Quebec/Russia/Crimea/Cuba/Iran/NK/Sudan/Syria/OFAC） | 中国不在列 ✓ |
| 法定成年年龄 | 21 岁 ✓ |
| 主办方/评委及其直系亲属 | 无关 ✓ |
| 项目须为 **2026-09-29 09:00 PT 报名期开始后新建** | 仓建于 2026-10-12 ✓ |
| 团队 ≤4 人 | 单人 ✓ |
| 未在其他竞赛获奖 | ✓ |
| 材料须英文 | 仓库/README/脚本全英文 ✓ |

## 提交硬性要求（官方）

1. 项目 Pitch/Description（构建了什么 + 用了哪些 Microsoft/Azure 技术 + 解决什么问题）
2. **Demo 视频 ≤ 2:00**，展示真实运行；平台限 YouTube/Vimeo/Facebook Video/**Youku**
3. **GitHub 仓库必须公开**（否则不评审）— 已公开 ✓
4. **测试访问**：网站/可运行 demo/测试构建；评审期须免费无限制开放（私有站须附凭据）
5. 不得侵犯第三方 IP；素材须自备（官方不分发比赛录像）

## 用户必须做的（按序）

1. **10-20 12:00 PT 前**：msft.it/6016aY5LY 用 Microsoft 账号注册（免费，全球开放）
2. 等 Innovation Studio 邀请邮件 → 建项目
3. 关联公开仓库 https://github.com/Zhiyilang/matchlens
4. 部署 Web demo（render.yaml 一键 Render，或本地 `python app.py` 内网穿透）→ 拿到无登录可访问的 URL
5. 按 DEMO_SCRIPT.md 录 ≤2:00 英文视频，传 YouTube(Unlisted)/优酷
6. 10-27 23:59 PT 前在平台提交

## 平台字段（可直接复制）

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
> matches to expand evaluation datasets. A zero-dependency web demo
> (`app.py`, render.yaml included) serves the report and live transcript for
> judging access. Pure Python standard library, 100% offline, MIT-licensed,
> 80-assertion eval suite green on Python 3.10/3.11/3.12.

**GitHub repo**: https://github.com/Zhiyilang/matchlens（public ✓）

**Demo video**: （录好后贴链接）

**Testing access**: https://clauseguard-ai.app.workbuddy.host/?lang=en
（已部署，免登录可访问；域名是工作区复用旧名，内容已核验为 MatchLens。
英文首页 `?lang=en`，另有 `/report?lang=en` 战报、`/live?lang=en` 实时播报实录。）

## 评分映射（官方五项 → MatchLens）

| 评审项 (20% each) | MatchLens 对应 | 演示位置 |
|---|---|---|
| Technological Implementation | 零依赖确定性引擎 + 80 断言 eval + 三版本 CI + 字节级一致生成器 | 视频 1:42-1:55 |
| Agentic Design & Innovation | 六阶段闭环 PERCEIVE→INDEX→RETRIEVE→REASON→EXPLAIN→ACT + MCP server | 视频 0:12-0:42 |
| Real-World Impact | 转播/演播室即用：HTML 报告 + 双语 + 离线可跑（弱网内网场景） | 视频 1:05-1:42 |
| User Experience & Presentation | 可访问 Web demo + 双语界面 + ≤2min 精剪视频 | 视频全程 |
| Adherence to Category | brief 六条全覆盖：实时分析/战报/解释/数据扩展/多语言/个性化 | 视频各段 |

## 差异化卖点（评委视角）

1. **可解释是硬约束**：每条洞察带证据引用，公式写进 README，可手工复核——正面回应 brief 的 "explainable"。
2. **零依赖 + 全离线**：转播现场弱网/内网直接跑，与云端方案互补而非重复。
3. **双语开箱即用**：i18n 覆盖 CLI/HTML/播报全文案。
4. **工程质量可见**：80 断言 + CI 绿徽标 + 生成器确定性测试。
5. **合规优先**：仓库公开 ✓、英文材料 ✓、2 分钟视频 ✓、demo 无登录可访问 ✓。

## 风险与规避

- **非 Microsoft 技术栈**：规则未硬性要求（"strongest submissions will leverage" 为导向语）；Stage 1 看"合理应用赛事技术"——以 GitHub（官方点名的 hero tech 之一）为主线，Pitch 中明确说明定位（离线优先，补云端空白）。
- **注册是硬门槛**：10-20 12:00 PT 截止，优先于其他一切。
- **视频超时即弃**：分镜按 1:55 设计，成片必须 <2:00。
