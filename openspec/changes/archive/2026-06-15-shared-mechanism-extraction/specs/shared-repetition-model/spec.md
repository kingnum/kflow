## ADDED Requirements

### Requirement: Shared repetition model definition file
The system SHALL provide `.claude/skills/kflow-shared/repetition-model.md` as the single source of truth for repetition mode execution specifications, including complexity formula, 10-round enforcement rules, acceptance criteria, and subagent prompt specifications.

#### Scenario: New file creation
- **WHEN** the change is applied
- **THEN** `kflow-shared/repetition-model.md` SHALL exist containing all content from `07-agent-model.md` §15 (complexity formula, round enforcement, acceptance criteria, prompt specifications, subagent isolation rules)

#### Scenario: Subagent prompt references shared file
- **WHEN** an execution-phase Skill constructs a subagent prompt
- **THEN** the prompt SHALL reference `kflow-shared/repetition-model.md` instead of inlining repetition rules

### Requirement: Core mechanism doc references shared file
`07-agent-model.md` §15 SHALL retain only a brief overview (≤5 lines) and a reference to `kflow-shared/repetition-model.md`. The full content SHALL be removed from the core mechanism doc.

#### Scenario: No duplicate content
- **WHEN** `07-agent-model.md` is read
- **THEN** §15 SHALL NOT contain the full complexity formula, round enforcement details, or prompt specifications — these SHALL only exist in `kflow-shared/repetition-model.md`

### Requirement: Skill design docs reference shared file
All execution-phase Skill design documents (kflow-code.md, kflow-code-review.md, kflow-api-test.md, kflow-e2e-test.md, kflow-integration-test.md) SHALL replace their inline repetition mode sections with a reference to `kflow-shared/repetition-model.md` plus phase-specific parameters only.

#### Scenario: Skill design doc redundancy eliminated
- **WHEN** kflow-code.md repetition section is read
- **THEN** it SHALL contain only: (1) a reference to `kflow-shared/repetition-model.md`, (2) phase-specific complexity weights, (3) phase-specific work item definitions, (4) phase-specific output requirements
