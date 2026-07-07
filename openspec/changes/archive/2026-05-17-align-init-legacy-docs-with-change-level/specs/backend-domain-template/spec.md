## ADDED Requirements

### Requirement: 纯后端项目功能设计简化模板

系统 SHALL 为纯后端项目提供独立的功能设计简化模板 `backend-domain.md`，按设计域组织，去除 UX 密集型章节。

#### Scenario: 纯后端项目使用简化模板

- **WHEN** 项目类型为纯后端项目
- **AND** kflow-init LEGACY 或 kflow-explore 需要产出功能设计文档
- **THEN** 系统使用 `backend-domain.md` 模板
- **AND** 文件位于 `docs/designs/functional-designs/{domain}.md`（产品级）或变更级对应目录

#### Scenario: 简化模板保留章节

- **WHEN** `backend-domain.md` 模板被使用
- **THEN** 模板保留以下章节：功能点ID/名称/优先级、用户故事（API 消费者视角）、可执行操作（API 操作/服务调用）、业务规则、业务流程上下文（服务调用链视角）、功能行为矩阵
- **AND** 保留修订记录章节

### Requirement: 纯后端章节替换规则

纯后端模板 SHALL 将 UX 密集型章节替换为后端特有章节。

#### Scenario: 页面与菜单 → 设计域

- **WHEN** 纯后端模板定义功能点归属
- **THEN** "所属页面与菜单"章节替换为"所属设计域"
- **AND** 设计域从 L2 目录扫描提取（如 controllers 域、services 域、models 域）

#### Scenario: 表单项定义 → 接口参数定义

- **WHEN** 纯后端模板定义输入定义
- **THEN** "表单项定义"章节替换为"接口参数定义"
- **AND** 参数定义包含：参数名、位置（query/body/path）、类型、必填、校验规则、默认值

#### Scenario: 交互约束 → 调用约束

- **WHEN** 纯后端模板定义约束条件
- **THEN** "交互约束"章节替换为"调用约束"
- **AND** 约束类型包含：限流约束、权限约束、超时约束、幂等约束
