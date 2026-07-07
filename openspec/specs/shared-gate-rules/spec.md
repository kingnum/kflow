## ADDED Requirements

### Requirement: Shared gate rules definition file
The system SHALL provide `.claude/skills/kflow-shared/gate-rules.md` as the single source of truth for all gate check rules, including 9 forward gates, rollback gates, HITL-blocking-plan-entry rules, and code-stage upstream discovery decision flow.

#### Scenario: New file creation
- **WHEN** the change is applied
- **THEN** `kflow-shared/gate-rules.md` SHALL exist containing: Gate 1-9 rules, rollback gate rules, HITL blocking plan entry, code-stage upstream discovery decision flow (currently in `03-status-and-tasks.md` §3.4)

#### Scenario: Single definition for rollback triggers
- **WHEN** rollback trigger sources are needed
- **THEN** they SHALL be read from `kflow-shared/gate-rules.md`, NOT from `03-status-and-tasks.md` or `04-gates-and-transitions.md`

### Requirement: Core mechanism docs gate sections replaced
`03-status-and-tasks.md` §3.4 gate rules and `04-gates-and-transitions.md` §6.5 rollback rules SHALL be replaced with references to `kflow-shared/gate-rules.md`.

#### Scenario: No duplicate gate rules
- **WHEN** `03-status-and-tasks.md` and `04-gates-and-transitions.md` are read
- **THEN** neither SHALL contain the full gate check rules — both SHALL reference `kflow-shared/gate-rules.md`

### Requirement: Internal duplication eliminated
`04-gates-and-transitions.md` §6.9 (编码阶段发现上游问题的标准化决策流程, duplicate of §6.6) SHALL be deleted.

#### Scenario: No duplicate code-stage decision flow
- **WHEN** `04-gates-and-transitions.md` is read
- **THEN** the code-stage upstream discovery decision flow SHALL appear only once (§6.6), §6.9 SHALL NOT exist
