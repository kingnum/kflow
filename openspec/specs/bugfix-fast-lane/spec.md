# bugfix-fast-lane Specification

## Purpose

定义 L4 实现层缺陷的独立修复快车道：在 triage 判定问题源头为实现层且设计已被判定正确的前提下，以「分诊 → 修复 → 定向验证 → 快速收口」的轻量闭环完成缺陷修复，不生成或重跑设计产物、不进入变更级阶段门控矩阵，其状态由缺陷级状态文件独立承载。

## Requirements

### Requirement: 快车道入口条件

快车道 SHALL 仅由 `kflow-bug-triage` 的四层溯源诊断得出 L4 结论时进入，SHALL NOT 提供其他入口。进入快车道 SHALL 以「L1 需求定义、L2 原型设计、L3 详细设计三层均判定通过」为前提。快车道 SHALL 在项目级与变更级两种缺陷工作区均可执行，SHALL NOT 要求存在活跃变更。

#### Scenario: L4 结论触发快车道入口

- **WHEN** kflow-bug-triage 完成四层溯源诊断且结论为 L4 实现执行
- **THEN** 系统 SHALL 为该缺陷创建快车道
- **AND** SHALL 在 triage 选定的缺陷工作区创建缺陷级状态文件 `bugfix-status.md`
- **AND** SHALL 在缺陷详情文件中标记快车道入口

#### Scenario: 无活跃变更时进入快车道

- **WHEN** 诊断结论为 L4 且不存在活跃变更
- **THEN** 系统 SHALL 使用项目级工作区 `docs/bugs/`
- **AND** SHALL NOT 要求用户先创建变更

#### Scenario: 非 L4 结论不进入快车道

- **WHEN** 诊断结论为 L1、L2 或 L3
- **THEN** 系统 SHALL 路由到对应阶段的 REVISION 模式；不存在活跃变更时 SHALL 先创建 `功能缺陷` 变更
- **AND** SHALL NOT 创建快车道状态文件

#### Scenario: L4 但不满足快车道条件

- **WHEN** 诊断结论为 L4 但修复需要修改设计产物、需要数据迁移、需要破坏性契约变更，或受影响项无法枚举
- **THEN** 系统 SHALL 创建 `功能缺陷` 变更并路由到设计阶段
- **AND** SHALL NOT 进入快车道

#### Scenario: 无 triage 诊断结论不得进入快车道

- **WHEN** 请求进入快车道但未经 kflow-bug-triage 诊断
- **THEN** 系统 SHALL 拒绝进入快车道
- **AND** SHALL 要求先执行四层溯源诊断

#### Scenario: 用户覆盖诊断结论时的入口判定

- **WHEN** 用户在 triage 的确认环节覆盖诊断结论并指定源头层级
- **THEN** 系统 SHALL 按用户指定的层级路由
- **AND** 指定层级为 L4 且满足快车道条件时 SHALL 进入快车道
- **AND** 覆盖原因 SHALL 记录到问题登记文件

### Requirement: 缺陷级状态文件

快车道缺陷 SHALL 拥有独立的状态文件 `bugfix-status.md`，记录缺陷标识、工作区、分诊结论、受影响项清单、修复状态、定向验证结果与收口结论。该文件 SHALL 独立于变更级 `.status.md`——快车道 SHALL NOT 读写变更级状态文件的阶段矩阵字段。

#### Scenario: 状态文件路径

- **WHEN** 快车道启动
- **THEN** 状态文件 SHALL 位于 triage 选定的缺陷工作区：
  - 项目级：`docs/bugs/fix/{BUG-ID}/bugfix-status.md`
  - 变更级：`docs/changes/{change}/bugs/fix/{BUG-ID}/bugfix-status.md`
- **AND** 工作区路径 SHALL 在 triage 的路由输出中声明

#### Scenario: 状态文件结构

