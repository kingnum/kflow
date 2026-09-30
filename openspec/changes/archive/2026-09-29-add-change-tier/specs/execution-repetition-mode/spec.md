# Spec Delta

## MODIFIED Requirements

### Requirement: Per-skill repetition model definition file

Each execution-phase skill SHALL provide its own `references/repetition.md` file as the source of truth for repetition mode execution specifications. The model SHALL support both the tier baseline (rounds determined by the change tier) and the flexible re-execution overlay (rounds raised by the impact scope score). No centralized `kflow-shared/repetition-model.md` SHALL exist.

#### Scenario: Standard repetition for first execution

- **WHEN** an execution phase runs for the first time in a change
- **THEN** the repetition model SHALL enforce the tier baseline rounds (轻量 1 / 标准 3 / 完整 10)
- **AND** each round SHALL traverse all work items with complete phase-specific workflow
- **AND** the rounds SHALL NOT be fixed at 10 regardless of tier

#### Scenario: Flexible repetition for re-execution

- **WHEN** an execution phase re-executes after a phase rollback
- **THEN** the repetition model SHALL determine rounds as `max(tier baseline, impact score mapping)` using the score from .status.md
- **AND** apply the score-to-round mapping rules defined in the tier-driven-repetition capability

#### Scenario: Verification gate for flexible mode

- **WHEN** target rounds are fewer than 10 (flexible mode)
- **THEN** the acceptance criteria SHALL include:
  - Affected items: 100% coverage verification
  - Full sweep: at least 1 complete round
  - Product integrity: all required outputs exist and are format-compliant
