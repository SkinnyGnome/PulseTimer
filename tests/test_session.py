import pytest

from pulsetimer.session import AlertMode, SessionConfig


def test_valid_session_configuration() -> None:
    config = SessionConfig(interval_seconds=180, duration_seconds=5400, alert_mode=AlertMode.BEEP)
    assert config.interval_seconds == 180
    assert config.duration_seconds == 5400


def test_planned_alert_count_floor() -> None:
    config = SessionConfig(
        interval_seconds=180,
        duration_seconds=5459,
        alert_mode=AlertMode.VIBRATION,
    )
    assert config.planned_alert_count == 30


@pytest.mark.parametrize(
    "interval,duration",
    [(0, 100), (100, 0), (-1, 100), (300, 100)],
)
def test_invalid_session_configuration(interval: int, duration: int) -> None:
    with pytest.raises(ValueError):
        SessionConfig(interval_seconds=interval, duration_seconds=duration, alert_mode=AlertMode.BEEP)
