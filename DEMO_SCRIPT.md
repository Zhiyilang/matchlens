# MatchLens — 演示视频分镜（<5min，目标 4:40）

> 录制环境：Windows 终端（PowerShell），字体调大，1080p。
> 全部命令零等待（本地离线），可一遍过；建议先 `python eval.py` 跑一次确认全绿。

## 0:00-0:30 开场（问题定位）

- 画面：README 仓库页 → 终端
- 口播："足球数据不缺，缺的是**说得清、看得懂、当场能播**的分析。MatchLens 是一个离线的可解释战报智能体——纯 Python 标准库，零依赖，断网可跑。"
- 动作：`python -m matchlens.cli examples/match_events.csv --teams examples/teams.csv`（中文批量输出滚过）

## 0:30-1:10 可解释情报（核心卖点一）

- 画面：终端停在洞察区
- 口播："六步智能体闭环。看这条『红牌连锁反应』——67 分钟红牌后，本队 xG 从 1.39 掉到 0.15，对手从 0.63 涨到 1.18。**每条结论都带证据引用：哪个文件、哪一行、第几分钟、哪个球员。** 评委可以当场复核任何一个数字。"
- 动作：放大证据行；打开 README「规则与公式」表

## 1:10-1:50 实时播报（核心卖点二，对应 brief "real-time"）

- 画面：新终端
- 口播："同一份数据，切到实时模式——`--live`，它像解说员一样逐条播报。"
- 动作：`python -m matchlens.cli examples/match_events.csv --teams examples/teams.csv --live --delay 0.15`
- 让「⚽ 12' 进球！（比分 1-0）」和「🪑 半场结束」自然滚出来

## 1:50-2:30 自动战报 + HTML 报告（核心卖点三）

- 画面：终端 → 浏览器打开 report.html
- 口播："比赛结束自动生成战报，每个数字可溯源。HTML 报告直接给演播室用：比分板、xG 对比条、关键节点时间线、洞察卡。"
- 动作：`--html report.html` 重新生成一次；浏览器滚动展示

## 2:30-3:10 多语言（对应 brief "multiple languages"）

- 画面：终端
- 口播："面向国际观众，一个flag切换全英文——所有文案走同一套 i18n 层。"
- 动作：`python -m matchlens.cli examples/match_events.csv --teams examples/teams.csv --lang en | head -40`；再跑一次 `--lang en --html report_en.html` 展示英文报告

## 3:10-3:50 合成数据扩展（对应 brief "expand datasets"）

- 画面：终端
- 口播："官方提供合成数据；我们还能自己造。`--gen 7` 用确定性种子生成一整场新比赛，同样的分析闭环直接跑。"
- 动作：`python -m matchlens.cli --gen 7 --out examples/generated_match.csv --teams-out examples/generated_teams.csv` → 立刻分析生成的文件

## 3:50-4:20 工程质量

- 画面：终端 + GitHub 页面
- 口播："70 条断言全过，CI 在三个 Python 版本全绿；生成器做到同种子字节级一致。"
- 动作：`python eval.py` 尾部 `70/70 passed`；切到 GitHub Actions 绿勾

## 4:20-4:40 收尾

- 画面：README 页
- 口播："MatchLens——agents propose, evidence decides。把比赛数据变成说得清的情报、当场能播的叙事。MIT 开源，欢迎复用。"
- 定格仓库 URL

## 录制检查清单

- [ ] 终端字号 ≥ 14pt，窗口 1920×1080，无敏感信息露出
- [ ] 每条命令先手工跑通，避免直播事故
- [ ] 视频 < 5:00（分镜 4:40，留 20 秒余量）
- [ ] YouTube 标题：`MatchLens — Explainable Match-Intelligence Agent (Microsoft × Premier League Inside the Game)`
- [ ] YouTube 描述贴仓库 URL + 一句话定位
- [ ] 权限 Unlisted 即可（评委能看）
