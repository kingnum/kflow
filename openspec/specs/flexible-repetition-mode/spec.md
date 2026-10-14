# flexible-repetition-mode Specification

## Purpose

定义灵活重复制模式的验证门控规则（与收敛终止对齐：受影响项 100% 覆盖 + 产物完整性），包括阶段执行历史记录以及在状态文件中呈现近期修订信息的要求。

## Requirements

### Requirement: Phase execution history tracking

The system SHALL track phase execution history in .status.md to distinguish first execution from re-execution.

#### Scenario: Execution history table in status file

- **WHEN** .status.md is created or updated
- **THEN** it SHALL include a "Phase Execution History" table with columns:
  - Phase name
  - Execution count (1st, 2nd, etc.)
  - Last execution type (First Execution / REVISION / Rollback Re-execution)
  - Rounds completed (e.g., 3/3, 2/5)
  - Impact scope score (if applicable)
  - Notes

#### Scenario: History updated on phase completion

- **WHEN** an execution phase completes
- **THEN** the system SHALL update the execution history table
- **AND** increment the execution count for that phase
- **AND** record the execution type and rounds completed

### Requirement: Recent revision info in status file

The system SHALL store recent revision information in .status.md for downstream phases to read. The impact scope score SHALL be retained, but it SHALL NOT be used to determine repetition rounds; it SHALL only inform the affected-items list and the rollback decision.

#### Scenario: Revision info populated on rollback

- **WHEN** a phase rollback occurs (via triage route or design revision)
- **THEN** .status.md SHALL include a "Recent Revision Info" section with:
  - Revision trigger (e.g., BUG-003 triage diagnosis)
  - Revision source phase (e.g., L3 Detailed Design)
  - Revision timestamp
  - Revision content summary
  - Affected functional points list
  - Affected interfaces list
  - Data model changes (none / description)
  - Impact scope score
- **AND** the section SHALL NOT include recommended repetition rounds

#### Scenario: Revision info consumed by downstream phases

- **WHEN** an execution phase starts after a rollback
- **THEN** the phase SHALL read "Recent Revision Info" from .status.md
- **AND** use the affected items list for the verification gate
- **AND** use the impact scope score for the affected-items list and rollback determination, SHALL NOT use it for round determination

#### Scenario: Revision info cleared on archive

- **WHEN** kflow-archive completes for the change
- **THEN** the "Recent Revision Info" section MAY be cleared or archived with the change

### Requirement: Convergence-aligned flexible repetition verification gate

When an execution phase terminates by convergence, the system SHALL enforce the following verification criteria: affected items 100% coverage (every affected functional point/interface fully checked) and product integrity (all required outputs exist and are format-compliant). All criteria MUST pass for acceptance. The system SHALL NOT require a fixed full-sweep floor round as a separate criterion, and SHALL NOT append a recheck round.

#### Scenario: Verification gate at convergence

- **WHEN** an execution phase terminates by convergence
- **THEN** the verification criteria SHALL include:
  - Affected items: 100% coverage verification
  - Product integrity: all required outputs exist and are format-compliant
- **AND** all criteria MUST pass for acceptance
- **AND** no fixed full-sweep floor round SHALL be required

#### Scenario: Verification gate on rollback re-execution

- **WHEN** a phase re-executes after a phase rollback and .status.md carries an affected items list
- **THEN** every affected item SHALL receive complete phase-specific verification
- **AND** the affected items 100% coverage criterion MUST pass

#### Scenario: Affected items verification

- **WHEN** verifying affected items
- **THEN** the system SHALL cross-reference the affected items list from .status.md "Recent Revision Info"
- **AND** each affected item SHALL receive complete phase-specific verification (not abbreviated)
- **AND** verification results SHALL be recorded in the phase output
