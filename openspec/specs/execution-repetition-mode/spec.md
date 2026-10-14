# execution-repetition-mode Specification

## Purpose

本能力定义各执行阶段 Skill 的重复制执行模型，规定重复模式权威定义文件的位置、收敛驱动的终止口径（`SHALL NOT` 保留任何轮数上限或分数→轮次映射）、子代理 prompt 的分层加载构造方式与审查范围冻结要求，以及轮次间摘要要求。

## Requirements

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

### Requirement: Per-skill convergence-driven repetition model definition file

Each execution-phase skill SHALL provide its own `references/repetition.md` file as the source of truth for repetition mode execution specifications. The model SHALL determine rounds by when convergence actually occurs, SHALL NOT cap rounds by the change tier, and SHALL NOT define or retain any round upper bound, impact-score-to-round mapping, or recheck round. No centralized `kflow-shared/repetition-model.md` SHALL exist. Termination SHALL follow the convergence condition defined in the `convergence-driven-repetition` capability (the witness round with its four conditions).

#### Scenario: Convergence-driven repetition for first execution

- **WHEN** an execution phase runs for the first time in a change
- **THEN** the repetition model SHALL determine rounds by convergence, not by the change tier
- **AND** execution rounds SHALL be at least the global floor of 1
- **AND** each round SHALL traverse all work items with the complete phase-specific workflow
- **AND** the phase SHALL terminate as soon as the convergence condition (witness round) is met
- **AND** the rounds SHALL NOT be capped by any tier round upper bound

#### Scenario: Re-execution does not preset or raise rounds

- **WHEN** an execution phase re-executes after a phase rollback
- **THEN** the repetition model SHALL NOT preset or raise a round upper bound
- **AND** rounds SHALL be determined by convergence, exactly as for a first execution
- **AND** the impact scope score SHALL NOT be mapped to a round count

#### Scenario: Verification gate for flexible mode

- **WHEN** an execution phase terminates by convergence
- **THEN** the acceptance criteria SHALL include:
  - Affected items: 100% coverage verification
  - Product integrity: all required outputs exist and are format-compliant
- **AND** all criteria MUST pass for acceptance
- **AND** no fixed full-sweep floor round SHALL be required as a separate criterion

#### Scenario: Verification gate aligned with the witness round

- **WHEN** an execution phase terminates by convergence
- **THEN** the terminating round SHALL have verified every accumulated unverified fix (the witness-round condition (d))
- **AND** the acceptance criteria SHALL include affected items 100% coverage and product integrity
- **AND** no recheck round SHALL be appended
