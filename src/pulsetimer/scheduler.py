from __future__ import annotations

from dataclasses import dataclass

from .session import SessionConfig


@dataclass
class SchedulerState:
    next_index: int = 1


@dataclass
class TickDecision:
    should_alert: bool
    catch_up: bool
    delayed: bool
    completed: bool


def scheduled_time(start_ts: float, interval_seconds: int, index: int) -> float:
    return start_ts + (interval_seconds * index)


def evaluate_tick(
    *,
    now_ts: float,
    start_ts: float,
    config: SessionConfig,
    state: SchedulerState,
) -> TickDecision:
    planned = config.planned_alert_count
    if state.next_index > planned:
        return TickDecision(False, False, False, completed=now_ts >= start_ts + config.duration_seconds)

    next_due = scheduled_time(start_ts, config.interval_seconds, state.next_index)
    if now_ts < next_due:
        return TickDecision(False, False, False, completed=False)

    highest_due_index = int((now_ts - start_ts) // config.interval_seconds)
    highest_due_index = min(max(highest_due_index, state.next_index), planned)
    missed_count = highest_due_index - state.next_index + 1

    delayed = missed_count > 1
    catch_up = delayed

    # Hybrid policy: deliver at most one alert when multiple intervals were missed,
    # then skip directly to the next future schedule slot.
    state.next_index = highest_due_index + 1

    completed = state.next_index > planned and now_ts >= start_ts + config.duration_seconds
    return TickDecision(True, catch_up, delayed, completed)
