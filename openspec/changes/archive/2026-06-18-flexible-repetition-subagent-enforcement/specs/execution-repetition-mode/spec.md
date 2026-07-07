## MODIFIED Requirements

### Requirement: Shared repetition model definition file
The system SHALL provide `.claude/skills/kflow-shared/repetition-model.md` as the single source of truth for repetition mode execution specifications. The model SHALL support both standard repetition (10 rounds for first execution) and flexible repetition (impact-based rounds for re-execution after rollback).

#### Scenario: Standard repetition for first execution
- **WHEN** an execution phase runs for the first time in a change
- **THEN** the repetition model SHALL enforce 10 rounds
- **AND** each round SHALL traverse all work items with complete phase-specific workflow

#### Scenario: Flexible repetition for re-execution
- **WHEN** an execution phase re-executes after a phase rollback
- **THEN** the repetition model SHALL determine rounds based on impact scope score from .status.md
- **AND** apply the score-to-round mapping rules defined in the flexible-repetition-mode capability

#### Scenario: Verification gate for flexible mode
- **WHEN** flexible repetition mode is active (rounds < 10)
- **THEN** the acceptance criteria SHALL include:
  - Affected items: 100% coverage verification
  - Full sweep: at least 1 complete round
  - Product integrity: all required outputs exist and are format-compliant