- **WHEN** 快车道启动
- **THEN** `bugfix-status.md` SHALL 包含以下区：
  - 基本信息（BUG-ID、工作区、关联变更（可选）、分诊时间、问题源头层级）
  - 分诊结论（四层判断摘要、影响范围评估）
  - 受影响项清单（受影响功能点、接口、验证目标）
  - 修复记录（修复阶段状态、耗时、轮次、根因分类）
  - 定向验证（验证范围、验证目标清单、通过结果、报告路径）
  - 收口结论（收口时间、校验项结论）
- **AND** SHALL NOT 省略任何区

#### Scenario: 状态文件独立于变更级状态

- **WHEN** 快车道执行
- **THEN** 系统 SHALL NOT 修改变更级 `.status.md` 的阶段状态矩阵字段
- **AND** 快车道的进度 SHALL 仅由 `bugfix-status.md` 承载

#### Scenario: 多个缺陷并行修复的隔离

- **WHEN** 同一工作区存在多个进入快车道的缺陷
- **THEN** 每个缺陷 SHALL 拥有独立的 `bugfix-status.md`
- **AND** 各缺陷的修复与验证 SHALL NOT 相互干扰
- **AND** 项目级缺陷与变更级缺陷 SHALL NOT 共享状态文件

#### Scenario: 状态文件的生命周期

- **WHEN** 缺陷快速收口完成
- **THEN** `bugfix-status.md` SHALL 保留为历史记录
- **AND** SHALL NOT 随收口而删除

### Requirement: 定向验证机制

快车道的验证 SHALL 为定向验证——仅执行受影响项清单覆盖的验证目标，SHALL NOT 重跑全量测试套件。受影响项清单 SHALL 由 `kflow-bug-triage` 的影响范围评估产出，SHALL NOT 由修复者自行圈定。

#### Scenario: 定向验证只覆盖受影响项

- **WHEN** 快车道进入定向验证
- **THEN** 系统 SHALL 仅执行受影响项清单覆盖的验证目标
- **AND** 验证目标 SHALL 为以下之一或组合：已有自动化测试用例、新增回归测试、手工验证步骤
- **AND** SHALL NOT 重跑该变更或项目的全量测试套件
- **AND** SHALL 输出定向验证报告

#### Scenario: 受影响项清单 100% 覆盖

- **WHEN** 定向验证执行
- **THEN** 受影响项清单中每一项 SHALL 被完整验证
- **AND** 覆盖率 SHALL 达到 100%
- **AND** 未达 100% 时定向验证 SHALL 判定为不通过

#### Scenario: 影响面超出清单时判定分诊失效

- **WHEN** 修复过程中发现实际影响面超出受影响项清单覆盖范围
- **THEN** 系统 SHALL 判定为分诊失效
- **AND** SHALL 退回 `kflow-bug-triage` 重新评估影响范围
- **AND** SHALL NOT 由修复者擅自扩大或缩小验证范围

#### Scenario: 定向验证失败的重试上限

- **WHEN** 定向验证未通过
- **THEN** 系统 SHALL 复用 `kflow-bug-fix` 既有的「子变更修复三次尝试上限」处理
- **AND** SHALL NOT 引入新的轮次模型
- **AND** 达到上限时 SHALL 使用 AskUserQuestion 升级用户

#### Scenario: 定向验证不使用收敛驱动循环

- **WHEN** 快车道执行验证
- **THEN** 系统 SHALL NOT 使用收敛驱动循环或见证轮判据
- **AND** 验证轮次 SHALL 由定向验证的实际重试次数决定，有界

### Requirement: 快速收口机制

定向验证通过后，系统 SHALL 收口该缺陷：更新 `bugs/index.md` 状态、写入 `bugfix-status.md` 收口结论、标记缺陷为「已解决」。快速收口 SHALL NOT 触发阶段回退、SHALL NOT 阻塞变更级阶段流转。

#### Scenario: 验证通过后收口

- **WHEN** 定向验证通过且受影响项清单 100% 覆盖
- **THEN** 系统 SHALL 更新 `bugs/index.md` 对应行状态为「已解决」
- **AND** SHALL 在 `bugfix-status.md` 的收口结论区写入收口时间与校验项结论
- **AND** SHALL 标记缺陷状态为「已解决」

