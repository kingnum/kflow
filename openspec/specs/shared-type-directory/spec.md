# shared-type-directory Specification

## Purpose

定义 `changes/{change}/shared-types/` 目录的创建、更新、引用规范。该目录作为条件产物（🔶），存放前后端子变更共同消费的 DTO/interface 类型定义。

## ADDED Requirements

### Requirement: 共享类型目录创建

design 阶段 SHALL 在完成接口设计且存在前后端子变更共同消费的 DTO/interface 时创建 `changes/{change}/shared-types/` 目录。

#### Scenario: 创建共享类型目录

- **WHEN** design 阶段完成接口设计
- **AND** 存在前后端子变更共同消费的 DTO/interface
- **THEN** 系统 SHALL 创建 `changes/{change}/shared-types/` 目录
- **AND** 目录内 SHALL 包含 `README.md` 描述类型清单和文件规范
- **AND** SHALL 产出后端语言和前端语言各自可用的类型定义文件

#### Scenario: 无共享类型时跳过

- **WHEN** 变更不存在跨子变更共享的类型定义（纯后端或前后端无共同 DTO）
- **THEN** `shared-types/` 目录 SHALL NOT 被创建
- **AND** 缺失不阻塞任何阶段门控

### Requirement: 共享类型文件格式

shared-types/ 目录中的类型定义文件 SHALL 为各目标语言的原生格式。

#### Scenario: 后端语言类型文件

- **WHEN** 后端子变更的目标语言为 TypeScript/Go/Java/Python/Rust 等
- **THEN** 系统 SHALL 产出对应语言格式的类型定义文件
- **AND** 类型定义 SHALL 包含字段名、类型、可选性标注

#### Scenario: 前端语言类型文件

- **WHEN** 前端子变更的目标语言为 TypeScript
- **THEN** 系统 SHALL 产出 TypeScript 类型定义文件
- **AND** 类型定义 SHALL 与后端语义一致（字段名和类型对应关系可追溯）

### Requirement: 共享类型作为 plan 阶段输入

后端子变更和前端子变更的 plan 阶段 SHALL 将 `shared-types/` 目录作为条件输入（🔶）。

#### Scenario: 后端子变更引用共享类型

- **WHEN** `shared-types/` 目录存在
- **AND** 后端子变更进入 plan 阶段
- **THEN** `shared-types/` SHALL 作为 🔶 条件输入
- **AND** tasks.md SHALL 包含「引用共享类型」任务项

#### Scenario: 前端子变更引用共享类型

- **WHEN** `shared-types/` 目录存在
- **AND** 前端子变更进入 plan 阶段
- **THEN** `shared-types/` SHALL 作为 🔶 条件输入
- **AND** 前端编码 SHALL 基于 `shared-types/` 中的类型定义编写 mock 数据

#### Scenario: 无共享类型目录时跳过

- **WHEN** `shared-types/` 目录不存在
- **THEN** plan 阶段 SHALL NOT 将其列为输入
- **AND** 不阻塞门控

### Requirement: 共享类型与子变更类型边界

shared-types/ 目录 SHALL 由变更级 agent 管理，不归属于任何子变更。

#### Scenario: 共享类型不属于子变更域

- **WHEN** 存在共享类型定义
- **THEN** 类型定义 SHALL 存放在变更级 `shared-types/` 目录
- **AND** SHALL NOT 存放在任何子变更的源码目录中
- **AND** SHALL NOT 被任何单独的子变更「拥有」

#### Scenario: 共享类型更新

- **WHEN** 接口契约变更导致共享类型需要更新
- **THEN** 变更级 agent SHALL 同步更新 `shared-types/` 中的两种语言文件
- **AND** SHALL 通知消费该类型的子变更
