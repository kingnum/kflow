## ADDED Requirements

### Requirement: Shared state values definition file
The system SHALL provide `.claude/skills/kflow-shared/state-values.md` as the single source of truth for all 13 status values used in `.status.md` files.

#### Scenario: New file creation
- **WHEN** the change is applied
- **THEN** `kflow-shared/state-values.md` SHALL exist containing the complete definition of all 13 state values (✅ 完成, 🔄 进行中, ⏳ 待开始, ❌ 阻塞, ⚠️ 需修订, ⏸️ 暂缓, etc.) with their semantics and transition rules (currently in `03-status-and-tasks.md` §3.3)

#### Scenario: All docs reference single definition
- **WHEN** any Skill design doc or core mechanism doc references state values
- **THEN** it SHALL reference `kflow-shared/state-values.md` rather than redefining state values inline

### Requirement: Core mechanism doc state values section replaced
`03-status-and-tasks.md` §3.3 state value table SHALL be replaced with a reference to `kflow-shared/state-values.md`.

#### Scenario: No duplicate state value definitions
- **WHEN** `03-status-and-tasks.md` is read
- **THEN** §3.3 SHALL NOT contain the full state value table — it SHALL reference `kflow-shared/state-values.md`
