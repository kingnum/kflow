## Purpose

Define the kflow-bug-triage Skill — an independent diagnostic Skill that performs four-layer root cause tracing (L1 Requirements → L2 Prototype → L3 Detailed Design → L4 Implementation) for user-reported issues, registers issues in `bugs/` directory, and routes to the correct REVISION mode or kflow-bug-fix.

## Requirements

### Requirement: 四层溯源诊断流程

系统 SHALL 提供独立的四层溯源诊断 Skill（kflow-bug-triage），接收用户反馈后从最上游逐层排查问题源头，确定源头阶段后路由到对应的修复流程。诊断 SHALL 在项目级与变更级两种工作区均可执行，诊断完成后 SHALL 一并执行影响范围评估。

#### Scenario: 完整四层诊断

- **WHEN** 用户通过 kflow-bug-triage 反馈问题
- **THEN** 系统按以下顺序逐层诊断：
  - L1 需求定义：检查功能设计是否覆盖用户期望的行为、是否存在歧义或遗漏
  - L2 原型设计：检查产品级 `docs/designs/prototypes/` 是否正确实现了 L1 确认的功能点
  - L3 详细设计：检查详细设计中的接口/数据模型/状态流转是否与上游一致
  - L4 实现执行：检查代码是否正确实现了详细设计的定义
- **AND** 每层 SHALL 输出判断结论（✅ 通过 / ❌ 有缺陷）和证据
- **AND** 当某层判定为 ❌ 时 SHALL 停止向下排查，将该层确定为问题源头
- **AND** 诊断完成后 SHALL 执行影响范围评估

#### Scenario: 快速排除

- **WHEN** 某层有明确证据表明问题不在该层
- **THEN** 系统 SHALL 跳过该层的详细检查，直接进入下一层
- **AND** 在诊断报告中标注快速排除的理由

#### Scenario: 诊断证据来源

- **WHEN** 系统执行某层诊断 且 存在活跃变更
- **THEN** SHALL 使用以下证据来源：
  - L1：变更级 `functional-designs/index.md` + `functional-designs/part-NN.md` + `CONTEXT.md`
  - L2：`docs/designs/prototypes/index.html` + 变更级 `prototype-changes.md` + 变更级 `element-coverage-tree.md` + `functional-designs/`
  - L3：变更级 `detailed-design.md` + `api-tests/index.md` + `functional-designs/`
  - L4：代码实现 + 变更级 `detailed-design.md`

#### Scenario: 诊断证据来源（无活跃变更）

- **WHEN** 系统执行某层诊断 且 不存在活跃变更
- **THEN** SHALL 使用产品级设计产物作为证据来源：
  - L1：`docs/designs/functional-designs/`
  - L2：`docs/designs/prototypes/`
  - L3：`docs/designs/detailed-designs/`
  - L4：代码实现 + `docs/designs/detailed-designs/`
- **AND** 产品级设计产物缺失时 SHALL 在诊断报告中标注“该层无法评估”
- **AND** 无法评估的层级 SHALL NOT 被直接判定为通过

#### Scenario: 影响范围评估作为诊断的一部分

- **WHEN** 四层诊断完成
- **THEN** 系统 SHALL 执行影响范围评估（参见 triage-impact-assessment capability）
- **AND** 评估结果 SHALL 写入问题详情文件的影响范围评估节

### Requirement: 诊断结果路由

系统 SHALL 根据四层诊断结果将问题路由到对应的问题源头阶段进行处理。路由输出 SHALL 包含执行模式声明与缺陷工作区声明。L4 结论 SHALL 路由至缺陷修复快车道；L1/L2/L3 结论需要修改设计产物时 SHALL 创建变更或路由到已有变更的 REVISION 模式。

#### Scenario: L1 需求问题路由

