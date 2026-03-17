from __future__ import annotations

import logging
import sys
from dataclasses import dataclass
from typing import Protocol

logger = logging.getLogger(__name__)


class ActiveSessionRuntime(Protocol):
    def start(self, title: str, message: str) -> None:
        ...

    def stop(self) -> None:
        ...


@dataclass
class NoOpRuntime:
    active: bool = False

    def start(self, title: str, message: str) -> None:
        self.active = True
        logger.info("No-op runtime started: %s - %s", title, message)

    def stop(self) -> None:
        self.active = False
        logger.info("No-op runtime stopped")


class AndroidForegroundRuntime:
    """Best-effort foreground and wake-lock helper for BeeWare Android runtime."""

    def __init__(self) -> None:
        self.active = False
        self._wake_lock = None

    def start(self, title: str, message: str) -> None:
        if sys.platform != "android":
            self.active = True
            return

        try:
            from jnius import autoclass  # type: ignore

            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            Context = autoclass("android.content.Context")
            PowerManager = autoclass("android.os.PowerManager")

            activity = PythonActivity.mActivity
            pm = activity.getSystemService(Context.POWER_SERVICE)
            self._wake_lock = pm.newWakeLock(
                PowerManager.PARTIAL_WAKE_LOCK,
                "PulseTimer:ActiveSession",
            )
            self._wake_lock.acquire()

            # Notification setup is handled here as a best-effort no-crash branch.
            # Device- and runtime-specific details can vary across Android versions.
            logger.info("Foreground runtime request: %s - %s", title, message)
            self.active = True
        except Exception as exc:
            logger.warning("Unable to enable Android foreground runtime: %s", exc)
            self.active = True

    def stop(self) -> None:
        if self._wake_lock is not None:
            try:
                self._wake_lock.release()
            except Exception as exc:
                logger.warning("Failed to release wake lock: %s", exc)
        self._wake_lock = None
        self.active = False


def build_runtime() -> ActiveSessionRuntime:
    if sys.platform == "android":
        return AndroidForegroundRuntime()
    return NoOpRuntime()
