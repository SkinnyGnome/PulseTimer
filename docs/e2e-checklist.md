# PulseTimer V1 End-to-End Verification Checklist

## Session Configuration

- [ ] Start session with interval 3 min, duration 90 min, mode Beep.
- [ ] Verify invalid settings are rejected (interval 0, duration 0, interval > duration).
- [ ] Confirm planned alert count displays 30 for 90/3 session.

## Alert Modes

- [ ] Verify Beep mode emits beep only.
- [ ] Verify Vibration mode emits vibration only.
- [ ] Verify Beep + Vibration mode emits both signals.

## Runtime Continuity

- [ ] Start session and background app for at least two intervals; verify session progresses.
- [ ] Start session, turn screen off for at least two intervals; verify session progresses.
- [ ] Confirm active-session notification is present while running.

## Hybrid Delay Policy

- [ ] Create delay spanning multiple intervals (for example by pausing process scheduling).
- [ ] Verify at most one immediate catch-up alert is emitted after delay.
- [ ] Verify subsequent alerts resume at normal cadence without burst playback.

## Completion Behavior

- [ ] Verify session stops scheduling future alerts at duration boundary.
- [ ] Verify delivered count never exceeds planned count.
- [ ] Verify manual stop ends active session and removes foreground runtime state.

## Notes

- Device tested:
- Android version:
- Build identifier:
- Issues found:
