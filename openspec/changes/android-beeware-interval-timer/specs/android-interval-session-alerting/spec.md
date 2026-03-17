## ADDED Requirements

### Requirement: User can configure and start a single interval session
The system MUST allow a user to configure interval length, total session duration, and alert mode before starting a session. The system MUST reject session start when interval or duration is non-positive, or when interval is greater than total duration.

#### Scenario: Start valid session
- **WHEN** the user sets interval to 3 minutes, duration to 90 minutes, alert mode to Beep, and starts the session
- **THEN** the system starts one active session with those values and computes planned alert count as floor(duration / interval)

#### Scenario: Reject invalid session values
- **WHEN** the user attempts to start a session with interval 0 or duration 0 or interval greater than duration
- **THEN** the system MUST prevent session start and present a validation error

### Requirement: Active sessions continue while app is backgrounded or screen is off
During an active session, the system MUST continue timer progression and scheduled alert evaluation when the app is backgrounded and/or the device screen is off.

#### Scenario: Background continuity
- **WHEN** a session is active and the user backgrounds the app for two intervals
- **THEN** the system continues schedule progression and performs alert handling according to the configured mode and late-delivery policy

#### Scenario: Screen-off continuity
- **WHEN** a session is active and the device screen turns off
- **THEN** the system continues session timing without resetting or pausing solely because the screen is off

### Requirement: System supports selectable alert mode
The system MUST support exactly three V1 alert modes for each session: Beep, Vibration, and Beep + Vibration. The selected mode MUST be applied consistently for every delivered alert in that session unless the session is stopped.

#### Scenario: Beep mode session
- **WHEN** the user starts a session with alert mode Beep
- **THEN** each delivered alert uses beep signaling without vibration

#### Scenario: Vibration mode session
- **WHEN** the user starts a session with alert mode Vibration
- **THEN** each delivered alert uses vibration signaling without beep

#### Scenario: Beep plus vibration session
- **WHEN** the user starts a session with alert mode Beep + Vibration
- **THEN** each delivered alert uses both beep and vibration signaling

### Requirement: Session uses deterministic absolute-time schedule
The system MUST compute alert timestamps from a fixed session start time using absolute intervals rather than chaining repeated interval delays.

#### Scenario: Long session drift control
- **WHEN** a session of 90 minutes with 3-minute intervals runs continuously
- **THEN** scheduled alert index n corresponds to session_start + n * interval and does not drift from cumulative repeated-sleep error

### Requirement: Hybrid late-delivery policy governs delayed execution
If runtime delay causes one or more scheduled alert timestamps to be missed, the system MUST deliver at most one immediate catch-up alert, then resume normal cadence from the current schedule position.

#### Scenario: Multiple missed intervals while delayed
- **WHEN** runtime resumes after delay that spans three scheduled alerts
- **THEN** the system emits one immediate catch-up alert and continues with the next future scheduled timestamp without emitting a burst of all missed alerts

#### Scenario: No missed interval
- **WHEN** runtime reaches an on-time scheduled timestamp
- **THEN** the system emits the configured alert mode at that timestamp and continues to the next scheduled timestamp

### Requirement: Planned alert count is deterministic and auditable
For each session, planned alert count MUST equal floor(total_duration / interval). The system MUST expose session progress with delivered alert count and planned alert count, and the session MUST finish after the schedule reaches the configured duration boundary.

#### Scenario: Planned count for 90-minute and 3-minute session
- **WHEN** the user starts a session with total duration 90 minutes and interval 3 minutes
- **THEN** planned alert count is 30 and progress reporting displays delivered_count out of 30

#### Scenario: Session completion boundary
- **WHEN** the schedule reaches the total duration boundary
- **THEN** the system ends the active session and stops future alert scheduling for that session
