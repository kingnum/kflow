## Requirements

### Requirement: 详细设计包含 NFR 章节

系统 SHALL 在详细设计文档（design.md）中包含非功能需求（NFR）章节。

#### Scenario: NFR 章节结构
- **WHEN** 详细设计文档生成
- **THEN** design.md 包含 NFR 章节，下设性能需求、安全需求、可用性需求、可维护性需求四个子节
- **AND** 每项 NFR 包含目标值、测量方法、验证阶段

#### Scenario: NFR 最小要求
- **WHEN** 编码阶段门控检查
- **THEN** design.md 的 NFR 章节必须包含至少 1 项性能需求和 1 项安全需求
- **AND** 不满足时 ❌ 阻塞编码阶段

#### Scenario: 功能缺陷级 NFR 简化
- **WHEN** 变更类型为功能缺陷级
- **THEN** NFR 章节可简化（仅包含安全需求，如缺陷涉及安全）

### Requirement: NFR 级联到测试用例

系统 SHALL 将 NFR 中的可测量需求级联到测试用例文档中。

#### Scenario: 性能需求生成测试用例
- **WHEN** design.md 中定义了性能需求（如"接口响应时间 P95 < 200ms"）
- **THEN** api-tests.md 自动包含性能验证用例
- **AND** 用例包含被测接口、并发数、目标响应时间、验证方式

#### Scenario: 安全需求在代码审查中验证
- **WHEN** design.md 中定义了安全需求（如"使用参数化查询防SQL注入"）
- **THEN** 代码审查 Agent 将安全需求作为检查项
- **AND** 不满足时标记为高严重度问题
