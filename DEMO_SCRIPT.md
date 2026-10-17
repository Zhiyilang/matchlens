# MatchLens — Demo Video 成片分段图（最终版 1:26，官方硬限 2:00）

> **成片状态：已产出** — `matchlens_demo.mp4`（86.4s / 1002 KB / 1280×720@30fps，终端实录风格，全部真实命令真实输出）。由 `_videotool/demovid.py` + 脚本 `_videotool/scripts/matchlens_video.json` 生成；演示数据 = `--gen 17 --home-name "Blue Lions" --away-name "Red Eagles"`（生成器配英文队名 → 全英文输出，对英文评委友好；该场次含 61' 红牌、两记超级替补、75-90 阶段统治，六类洞察中四类上场）。
>
> **官方规则（aka.ms/insidethegame/rules）**：Demo 视频 ≤2:00；须展示真实运行；平台限 YouTube/Vimeo/Facebook Video/**Youku**（优酷国内免 VPN）；材料须英文；须有测试访问链接（评审期免费无登录）。

## 分段图（与实际成片一一对应）

| 时间 | 段落 | 画面内容 |
|---|---|---|
| 0:00–0:02 | 片头 | MatchLens 标题卡：定位语 + 仓库/MIT/零依赖/赛事名 |
| 0:02–0:09 | 数据制造 | `--gen 17` 确定性生成一场全新比赛——同种子同 90 分钟，逐字节一致（brief 的"数据扩展"要求） |
| 0:09–0:38 | 核心价值：带证据的洞察 | 六阶段闭环 PERCEIVE→INDEX→RETRIEVE→REASON→EXPLAIN→ACT 全过程；比分/xG/关键时刻；六类洞察（临床终结/超级替补/man-down 涟漪/阶段统治/纪律/浪费机会）——**每条洞察下挂 Evidence 行（文件+行号+分钟+球员）** |
| 0:38–0:58 | 实时叙事 | `--live` 播报模式：进球呼叫、15 分钟 xG 更新、红牌、halftime/全场小结——brief 的"实时分析"要求 |
| 0:58–1:05 | 演播室报告 | HTML 报告卡：比分板/xG 条形图/关键时刻时间线/洞察卡 + 已部署免登录 URL |
| 1:05–1:14 | 双语切换 | 同一命令 `--lang zh` 全链路切换——brief 的"多语言"要求 |
| 1:14–1:22 | 工程质量 | `python eval.py` → 80/80 断言；CI 三 Python 版本；生成器逐字节测试 |
| 1:22–1:26 | 收尾 | "Agents propose. Evidence decides." + 仓库 URL |

## 上传清单（用户动作）

- [ ] 传 **YouTube (Unlisted)** 或 **优酷**（国内回访问优酷更稳，可两边都传）
- [ ] 标题：`MatchLens — Explainable Match-Intelligence Agent (Microsoft × Premier League Inside the Game)`
- [ ] 简介：仓库 URL + 一句话定位 + 部署 demo URL（clauseguard-ai.app.workbuddy.host/?lang=en）
- [ ] 提交前确认 demo URL **无登录可访问**（已在线核验过，提交日再点一次）
- [ ] 成片 1:26 < 2:00 硬限，无需再剪

## 重新生成（如需微调）

```bash
cd matchlens
"C:/Users/支一郎/AppData/Local/Programs/Python/Python314/python.exe" ../_videotool/demovid.py ../_videotool/scripts/matchlens_video.json matchlens_demo.mp4
```

（注：托管 Python 缺 Pillow，用系统 Python 3.14 跑生成器；视频内命令由托管 Python 执行。改剧本后重跑约 2 分钟。）
