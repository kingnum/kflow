# flexible-repetition-mode Specification

## Purpose

定义灵活重复制模式的轮次决策与验证门控规则，包括阶段执行历史记录以及在状态文件中呈现近期修订信息的要求。

## Requirements

### Requirement: Change-tier repetition round decision

The system SHALL determine repetition target rounds from the change tier, and for re-execution SHALL use the higher of the tier baseline and the impact scope score mapping. The fixed 10-round minimum for first execution SHALL NOT exist.

#### Scenario: First execution uses the tier baseline

- **WHEN** an execution phase (code/code-review/api-test/e2e-test/integration-test/bug-fix, and plan) is executed for the first time in a change
- **THEN** the target rounds SHALL be the tier baseline: 轻量 = 1 round, 标准 = 3 rounds, 完整 = 10 rounds
- **AND** for the plan phase, whose iteration loop is a product self-review, the target rounds SHALL be the design self-review basis instead: 轻量 = 0 rounds, 标准 = 2 rounds, 完整 = 10 rounds
- **AND** all standard repetition rules apply (full sweep each round, natural convergence)
- **AND** the target rounds SHALL NOT be fixed at 10 regardless of tier

#### Scenario: Re-execution uses the higher of tier baseline and impact mapping

- **WHEN** an execution phase is re-executed after a phase rollback (REVISION or rollback re-execution)
- **THEN** the system SHALL read the impact scope score from .status.md "Recent Revision Info"
- **AND** the target rounds SHALL be `max(tier baseline, impact mapping)` where the impact mapping is:
  - Score <= 3: 1 round
  - Score 4-15: 3 rounds
  - Score > 15: 10 rounds
- **AND** the determined rounds SHALL be written to .status.md as the target round count

#### Scenario: No impact score falls back to the tier baseline

- **WHEN** a phase is re-executed but no impact scope score is available in .status.md
- **THEN** the target rounds SHALL be the tier baseline for the change tier

#### Scenario: Change tier is not determined by project design basis

- **WHEN** determining the target rounds for any execution phase
- **THEN** the system SHALL NOT use whether the project has design basis (docs/CONTEXT.md existence, docs/designs/detailed-designs/ emptiness) as an input

### Requirement: Flexible repetition verification gate

When target rounds are fewer than 10, the system SHALL enforce a verification gate to ensure quality.

#### Scenario: Verification gate for reduced rounds

- **WHEN** target rounds < 10 (flexible mode)
- **THEN** the system SHALL enforce the following verification criteria:
  - Affected items: 100% coverage verification (every affected functional point/interface fully checked)
  - Full sweep: at least 1 round of complete full-sweep traversal (all work items)
  - Product integrity: all required outputs exist and are format-compliant
- **AND** all three criteria MUST pass for acceptance

#### Scenario: Affected items verification

- **WHEN** verifying affected items
- **THEN** the system SHALL cross-reference the affected items list from .status.md "Recent Revision Info"
- **AND** each affected item SHALL receive complete phase-specific verification (not abbreviated)
- **AND** verification results SHALL be recorded in the phase output

#### Scenario: Full sweep兜底 round

- **WHEN** flexible repetition mode is active
- **THEN** at least one round SHALL be a complete full-sweep traversal of ALL work items
- **AND** this round SHALL NOT skip any work item based on impact assessment
- **AND** this ensures no collateral issues are missed

### Requirement: Phase execution history tracking

The system SHALL track phase execution history in .status.md to distinguish first execution from re-execution.

#### Scenario: Execution history table in status file

- **WHEN** .status.md is created or updated
- **THEN** it SHALL include a "Phase Execution History" table with columns:
  - Phase name
  - Execution count (1st, 2nd, etc.)
  - Last execution type (First Execution / REVISION / Rollback Re-execution)
  - Rounds completed (e.g., 3/3, 10/10)
  - Impact scope score (if applicable)
  - Notes

#### Scenario: History updated on phase completion

- **WHEN** an execution phase completes
- **THEN** the system SHALL update the execution history table
- **AND** increment the execution count for that phase
- **AND** record the execution type and rounds completed

### Requirement: Recent revision info in status file

The system SHALL store recent revision information in .status.md for downstream phases to read.

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
  - Recommended repetition rounds

#### Scenario: Revision info consumed by downstream phases

- **WHEN** an execution phase starts after a rollback
- **THEN** the phase SHALL read "Recent Revision Info" from .status.md
- **AND** use the impact scope score for round determination
- **AND** use the affected items list for verification gate

#### Scenario: Revision info cleared on archive

- **WHEN** kflow-archive completes for the change
- **THEN** the "Recent Revision Info" section MAY be cleared or archived with the change
