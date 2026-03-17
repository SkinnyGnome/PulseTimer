from __future__ import annotations

import logging
import sys
from dataclasses import dataclass, field
from typing import Protocol

from .session import AlertMode

logger = logging.getLogger(__name__)


class AlertDeliveryAdapter(Protocol):
    def deliver(self, mode: AlertMode, *, catch_up: bool = False) -> None:
        ...


@dataclass
class InstrumentedAlertAdapter:
    events: list[tuple[AlertMode, bool]] = field(default_factory=list)

    def deliver(self, mode: AlertMode, *, catch_up: bool = False) -> None:
        self.events.append((mode, catch_up))


class AndroidAlertAdapter:
    def deliver(self, mode: AlertMode, *, catch_up: bool = False) -> None:
        if mode in (AlertMode.BEEP, AlertMode.BEEP_AND_VIBRATION):
            self._beep()
        if mode in (AlertMode.VIBRATION, AlertMode.BEEP_AND_VIBRATION):
            self._vibrate()
        logger.info("Delivered alert mode=%s catch_up=%s", mode.value, catch_up)

    def _beep(self) -> None:
        if sys.platform != "android":
            logger.info("Beep on non-Android runtime")
            return

        try:
            from jnius import autoclass  # type: ignore

            ToneGenerator = autoclass("android.media.ToneGenerator")
            AudioManager = autoclass("android.media.AudioManager")
            tone = ToneGenerator(AudioManager.STREAM_NOTIFICATION, 80)
            tone.startTone(ToneGenerator.TONE_PROP_BEEP, 200)
        except Exception as exc:
            logger.warning("Beep delivery failed: %s", exc)

    def _vibrate(self) -> None:
        if sys.platform != "android":
            logger.info("Vibration on non-Android runtime")
            return

        try:
            from jnius import autoclass  # type: ignore

            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            Context = autoclass("android.content.Context")

            activity = PythonActivity.mActivity
            vibrator = activity.getSystemService(Context.VIBRATOR_SERVICE)
            vibrator.vibrate(200)
        except Exception as exc:
            logger.warning("Vibration delivery failed: %s", exc)


def build_alert_adapter() -> AlertDeliveryAdapter:
    return AndroidAlertAdapter()
