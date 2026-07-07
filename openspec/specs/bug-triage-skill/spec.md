## Purpose

Define the kflow-bug-triage Skill — an independent diagnostic Skill that performs four-layer root cause tracing (L1 Requirements → L2 Prototype → L3 Detailed Design → L4 Implementation) for user-reported issues, registers issues in `bugs/` directory, and routes to the correct REVISION mode or kflow-bug-fix.

## Requirements

### Requirement: 四层溯源诊断流程

系统 SHALL 提供独立的四层溯源诊断 Skill（kflow-bug-triage），接收用户反馈后从最上游逐层排查问题源头，确定源头阶段后路由到对应的修复流程。诊断完成后 SHALL 一并执行影响范围评估。

#### Scenario: 完整四层诊断
- **WHEN** 用户通过 kflow-bug-triage 反馈问题
- **THEN** 系统按以下顺序逐层诊断：
  - L1 需求定义：检查 functional-designs/ 是否覆盖用户期望的行为、是否存在歧义或遗漏
  - L2 原型设计：检查 prototype/ 是否正确实现了 L1 确认的功能点
  - L3 详细设计：检查 detailed-design.md 中的接口/数据模型/状态流转是否与上游一致
  - L4 实现执行：检查代码是否正确实现了 detailed-design.md 的定义
- **AND** 每层 SHALL 输出判断结论（✅ 通过 / ❌ 有缺陷）和证据
- **AND** 当某层判定为 ❌ 时 SHALL 停止向下排查，将该层确定为问题源头
- **AND** 诊断完成后 SHALL 执行影响范围评估

#### Scenario: 快速排除
- **WHEN** 某层有明确证据表明问题不在该层
- **THEN** 系统 SHALL 跳过该层的详细检查，直接进入下一层
- **AND** 在诊断报告中标注快速排除的理由

#### Scenario: 诊断证据来源
- **WHEN** 系统执行某层诊断
- **THEN** SHALL 使用以下证据来源：
  - L1：functional-designs/index.md + functional-designs/part-NN.md + CONTEXT.md
  - L2：prototype/index.html + element-coverage-tree.md + functional-designs/
  - L3：detailed-design.md + api-tests/index.md + functional-designs/
  - L4：代码实现 + detailed-design.md

#### Scenario: 影响范围评估作为诊断的一部分
- **WHEN** 四层诊断完成
- **THEN** 系统 SHALL 执行影响范围评估（参见 triage-impact-assessment capability）
- **AND** 评估结果 SHALL 写入问题详情文件的影响范围评估节

### Requirement: 诊断结果路由

系统 SHALL 根据四层诊断结果将问题路由到对应的问题源头阶段进行处理。路由输出 SHALL 包含执行模式声明。

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
- **THEN** 系统 SHALL 调用 kflow-bug-fix 执行修复
- **AND** 将诊断报告中的问题描述、证据和影响范围评估传递给 bug-fix 作为输入
- **AND** bug-fix 使用二分法（实现错误/测试错误）进行分类和修复
- **AND** 路由输出 SHALL 包含 EXECUTION_MODE = SUBAGENT_REQUIRED 声明

### Requirement: 用户确认路由

系统 SHALL 在诊断完成后、执行路由前获取用户确认。

#### Scenario: 展示诊断结果并等待确认
- **WHEN** 四层诊断完成且问题登记写入 bugs/ 目录
- **THEN** 系统 SHALL 通过 AskUserQuestion 向用户展示：
  - 诊断结论（问题源头层级）
  - 各层判断依据和证据摘要
  - 影响范围评估结果
  - 建议的路由目标和解决方案
- **AND** 用户 SHALL 有三个选项：确认执行路由 / 覆盖诊断结论 / 暂不处理
- **AND** 用户确认前 SHALL NOT 执行任何路由动作

#### Scenario: 用户覆盖诊断结论
- **WHEN** 用户选择覆盖诊断结论
- **THEN** 系统 SHALL 询问用户指定的源头层级
- **AND** 按用户指定的层级执行路由
- **AND** 在问题登记文件中记录覆盖原因

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
- **AND** 问题详情 SHALL 按以下顺序包含必填节：基本信息、问题描述、诊断结果、影响范围评估、解决方案（含执行模式声明）、处理状态、修复记录（占位）、关联
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
