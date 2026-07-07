## ADDED Requirements

### Requirement: E2E 测试用例标注页面数据来源

每个 E2E 测试用例 SHALL 标注用例执行过程中页面元素的数据来源，区分后端 API 数据、前端静态数据、配置控制数据。

#### Scenario: 页面数据来源表

- **WHEN** e2e-tests/part-NN.md 中定义测试场景
- **THEN** 每个测试场景 SHALL 包含"页面数据来源表"
- **AND** 表格 SHALL 包含：页面元素描述、数据字段、数据来源类型（后端API/前端静态/配置控制）、来源接口/文件、依赖配置项

#### Scenario: 后端 API 数据标注

- **WHEN** 页面元素的数据来自后端 API 响应
- **THEN** 数据来源 SHALL 标注为"后端API"
- **AND** SHALL 标注具体的接口路径（如 `GET /api/users?page=1&size=20`）
- **AND** SHALL 标注数据在响应中的字段路径（如 `data[].username`）

#### Scenario: 前端静态数据标注

- **WHEN** 页面元素的数据来自前端静态定义（常量、枚举映射等）
- **THEN** 数据来源 SHALL 标注为"前端静态"
- **AND** SHALL 标注来源文件路径（如 `constants.ts: ROLE_COLORS`）

#### Scenario: 配置控制数据标注

- **WHEN** 页面元素的数据或行为受配置项控制
- **THEN** 数据来源 SHALL 标注为"配置控制"
- **AND** SHALL 标注依赖的配置项名称

### Requirement: E2E 测试用例包含配置项变更影响矩阵

每个 E2E 测试用例 SHALL 包含配置项变更影响矩阵，明确配置项调整后哪些功能和数据显示会发生变化。

#### Scenario: 配置项变更影响矩阵格式

- **WHEN** e2e-tests/part-NN.md 中定义测试场景
- **THEN** 每个测试场景 SHALL 包含"配置项变更影响矩阵"
- **AND** 矩阵 SHALL 包含：配置项、变更前值、变更后值、受影响功能、受影响页面元素、验证方式

#### Scenario: 配置变更的 E2E 验证方式

- **WHEN** 定义配置项变更的验证方式
- **THEN** 验证方式 SHALL 从以下方式中选择：DOM 验证（具体选择器+预期结果）、API 响应验证（接口路径+预期字段值）、行为验证（操作后预期行为变化）
- **AND** 每个配置变更 SHALL 至少有一个可执行的验证方式

#### Scenario: 测试场景无关联配置项

- **WHEN** 测试场景不涉及任何配置项
- **THEN** "配置项变更影响矩阵"章节 SHALL 标注"本测试场景无关联配置项"
- **AND** SHALL NOT 省略该章节