- **WHEN** 诊断确定问题源头为 L1 需求定义 且 存在活跃变更
- **THEN** 系统 SHALL 回退到该变更的 explore 阶段 REVISION 模式
- **AND** 标记后续所有阶段状态为 ⏳ 待开始
- **AND** 将问题登记信息和影响范围评估传递给 explore
- **AND** 路由输出 SHALL 包含 EXECUTION_MODE = SUBAGENT_REQUIRED 声明

#### Scenario: L1/L2/L3 问题路由（无活跃变更）

- **WHEN** 诊断确定问题源头为 L1、L2 或 L3 且 不存在活跃变更
- **THEN** 系统 SHALL 创建一个 `功能缺陷` 变更并将缺陷与之关联
- **AND** SHALL 路由到对应阶段的 REVISION 模式（L1→explore / L2→prototype-design / L3→design）
- **AND** SHALL NOT 在项目级工作区内直接修改设计产物
- **AND** 路由输出 SHALL 包含 EXECUTION_MODE = SUBAGENT_REQUIRED 声明

#### Scenario: L2 原型问题路由

- **WHEN** 诊断确定问题源头为 L2 原型设计 且 存在活跃变更
- **THEN** 系统 SHALL 回退到该变更的 prototype-design 阶段 REVISION 模式
- **AND** 标记 design、plan、code、test 等后续阶段状态为 ⏳ 待开始
- **AND** 路由输出 SHALL 包含 EXECUTION_MODE = SUBAGENT_REQUIRED 声明

#### Scenario: L3 设计问题路由

- **WHEN** 诊断确定问题源头为 L3 详细设计 且 存在活跃变更
- **THEN** 系统 SHALL 回退到该变更的 design 阶段 REVISION 模式
- **AND** 标记 plan、code、test 等后续阶段状态为 ⏳ 待开始
- **AND** 路由输出 SHALL 包含 EXECUTION_MODE = SUBAGENT_REQUIRED 声明

#### Scenario: L4 实现问题路由

- **WHEN** 诊断确定问题源头为 L4 实现执行
- **THEN** 系统 SHALL 将该缺陷路由至缺陷修复快车道（见 `bugfix-fast-lane` 能力）
- **AND** SHALL 在选定的缺陷工作区创建缺陷级状态文件 `bugfix-status.md`
- **AND** 将诊断报告中的问题描述、证据与影响范围评估（受影响项清单）写入状态文件
- **AND** 路由输出 SHALL 声明快车道入口、缺陷工作区与受影响项清单
- **AND** 路由输出 SHALL 包含 EXECUTION_MODE = SUBAGENT_REQUIRED 声明
- **AND** SHALL NOT 修改变更级 `.status.md` 的阶段状态矩阵字段

#### Scenario: L4 但修复需要改设计

- **WHEN** 诊断结论为 L4 但修复必须修改设计产物才能正确完成
- **THEN** 系统 SHALL 将该缺陷判定为诊断层级错误
- **AND** SHALL 重新执行四层溯源或将源头改判为 L3
- **AND** SHALL NOT 以 L4 快车道身份修改设计产物

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

系统 SHALL 将 kflow-bug-triage 实现为独立诊断 Skill（非流程阶段），可在存在或不存在活跃变更时执行。

#### Scenario: Skill 触发方式

- **WHEN** 用户通过 kflow-guide 表达修复意图或反馈问题
- **THEN** guide SHALL 路由到 kflow-bug-triage
- **AND** triage SHALL NOT 以“存在活跃变更”作为执行前置条件

#### Scenario: Skill 输入要求

- **WHEN** kflow-bug-triage 执行
- **THEN** 输入 SHALL 包含：
  - 用户的问题描述（必须）
  - 变更级 `.status.md` 与变更目录（存在活跃变更且缺陷归属于该变更时必须）
  - 产品级设计产物 `docs/designs/`（无活跃变更或缺陷不属于任何活跃变更时必须）
  - 项目级 `docs/bugs/index.md`（存在时读取）
