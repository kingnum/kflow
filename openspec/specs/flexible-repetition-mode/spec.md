# flexible-repetition-mode Specification

## Purpose

定义灵活重复制模式的轮次决策与验证门控规则，包括阶段执行历史记录以及在状态文件中呈现近期修订信息的要求。

## Requirements

### Requirement: Change-tier repetition round upper bound

The system SHALL determine the repetition round **upper bound** from the change tier, and for re-execution SHALL use the higher of the tier upper bound and the impact scope score mapping. Rounds SHALL never be fewer than the global floor of 1. The fixed 10-round minimum for first execution SHALL NOT exist. When the accumulated unverified-fix list is non-empty at the termination point, a recheck round SHALL be appended in addition to the determined upper bound, SHALL NOT consume it, and SHALL be limited to one per phase.

#### Scenario: First execution uses the tier upper bound

- **WHEN** an execution phase (code/code-review/api-test/e2e-test/integration-test/bug-fix, and plan) is executed for the first time in a change
- **THEN** the round upper bound SHALL be: 轻量 = 1 round, 标准 = 3 rounds, 完整 = 5 rounds
- **AND** for the plan phase, whose iteration loop is a product self-review, the round upper bound SHALL be the design self-review basis instead: 轻量 = 1 round, 标准 = 2 rounds, 完整 = 5 rounds
- **AND** the execution rounds SHALL be at least 1
- **AND** all repetition rules apply (full sweep each round, convergence-driven termination)
- **AND** the rounds SHALL NOT be fixed at 10 regardless of tier

#### Scenario: Re-execution uses the higher of tier upper bound and impact mapping

- **WHEN** an execution phase is re-executed after a phase rollback (REVISION or rollback re-execution)
- **THEN** the system SHALL read the impact scope score from .status.md "Recent Revision Info"
- **AND** the round upper bound SHALL be `max(tier upper bound, impact mapping)` where the impact mapping is:
  - Score <= 3: 1 round
  - Score 4-15: 3 rounds
  - Score > 15: 5 rounds
- **AND** the determined upper bound SHALL be written to .status.md as the target round count

#### Scenario: Recheck round applies outside the determined upper bound

- **WHEN** an execution phase reaches its termination point with a non-empty accumulated unverified-fix list
- **THEN** the recheck round SHALL be appended outside the determined upper bound
- **AND** the determined upper bound SHALL NOT be increased or reduced by the recheck round
- **AND** the recheck round SHALL be limited to one per phase

#### Scenario: No impact score falls back to the tier upper bound

- **WHEN** a phase is re-executed but no impact scope score is available in .status.md
- **THEN** the round upper bound SHALL be the tier upper bound for the change tier

#### Scenario: Change tier is not determined by project design basis

- **WHEN** determining the round upper bound for any execution phase
- **THEN** the system SHALL NOT use whether the project has design basis (docs/CONTEXT.md existence, docs/designs/detailed-designs/ emptiness) as an input

### Requirement: Flexible repetition verification gate

When an execution phase terminates by convergence before reaching the tier round upper bound, the system SHALL enforce a verification gate to ensure quality. When an execution phase terminates with 终止原因 `收敛（复检轮）`, the recheck round SHALL have verified every accumulated unverified fix, and this verification SHALL count as satisfying the full-sweep criterion.

#### Scenario: Verification gate for reduced rounds

- **WHEN** 执行轮次 < tier round upper bound at termination
- **THEN** the system SHALL enforce the following verification criteria:
  - Affected items: 100% coverage verification (every affected functional point/interface fully checked)
  - Full sweep: at least 1 round of complete full-sweep traversal (all work items)
  - Product integrity: all required outputs exist and are format-compliant
- **AND** all three criteria MUST pass for acceptance

#### Scenario: Verification gate when the recheck round is used

- **WHEN** an execution phase terminates with 终止原因 `收敛（复检轮）`
- **THEN** 执行轮次 SHALL equal the tier round upper bound (the recheck round is not counted)
- **AND** the full-sweep criterion SHALL be satisfied by the recheck round's proof of complete traversal
- **AND** the affected-items and product-integrity criteria MUST pass for acceptance

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
  - Rounds completed (e.g., 3/3, 2/5)
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
