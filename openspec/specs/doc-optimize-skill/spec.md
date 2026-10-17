# doc-optimize-skill Specification

## Purpose

定义文档优化 Skill——一个非流程阶段的独立维护能力，用于对项目中已生成的存量文档执行修订记录裁剪与大文档拆分，并保证优化后的引用完整、内容不失真，使用户可在任意时刻以自然语言触发存量文档的优化。

## Requirements

### Requirement: 文档优化 Skill 的定位与触发

系统 SHALL 提供 `kflow-doc-optimize`，定位为**独立维护 Skill（非流程阶段）**。它 SHALL NOT 写入任何变更的阶段状态，SHALL NOT 阻塞任何阶段流转，且 MAY 在任意时刻被调用。

#### Scenario: 手动触发

- **WHEN** 用户输入 `/kflow-doc-optimize` 或表达「文档优化」「文档瘦身」「拆分文档」「清理修订记录」等意图
- **THEN** 该 Skill SHALL 被调用
- **AND** 其 SHALL NOT 要求存在活跃变更

#### Scenario: 通过流程入口路由

- **WHEN** 用户通过 `kflow-guide` 表达文档优化意图
- **THEN** guide SHALL 将该意图路由到 `kflow-doc-optimize`
- **AND** 该路由 SHALL NOT 被视为变更流程的一环

#### Scenario: 不写入阶段状态

- **WHEN** 该 Skill 执行完毕
- **THEN** 变更级 `.status.md` 的阶段状态表 SHALL NOT 被修改
- **AND** 优化过程 SHALL 以独立报告承载

### Requirement: 不受变更流程适用边界约束

`kflow-doc-optimize` SHALL 被视为**项目级文档维护工具**，SHALL NOT 受「KFlow Skills 仅适用于功能变更与缺陷修复」这一变更流程适用边界的排除。

#### Scenario: 文档维护场景下的可调用性

- **WHEN** 项目在 CLAUDE.md 中声明了「KFlow Skills 仅在功能变更与缺陷修复场景调用，其余工作一律不调用」的适用边界
- **THEN** `kflow-doc-optimize` SHALL 被列为该边界的**例外**
- **AND** 在文档维护场景下 SHALL 可被正常调用

#### Scenario: kflow-init 注入时的例外声明

- **WHEN** kflow-init 注入或更新 CLAUDE.md 的流程规则区块
- **THEN** 注入内容 SHALL 声明 `kflow-doc-optimize` 作为独立维护工具不受变更流程适用边界约束
- **AND** 该声明 SHALL 便于项目在其自维护的规则区块中同步该例外

#### Scenario: 与变更流程的边界

- **WHEN** 判定该 Skill 与变更流程的关系
- **THEN** 它 SHALL NOT 被视为任何阶段的产物
- **AND** 其调用 SHALL NOT 改变任何变更的阶段状态
- **AND** 其产出 SHALL 以独立报告承载，SHALL NOT 登记进变更产物清单

### Requirement: 优化对象扫描与识别

该 Skill SHALL 扫描产品级与变更级文档，按既定阈值识别需要优化的文档，并输出优化清单。

#### Scenario: 扫描范围

- **WHEN** 执行扫描
- **THEN** 扫描范围 SHALL 包含 `CONTEXT.md`、`docs/designs/**`、`docs/open/**` 等产品级文档
- **AND** SHALL 包含 `docs/changes/` 下的活跃变更产物
- **AND** SHALL NOT 扫描已归档变更目录

#### Scenario: 识别修订记录超量

- **WHEN** 某文档头部修订记录条数超过保留上限
- **THEN** 该文档 SHALL 被列入优化清单，问题类型标记为「修订记录超量」

#### Scenario: 识别超大文档

- **WHEN** 某文档的单文件体积超过分片阈值
- **THEN** 该文档 SHALL 被列入优化清单，问题类型标记为「超出分片阈值」

#### Scenario: 识别缺失章节索引

- **WHEN** 某文档体积超过索引阈值但未提供章节索引
- **THEN** 该文档 SHALL 被列入优化清单，问题类型标记为「缺少章节索引」

#### Scenario: 清单内容

- **WHEN** 优化清单被输出
- **THEN** 每一项 SHALL 包含：文档路径、问题类型、当前体积、优化方式、预计优化后体积、受影响的引用位置

### Requirement: 执行前须经用户确认

该 Skill SHALL 在执行任何写入动作前，将优化清单提交用户确认，并支持用户选择执行范围。

#### Scenario: 提交清单确认

- **WHEN** 扫描与识别完成
- **THEN** 该 Skill SHALL 以用户可读形式提交优化清单
- **AND** SHALL 询问用户选择全部执行、部分执行或不执行

#### Scenario: 用户选择部分执行

- **WHEN** 用户选择仅执行清单中的部分项
- **THEN** 该 Skill SHALL 只执行所选项
- **AND** 未选项 SHALL NOT 被修改

#### Scenario: 无优化项时的行为

- **WHEN** 扫描未识别出任何需要优化的文档
- **THEN** 该 Skill SHALL 报告「无需优化」并终止
- **AND** SHALL NOT 发起确认询问

### Requirement: 优化的执行与内容保真

该 Skill 执行优化时 SHALL 仅搬移、拆分与建立索引，SHALL NOT 改写、删减或合并文档的实质内容。

#### Scenario: 修订记录裁剪保持内容保真

- **WHEN** 执行修订记录裁剪
- **THEN** 被移出的记录 SHALL 原样进入历史承载位置
- **AND** 保留在头部的记录 SHALL NOT 被改写

#### Scenario: 大文档拆分保持内容保真

- **WHEN** 执行大文档拆分
- **THEN** 拆分后的各分册内容 SHALL 为原文件对应章节的原文
- **AND** SHALL NOT 因拆分而改写表述、调整章节顺序或合并章节

#### Scenario: 拆分后建立索引

- **WHEN** 一个大文档被拆分
- **THEN** SHALL 在同级建立 `index.md` 承载章节导航
- **AND** 索引 SHALL 使读取侧能够按章节定位到目标分册

### Requirement: 优化后的引用完整性校验

优化执行完毕后，该 Skill SHALL 校验全部受影响引用的完整性，SHALL NOT 留下断链或失效路径。

#### Scenario: 拆分后的引用更新

- **WHEN** 一个大文档被拆分，且其他文档或 Skill 规则引用了该文档的路径
- **THEN** 该 Skill SHALL 定位这些引用并更新为拆分后的目标路径
- **AND** 更新范围 SHALL 包含项目文档、Skill 规则文件与脚本

#### Scenario: 引用校验

- **WHEN** 优化执行完毕
- **THEN** 该 Skill SHALL 校验全部受影响引用均能解析到存在的文件
- **AND** 存在无法解析的引用时 SHALL 报告并停止，不得静默通过

#### Scenario: 校验通过后输出报告

- **WHEN** 引用校验通过
- **THEN** 该 Skill SHALL 输出优化报告，含实际执行的项、体积变化、更新过的引用清单
