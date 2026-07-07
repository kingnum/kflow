# shared-concern-ownership Specification

## Purpose

定义跨层共享关切（错误码、配置项、共享 DTO、Schema 变更与 UI 影响）的默认归属规则和跨子变更引用格式。

## Requirements

### Requirement: 错误码归属于后端子变更

错误码的定义与后端处理逻辑 SHALL 归属到后端子变更。错误码对应的用户可见提示文案由消费该接口的前端子变更定义。

#### Scenario: 错误码定义归属

- **WHEN** design 阶段定义统一错误码表
- **THEN** 错误码定义（错误码/错误场景/后端处理方式）SHALL 归属到包含该接口的后端子变更
- **AND** 后端子变更的 detailed-design.md 中 SHALL 包含完整的错误码定义

#### Scenario: 错误码提示文案归属

- **WHEN** 错误码需要前端展示用户提示
- **THEN** 「用户提示」列内容 SHALL 作为 API 契约的一部分传递给前端子变更
- **AND** 前端子变更 SHALL 在编码阶段实现错误码到提示文案的映射
- **AND** 错误码映射的实现 SHALL 属于前端功能点

### Requirement: 配置项归属于后端子变更

配置项的定义（含默认值、环境区分）SHALL 归属到后端子变更。前端通过 API 获取配置值。

#### Scenario: 配置项定义归属

- **WHEN** design 阶段定义配置项
- **THEN** 配置项定义 SHALL 归属到包含该配置相关功能的后端子变更
- **AND** 若配置项影响多个后端子变更，SHALL 归属到最先实现的后端子变更
- **AND** 后端 FP 的 functional-designs/ 中 SHALL 标注关联配置项

#### Scenario: 配置项前端消费

- **WHEN** 前端需要读取配置值
- **THEN** 前端 SHALL 通过配置 API 获取（由后端子变更提供接口）
- **AND** 前端 SHALL NOT 直接定义或硬编码配置项默认值
- **AND** 前端功能点的「关联配置项」中 SHALL 标注「通过 API 获取」

### Requirement: 共享 DTO 由变更级统一管理

共享 DTO/interface 类型定义（前后端共同消费的数据结构）SHALL 由 design 阶段统一产出到 `changes/{change}/shared-types/` 目录，不归属任一子变更。

#### Scenario: 共享类型产出时机

- **WHEN** design 阶段完成接口设计
- **AND** 存在前后端子变更共同消费的 DTO/interface
- **THEN** 系统 SHALL 在 changes/{change}/shared-types/ 目录下产出共享类型文件
- **AND** 产出时机 SHALL 在子变更编码开始之前
- **AND** 产出格式 SHALL 包含 TypeScript 类型定义（供前端消费）和对应后端语言的类型定义（如 Java POJO / Go struct）

#### Scenario: 共享类型引用

- **WHEN** 前后端子变更引用共享 DTO
- **THEN** 后端子变更 SHALL 引用 shared-types/ 中的定义作为接口实现依据
- **AND** 前端子变更 SHALL 引用 shared-types/ 中的 TypeScript 类型作为 mock 数据和 API 对接依据
- **AND** SHALL NOT 在子变更内重复定义相同的类型

#### Scenario: 无共享类型时跳过

- **WHEN** 变更中不存在前后端子变更共同消费的 DTO（如纯后端项目或前端不消费该变更的接口）
- **THEN** shared-types/ 目录 SHALL NOT 被创建
- **AND** shared-types/ 作为条件产物（🔶），缺失不阻塞门控

### Requirement: Schema 变更归属后端子变更，UI 影响链由关联标注追踪

数据库 Schema 变更 SHALL 归属到后端子变更。Schema 变更导致的前端展示/表单变更 SHALL 通过 FP 关联关系标注追踪。

#### Scenario: Schema 变更归属

- **WHEN** 变更涉及数据库表结构变更
- **THEN** Schema 变更的 FP SHALL 标记为「后端」
- **AND** SHALL 归属到包含该数据模型的后端子变更

#### Scenario: Schema→UI 影响链追踪

- **WHEN** Schema 变更会影响前端展示或表单字段
- **THEN** 后端的 Schema 变更 FP SHALL 在「关联功能点」列标注受影响的前端 FP-ID
- **AND** 前端响应 FP SHALL 在「依赖功能点」列标注对应的 Schema 变更 FP-ID
- **AND** 关联关系类型 SHALL 标注为「数据模型变更」
