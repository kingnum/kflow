# functional-structure-tree Specification

## Purpose

定义功能设计阶段 `functional-designs/index.md` 中功能结构树的内容要求，以树状图展示模块→功能点层级，每个节点标注 FP-ID、优先级和简短功能描述，为下游阶段提供直观的功能全景。

## Requirements

### Requirement: 功能结构树替换页面导航结构图

系统 SHALL 在 `functional-designs/index.md` 中以"三、功能结构树"替换原有的"三、页面导航结构图"。

#### Scenario: 章节标题变更

- **WHEN** functional-designs/index.md 的 OUTPUT 步骤生成
- **THEN** "三、页面导航结构图" SHALL 被替换为"三、功能结构树"
- **AND** 保留原有的"四、核心业务流程图"及后续章节不变

#### Scenario: 旧格式不再使用

- **WHEN** functional-designs/index.md 生成
- **THEN** 系统 SHALL NOT 生成仅含页面名的导航结构图（如 `├── {一级菜单1} → ├── {二级菜单1-1} → ├── {页面1-1-1}`）
- **AND** SHALL 使用功能结构树格式替代

### Requirement: 功能结构树层级结构

功能结构树 SHALL 以模块→功能点的两级树状结构展示，每个功能点标注 FP-ID、优先级和简短描述。

#### Scenario: 树状结构格式

- **WHEN** functional-designs/index.md 的功能结构树章节生成
- **THEN** 树状结构 SHALL 使用以下格式：
  ```
  {应用名称}
  ├── 📁 {模块1}（{n}个功能点）
  │   ├── FP-001 {功能名} [P0] — {一句话功能简述}
  │   ├── FP-002 {功能名} [P1] — {一句话功能简述}
  │   └── ...
  ├── 📁 {模块2}（{m}个功能点）
  │   └── ...
  ```
- **AND** 模块使用 `📁` 前缀标识
- **AND** 每个功能点包含 FP-ID、功能名、优先级标记和简述

#### Scenario: 优先级可视化标记

- **WHEN** 功能结构树生成
- **THEN** 优先级 SHALL 使用统一的文本标记格式
- **AND** P0 标记为 `[P0]`、P1 标记为 `[P1]`、P2 标记为 `[P2]`
- **AND** 优先级标记紧跟在功能名之后

#### Scenario: 功能简述要求

- **WHEN** 功能结构树生成
- **THEN** 每个功能点的简述 SHALL 以一句话概括核心行为和价值
- **AND** 简述 SHALL 使用 `— {简述}` 格式，跟在优先级标记之后
- **AND** 简述长度 SHALL 控制在 40 字以内

### Requirement: 模块归类规则

功能点 SHALL 按业务模块归类到树状节点，模块名对应一级菜单或核心业务域。

#### Scenario: 模块划分依据

- **WHEN** 功能点归入模块
- **THEN** 模块划分 SHALL 基于业务域（如"用户管理""内容管理""订单管理""系统设置"）
- **AND** 每个模块标注其包含的功能点数量
- **AND** 无归属模块的功能点 SHALL 归入"其他"

#### Scenario: 模块与菜单对应

- **WHEN** 功能结构树生成
- **THEN** 模块名 SHALL 与应用的菜单结构对齐
- **AND** 一级菜单项对应一个顶层模块节点
- **AND** 模块排列顺序 SHALL 与菜单顺序一致

### Requirement: 功能点关联关系标注

功能结构树 SHALL 在功能点间标注依赖关系类型。

#### Scenario: 依赖关系标注

- **WHEN** 功能结构树生成且功能点间存在关联关系
- **THEN** 依赖关系 SHALL 在功能点简述后标注
- **AND** 前置依赖使用 `（依赖: FP-xxx）`
- **AND** 在每个节点的描述中体现关系
- **AND** 图例 SHALL 标注关系符号含义（`→` 前置依赖、`||` 并行、`⊃` 包含）
