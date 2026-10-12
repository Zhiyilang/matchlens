# MatchLens — An Explainable Match-Intelligence Agent (Offline · Zero-Dependency)

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

## Quick Start

```bash
python -m matchlens.cli examples/match_events.csv --teams examples/teams.csv --html report.html
python eval.py
```

Events CSV columns: `minute,team,player,event_type,detail,xg`
(`minute` supports stoppage-time notation like `45+2`; `xg` may be empty)
Teams CSV columns: `code,name`

Event types: `GOAL / SHOT / SHOT_ON_TARGET / PENALTY_MISSED / YELLOW_CARD / RED_CARD / SUB_IN / SUB_OUT`

## Real Demo Output (examples/match_events.csv)

```
Score: Blue Lions FC 3 - 1 Red Eagles
  Blue Lions: 3 goals | 5 shots (3 on target) | xG 1.81 | 1 yellow, 0 red
  Red Eagles: 1 goal  | 4 shots (2 on target) | xG 1.54 | 0 yellow, 1 red
Match shape: lopsided scoreline, evenly matched chances

Key moments:
   12' [GOAL] Blue Lions Zhang Wei scores (assist by No.7 Li Lei)   (1-0)
   34' [GOAL] Red Eagles Diego scores (penalty)                    (1-1)
  45+2'[GOAL] Blue Lions Chen Yu scores (corner header, assist No.7 Li Lei) (2-1)
   67' [RED ] Red Eagles Tomas sent off (second yellow)
   88' [GOAL] Blue Lions Zhao Peng scores (10 minutes after coming on) (3-1)
  90+3'[MISS] Blue Lions Chen Yu misses penalty (saved by the keeper)

Insights:
  * Clinical finishing: Blue Lions scored 3 from xG 1.81 (surplus +1.19)
  * Wasted chances: Red Eagles xG 1.54 produced only 1 goal (gap -0.54)
  * Man-down ripple effect: after Red Eagles' 67' red card, their xG fell 1.39->0.15
    while the opponent's rose 0.63->1.18
  * Super-sub impact: Blue Lions sub Zhao Peng came on at 78' and scored at 88'
  * Phase dominance: 75-90 minute window, Blue Lions xG 0.87 vs 0.15
  * Discipline: Blue Lions 1 yellow 0 red; Red Eagles 0 yellow 1 red

Recap: Blue Lions FC 3-1 Red Eagles. Scoring sequence: 12' Zhang Wei (assist No.7
Li Lei); 34' Diego penalty; 45+2' Chen Yu corner header (assist No.7 Li Lei);
88' Zhao Peng (10 minutes after coming on). xG 1.81-1.54: both teams created
almost identical chances; the margin came from finishing efficiency. Red Eagles
played a man down from 67' (Tomas). Sub Zhao Peng (78') scored at 88' and became
one of the decisive differences. Chen Yu's 90+3' penalty miss kept the suspense
alive to the end.
```

*(Team and player names above are English renderings of the bundled sample data.)*

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

## Contest Entry

Built for **Microsoft × Premier League "Inside the Game: Developer Hackathon"**
($50,000 cash prize pool): turning match-event data into **explainable match
intelligence and automated recaps** — zero-dependency, offline-capable, fully
traceable conclusions. See `eval.py` (19 assertions, all PASS).

## Disclaimer

This tool generates analysis from event data and is not betting advice.

## License

MIT

中文说明见 [README.zh.md](README.zh.md)。
