from pulsetimer.alerts import InstrumentedAlertAdapter
from pulsetimer.android_runtime import NoOpRuntime
from pulsetimer.engine import IntervalTimerEngine
from pulsetimer.session import AlertMode, SessionConfig


def test_mode_selection_beep() -> None:
    adapter = InstrumentedAlertAdapter()
    runtime = NoOpRuntime()
    engine = IntervalTimerEngine(adapter, runtime)
    config = SessionConfig(interval_seconds=60, duration_seconds=180, alert_mode=AlertMode.BEEP)

    engine.start(config, start_ts=1000.0)
    engine.tick(now_ts=1060.0)

    assert adapter.events == [(AlertMode.BEEP, False)]


def test_mode_selection_vibration() -> None:
    adapter = InstrumentedAlertAdapter()
    runtime = NoOpRuntime()
    engine = IntervalTimerEngine(adapter, runtime)
    config = SessionConfig(interval_seconds=60, duration_seconds=180, alert_mode=AlertMode.VIBRATION)

    engine.start(config, start_ts=1000.0)
    engine.tick(now_ts=1060.0)

    assert adapter.events == [(AlertMode.VIBRATION, False)]


def test_mode_selection_beep_and_vibration() -> None:
    adapter = InstrumentedAlertAdapter()
    runtime = NoOpRuntime()
    engine = IntervalTimerEngine(adapter, runtime)
    config = SessionConfig(
        interval_seconds=60,
        duration_seconds=180,
        alert_mode=AlertMode.BEEP_AND_VIBRATION,
    )

    engine.start(config, start_ts=1000.0)
    engine.tick(now_ts=1060.0)

    assert adapter.events == [(AlertMode.BEEP_AND_VIBRATION, False)]


def test_hybrid_policy_only_one_catch_up_alert() -> None:
    adapter = InstrumentedAlertAdapter()
    runtime = NoOpRuntime()
    engine = IntervalTimerEngine(adapter, runtime)
    config = SessionConfig(interval_seconds=60, duration_seconds=300, alert_mode=AlertMode.BEEP)

    progress = engine.start(config, start_ts=1000.0)
    assert progress.planned_alert_count == 5

    # Skip ahead past three due slots -> one catch-up alert should fire.
    progress = engine.tick(now_ts=1190.0)
    assert progress is not None
    assert adapter.events == [(AlertMode.BEEP, True)]
    assert progress.delivered_alert_count == 1
    assert progress.attempted_alert_count == 1


def test_completion_stops_future_alerts() -> None:
    adapter = InstrumentedAlertAdapter()
    runtime = NoOpRuntime()
    engine = IntervalTimerEngine(adapter, runtime)
    config = SessionConfig(interval_seconds=60, duration_seconds=180, alert_mode=AlertMode.BEEP)

    engine.start(config, start_ts=1000.0)
    engine.tick(now_ts=1060.0)
    engine.tick(now_ts=1120.0)
    progress = engine.tick(now_ts=1180.0)

    assert progress is not None
    assert progress.completed is True
    assert progress.running is False

    before = len(adapter.events)
    assert engine.tick(now_ts=1300.0) is None
    assert len(adapter.events) == before
