# Spec Delta

## ADDED Requirements

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

## MODIFIED Requirements

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

## REMOVED Requirements

### Requirement: Change-tier repetition round upper bound

**Reason**: 该需求以「档位轮次上限」与「`max(tier upper bound, impact mapping)` 回退叠加」决定轮次上限，并配套复检轮。本变更删除全部档位轮次上限、分数→轮次映射与复检轮，收敛成为唯一成功终止条件。

**Migration**: 轮数改由收敛实际发生在第几轮决定；影响范围分数本身保留，但仅用于受影响项清单与回退判定，不再用于推轮次。权威定义见 `convergence-driven-repetition` 能力。

### Requirement: Flexible repetition verification gate

**Reason**: 该需求的门控含「Full sweep: at least 1 round」兜底与「复检轮」分支；前者被见证轮第 (c) 项（报告证明全维全量遍历）吞并，后者随复检轮机制删除。

**Migration**: 迁移至本能力新增的 `Convergence-aligned flexible repetition verification gate`——门控退化为受影响项 100% 覆盖（回退场景）＋产物完整性；不再要求固定的全量兜底轮，也不再追加复检轮。
