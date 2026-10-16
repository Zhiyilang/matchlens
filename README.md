# MatchLens — An Explainable Match-Intelligence Agent (Offline · Zero-Dependency)

[![CI](https://github.com/Zhiyilang/matchlens/actions/workflows/ci.yml/badge.svg)](https://github.com/Zhiyilang/matchlens/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)

Paste in a match-events CSV and MatchLens runs a full **explainable agent loop** —
PERCEIVE → INDEX → RETRIEVE → REASON → EXPLAIN → ACT — to produce:

- **Scoreline + xG comparison** (chance quality, not just the result)
- **Key-moment timeline** (goals / missed penalties / red cards, with live score)
- **Data insights** (clinical finishing, wasted chances, man-down ripple effect,
  super-sub impact, phase dominance, discipline)
- **Natural-language recap** (template-generated, every number traceable)
- **Next-step analysis suggestions** (an analyst's view of what to dig into)

Every insight carries an **evidence citation** (which file, which row, which
minute, which player, how much xG).

- **Zero dependencies**: pure Python standard library
- **100% offline**: match data never leaves your machine
- **Not a black box**: the rules are transparent, formulas are documented in this
  README, everything is hand-verifiable
- **Bilingual output**: `--lang zh|en` — all prose flows through an i18n layer
  (for broadcast/studio rollouts to international audiences)
- **Real-time narration**: `--live` commentates the event stream as it arrives —
  15-minute xG updates, halftime and full-time summaries, auto-recap
- **Synthetic data**: `--gen SEED` deterministically manufactures a whole match
  (expand the evaluation dataset without any external feed)

## Quick Start

```bash
# Batch analysis (writes an HTML report)
python -m matchlens.cli examples/match_events.csv --teams examples/teams.csv --html report.html

# Real-time narration (broadcast style; --delay sets the pace)
python -m matchlens.cli examples/match_events.csv --teams examples/teams.csv --live --delay 0.05

# English output
python -m matchlens.cli examples/match_events.csv --teams examples/teams.csv --lang en

# Generate a fresh synthetic match (seed 7 is deterministic)
python -m matchlens.cli --gen 7 --out examples/generated_match.csv --teams-out examples/generated_teams.csv

# Evaluation suite
python eval.py
```

Events CSV columns: `minute,team,player,event_type,detail,xg`
(`minute` supports stoppage-time notation like `45+2`; `xg` may be empty)
Teams CSV columns: `code,name`

Event types: `GOAL / SHOT / SHOT_ON_TARGET / PENALTY_MISSED / YELLOW_CARD / RED_CARD / SUB_IN / SUB_OUT`

## Live narration sample (--live)

```
⚽ 12' GOAL! Blue Lions FC No.9 Zhang Wei (assist by No.7 Li Lei) (score 1-0)
⏱ 15-30' xG update: Blue Lions FC 0.35, Red Eagles 0.18
⚽ 34' GOAL! Red Eagles No.8 Diego (penalty) (score 1-1)
🪑 Halftime: 1-1 | xG Blue Lions FC 0.63, Red Eagles 0.97
🟥 67' Red Eagles No.5 Tomas is sent off! (second yellow)
⚽ 88' GOAL! Blue Lions FC No.20 Zhao Peng (scored within 10 minutes of coming on) (score 3-1)
🏁 Full time: 3-1 | xG Blue Lions FC 1.81, Red Eagles 1.54 | shots Blue Lions FC 5, Red Eagles 4
📝 Auto-recap: Blue Lions FC 3-1 Red Eagles. Scoring sequence: ...
```

## Rules & Formulas (transparent, auditable)

| Insight | Rule |
|---|---|
| `CLINICAL_FINISHING` | goals − xG ≥ +0.5 (finishing above chance quality) |
| `WASTEFUL_ATTACK` | goals − xG ≤ −0.5 (chances wasted) |
| `MAN_DOWN_EFFECT` | team/opponent xG change in the 15-minute window around a red card |
| `SUB_IMPACT` | same-team goal within 12 minutes of a substitution |
| `MOMENTUM_PHASE` | 15-minute xG bins; the window with the largest inter-team gap ≥ 0.4 |
| `DISCIPLINE` | yellow/red card tallies |

Shots = count of `GOAL/OWN_GOAL/SHOT/SHOT_ON_TARGET/PENALTY_MISSED`;
on target = `GOAL/SHOT_ON_TARGET`; xG = sum of the `xg` field over those events.

## The Agent Loop

```
PERCEIVE  read the event stream and team names
INDEX     sort by minute; build player / event-type / xG indexes
RETRIEVE  tally shots / xG / discipline / subs; run 5 insight rules
REASON    score progression + xG comparison to judge match shape
EXPLAIN   emit insights (with evidence citations) + natural-language recap
ACT       produce next-step analysis suggestions
```

## Tests & quality

`python eval.py` → **80 assertions passing**: demo-match analysis, i18n
parity, English rendering, the live narrator (score progression / single
halftime call / deterministic replay), the synthetic generator
(byte-identical per seed / round-trip analysis / realistic volume), the
CLI end-to-end via real subprocesses (zh/en/live/gen/HTML/exit codes), and
the bilingual web demo over real HTTP (landing / report / live transcript /
healthz / language fallback / 404).

## Web demo

`python app.py` serves a zero-dependency bilingual demo (landing page,
full HTML report, live-narration transcript). Reads `PORT`, binds
`0.0.0.0`; `render.yaml` included for one-click deploy.
CI runs the same suite on Python 3.10 / 3.11 / 3.12.

## Contest Entry

Built for the **Microsoft × Premier League "Inside the Game: Developer
Hackathon"** (**$50,000 cash prize pool**). Key facts:

- **Registration closes 2026-10-20 12:00 PT**; build window Oct 6–27;
  **submission deadline Oct 27, 11:59 PM PT**; top six notified Nov 10
- Brief: turn synthetic football data into **explainable match intelligence,
  real-time narratives, and automated recaps** for studio/broadcast/streaming
- MatchLens coverage: explainable intelligence (xG + 6 insight families +
  evidence citations) ✓, real-time narratives (`--live`) ✓, automated recaps
  (template-generated, traceable) ✓, multiple languages (`--lang en`) ✓,
  dataset expansion (`--gen`) ✓
- Register: msft.it/6016aY5LY (Innovation Studio platform)

## Disclaimer

This tool generates analysis from event data and is not betting advice.

## License

MIT

中文说明见 [README.zh.md](README.zh.md)。
