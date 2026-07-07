## MODIFIED Requirements

### Requirement: 详细设计在变更级执行

系统 SHALL 将详细设计阶段（kflow-design）从子变更级提升到变更级，在设计探索完成后、子变更划分前执行。当 FP > 20 时，输出 `detailed-design/` 目录结构；FP ≤ 20 时，输出单一 `detailed-design.md` 文件。

#### Scenario: 变更级统一设计（目录结构）
- **WHEN** 设计探索阶段完成且 FP > 20
- **THEN** 系统在变更级执行详细设计
- **AND** 输出 `detailed-design/` 目录（index.md + architecture.md + domains/*.md + nfr.md + config-and-errors.md + subchange-division.md）
- **AND** 子变更划分在详细设计完成后基于完整设计认知执行

#### Scenario: 变更级统一设计（单文件）
- **WHEN** 设计探索阶段完成且 FP ≤ 20
- **THEN** 系统在变更级执行详细设计
- **AND** 输出单一 `detailed-design.md` 文件（含所有功能点设计）
- **AND** 子变更划分在详细设计完成后基于完整设计认知执行

#### Scenario: 功能缺陷级走简化流程
- **WHEN** 变更类型为功能缺陷级
- **THEN** detailed-design.md 简化输出（仅包含受影响的功能点设计）
- **AND** 子变更划分可跳过（单变更内直接编码）

### Requirement: design 阶段边界明确化

系统 SHALL 将 kflow-design 限定为技术视角的详细设计。

#### Scenario: design 域内内容
- **WHEN** kflow-design 输出详细设计
- **THEN** 内容聚焦系统架构、数据模型、接口设计、NFR、子变更划分
- **AND** 包含 api-tests/ 和 e2e-tests/ 测试用例文档
- **AND** 包含功能点复杂度评估（低/中/高）和复杂度分布表
- **AND** 高复杂度 FP 在子变更划分前逐项与用户确认

#### Scenario: design 域外约束
- **WHEN** kflow-design 执行技术设计
- **THEN** 禁止修改 functional-designs/ 中的功能定义
- **AND** 禁止修改 prototype/ 中的 UI 设计
- **AND** 如发现上游设计问题，记录 skill-suggestion 并提示回退
