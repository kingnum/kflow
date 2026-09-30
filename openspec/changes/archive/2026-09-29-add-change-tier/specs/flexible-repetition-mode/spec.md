# Spec Delta

## ADDED Requirements

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

## MODIFIED Requirements

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

## REMOVED Requirements

### Requirement: Flexible repetition round decision

**Reason**: 该需求的「First execution uses full 10 rounds」场景对首次执行一律施加 10 轮，与变更规模无关；其余场景的分数-轮次映射与 `triage-impact-assessment`、`design-review-tiering` 各自定义的映射互不一致，形成三套并行口径。

**Migration**: 由本能力新增的 `Change-tier repetition round decision` 取代，轮次改由档位基线与统一映射的较大者决定；统一映射定义于 `tier-driven-repetition`。
