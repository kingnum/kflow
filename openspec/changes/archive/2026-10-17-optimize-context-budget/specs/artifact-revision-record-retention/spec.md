# Spec Delta

## Purpose

定义文档修订记录的留存边界——把「每次增补必须追加修订记录」与「读取侧只需要最新修订」之间缺失的一环补齐，使文档头部的版本历史不随项目年龄无界增长，从而避免每次读取整个文件时把全量历史一并载入上下文。

## ADDED Requirements

### Requirement: 文档头部修订记录保留最近条目

任一承载修订记录的文档，其头部 SHALL 仅保留最近 **3 条**修订记录；超出部分 SHALL 移入该文档对应的历史承载位置。

#### Scenario: 修订记录超出保留条数

- **WHEN** 向一个已有 3 条修订记录的文档追加第 4 条
- **THEN** 该文档头部 SHALL 保留最近 3 条
- **AND** 最早的一条 SHALL 被移入对应层级的历史承载位置
- **AND** 文档的版本号 SHALL 按既有规则递增

#### Scenario: 保留条数内的追加

- **WHEN** 向一个修订记录不足 3 条的文档追加新条目
- **THEN** 直接追加，SHALL NOT 触发移出动作

#### Scenario: 移出历史时的完整性

- **WHEN** 一条修订记录被移出文档头部
- **THEN** 其全部字段（版本、日期、修订类型、修订内容、影响对象、触发阶段）SHALL 原样保留于历史承载位置
- **AND** SHALL NOT 因移出而丢失任何字段或改写表述

### Requirement: 历史承载位置按层级划分

被移出的修订记录 SHALL 按文档层级进入对应的历史承载位置。

#### Scenario: 变更级产物的历史承载

- **WHEN** 变更级产物（`functional-designs/part-NN.md`、`detailed-design.md`、`api-tests/part-NN.md` 等）的修订记录被移出
- **THEN** 该记录 SHALL 移入该变更目录下的 `docs/changes/{change}/revision-history.md`
- **AND** `revision-history.md` SHALL 按产物文件分组组织

#### Scenario: 产品级文档的历史承载

- **WHEN** 产品级文档（`CONTEXT.md`、`docs/designs/**`、`docs/open/**`）的修订记录被移出
- **THEN** 该记录 SHALL 移入 `docs/designs/changelog.md`
- **AND** changelog 中的记录 SHALL 保留其原属文档的标识

#### Scenario: 历史承载位置不参与常规读取

- **WHEN** 任一阶段读取产物文档
- **THEN** 历史承载位置 SHALL NOT 被读取
- **AND** 仅在需要追溯特定版本的修订内容时才读取

### Requirement: 读取侧只消费最新修订

各阶段的阶段前置钩子读取文档修订记录时，SHALL 只消费文档头部保留的条目，SHALL NOT 因需要判断设计是否发生变更而读取历史承载位置。

#### Scenario: 判断设计是否变更

- **WHEN** 阶段需要判断某文档是否在本阶段之前发生了修订
- **THEN** 读取 SHALL 限于文档头部保留的最近条目
- **AND** 判定依据 SHALL 为最新的版本号与修订内容

#### Scenario: 修订记录被移出后的判断仍然成立

- **WHEN** 某次修订已被移入历史承载位置
- **THEN** 该次修订对「最新修订」的判定 SHALL NOT 产生影响
- **AND** 文档的当前版本号 SHALL 始终反映全部修订的累积结果

### Requirement: 状态文件的阶段记录不属于修订记录

变更级状态文件的「阶段状态」追加块 SHALL 按 `status-file-layering` 能力分层，SHALL NOT 套用本能力的修订记录保留条数规则。

#### Scenario: 状态文件与产物文档的分工

- **WHEN** 处理变更级状态文件的历史内容
- **THEN** 其分层规则 SHALL 由 `status-file-layering` 能力规定
- **AND** 本能力的 3 条保留规则 SHALL NOT 适用于状态文件

#### Scenario: 修订记录与状态记录的口径一致

- **WHEN** 两个能力同时落地
- **THEN** 二者 SHALL 遵循同一原则——当前有效状态留在头部、历史移入独立文件且不参与常规读取

### Requirement: 归档合并时自动执行留存边界

留存边界的执行 SHALL 由变更归档的设计合并步骤承担，使新变更产生的文档自动遵守该规则，用户无需为此发起任何操作。

#### Scenario: 归档合并时同步裁剪

- **WHEN** 归档阶段将变更级产物合并到产品级文档
- **THEN** 合并动作 SHALL 同时执行产品级文档的修订记录留存边界
- **AND** 被移出的记录 SHALL 落入 `docs/designs/changelog.md`

#### Scenario: 归档合并时同步维护章节索引

- **WHEN** 归档合并改变了某产品级文档的章节结构或体积
- **THEN** 该文档的章节索引 SHALL 被同步更新
- **AND** 体积跨越分片阈值时 SHALL 触发拆分并在同一步完成引用更新

#### Scenario: 自动机制不依赖用户操作

- **WHEN** 任一变更完成归档
- **THEN** 上述裁剪、索引维护与拆分 SHALL 全程自动完成
- **AND** SHALL NOT 要求用户输入任何指令或确认

#### Scenario: 需要用户裁决时的边界

- **WHEN** 归档合并遇到需要判断拆分边界、或引用更新存在歧义的情形
- **THEN** 该情形 SHALL 交由用户裁决
- **AND** 其余可自动完成的部分 SHALL 先行完成，SHALL NOT 因个别歧义阻塞整步
