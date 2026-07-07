## MODIFIED Requirements

### Requirement: Per-skill repetition model definition file
Each execution-phase skill SHALL provide its own `references/repetition.md` file as the source of truth for repetition mode execution specifications. The model SHALL support both standard repetition (10 rounds for first execution) and flexible repetition (impact-based rounds for re-execution after rollback). No centralized `kflow-shared/repetition-model.md` SHALL exist.

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

### Requirement: Subagent prompt construction follows layered loading from local references
Subagent prompt construction SHALL follow the layered loading strategy using files from the skill's own `references/` directory. Each phase SKILL.md SHALL specify which `references/` files to load.

#### Scenario: Phase SKILL.md documents local references loading
- **WHEN** an execution-phase SKILL.md constructs a subagent prompt
- **THEN** it SHALL list the specific `references/` files to load based on tier classification
- **AND** the file paths SHALL be relative to the project root (e.g., `skills/<skill>/references/repetition.md` in dev)

### Requirement: Repetition model includes inter-round summary
Each execution-phase skill's `references/repetition.md` SHALL include inter-round summary rules.

#### Scenario: Repetition file includes inter-round summary
- **WHEN** `references/repetition.md` is read for any execution-phase skill
- **THEN** it SHALL contain a section on inter-round summary format and injection rules

## REMOVED Requirements

### Requirement: Shared repetition model in kflow-shared
**Reason**: `kflow-shared/repetition-model.md` is removed. Each execution-phase skill maintains its own repetition model in `references/repetition.md`.
**Migration**: Repetition rules are distributed to each execution-phase skill's `references/repetition.md`. Consumer projects should delete `kflow-shared/repetition-model.md`.