#### Scenario: 收口校验项

- **WHEN** 快速收口执行
- **THEN** 系统 SHALL 校验以下条件全部满足：
  - 受影响项清单 100% 覆盖且全部通过
  - 定向验证报告存在
  - `bugfix-status.md` 全部必填区已填写且无占位符
- **AND** 任一条件不满足时收口 SHALL 判定为不通过

#### Scenario: 收口不触发阶段回退

- **WHEN** 缺陷快速收口完成
- **THEN** 系统 SHALL NOT 修改变更级 `.status.md` 的任何阶段状态
- **AND** SHALL NOT 阻塞变更级阶段的流转

#### Scenario: 收口失败时的处理

- **WHEN** 收口校验未通过
- **THEN** 系统 SHALL 保持缺陷状态为「处理中」
- **AND** SHALL 在 `bugfix-status.md` 记录未通过原因
- **AND** SHALL NOT 标记为「已解决」

### Requirement: 快车道产物边界

快车道 SHALL NOT 生成或修改设计产物，包括 `functional-designs/`、`detailed-design/`、`api-tests/`、`e2e-tests/`。修复需要修改设计产物时，系统 SHALL 判定诊断层级错误并退回 `kflow-bug-triage` 重新分层。

#### Scenario: 快车道不触碰设计产物

- **WHEN** 快车道执行修复
- **THEN** 系统 SHALL NOT 创建或修改 `functional-designs/`、`detailed-design/`、`api-tests/`、`e2e-tests/` 下的任何文件
- **AND** 允许修改的范围 SHALL 限于代码实现与测试代码

#### Scenario: 修复需要改设计时退回分层

- **WHEN** 修复过程中发现必须修改 `detailed-design.md` 或更上游的设计产物才能正确修复
- **THEN** 系统 SHALL 判定诊断层级错误
- **AND** SHALL 退回 `kflow-bug-triage` 重新执行四层溯源
- **AND** SHALL NOT 在快车道内修改设计产物

#### Scenario: 快车道产物清单

- **WHEN** 快车道完成
- **THEN** 产出 SHALL 限于：
  - 选定工作区的 `fix/{BUG-ID}/bugfix-status.md`（缺陷级状态文件）
  - 选定工作区的 `fix/{BUG-ID}/verify-report.md`（定向验证报告）
  - 代码与测试代码修改
  - 选定工作区的 `index.md` 与缺陷详情文件的更新
- **AND** SHALL NOT 产出设计阶段产物

### Requirement: kflow-bug-fix 快车道模式

`kflow-bug-fix` SHALL 支持在无触发测试阶段上下文时以快车道模式执行修复。快车道模式下，其状态写入、轮次计数与流程出口 SHALL 绑定缺陷级状态文件，SHALL NOT 依赖变更级 `.status.md`。子变更级与变更级两种既有模式的流程保持不变。

#### Scenario: 无测试阶段上下文时进入快车道模式

- **WHEN** `kflow-bug-fix` 被调用且无触发测试阶段上下文
- **AND** 调用来源为 `kflow-bug-triage` 的 L4 路由
- **THEN** 系统 SHALL 以快车道模式执行修复
- **AND** SHALL 从 triage 声明的缺陷工作区读取 `bugfix-status.md` 的受影响项清单与分诊结论
- **AND** SHALL NOT 读取变更级 `.status.md` 的「变更档位」或阶段状态字段

#### Scenario: 快车道模式复用既有修复能力

- **WHEN** 快车道模式执行修复
- **THEN** 系统 SHALL 复用 `kflow-bug-fix` 既有的根因二分法（实现错误 / 测试错误）
- **AND** SHALL 复用既有的「子变更修复三次尝试上限」
- **AND** SHALL 复用既有的 Regression Test at Correct Seam 环节与 Post-mortem 复盘环节
- **AND** SHALL NOT 定义第二套修复流程

