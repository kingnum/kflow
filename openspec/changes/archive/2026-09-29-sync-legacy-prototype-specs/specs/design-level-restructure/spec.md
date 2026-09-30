## MODIFIED Requirements

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
- **AND** 禁止直接修改产品级 `docs/designs/prototypes/` 中的 UI 设计，UI 布局问题须经 kflow-prototype-design 的 REVISION 模式回退处理
- **AND** 如发现上游设计问题，记录 skill-suggestion 并提示回退
