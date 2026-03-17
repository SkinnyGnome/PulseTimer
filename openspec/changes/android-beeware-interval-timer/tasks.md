## 1. Session Model and Validation

- [x] 1.1 Define session configuration model (interval, duration, alert mode) and enforce input validation rules.
- [x] 1.2 Implement planned alert count calculation using floor(duration / interval) and expose it in session state.
- [x] 1.3 Add unit tests for valid/invalid configuration and planned count calculation.

## 2. Deterministic Scheduling Engine

- [x] 2.1 Implement absolute-time schedule generation from fixed session start timestamp.
- [x] 2.2 Implement runtime progression that advances schedule index without cumulative sleep-drift assumptions.
- [x] 2.3 Add tests that verify schedule mapping for representative sessions (for example 90 minutes / 3 minutes).

## 3. Android Active-Session Runtime

- [x] 3.1 Add Android active-session lifecycle management that keeps timer processing alive while app is backgrounded or screen-off.
- [x] 3.2 Add active-session foreground notification behavior for runtime continuity.
- [ ] 3.3 Validate background and screen-off continuity on a physical Android device and record observed behavior.

## 4. Alert Delivery Modes

- [x] 4.1 Implement alert delivery adapter with Beep mode.
- [x] 4.2 Implement alert delivery adapter with Vibration mode.
- [x] 4.3 Implement combined Beep + Vibration mode and ensure mode is applied consistently across the active session.
- [x] 4.4 Add tests or instrumentation checks for mode selection and per-alert mode execution.

## 5. Hybrid Late-Delivery Policy

- [x] 5.1 Implement delay detection based on current time versus scheduled alert timestamps.
- [x] 5.2 Implement Hybrid behavior: emit at most one immediate catch-up alert after delay, then resume normal cadence.
- [x] 5.3 Add tests for no-delay, single-delay, and multi-missed-interval cases to prevent burst catch-up regressions.

## 6. Session Progress and Completion

- [x] 6.1 Expose delivered alert count and planned alert count in session progress state.
- [x] 6.2 Ensure session completes at duration boundary and stops future alert scheduling.
- [x] 6.3 Add UI wiring for single-session controls (start/pause/stop) and progress display.

## 7. Verification and Release Readiness

- [x] 7.1 Create end-to-end verification checklist for configured session, mode selection, background continuity, and completion behavior.
- [ ] 7.2 Run full test suite plus manual Android checks and resolve defects.
- [x] 7.3 Update user documentation for V1 behavior, including Hybrid late-delivery policy and active-session notification expectations.
