## Context

PulseTimer is a BeeWare-based mobile app focused on interval alert sessions. The V1 scope is a single active session where users configure interval, total duration, and alert mode, then receive alerts over time.

Android imposes background execution limits that can interrupt normal app timers when the app is backgrounded or the screen is off. The design must preserve reliable timing and alert delivery during active sessions while keeping implementation complexity suitable for V1.

Stakeholders are users who depend on periodic reminders during workouts, study blocks, or similar timed routines.

## Goals / Non-Goals

**Goals:**
- Provide a single-session timer with configurable interval and total duration.
- Keep active timer execution alive while app is backgrounded and/or screen is off.
- Deliver user-selected alert mode (Beep, Vibration, Beep + Vibration).
- Achieve deterministic planned alert count using absolute-time scheduling.
- Use Hybrid late-delivery policy to balance exact-count intent and user experience.

**Non-Goals:**
- Multi-session queueing.
- Presets, history, or analytics.
- Cross-device sync or cloud state.
- Rich customization beyond the three alert modes.

## Decisions

1. Active session runs as foreground-managed runtime on Android.
- Rationale: Background-only timers are not reliable under Android doze/app standby.
- Alternative considered: Standard in-app periodic timer without foreground management.
- Why not: High risk of suspended execution while backgrounded or screen-off.

2. Schedule alerts from fixed session start timestamps (absolute-time model).
- Rationale: Avoid cumulative drift from repeating sleep intervals.
- Alternative considered: Chained delay model (sleep interval repeatedly).
- Why not: Drift accumulation and unpredictable count at long durations.

3. Hybrid late-delivery policy for delayed execution.
- Behavior: If one or more alert timestamps were missed due to delay, deliver at most one immediate catch-up alert, then resume normal cadence from current schedule position.
- Rationale: Preserves user awareness of missed cadence without burst-spamming many alerts.
- Alternative considered: Full catch-up (emit every missed alert immediately) and full skip (emit none).
- Why not: Full catch-up can create noisy bursts; full skip can violate exact-count intent.

4. Deterministic planned alert count contract.
- Contract: planned_alert_count = floor(total_duration / interval).
- Runtime tracks attempted_delivery_count and completed_delivery_count to make behavior auditable.
- Rationale: Gives users a predictable session expectation and supports testability.

5. Alert delivery abstraction with mode-specific execution.
- Rationale: Separate scheduling concerns from audio/vibration mechanics.
- Alternative considered: Inline alert handling in timer engine.
- Why not: Harder to test and harder to adapt across runtime constraints.

## Risks / Trade-offs

- [Android policy variance across devices] -> Mitigation: Validate on at least one physical Android device and log lifecycle transitions for diagnostics.
- [Foreground execution perceived as persistent notification noise] -> Mitigation: Keep active-session notification concise and only present while session is active.
- [Hybrid policy may still surprise users expecting strict every-missed-alert playback] -> Mitigation: Document behavior in UI help text and spec scenarios.
- [Timing under deep sleep may shift wall-clock delivery moments] -> Mitigation: Preserve deterministic schedule index and avoid repeated-interval drift.

## Migration Plan

- No data migration is required for V1 because there is no persisted session history or preset schema.
- Rollback strategy: revert to previous app version; no stored schema changes are introduced by this change.

## Open Questions

- Whether Android notification sound should be treated as an optional fourth alert pathway in future versions.
- Whether users should be able to choose Hybrid vs strict catch-up policy in a later release.
