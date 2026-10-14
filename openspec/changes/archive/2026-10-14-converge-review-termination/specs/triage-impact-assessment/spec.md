# Spec Delta

## MODIFIED Requirements

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

## REMOVED Requirements

### Requirement: Impact score to round mapping

**Reason**: 影响评分到重复制轮次的映射（`Score <= 3: 1 round` / `Score 4-15: 3 rounds` / `Score > 15: 5 rounds`）仅用于抬高档位轮次上限；本变更删除全部档位轮次上限与分数→轮次映射，收敛成为唯一成功终止条件。

**Migration**: 影响评分本身保留（见 `Triage impact assessment on diagnosis`），下游仅用于受影响项清单与回退判定，不再用于推轮次。原引用能力 `tier-driven-repetition` 已废弃，其职责迁移至 `convergence-driven-repetition`；该能力不再定义任何分数→轮次映射。
