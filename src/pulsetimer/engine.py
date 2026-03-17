from __future__ import annotations

from dataclasses import dataclass

from .alerts import AlertDeliveryAdapter
from .android_runtime import ActiveSessionRuntime
from .scheduler import SchedulerState, evaluate_tick
from .session import SessionConfig, SessionProgress


@dataclass
class EngineState:
    config: SessionConfig
    start_ts: float
    scheduler_state: SchedulerState


class IntervalTimerEngine:
    def __init__(self, alerts: AlertDeliveryAdapter, runtime: ActiveSessionRuntime) -> None:
        self._alerts = alerts
        self._runtime = runtime
        self._state: EngineState | None = None
        self._progress: SessionProgress | None = None

    @property
    def progress(self) -> SessionProgress | None:
        return self._progress

    def start(self, config: SessionConfig, *, start_ts: float) -> SessionProgress:
        self._state = EngineState(config=config, start_ts=start_ts, scheduler_state=SchedulerState())
        self._progress = SessionProgress(
            planned_alert_count=config.planned_alert_count,
            running=True,
            paused=False,
            completed=False,
        )
        self._runtime.start("PulseTimer active session", "Timer running in background")
        return self._progress

    def pause(self) -> None:
        if self._progress and self._progress.running and not self._progress.completed:
            self._progress.paused = True

    def resume(self) -> None:
        if self._progress and self._progress.running and not self._progress.completed:
            self._progress.paused = False

    def stop(self) -> None:
        if self._progress:
            self._progress.running = False
            self._progress.paused = False
            self._progress.completed = True
        self._state = None
        self._runtime.stop()

    def tick(self, *, now_ts: float) -> SessionProgress | None:
        if self._state is None or self._progress is None:
            return None
        if not self._progress.running or self._progress.paused or self._progress.completed:
            return self._progress

        decision = evaluate_tick(
            now_ts=now_ts,
            start_ts=self._state.start_ts,
            config=self._state.config,
            state=self._state.scheduler_state,
        )

        if decision.should_alert:
            self._progress.attempted_alert_count += 1
            self._alerts.deliver(self._state.config.alert_mode, catch_up=decision.catch_up)
            self._progress.delivered_alert_count += 1

        if decision.completed:
            self.stop()

        return self._progress
