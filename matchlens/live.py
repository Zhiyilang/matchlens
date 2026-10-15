"""LiveNarrator — real-time match narration (broadcast/studio style).

Feed match events one by one (in minute order) via .feed(); the narrator
keeps the running score and xG, and emits commentary lines as things happen:

- goals / penalties / red cards -> instant call-outs with the running score
- every 15-minute xG bin -> a momentum update line
- halftime (first event past 45') -> one halftime summary
- .finish() -> full-time summary + an auto-generated recap (reuses core)

Everything is deterministic and offline; language via i18n (zh/en).
"""
from __future__ import annotations

from . import core
from . import i18n

_CALL_KEY = {"GOAL": "live_goal", "PENALTY_MISSED": "live_pen_miss",
             "RED_CARD": "live_red", "YELLOW_CARD": "live_yellow"}


class LiveNarrator:
    def __init__(self, names=None, lang="zh"):
        self.names = dict(names or {})
        self.lang = lang
        self.events = []
        # Pre-seed the scoreboard from the team table when available, so the
        # first goal of the match already renders a full "1-0" scoreline
        # (a streaming narrator otherwise can't know the away team yet).
        self.score = {c: 0 for c in self.names}
        self.xg = {c: 0.0 for c in self.names}
        self.shots = {c: 0 for c in self.names}
        self._last_bin = None
        self._halftime_done = False

    # -- helpers ------------------------------------------------------------
    def _name(self, code):
        return self.names.get(code, code)

    def _scoreline(self):
        ts = sorted(self.score)
        if len(ts) == 2:
            return i18n.t(self.lang, "live_score_fmt",
                          a=self.score[ts[0]], b=self.score[ts[1]])
        return "-".join(str(self.score[t]) for t in ts)

    def _xg_parts(self):
        return ", ".join(
            i18n.t(self.lang, "live_bin_part", name=self._name(t),
                   xg=f"{self.xg.get(t, 0.0):.2f}")
            for t in sorted(self.xg))

    def _shot_parts(self):
        return ", ".join(
            f"{self._name(t)} {self.shots.get(t, 0)}" for t in sorted(self.shots))

    # -- main entry ---------------------------------------------------------
    def feed(self, e):
        """Consume one event dict (same shape as core.load_events rows).

        Returns a list of commentary lines produced by this event (0..n).
        """
        lines = []
        self.events.append(e)
        team = e["team"]
        self.score.setdefault(team, 0)
        self.xg.setdefault(team, 0.0)
        self.shots.setdefault(team, 0)
        if e["xg"] is not None:
            self.xg[team] += e["xg"]
        if e["type"] in core._SHOT_TYPES:
            self.shots[team] += 1

        # halftime boundary (once)
        if not self._halftime_done and (e["minute"] or 0) > 45.0:
            self._halftime_done = True
            lines.append(i18n.t(self.lang, "live_halftime",
                                score=self._scoreline(), parts=self._xg_parts()))

        t = e["type"]
        if t == "GOAL":
            self.score[team] += 1
            det = f" ({e['detail']})" if e["detail"] else ""
            lines.append(i18n.t(self.lang, "live_goal", minute=e["minute_raw"],
                                team=self._name(team), player=e["player"],
                                detail=det, score=self._scoreline()))
        elif t in _CALL_KEY:
            det = f" ({e['detail']})" if e["detail"] else ""
            lines.append(i18n.t(self.lang, _CALL_KEY[t], minute=e["minute_raw"],
                                team=self._name(team), player=e["player"],
                                detail=det))

        # 15-minute xG bin update (only when this event carries xG)
        if e["xg"] is not None:
            b = int(min(e["minute"] or 0.0, 89.99) // 15) * 15
            if b != self._last_bin:
                self._last_bin = b
                lines.append(i18n.t(self.lang, "live_bin", b=b, be=b + 15,
                                    parts=self._xg_parts()))
        return lines

    def finish(self):
        """Full-time summary lines (+ auto recap from the fed stream)."""
        stats = core.compute_stats(self.events)
        moments = core.extract_moments(self.events, self.lang)
        recap = core.build_recap(self.events, stats, self.names, moments, self.lang)
        lines = [i18n.t(self.lang, "live_fulltime", score=self._scoreline(),
                        parts=self._xg_parts(), shots=self._shot_parts()),
                 i18n.t(self.lang, "live_auto_recap", recap=recap)]
        return lines

    def replay(self, events, on_line=None, delay=0.0):
        """Feed a list of events; call on_line(line) per commentary line.

        delay > 0 sleeps between events (demo pacing). Returns all lines.
        """
        import time
        all_lines = []
        for e in events:
            if delay:
                time.sleep(delay)
            for ln in self.feed(e):
                all_lines.append(ln)
                if on_line:
                    on_line(ln)
        for ln in self.finish():
            all_lines.append(ln)
            if on_line:
                on_line(ln)
        return all_lines