- **AND** 缺失的输入 SHALL 在诊断报告中标注，SHALL NOT 静默跳过

#### Scenario: Skill 输出产物

- **WHEN** kflow-bug-triage 完成诊断
- **THEN** 输出 SHALL 包含：
  - 选定工作区的 `index.md` 更新（新增问题条目）
  - 选定工作区的分页详情文件新增或更新（问题详情，含影响范围评估节和修复记录占位节）
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
- **THEN** 输入来自用户反馈或修复意图（经 kflow-guide 路由）
- **AND** 输出给 kflow-explore REVISION（L1 路由）
- **AND** 输出给 kflow-prototype-design REVISION（L2 路由）
- **AND** 输出给 kflow-design REVISION（L3 路由）
- **AND** 输出给缺陷修复快车道（L4 路由，由 `kflow-bug-fix` 的快车道模式承载）

### Requirement: 严重度分级

系统 SHALL 对登记的问题进行三级严重度分级，严重度作为独立字段，不编码到 BUG-ID 中。项目级与变更级工作区的未关闭 🔴 阻塞级问题均阻断归档。

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
- **AND** 项目级 `docs/bugs/index.md` 与变更级 `bugs/index.md` 中的未关闭 🔴 问题 SHALL 分别被归档门控读取

### Requirement: 缺陷工作区判定与归属

kflow-bug-triage SHALL 在执行诊断前判定缺陷工作区，并记录判定依据。

#### Scenario: 项目级工作区判定

- **WHEN** 不存在活跃变更
- **THEN** 缺陷 SHALL 登记到项目级 `docs/bugs/`
- **AND** 问题详情 SHALL 记录“工作区: 项目级”

#### Scenario: 变更级工作区判定

- **WHEN** 存在活跃变更 且 缺陷由该变更引入的代码或产物导致
- **THEN** 缺陷 SHALL 登记到该变更的 `bugs/`
- **AND** 问题详情 SHALL 记录“工作区: 变更级”与关联变更名

#### Scenario: 活跃变更存在但缺陷不属于该变更

- **WHEN** 存在活跃变更 但 缺陷由既有功能或历史代码导致
- **THEN** 缺陷 SHALL 登记到项目级 `docs/bugs/`
- **AND** 问题详情 MAY 记录关联变更（仅作追溯）
- **AND** SHALL NOT 因存在活跃变更而新建变更

#### Scenario: 归属无法判断

- **WHEN** 系统无法判断缺陷是否由活跃变更引入
- **THEN** 系统 SHALL 使用 AskUserQuestion 询问用户
- **AND** 用户确认前 SHALL NOT 创建新的变更

### Requirement: 快车道与变更路径判定

kflow-bug-triage SHALL 在诊断结论为 L4 时判定是否进入快车道；不满足快车道条件时 SHALL 创建 `功能缺陷` 变更并路由到对应设计阶段。

#### Scenario: 默认进入快车道

- **WHEN** 诊断结论为 L4
- **AND** 修复不需要修改 L1/L2/L3 产物
- **AND** 修复不需要数据迁移或破坏性契约变更
- **AND** 受影响项可枚举
- **AND** 用户确认
- **THEN** 系统 SHALL 进入缺陷修复快车道
- **AND** SHALL NOT 创建变更

#### Scenario: 不满足快车道条件时创建变更

- **WHEN** 诊断结论为 L4 但修复需要修改设计产物、需要数据迁移、需要破坏性契约变更，或受影响项无法枚举
- **THEN** 系统 SHALL 创建 `功能缺陷` 变更
- **AND** SHALL 将缺陷与变更关联
- **AND** SHALL 路由到 kflow-explore 或对应的设计 REVISION 模式

#### Scenario: 用户选择变更路径

- **WHEN** 缺陷满足快车道条件但用户选择创建变更
- **THEN** 系统 SHALL 创建 `功能缺陷` 变更
- **AND** 用户选择原因 SHALL 记录到问题详情
