from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class AlertMode(str, Enum):
    BEEP = "beep"
    VIBRATION = "vibration"
    BEEP_AND_VIBRATION = "beep_and_vibration"


@dataclass(frozen=True)
class SessionConfig:
    interval_seconds: int
    duration_seconds: int
    alert_mode: AlertMode

    def __post_init__(self) -> None:
        if self.interval_seconds <= 0:
            raise ValueError("Interval must be greater than 0 seconds")
        if self.duration_seconds <= 0:
            raise ValueError("Duration must be greater than 0 seconds")
        if self.interval_seconds > self.duration_seconds:
            raise ValueError("Interval cannot be greater than duration")

    @property
    def planned_alert_count(self) -> int:
        return self.duration_seconds // self.interval_seconds


@dataclass
class SessionProgress:
    planned_alert_count: int
    delivered_alert_count: int = 0
    attempted_alert_count: int = 0
    running: bool = False
    paused: bool = False
    completed: bool = False
