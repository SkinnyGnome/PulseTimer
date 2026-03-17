## Why

PulseTimer needs a clear V1 product contract so implementation stays focused and reliable on Android. Users need interval alerts that continue while backgrounded or with screen off, with predictable counts over a fixed session.

## What Changes

- Define a V1 single-session interval timer for Android built with BeeWare.
- Require alerts to continue during app backgrounding and screen-off periods while a session is active.
- Support user-selectable alert mode: Beep, Vibration, or Beep + Vibration.
- Define exact planned alert count behavior over configured duration and interval.
- Define Hybrid late-delivery policy when the app/runtime is delayed: deliver at most one catch-up alert immediately, then resume cadence.
- Require an active-session runtime strategy that prevents timer sleep during an active session.

## Capabilities

### New Capabilities
- `android-interval-session-alerting`: Configure and run a single interval session that reliably delivers alerts on Android, including background/screen-off continuity and Hybrid catch-up behavior.

### Modified Capabilities
- None.

## Impact

- Affected areas: Android runtime behavior, session timing engine, alert delivery integration, and in-session UI state display.
- Platform constraints: Android background execution rules and active session notification expectations.
- Dependencies/systems: BeeWare app runtime, Android audio and vibration facilities, foreground session lifecycle management.
