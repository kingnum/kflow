# phase-self-review Delta Specification

## MODIFIED Requirements

### Requirement: 自审由当前阶段 Agent 执行

系统 SHALL 由子代理（Agent subagent）执行自审，不再由当前阶段 Agent 自身执行。子代理拥有独立上下文，每轮启动独立子代理，10 轮串行执行。

#### Scenario: Agent 自审流程
- **WHEN** 阶段产物初稿生成完毕
- **THEN** 主 Agent 启动第一轮子代理（Agent subagent）
- **AND** 子代理读取自身产出，按维度逐项检查
- **AND** 子代理发现问题后自行修复并记录

#### Scenario: 自审必须使用子代理
- **WHEN** 自审过程中
- **THEN** 必须启动独立的审查子代理
- **AND** SHALL NOT 由当前阶段 Agent 自身执行自审
- **AND** 子代理串行执行（前一轮完成后再启动下一轮），不允许并行

### Requirement: explore 阶段自审（重复制）

kflow-explore 的 SELFREV 步骤 SHALL 由子代理串行执行 10 轮自审，采用"重复制"。

#### Scenario: explore 阶段自审（重复制）
- **WHEN** kflow-explore 完成 functional-designs/ 初稿
- **THEN** 主 Agent 启动第一轮子代理执行自审
- **AND** 每轮子代理 SHALL 按完整性、闭环性、必要性、清晰性**全部四个维度**独立检查
- **AND** 子代理发现问题直接修复产物文件
- **AND** SHALL NOT 按维度分组分配轮次
- **AND** 必须串行完成全部 10 轮后方可标记阶段完成

### Requirement: prototype 阶段自审（重复制）

kflow-prototype-design 的 SELFREV 步骤 SHALL 由子代理串行执行 10 轮自审，采用"重复制"。

#### Scenario: prototype 阶段自审（重复制）
- **WHEN** kflow-prototype-design 完成 VERIFY 步骤后
- **THEN** 主 Agent 启动第一轮子代理执行自审
- **AND** 每轮子代理 SHALL 按覆盖性、一致性、可用性、完整性**全部四个维度**独立检查
- **AND** 覆盖性为第一优先级
- **AND** 子代理发现问题直接修复原型文件
- **AND** SHALL NOT 按维度分组分配轮次
- **AND** 必须串行完成全部 10 轮后方可进入用户评审

### Requirement: design 阶段自审（重复制）

kflow-design 的 SELFREV 步骤 SHALL 由子代理串行执行 10 轮自审，采用"重复制"（废除分工制）。

#### Scenario: design 阶段自审（重复制）
- **WHEN** kflow-design 完成 detailed-design.md 初稿
- **THEN** 主 Agent 启动第一轮子代理执行自审
- **AND** 每轮子代理 SHALL 按一致性、完备性、可行性、可测性**全部四个维度**独立检查
- **AND** SHALL NOT 按维度分组分配轮次（如 Round 1-3 结构性、Round 4-7 细节、Round 8-10 边界）
- **AND** 子代理发现问题直接修复设计文档
- **AND** 必须串行完成全部 10 轮后方可进入四视角交叉审查

## REMOVED Requirements

### Requirement: design 自审轮次分配

**Reason**: design 阶段从"分工制"改为"重复制"，轮次分配表不再适用。废除 Round 1-3 结构性/4-7 细节/8-10 边界的维度分组，改为每轮全四维度独立检查。

**Migration**: design 阶段的 10 轮自审每轮均覆盖一致性、完备性、可行性、可测性全部四个维度，无轮次偏向。