#### Scenario: 快车道模式的状态写入位置

- **WHEN** 快车道模式执行
- **THEN** 修复阶段状态、耗时与轮次 SHALL 写入选定工作区的 `bugfix-status.md` 修复记录区
- **AND** SHALL NOT 写入变更级 `.status.md` 的 `执行轮次` 字段

#### Scenario: 快车道模式的流程出口

- **WHEN** 快车道模式完成修复
- **THEN** 流程出口 SHALL 为「进入定向验证」，而非「返回测试阶段」
- **AND** 定向验证通过并完成快速收口后，流程 SHALL 终止
- **AND** SHALL NOT 返回任何变更级测试阶段

#### Scenario: 既有模式流程不变

- **WHEN** `kflow-bug-fix` 被调用且存在触发测试阶段上下文（接口单元测试 / E2E 测试 / 集成测试）
- **THEN** 系统 SHALL 按既有的子变更级或变更级模式执行
- **AND** 流程出口 SHALL 保持为「返回测试阶段」

### Requirement: 快车道与变更级阶段门控的隔离

快车道 SHALL NOT 进入变更级阶段门控矩阵，SHALL NOT 影响变更级阶段的完成判定。审计的记账职责中，门控校验 SHALL NOT 覆盖快车道缺陷；覆盖率与产物存在性校验 SHALL 覆盖变更级快车道状态文件的完整性。

#### Scenario: 快车道不进入阶段门控

- **WHEN** 快车道执行修复与验证
- **THEN** 系统 SHALL NOT 要求任何变更级阶段的门控通过
- **AND** SHALL NOT 因快车道未完成而阻塞变更级阶段流转

#### Scenario: 审计不校验快车道流程形态

- **WHEN** 审计执行门控校验
- **THEN** 系统 SHALL NOT 要求快车道缺陷经过阶段门控
- **AND** SHALL NOT 将未走阶段门控的快车道缺陷判定为跳阶段

#### Scenario: 审计校验快车道产物完整性

- **WHEN** 审计执行覆盖率与产物存在性校验
- **AND** 该变更存在进入快车道的缺陷
- **THEN** 系统 SHALL 校验每个变更级快车道缺陷的 `bugfix-status.md` 是否存在且必填区完整
- **AND** 状态文件缺失或必填区不完整时 SHALL 判定为阻塞

#### Scenario: 项目级快车道不受变更审计约束

- **WHEN** 项目级缺陷进入快车道
- **THEN** 该缺陷 SHALL NOT 被任何变更级审计或归档门控要求阶段产物
- **AND** 归档门控 SHALL 仅按项目级 `docs/bugs/index.md` 的阻塞级状态判定是否阻断

### Requirement: 项目级缺陷快车道

系统 SHALL 支持不依附于任何变更的项目级缺陷快车道，其状态与产物根为 `docs/bugs/`。

#### Scenario: 项目级快车道生命周期

- **WHEN** 项目级缺陷进入快车道
- **THEN** 生命周期 SHALL 为：分诊 → 修复 → 定向验证 → 快速收口
- **AND** SHALL NOT 创建 `docs/changes/{change}/` 目录
- **AND** SHALL NOT 触发变更级阶段、审计或归档

#### Scenario: 项目级快车道收口

- **WHEN** 项目级缺陷定向验证通过且收口校验项全部满足
- **THEN** 系统 SHALL 更新 `docs/bugs/index.md` 对应行状态为「已解决」
- **AND** SHALL 写入 `docs/bugs/fix/{BUG-ID}/bugfix-status.md` 收口结论
- **AND** SHALL 在项目级问题详情文件中标记快车道收口完成

#### Scenario: 项目级快车道与 release 解耦

- **WHEN** 项目级缺陷快速收口完成
- **THEN** 系统 SHALL NOT 触发 KFlow 变更归档、版本自增或打包
- **AND** 项目自身的发布流程 MAY 读取 `docs/bugs/index.md` 汇总已解决缺陷
