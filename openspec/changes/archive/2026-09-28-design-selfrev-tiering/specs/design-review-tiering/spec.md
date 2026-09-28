# Spec Delta

## ADDED Requirements

### Requirement: 设计自审按首次/非首次分级

系统 SHALL 依据项目是否已有设计基础决定设计三阶段（kflow-explore、kflow-prototype-design、kflow-design）SELFREV 自审的执行模式：首次创建走完整自审（固定 10 轮），非首次创建走弹性自审（弹性轮次 + 评分底线）。

#### Scenario: 首次创建走完整自审
- **WHEN** 项目无设计基础（首次创建）
- **THEN** SELFREV SHALL 固定执行 10 轮自审

#### Scenario: 非首次创建走弹性自审
- **WHEN** 项目已有设计基础（非首次创建）
- **THEN** SELFREV SHALL 按弹性轮次（下限 1 轮）+ 评分底线执行

### Requirement: 首次/非首次判定信号

系统 SHALL 以 `docs/CONTEXT.md` 存在 且 `docs/designs/detailed-designs/` 非空 判定为「非首次创建（已有设计基础）」，否则判定为「首次创建（无设计基础）」。

#### Scenario: 已有设计基础判定为非首次
- **WHEN** `docs/CONTEXT.md` 存在 且 `docs/designs/detailed-designs/` 非空
- **THEN** 判定为「非首次创建」

#### Scenario: 无设计基础判定为首次
- **WHEN** `docs/CONTEXT.md` 不存在 或 `docs/designs/detailed-designs/` 为空
- **THEN** 判定为「首次创建」

### Requirement: 非首次弹性轮次

非首次创建时，SELFREV 目标轮次 SHALL 由影响范围分数决定，下限 1 轮、上限 10 轮。各阶段影响范围分数：explore = 功能点数 × 1；prototype = 页面数 × 2 + 交互元素数 × 1；design = 功能点数 × 1 + 接口数 × 1.5 + 数据模型数 × 2。轮次映射：分数 1 → 1 轮；分数 2–5 → ceil(分数) 轮；分数 6–15 → max(5, ceil(分数/2)) 轮；分数 >15 → 10 轮。

#### Scenario: 微小变更最少 1 轮
- **WHEN** 非首次创建 且 影响范围分数为 1
- **THEN** 目标轮次为 1 轮

#### Scenario: 小变更线性递增
- **WHEN** 非首次创建 且 影响范围分数为 2–5
- **THEN** 目标轮次 = ceil(分数) 轮

#### Scenario: 较大变更减半递增
- **WHEN** 非首次创建 且 影响范围分数为 6–15
- **THEN** 目标轮次 = max(5, ceil(分数/2)) 轮

#### Scenario: 大变更封顶 10 轮
- **WHEN** 非首次创建 且 影响范围分数 > 15
- **THEN** 目标轮次为 10 轮

### Requirement: 自审评分底线

非首次创建时，SELFREV 每轮 SHALL 输出各维度评分（0–10 量纲），自审通过 SHALL 要求各维度评分均 > 8；任一维度 ≤ 8 SHALL 继续补审，直至各维度均 > 8 或达到 10 轮上限。

#### Scenario: 各维度达标即通过
- **WHEN** 非首次创建 且 本轮各维度评分均 > 8
- **THEN** 自审通过

#### Scenario: 未达标继续补审
- **WHEN** 非首次创建 且 任一维度评分 ≤ 8
- **THEN** 继续补审，直至各维度均 > 8 或达到 10 轮上限
