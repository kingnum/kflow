## Requirements

### Requirement: 覆盖追溯矩阵文件

系统 SHALL 在每个变更目录下维护 `docs/changes/{change}/traceability.md` 文件，记录每个功能点在各阶段产物中的覆盖映射。

#### Scenario: 详细设计阶段创建 traceability.md

- **WHEN** 执行 `kflow-design` Skill 且 functional-designs/index.md 中功能点清单已确定
- **THEN** 系统创建 traceability.md 文件
- **AND** 文件中包含基于 FP 清单初始化的覆盖总览表（功能点ID 列已填充，其余列留空）
- **AND** 文件中包含阶段覆盖统计表（各阶段覆盖率初始为 0%）

#### Scenario: 执行阶段完成后填写对应列

- **WHEN** 某个执行阶段（计划/编码/审查/接口单元测试/E2E测试/集成测试）通过 Agent 迭代执行完成
- **THEN** 系统在 traceability.md 覆盖总览表中填写该阶段对应列
- **AND** 更新阶段覆盖统计表中该阶段的覆盖率、状态和更新时间

#### Scenario: 覆盖总览表格式

- **WHEN** traceability.md 被创建或更新
- **THEN** 覆盖总览表 MUST 包含以下列：功能点ID、功能设计(§)、详细设计(§)、接口测试(ID)、E2E测试(ID)、编码实现(SC)、集成测试(ID)
- **AND** 每个功能点占一行
- **AND** 纯后端项目的 E2E测试列标记为 ⏭️

### Requirement: 覆盖率门控检查

系统 SHALL 在每个执行阶段的门控检查中验证 traceability.md 对应列的覆盖率。

#### Scenario: 进入计划阶段前检查设计覆盖率

- **WHEN** 变更级详细设计完成，尝试进入计划阶段
- **THEN** 门控检查 traceability.md 中「功能设计」列覆盖率 = 100%
- **AND** 门控检查 traceability.md 中「详细设计」列覆盖率 = 100%
- **AND** 任一列覆盖率 < 100% 时门控阻塞，输出未覆盖 FP 清单

#### Scenario: 进入 E2E 测试前检查接口测试覆盖率

- **WHEN** 接口单元测试完成，尝试进入 E2E 测试阶段
- **THEN** 门控检查 traceability.md 中「接口测试」列覆盖率 = 100%
- **AND** 覆盖率 < 100% 时门控阻塞

#### Scenario: 进入集成测试前检查所有前置覆盖率

- **WHEN** 所有子变更 E2E 测试完成，尝试进入集成测试
- **THEN** 门控检查 traceability.md 中「编码实现」列覆盖率 = 100%
- **AND** 门控检查「E2E测试」列覆盖率 = 100%（前后端项目）
- **AND** 任一列覆盖率 < 100% 时门控阻塞

#### Scenario: 归档前最终覆盖检查

- **WHEN** 集成测试完成，尝试进入归档阶段
- **THEN** 门控检查 traceability.md 所有适用列覆盖率 = 100%
- **AND** 任一列覆盖率 < 100% 时归档阻塞

### Requirement: 缺口自动发现与追踪

系统 SHALL 在门控检查时自动发现未覆盖的功能点，并记录到 traceability.md 的缺口追踪表。

#### Scenario: 门控检查发现覆盖率缺口

- **WHEN** 门控检查发现某列覆盖率 < 100%
- **THEN** 系统在缺口追踪表中添加记录，包含功能点ID、缺失阶段、发现时间、状态（待补充）
- **AND** 输出缺口清单供用户和子代理参考

#### Scenario: 缺口补充后自动更新状态

- **WHEN** 之前缺失的覆盖被补充
- **THEN** 系统在缺口追踪表中将该记录状态更新为「已补充」
- **AND** 阶段覆盖统计表中对应阶段的覆盖率重新计算

### Requirement: 各阶段独立维护

系统 SHALL 要求各阶段独立填写 traceability.md 对应列，不依赖跨阶段聚合。

#### Scenario: 各阶段仅写入自身列

- **WHEN** 接口单元测试阶段完成
- **THEN** 该阶段的 Agent 迭代子代理仅写入「接口测试」列
- **AND** 不修改其他阶段已填写的列

#### Scenario: 后续阶段不覆盖已有数据

- **WHEN** 某阶段尝试修改已填写的列
- **THEN** 系统保持已有数据不变（除非通过阶段回退流程重置）
