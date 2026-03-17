from pulsetimer.scheduler import SchedulerState, evaluate_tick, scheduled_time
from pulsetimer.session import AlertMode, SessionConfig


def test_absolute_schedule_mapping_for_ninety_min_three_minute_session() -> None:
    start = 1000.0
    interval = 180
    assert scheduled_time(start, interval, 1) == 1180.0
    assert scheduled_time(start, interval, 30) == 6400.0


def test_no_delay_on_time_tick() -> None:
    config = SessionConfig(interval_seconds=180, duration_seconds=5400, alert_mode=AlertMode.BEEP)
    state = SchedulerState(next_index=1)

    decision = evaluate_tick(now_ts=1180.0, start_ts=1000.0, config=config, state=state)

    assert decision.should_alert is True
    assert decision.catch_up is False
    assert decision.delayed is False
    assert state.next_index == 2


def test_hybrid_catch_up_for_multiple_missed_intervals() -> None:
    config = SessionConfig(interval_seconds=180, duration_seconds=5400, alert_mode=AlertMode.BEEP)
    state = SchedulerState(next_index=2)

    # Misses schedule indices 2,3,4 then resumes.
    decision = evaluate_tick(now_ts=1725.0, start_ts=1000.0, config=config, state=state)

    assert decision.should_alert is True
    assert decision.catch_up is True
    assert decision.delayed is True
    assert state.next_index == 5


def test_completion_at_duration_boundary() -> None:
    config = SessionConfig(interval_seconds=180, duration_seconds=5400, alert_mode=AlertMode.BEEP)
    state = SchedulerState(next_index=31)

    decision = evaluate_tick(now_ts=6400.0, start_ts=1000.0, config=config, state=state)

    assert decision.should_alert is False
    assert decision.completed is True
