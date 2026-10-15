# MatchLens — Demo Video Storyboard (hard limit 2:00, target 1:55)

> **Official rules (aka.ms/insidethegame/rules):**
> - Demo video **must not exceed 2 minutes** — judges have no obligation to watch beyond that.
> - Must show the project actually running; hosted on YouTube / Vimeo / Facebook Video / **Youku** (any of these; Youku works from China without a VPN).
> - **All submission materials must be in English** — narration below is English.
> - A testing link (website / runnable demo) must be freely accessible to judges during the judging period → deploy `app.py` (see DEPLOY.md / render.yaml).
>
> Recording setup: Windows terminal (PowerShell), font ≥14pt, 1920×1080, no personal info on screen. Every command runs offline with zero wait — one take is feasible. Run `python eval.py` once beforehand to confirm all green.

## 0:00–0:12 — Hook

- Visual: repo README → terminal
- Narration (EN): "Match data is everywhere. What studios lack is analysis you can explain and broadcast on the spot. Meet MatchLens — an offline, zero-dependency, explainable match-intelligence agent. Pure Python standard library."

## 0:12–0:42 — Core value: cited insights

- Visual: terminal on the insights block
- Narration: "A six-stage agent loop turns a match-events CSV into cited intelligence. This insight — man-down ripple effect: after the 67th-minute red card, xG swings from 1.39 to 0.15 for the team down a man. Every claim carries an evidence citation — file, row, minute, player — so an analyst can verify any number in seconds."
- Action: `python -m matchlens.cli examples/match_events.csv --teams examples/teams.csv --lang en`; zoom on an evidence line

## 0:42–1:05 — Real-time narrative (brief: "real-time")

- Visual: second terminal
- Narration: "Same data, live mode — it commentates like a broadcaster: goal calls, running score, 15-minute xG updates, halftime summary."
- Action: `python -m matchlens.cli examples/match_events.csv --teams examples/teams.csv --live --delay 0.15 --lang en`; let "GOAL!" and "Halftime" scroll naturally

## 1:05–1:25 — Automated recap + studio-ready report

- Visual: terminal → browser on the deployed web demo
- Narration: "Full time triggers an automated recap, and an HTML report ready for the studio: scoreboard, xG bars, key-moment timeline, insight cards — deployed and freely accessible for judges."
- Action: open the deployed demo URL, scroll through /report

## 1:25–1:42 — Brief coverage in two quick cuts

- Visual: terminal
- Narration: "For international audiences, one flag switches the entire output to English. And with a deterministic seed we manufacture brand-new synthetic matches the same loop can analyze — expanding datasets for AI and analytics."
- Action: show `--lang en` output; `python -m matchlens.cli --gen 7 --out gen.csv --teams-out gen_teams.csv --lang en` → analyze the generated file

## 1:42–1:55 — Engineering quality + close

- Visual: terminal tail + GitHub page
- Narration: "79 assertions green, CI across three Python versions, byte-identical generator tests. MatchLens — agents propose, evidence decides. MIT-licensed, on GitHub."
- Action: `python eval.py` tail shows `79/79 passed`; cut to GitHub repo page, freeze on URL

## Recording checklist

- [ ] Font ≥14pt, 1920×1080, nothing personal on screen
- [ ] Rehearse every command once; no live debugging in the take
- [ ] Final cut **under 2:00** (storyboard 1:55 + 5s margin) — this is a hard judging rule
- [ ] Narration fully in English
- [ ] Upload to YouTube (Unlisted) or Youku; title: `MatchLens — Explainable Match-Intelligence Agent (Microsoft × Premier League Inside the Game)`
- [ ] Description: repo URL + one-line positioning + deployed demo URL
- [ ] Confirm the deployed demo URL is reachable **without login** before submitting
