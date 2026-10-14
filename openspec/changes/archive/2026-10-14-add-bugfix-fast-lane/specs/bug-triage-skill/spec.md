# Spec Delta

## MODIFIED Requirements

### Requirement: 诊断结果路由

系统 SHALL 根据四层诊断结果将问题路由到对应的问题源头阶段进行处理。路由输出 SHALL 包含执行模式声明。L4 结论 SHALL 路由至缺陷修复快车道。

#### Scenario: L1 需求问题路由

- **WHEN** 诊断确定问题源头为 L1 需求定义
- **THEN** 系统 SHALL 回退到 explore 阶段的 REVISION 模式
- **AND** 标记后续所有阶段状态为 ⏳ 待开始
- **AND** 将问题登记信息和影响范围评估传递给 explore
- **AND** 路由输出 SHALL 包含 EXECUTION_MODE = SUBAGENT_REQUIRED 声明

#### Scenario: L2 原型问题路由

- **WHEN** 诊断确定问题源头为 L2 原型设计
- **THEN** 系统 SHALL 回退到 prototype-design 阶段的 REVISION 模式
- **AND** 标记 design、plan、code、test 等后续阶段状态为 ⏳ 待开始
- **AND** 将问题登记信息和影响范围评估传递给 prototype-design
- **AND** 路由输出 SHALL 包含 EXECUTION_MODE = SUBAGENT_REQUIRED 声明

#### Scenario: L3 设计问题路由

- **WHEN** 诊断确定问题源头为 L3 详细设计
- **THEN** 系统 SHALL 回退到 design 阶段的 REVISION 模式
- **AND** 标记 plan、code、test 等后续阶段状态为 ⏳ 待开始
- **AND** 将问题登记信息和影响范围评估传递给 design
- **AND** 路由输出 SHALL 包含 EXECUTION_MODE = SUBAGENT_REQUIRED 声明

#### Scenario: L4 实现问题路由

- **WHEN** 诊断确定问题源头为 L4 实现执行
- **THEN** 系统 SHALL 将该缺陷路由至缺陷修复快车道（见 `bugfix-fast-lane` 能力）
- **AND** SHALL 为该缺陷创建缺陷级状态文件 `bugfix-status.md`
- **AND** 将诊断报告中的问题描述、证据与影响范围评估（受影响项清单）写入状态文件
- **AND** 路由输出 SHALL 声明快车道入口与受影响项清单
- **AND** 路由输出 SHALL 包含 EXECUTION_MODE = SUBAGENT_REQUIRED 声明
- **AND** SHALL NOT 修改变更级 `.status.md` 的阶段状态矩阵字段

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
  - bugs/bug-NNN-NNN.md 新增或更新（问题详情，含影响范围评估节和修复记录占位节）
  - 诊断报告（含四层判断过程和影响范围评估）
  - 结论为 L4 时 SHALL 一并创建缺陷级状态文件 `bugfix-status.md` 并写入受影响项清单
- **AND** 问题详情 SHALL 按以下顺序包含必填节：基本信息、问题描述、诊断结果、影响范围评估、解决方案（含执行模式声明）、处理状态、修复记录（占位）、关联
- **AND** SHALL NOT 省略任何必填节

#### Scenario: Skill 不执行修复

- **WHEN** kflow-bug-triage 完成路由决策
- **THEN** triage SHALL NOT 修改任何代码、测试、设计文档
- **AND** 所有修复动作 SHALL 委托给下游 Skill（explore REVISION / prototype-design REVISION / design REVISION / 缺陷修复快车道）

#### Scenario: Skill 与其他 Skill 的关系

- **WHEN** 定义 kflow-bug-triage 在 Skill 体系中的位置
- **THEN** 输入来自用户反馈（经 kflow-guide 路由）
- **AND** 输出给 kflow-explore REVISION（L1 路由）
- **AND** 输出给 kflow-prototype-design REVISION（L2 路由）
- **AND** 输出给 kflow-design REVISION（L3 路由）
- **AND** 输出给缺陷修复快车道（L4 路由，由 `kflow-bug-fix` 的快车道模式承载）
