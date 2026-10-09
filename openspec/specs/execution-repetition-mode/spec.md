# execution-repetition-mode Specification

## Purpose

本能力定义各执行阶段 Skill 的重复制执行模型，规定重复模式权威定义文件的位置、标准重复与灵活重复两套轮次规则、子代理 prompt 的分层加载构造方式，以及轮次间摘要要求。

## Requirements

### Requirement: Per-skill repetition model definition file
Each execution-phase skill SHALL provide its own `references/repetition.md` file as the source of truth for repetition mode execution specifications. The model SHALL support both the tier round **upper bound** (rounds capped by the change tier) and the flexible re-execution overlay (the upper bound raised by the impact scope score). No centralized `kflow-shared/repetition-model.md` SHALL exist. Termination SHALL follow the convergence condition defined in the `tier-driven-repetition` capability.

#### Scenario: Standard repetition for first execution
- **WHEN** an execution phase runs for the first time in a change
- **THEN** the repetition model SHALL cap rounds by the tier upper bound (轻量 1 / 标准 3 / 完整 5)
- **AND** execution rounds SHALL be at least the global floor of 1
- **AND** each round SHALL traverse all work items with complete phase-specific workflow
- **AND** the rounds SHALL NOT be fixed at 10 regardless of tier
- **AND** the phase SHALL terminate early when the convergence condition (witness round) is met

#### Scenario: Flexible repetition for re-execution
- **WHEN** an execution phase re-executes after a phase rollback
- **THEN** the repetition model SHALL determine the round upper bound as `max(tier upper bound, impact score mapping)` using the score from .status.md
- **AND** apply the score-to-round mapping rules defined in the tier-driven-repetition capability

#### Scenario: Verification gate for flexible mode
- **WHEN** an execution phase terminates by convergence with 执行轮次 < the tier round upper bound
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
