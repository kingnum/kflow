## MODIFIED Requirements

### Requirement: 严重度分级

系统 SHALL 对登记的问题进行三级严重度分级，严重度作为独立字段，不编码到 BUG-ID 中。

#### Scenario: 严重度定义
- **WHEN** 系统登记问题
- **THEN** SHALL 按以下标准分级：
  - 🔴 阻塞：问题导致功能无法正常使用或核心流程中断
  - 🟡 警告：功能可用但存在明显异常或体验问题
  - 🔵 建议：非功能性问题，如性能优化、代码风格改进
- **AND** 严重度 SHALL 作为独立字段记录（`🔴 阻塞`、`🟡 警告`、`🔵 建议`）
- **AND** SHALL NOT 使用 `B-`/`W-`/`S-` 前缀作为 BUG-ID 的一部分

#### Scenario: 严重度影响路由
- **WHEN** 问题严重度为 🔴 阻塞
- **THEN** 路由 SHALL 立即执行（不阻塞在后续流程节点）
- **AND** 未关闭的 🔴 阻塞问题 SHALL 阻断 kflow-archive 归档

### Requirement: kflow-bug-triage Skill 定义

系统 SHALL 将 kflow-bug-triage 实现为独立诊断 Skill（非流程阶段）。

#### Scenario: Skill 触发方式
- **WHEN** 用户通过 kflow-guide 反馈问题（关键词匹配：反馈/报告问题/报bug/提bug）
- **THEN** guide SHALL 路由到 kflow-bug-triage
- **AND** triage 加载当前活跃变更的上下文

#### Scenario: Skill 输入要求
- **WHEN** kflow-bug-triage 执行
- **THEN** 输入 SHALL 包含：
  - .status.md（必须）—— 获取当前变更状态
  - 变更目录 docs/changes/{change}/（必须）—— 获取所有阶段产物
  - 用户的问题描述（必须）—— 自然语言描述

#### Scenario: Skill 输出产物
- **WHEN** kflow-bug-triage 完成诊断
- **THEN** 输出 SHALL 包含：
  - bugs/index.md 更新（新增问题条目）
  - bugs/bug-NNN-NNN.md 新增或更新（问题详情，含修复记录占位节）
  - 诊断报告（含四层判断过程）
- **AND** 问题详情 SHALL 按以下顺序包含必填节：基本信息、问题描述、诊断结果、解决方案、处理状态、修复记录（占位）、关联
- **AND** SHALL NOT 省略任何必填节

#### Scenario: Skill 不执行修复
- **WHEN** kflow-bug-triage 完成路由决策
- **THEN** triage SHALL NOT 修改任何代码、测试、设计文档
- **AND** 所有修复动作 SHALL 委托给下游 Skill（explore REVISION / prototype-design REVISION / design REVISION / bug-fix）

#### Scenario: Skill 与其他 Skill 的关系
- **WHEN** 定义 kflow-bug-triage 在 Skill 体系中的位置
- **THEN** 输入来自用户反馈（经 kflow-guide 路由）
- **AND** 输出给 kflow-explore REVISION（L1 路由）
- **AND** 输出给 kflow-prototype-design REVISION（L2 路由）
- **AND** 输出给 kflow-design REVISION（L3 路由）
- **AND** 输出给 kflow-bug-fix（L4 路由）
