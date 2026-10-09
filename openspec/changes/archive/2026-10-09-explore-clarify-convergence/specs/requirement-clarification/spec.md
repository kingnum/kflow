# Spec Delta

## Purpose

定义需求澄清的收敛门与内容克制规则：以「未决问题清单归零」作为进入功能点拆分的硬性出口条件，限定消歧路径，并禁止以扩增功能设计内容的方式消除歧义。

## ADDED Requirements

### Requirement: 需求澄清收敛硬门

系统 SHALL 在 kflow-explore 的 CLARIFY 步骤维护「未决问题清单」，并在进入 SPLIT 步骤之前要求该清单为**空**。清单中的每一项必须被**消解**，或被**显式降级**为 `待补充` 并记录降级理由与责任阶段。存在未消解且未降级的清单项时，系统 SHALL NOT 进入 SPLIT。

#### Scenario: 清单为空时放行

- **WHEN** CLARIFY 完成且未决问题清单为空
- **THEN** 系统 SHALL 允许进入 SPLIT 步骤

#### Scenario: 清单非空时阻塞

- **WHEN** CLARIFY 完成且未决问题清单存在未消解、未降级的项
- **THEN** 系统 SHALL NOT 进入 SPLIT 步骤
- **AND** 系统 SHALL 逐项处理：消解，或降级为 `待补充`

#### Scenario: 显式降级放行

- **WHEN** 某项无法在本阶段消解
- **AND** 该项被显式标记为 `待补充` 并记录了降级理由与责任阶段
- **THEN** 该项 SHALL NOT 阻塞进入 SPLIT

#### Scenario: 降级项留痕

- **WHEN** 任一清单项被降级为 `待补充`
- **THEN** 系统 SHALL 在变更级 `.status.md` 记录该降级项及其理由
- **AND** 该记录 SHALL 可被后续阶段读取

#### Scenario: 清单候选来源覆盖澄清内容域

- **WHEN** 系统生成或更新未决问题清单
- **THEN** 候选 SHALL 由页面结构/菜单、可执行操作、表单项、业务规则、业务流程五个内容域逐域遍历产生
- **AND** SHALL NOT 以直接置空代替逐域遍历
- **AND** 清单为空时 SHALL 说明五个内容域均已遍历且未发现歧义

### Requirement: 消歧路径限定

消解一项歧义 SHALL 通过以下路径之一完成：(a) 向用户澄清提问；(b) 精确化 `CONTEXT.md` 中的术语定义；(c) 通过代码库或事实查库直接解析。系统 SHALL NOT 以扩增功能设计内容（新增功能点、字段、章节或分支）的方式消除歧义。

#### Scenario: 以提问消解

- **WHEN** 歧义属于用户可决策的需求问题
- **THEN** 系统 SHALL 向用户提出问题以获得单一确定答案
- **AND** 该清单项 SHALL 标记为已消解

#### Scenario: 以术语精确化消解

- **WHEN** 歧义源于术语模糊或过载
- **THEN** 系统 SHALL 精确化 `CONTEXT.md` 中的对应术语定义
- **AND** 该清单项 SHALL 标记为已消解

#### Scenario: 以扩增内容消解被拒

- **WHEN** 消除某歧义的手段是新增功能点、字段、章节或分支以覆盖多种可能
- **THEN** 该手段 SHALL NOT 被视为有效消解
- **AND** 系统 SHALL 改为通过澄清提问或术语精确化收敛为单一确定答案

### Requirement: 需求内容非必要不增加

需求探索 SHALL NOT 为假想分支、将来需求或未确认的边界情况预留功能点、字段或章节。歧义 SHALL 收敛为一个确定答案，SHALL NOT 铺开为多个可能。本要求 SHALL NOT 与既有「结构性章节不得省略」的要求冲突——结构性章节在无内容时 SHALL 按既有规则标注「无」，而非删除。

#### Scenario: 不为假想分支预留

- **WHEN** 某项内容仅因「将来可能需要」而被纳入功能设计
- **THEN** 系统 SHALL NOT 产出该项内容
- **AND** 若确有需求，SHALL 先确认该需求存在

#### Scenario: 歧义收敛为单一答案

- **WHEN** 某需求点存在多种可能实现
- **THEN** 系统 SHALL 通过消歧路径将其收敛为一个确定答案
- **AND** SHALL NOT 在功能设计中并列保留多个可能

### Requirement: 提问纪律

系统 SHALL 区分**事实项**与**决策项**：事实项 SHALL 通过查库或代码探索自动解析，SHALL NOT 占用用户注意力；决策项 SHALL 提交用户，且一次只提交一项决策。

#### Scenario: 事实项自动解析

- **WHEN** 某清单项可通过代码库、配置或既有文档查证
- **THEN** 系统 SHALL 自行查证并消解该项
- **AND** SHALL NOT 向用户提问

#### Scenario: 决策项一次一项

- **WHEN** 存在多个需用户决策的清单项
- **THEN** 系统 SHALL 逐项提交，等待用户对当前项的反馈后再提交下一项
- **AND** SHALL NOT 在一次交互中并行提交多项决策
