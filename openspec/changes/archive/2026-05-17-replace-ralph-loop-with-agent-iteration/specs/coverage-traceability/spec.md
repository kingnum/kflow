## MODIFIED Requirements

### Requirement: 执行阶段完成后填写对应列

- **WHEN** 某个执行阶段（计划/编码/审查/接口单元测试/E2E测试/集成测试）通过 Agent 迭代执行完成
- **THEN** 系统在 traceability.md 覆盖总览表中填写该阶段对应列
- **AND** 更新阶段覆盖统计表中该阶段的覆盖率、状态和更新时间

### Requirement: 各阶段独立维护

系统 SHALL 要求各阶段独立填写 traceability.md 对应列，不依赖跨阶段聚合。

#### Scenario: 各阶段仅写入自身列

- **WHEN** 接口单元测试阶段完成
- **THEN** 该阶段的 Agent 迭代子代理仅写入「接口测试」列
- **AND** 不修改其他阶段已填写的列

#### Scenario: 后续阶段不覆盖已有数据

- **WHEN** 某阶段尝试修改已填写的列
- **THEN** 系统保持已有数据不变（除非通过阶段回退流程重置）
