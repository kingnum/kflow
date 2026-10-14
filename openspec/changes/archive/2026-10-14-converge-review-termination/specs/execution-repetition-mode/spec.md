# Spec Delta

## ADDED Requirements

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

## REMOVED Requirements

### Requirement: Per-skill repetition model definition file

**Reason**: 该需求把重复制模型定义为「档位轮次上限 + 回退叠加影响范围分数映射抬高上限」，并规定终止点追加复检轮。本变更删除全部档位轮次上限、分数→轮次映射与复检轮，收敛成为唯一成功终止条件。

**Migration**: 迁移至本能力新增的 `Per-skill convergence-driven repetition model definition file`——轮数由收敛实际发生在第几轮决定；验证门控退化为「受影响项 100% 覆盖」（回退场景）＋产物完整性，「全量至少 1 轮兜底」被见证轮第 (c) 项吞并删除。终止模型、见证轮判据、不收敛判定与审查范围冻结的权威定义见 `convergence-driven-repetition` 能力。
