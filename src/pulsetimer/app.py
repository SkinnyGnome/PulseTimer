from __future__ import annotations

from datetime import datetime

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from .alerts import build_alert_adapter
from .android_runtime import build_runtime
from .engine import IntervalTimerEngine
from .session import AlertMode, SessionConfig


class PulseTimerApp(toga.App):
    def startup(self) -> None:
        self.engine = IntervalTimerEngine(build_alert_adapter(), build_runtime())

        self.interval_input = toga.TextInput(value="3", style=Pack(flex=1))
        self.duration_input = toga.TextInput(value="90", style=Pack(flex=1))
        self.mode_select = toga.Selection(
            items=[AlertMode.BEEP.value, AlertMode.VIBRATION.value, AlertMode.BEEP_AND_VIBRATION.value],
            value=AlertMode.BEEP.value,
            style=Pack(flex=1),
        )

        self.status_label = toga.Label("Ready", style=Pack(padding_top=8))
        self.progress_label = toga.Label("Delivered: 0 / 0", style=Pack(padding_top=4))

        start_btn = toga.Button("Start", on_press=self.start_session, style=Pack(flex=1))
        pause_btn = toga.Button("Pause", on_press=self.pause_session, style=Pack(flex=1))
        resume_btn = toga.Button("Resume", on_press=self.resume_session, style=Pack(flex=1))
        stop_btn = toga.Button("Stop", on_press=self.stop_session, style=Pack(flex=1))

        controls = toga.Box(
            children=[start_btn, pause_btn, resume_btn, stop_btn],
            style=Pack(direction=ROW, gap=6, padding_top=8),
        )

        root = toga.Box(
            children=[
                toga.Label("Interval (minutes)"),
                self.interval_input,
                toga.Label("Duration (minutes)"),
                self.duration_input,
                toga.Label("Alert mode"),
                self.mode_select,
                controls,
                self.status_label,
                self.progress_label,
            ],
            style=Pack(direction=COLUMN, padding=12),
        )

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = root
        self.main_window.show()

        self.add_background_task(self._ticker)

    async def _ticker(self, widget: toga.Widget) -> None:
        while True:
            progress = self.engine.tick(now_ts=datetime.now().timestamp())
            if progress:
                self.progress_label.text = (
                    f"Delivered: {progress.delivered_alert_count} / {progress.planned_alert_count}"
                )
                if progress.completed:
                    self.status_label.text = "Completed"
            await self.sleep(0.5)

    def start_session(self, widget: toga.Widget) -> None:
        try:
            interval_seconds = int(self.interval_input.value) * 60
            duration_seconds = int(self.duration_input.value) * 60
            mode = AlertMode(self.mode_select.value)
            config = SessionConfig(
                interval_seconds=interval_seconds,
                duration_seconds=duration_seconds,
                alert_mode=mode,
            )
            progress = self.engine.start(config, start_ts=datetime.now().timestamp())
            self.status_label.text = "Running"
            self.progress_label.text = (
                f"Delivered: {progress.delivered_alert_count} / {progress.planned_alert_count}"
            )
        except Exception as exc:
            self.status_label.text = f"Error: {exc}"

    def pause_session(self, widget: toga.Widget) -> None:
        self.engine.pause()
        self.status_label.text = "Paused"

    def resume_session(self, widget: toga.Widget) -> None:
        self.engine.resume()
        self.status_label.text = "Running"

    def stop_session(self, widget: toga.Widget) -> None:
        self.engine.stop()
        self.status_label.text = "Stopped"


def main() -> PulseTimerApp:
    return PulseTimerApp("PulseTimer", "com.skinnygnome.pulsetimer")
