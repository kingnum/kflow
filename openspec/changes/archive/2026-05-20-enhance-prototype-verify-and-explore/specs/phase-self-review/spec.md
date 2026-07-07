# phase-self-review Delta Specification

## MODIFIED Requirements

### Requirement: 三阶段 10 轮自审强制执行

系统 SHALL 在 kflow-explore、kflow-prototype-design、kflow-design 三个阶段各强制执行 10 轮自循环审查，不允许提前终止。explore 和 prototype 自审采用"重复制"（每轮全维度独立审查），design 自审保持"分工制"不变。

#### Scenario: explore 阶段自审

- **WHEN** kflow-explore 完成 functional-designs/ 初稿
- **THEN** 系统执行 10 轮自审，采用"重复制"
- **AND** 每轮 SHALL 按完整性、闭环性、必要性、清晰性**全部四个维度**独立检查
- **AND** SHALL NOT 按维度分组分配轮次（如 Round 1-3 仅结构性检查）
- **AND** 必须完成全部 10 轮后方可标记阶段完成

#### Scenario: prototype 阶段自审

- **WHEN** kflow-prototype-design 完成 prototype 初稿
- **THEN** 系统执行 10 轮自审，采用"重复制"
- **AND** 每轮 SHALL 按覆盖性、一致性、可用性、完整性**全部四个维度**独立检查
- **AND** 覆盖性为第一优先级：确保所有 FP 有对应原型页面
- **AND** SHALL NOT 按维度分组分配轮次
- **AND** 必须完成全部 10 轮后方可进入用户评审

#### Scenario: design 阶段自审

- **WHEN** kflow-design 完成 detailed-design.md 初稿
- **THEN** 系统执行 10 轮自审
- **AND** 每轮按一致性、完备性、可行性、可测性四个维度检查
- **AND** 必须完成全部 10 轮后方可进入四视角交叉审查

### Requirement: explore 阶段自审维度

kflow-explore 自审 SHALL 覆盖完整性、闭环性、必要性、清晰性四个维度。采用"重复制"模式：每轮自审独立执行全部四个维度。

#### Scenario: 完整性检查

- **WHEN** explore 自审执行完整性维度
- **THEN** 检查是否所有页面/菜单/操作/表单项均已覆盖
- **AND** 检查是否所有用户可执行操作均有对应功能点

#### Scenario: 闭环性检查

- **WHEN** explore 自审执行闭环性维度
- **THEN** 检查业务流程是否无断点
- **AND** 检查每个业务流程是否从触发到结果形成完整闭环

#### Scenario: 必要性检查

- **WHEN** explore 自审执行必要性维度
- **THEN** 检查是否存在多余/冗余功能点
- **AND** 检查每个功能点是否有明确的用户价值

#### Scenario: 清晰性检查

- **WHEN** explore 自审执行清晰性维度
- **THEN** 检查每个功能点描述是否无歧义
- **AND** 检查每个功能点的边界是否明确

#### Scenario: 重复制执行规则

- **WHEN** explore 自审每轮执行
- **THEN** 每轮 SHALL 独立执行全部四个维度的完整检查
- **AND** SHALL NOT 将维度分组到不同轮次（如 Round 1-3 仅结构性、Round 4-7 仅细节）
- **AND** 每轮检查均从四个维度视角发现问题，形成自然收敛

### Requirement: prototype 阶段自审维度

kflow-prototype-design 自审 SHALL 覆盖覆盖性、一致性、可用性、完整性四个维度，覆盖性为第一优先级。采用"重复制"模式：每轮自审独立执行全部四个维度。

#### Scenario: 覆盖性检查（第一优先级）

- **WHEN** prototype 自审执行覆盖性维度
- **THEN** 检查是否所有 FP 有对应原型页面
- **AND** 检查是否所有页面可执行操作有对应交互组件
- **AND** 检查是否所有表单项有对应表单组件

#### Scenario: 一致性检查

- **WHEN** prototype 自审执行一致性维度
- **THEN** 检查视觉风格是否统一
- **AND** 检查组件命名是否一致

#### Scenario: 可用性检查

- **WHEN** prototype 自审执行可用性维度
- **THEN** 检查交互流程是否顺畅
- **AND** 检查交互状态覆盖是否完整（加载/空/错误/边界）

#### Scenario: 完整性检查

- **WHEN** prototype 自审执行完整性维度
- **THEN** 检查组件状态覆盖（加载态、空态、错误态、边界态）
- **AND** 检查所有页面入口是否可达

#### Scenario: 重复制执行规则

- **WHEN** prototype 自审每轮执行
- **THEN** 每轮 SHALL 独立执行全部四个维度的完整检查
- **AND** SHALL NOT 将维度分组到不同轮次（如 Round 1-3 仅覆盖性、Round 4-7 仅可用性）
- **AND** 每轮检查均从四个维度视角发现问题，形成自然收敛
