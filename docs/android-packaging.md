# Android Packaging With Briefcase

This repository is configured for BeeWare Briefcase Android packaging.

## Install tooling

From the workspace root:

```bash
python -m pip install -e ".[dev]"
```

If you want Briefcase available as a command, add its install location to `PATH` or continue using the module form:

```bash
python -m briefcase --help
```

## Create Android project files

```bash
python -m briefcase create android
```

Briefcase will prompt for any missing Android build prerequisites such as:
- Java/JDK
- Android SDK command-line tools
- Android platform packages

## Build the debug APK

```bash
python -m briefcase build android
```

## Package the app

```bash
python -m briefcase package android
```

The generated Android artifacts will be placed in the Briefcase build/dist output directories.

## Install and test on a phone

Codespaces cannot directly attach to a USB Android device for `adb install` in the usual way. The practical flow is:

1. Build/package in Codespaces.
2. Download the generated APK from the workspace or artifact output.
3. Transfer it to your Android device.
4. Install it manually after enabling sideloading from unknown sources.
5. Run the checks in `docs/e2e-checklist.md`.

## Android permissions configured

The Briefcase config currently requests:
- `android.permission.VIBRATE`
- `android.permission.WAKE_LOCK`
- `android.permission.FOREGROUND_SERVICE`
- `android.permission.POST_NOTIFICATIONS`

These support the current app design for vibration alerts, active-session wakefulness, foreground runtime continuity, and notification visibility.

## Notes

- The current project is configured for Android packaging, but device behavior still needs physical Android validation.
- Desktop Toga UI testing in this Codespace is not a reliable validation path because of GTK/PyGObject runtime mismatches in the container.
