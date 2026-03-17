# PulseTimer
PulseTimer is a tiny but mighty interval-beeping machine built with BeeWare.
Tell it how often to alert and for how long, and it keeps cadence for one active session.

## V1 behavior

- Single-session timer with configurable interval and duration.
- Alert modes: Beep, Vibration, or Beep + Vibration.
- Deterministic planned alert count: floor(duration / interval).
- Hybrid late-delivery policy: if multiple intervals are missed, emit at most one immediate catch-up alert, then resume normal cadence.
- Android runtime integration includes active-session runtime hooks and foreground continuity support.

## Project layout

- `src/pulsetimer/session.py`: session model, validation, and progress state.
- `src/pulsetimer/scheduler.py`: absolute-time scheduling and Hybrid policy decisions.
- `src/pulsetimer/engine.py`: runtime loop, delivery counts, and completion handling.
- `src/pulsetimer/alerts.py`: alert adapters including Android beep/vibration paths.
- `src/pulsetimer/android_runtime.py`: Android active-session lifecycle hooks.
- `src/pulsetimer/app.py`: BeeWare (Toga) UI with Start/Pause/Resume/Stop controls.

## Development

Install dev dependencies:

```bash
python -m pip install -e ".[dev]"
```

Run tests:

```bash
python -m pytest -q
```

Run the app locally (requires optional BeeWare dependency):

```bash
python -m pip install -e ".[app]"
python -m pulsetimer
```

## Android packaging

This project now includes Briefcase configuration for Android packaging.

Create Android project files:

```bash
python -m briefcase create android
```

Build and package the app:

```bash
python -m briefcase build android
python -m briefcase package android
```

Codespaces is suitable for generating Android build artifacts, but it is not a good place to validate the desktop BeeWare GTK UI and it cannot directly USB-deploy to a physical phone in the usual way. The expected flow is to build in Codespaces, download the generated APK, install it on your Android device, and then execute the checks in `docs/e2e-checklist.md`.

See `docs/android-packaging.md` for the full workflow.

## Manual Android verification

Use the checklist in `docs/e2e-checklist.md` on a physical device to validate background and screen-off continuity behavior.
