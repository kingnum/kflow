# triage-impact-assessment Specification

## Purpose

定义诊断阶段的影响面评估规则，包括评估证据来源、路由输出中的执行模式声明，以及影响面评估信息的去向——受影响项清单与影响范围分数 SHALL 仅用于下游阶段的受影响项清单与回退判定，`SHALL NOT` 映射为重复制轮次（轮数由收敛决定）。

## Requirements

### Requirement: Triage impact assessment on diagnosis

kflow-bug-triage SHALL perform impact assessment as part of the diagnostic process, producing an impact scope evaluation that includes affected functional points, interfaces, data model changes, and an impact scope score. The impact scope score SHALL NOT be mapped to repetition rounds.

#### Scenario: Impact assessment included in diagnostic report

- **WHEN** kflow-bug-triage completes four-layer root cause diagnosis
- **THEN** the diagnostic report (bugs/bug-NNN-NNN.md) SHALL include an "Impact Assessment" section containing:
  - Affected functional points list (e.g., FP-001, FP-003)
  - Affected interfaces list (e.g., /api/orders/export)
  - Data model changes (none / description of changes)
  - Impact scope score (calculated value)
- **AND** the impact assessment SHALL be performed before route confirmation

#### Scenario: Impact score calculation

- **WHEN** the system calculates the impact scope score
- **THEN** the score SHALL be computed as: `score = functional_points × 1 + interfaces × 1.5 + data_model_changes × 2`
- **AND** functional_points count = number of affected functional points
- **AND** interfaces count = number of affected API endpoints
- **AND** data_model_changes = 1 if any data model modification exists, 0 otherwise

#### Scenario: Impact assessment for L1/L2/L3 routes

- **WHEN** triage routes to L1 (explore REVISION), L2 (prototype-design REVISION), or L3 (design REVISION)
- **THEN** the impact assessment SHALL be passed to the target phase via .status.md "Recent Revision Info" section
- **AND** downstream phases SHALL use the affected items list for the verification gate and the rollback decision
- **AND** downstream phases SHALL NOT use the impact scope score to determine repetition rounds

### Requirement: Impact assessment evidence sources

The impact assessment SHALL use specific evidence sources to identify affected scope.

#### Scenario: Evidence-based assessment

- **WHEN** performing impact assessment
- **THEN** the system SHALL identify affected functional points by cross-referencing the diagnostic conclusion with functional-designs/
- **AND** SHALL identify affected interfaces by checking detailed-design.md API definitions
- **AND** SHALL identify data model changes by examining the diagnostic evidence for schema/storage modifications

### Requirement: Execution mode declaration in route output

kflow-bug-triage SHALL include an execution mode declaration when routing to execution phases.

#### Scenario: Route output includes execution mode

- **WHEN** triage routes to any execution phase (including kflow-bug-fix)
- **THEN** the route output SHALL include: `EXECUTION_MODE = SUBAGENT_REQUIRED`
- **AND** the declaration SHALL specify that the target Skill MUST use Agent subagent for main work
- **AND** the declaration SHALL specify that subagent SHOULD run in foreground mode (run_in_background=false recommended)
