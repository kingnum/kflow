# subchange-input-source Delta Spec

## MODIFIED Requirements

### Requirement: 子变更类型严格二分

系统 SHALL 将子变更类型限定为「后端子变更」或「前端子变更」，禁止创建前后端混合子变更。子变更类型 SHALL 由 design 阶段 DIVIDE 步骤基于包含的 FP 类型自动校验。

#### Scenario: 后端子变更判定

- **WHEN** 子变更包含的全部功能点类型均为「后端」（依据 functional-designs/index.md FP 类型列）
- **THEN** 系统 SHALL 自动标记该子变更为「后端子变更」
- **AND** SHALL NOT 包含类型为「前端」的 FP

#### Scenario: 前端子变更判定

- **WHEN** 子变更包含的全部功能点类型均为「前端」（依据 functional-designs/index.md FP 类型列）
- **THEN** 系统 SHALL 自动标记该子变更为「前端子变更」
- **AND** SHALL NOT 包含类型为「后端」的 FP

#### Scenario: 混合子变更拒绝

- **WHEN** 子变更同时包含类型为「后端」和「前端」的 FP
- **THEN** 系统 SHALL 拒绝此划分
- **AND** 提示将后端 FP 和前端 FP 拆分到两个独立子变更
- **AND** 子变更类型 SHALL NOT 由人工手动填写，SHALL 由系统自动推断

## ADDED Requirements

### Requirement: 共享类型目录作为条件产物

系统 SHALL 在 design 阶段产出共享类型定义到 `changes/{change}/shared-types/` 目录，作为条件产物（🔶）。

#### Scenario: 共享类型目录创建

- **WHEN** design 阶段完成接口设计且存在前后端子变更共同消费的 DTO/interface
- **THEN** 系统 SHALL 创建 changes/{change}/shared-types/ 目录
- **AND** SHALL 产出前后端各自语言的类型定义文件
- **AND** 后端子变更 plan 阶段输入增加 shared-types/ 目录（🔶 条件）

#### Scenario: 无共享类型时跳过

- **WHEN** 变更不存在跨子变更共享的类型定义（纯后端或前后端无共同 DTO）
- **THEN** shared-types/ 目录 SHALL NOT 被创建
- **AND** 缺失不阻塞门控

#### Scenario: 前端子变更输入源增加 shared-types

- **WHEN** shared-types/ 目录存在
- **THEN** 前端子变更 plan 阶段 SHALL 将 shared-types/ 作为输入源（🔶 条件）
- **AND** 前端编码 SHALL 基于 shared-types/ 中的类型定义编写 mock 数据
