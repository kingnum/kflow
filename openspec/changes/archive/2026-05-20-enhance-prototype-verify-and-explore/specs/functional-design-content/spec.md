# functional-design-content Delta Specification

## MODIFIED Requirements

### Requirement: 功能点包含页面导航信息

每个功能点 SHALL 标注其所属页面和菜单路径。

#### Scenario: 功能点标注页面归属

- **WHEN** functional-designs/ 中定义功能点
- **THEN** 每个功能点包含"所属页面"字段
- **AND** 包含"菜单路径"字段（如适用）
- **AND** 页面和菜单使用用户可见的名称

#### Scenario: 多级菜单结构描述

- **WHEN** 应用包含多级菜单
- **THEN** functional-designs/index.md 包含"三、功能结构树"
- **AND** 以树状图展示模块→功能点层级，每个节点标注 FP-ID、功能名、优先级（[P0]/[P1]/[P2]）和一句话功能简述
- **AND** 明确每个功能点的模块归属

## ADDED Requirements

### Requirement: 功能结构树内容要求

functional-designs/index.md 中的"三、功能结构树" SHALL 以模块→功能点的两级树状结构展示，替代原有的"三、页面导航结构图"。

#### Scenario: 树状结构格式

- **WHEN** functional-designs/index.md 生成功能结构树
- **THEN** 树状结构 SHALL 以应用名称为根节点
- **AND** 一级节点为业务模块（以 `📁` 前缀标识，标注功能点数量）
- **AND** 二级节点为功能点（标注 FP-ID、功能名、优先级 [P0]/[P1]/[P2]、一句话简述）
- **AND** 模块划分 SHALL 基于业务域，与菜单结构对齐

#### Scenario: 功能简述规范

- **WHEN** 功能结构树中描述功能点
- **THEN** 每个功能点 SHALL 使用 `— {一句话简述}` 格式
- **AND** 简述 SHALL 概括核心行为和价值
- **AND** 简述长度 SHALL 控制在 40 字以内
- **AND** 存在依赖关系时 SHALL 在简述后标注（如"依赖: FP-xxx"）

#### Scenario: 与下游阶段的对接

- **WHEN** 功能结构树生成完成
- **THEN** 原型设计阶段 SHALL 以功能结构树为页面/功能全景参考
- **AND** 详细设计阶段 SHALL 以功能结构树的模块划分为技术设计分组依据
- **AND** 功能结构树 SHALL 与功能点清单表格（第二章）保持一一对应
