# phase-boundary-enforcement Specification

## Purpose
TBD - created by archiving change phase-review-mechanism-upgrade. Update Purpose after archive.
## Requirements
### Requirement: 文档创建白名单模式

系统 SHALL 在每个阶段仅允许创建其输出产物表中列出的文件，禁止创建任何未在输出产物表中列出的文件。

#### Scenario: 白名单内文件允许创建
- **WHEN** 阶段需要创建输出产物表中的文件
- **THEN** 系统允许创建该文件
- **AND** 文件内容遵循阶段任务边界约束

#### Scenario: 白名单外文件禁止创建
- **WHEN** 阶段尝试创建输出产物表中未列出的文件
- **THEN** 系统禁止创建
- **AND** 如内容确有必要，记录到 docs/skill-suggestion.md

### Requirement: 标准产物强制生成

系统 SHALL 无论用户输入来源是什么（口述/文件/URL），都必须生成该阶段完整的标准输出产物。

#### Scenario: 用户以文件提供输入
- **WHEN** 用户以文档文件提供需求输入
- **THEN** 系统仍需生成 functional-designs/ 目录（explore 阶段）
- **AND** 不可直接引用用户文件替代标准产物

#### Scenario: 用户以 URL 提供输入
- **WHEN** 用户以 URL 指向外部需求描述
- **THEN** 系统读取 URL 内容后仍需生成完整的标准输出产物
- **AND** 不可仅保存 URL 引用作为替代

#### Scenario: 用户口述需求
- **WHEN** 用户口头描述需求
- **THEN** 系统基于对话内容生成完整的标准输出产物
- **AND** 产出物质量与文件输入模式一致

### Requirement: 信息不足时的溢出路径

系统 SHALL 当当前文档内容无法满足需求时，记录到 docs/skill-suggestion.md 并在当前阶段文档中扩充，禁止创建额外文档。

#### Scenario: 发现信息不足
- **WHEN** 阶段执行过程中发现需要额外信息
- **THEN** 在当前阶段文档中标记"待补充"并说明缺少什么
- **AND** 记录到 docs/skill-suggestion.md 作为流程改进建议

#### Scenario: 禁止自创新文档
- **WHEN** 阶段发现当前文档无法容纳某类信息
- **THEN** 禁止创建额外文档来填补信息空缺
- **AND** 如需扩展文档结构，通过 skill-suggestion 提议流程改进

### Requirement: 阶段内容禁止越界

系统 SHALL 确保每个阶段仅输出其职责范围内的内容，禁止输出后续阶段的职责内容。

#### Scenario: explore 禁止输出技术设计
- **WHEN** kflow-explore 生成 functional-designs/
- **THEN** 内容聚焦用户视角（页面/操作/表单/规则）
- **AND** 不包含技术架构选型、数据模型设计、接口定义

#### Scenario: prototype 禁止输出业务规则变更
- **WHEN** kflow-prototype-design 生成 prototype.pen
- **THEN** 原型基于 functional-designs/ 的业务规则设计交互
- **AND** 不可以在原型设计过程中修改业务规则

#### Scenario: design 禁止输出功能设计
- **WHEN** kflow-design 生成 detailed-design.md
- **THEN** 内容聚焦技术视角（架构/数据模型/接口/NFR）
- **AND** 不修改 functional-designs/ 中的功能定义

### Requirement: 越界内容触发阶段回退提醒

系统 SHALL 当发现上游阶段产物存在问题时，记录到 skill-suggestion.md 并提示可能的阶段回退，但不可直接修改上游产物。

#### Scenario: design 发现功能设计不完整
- **WHEN** kflow-design 发现 functional-designs/ 缺失关键信息
- **THEN** 记录到 skill-suggestion.md
- **AND** 提示用户是否需要回退到 explore 阶段补充
- **AND** 不直接修改 functional-designs/ 内容

#### Scenario: prototype 发现功能点定义不清晰
- **WHEN** kflow-prototype-design 发现某功能点描述不足以支撑原型设计
- **THEN** 记录到 skill-suggestion.md
- **AND** 在当前能力范围内完成原型
- **AND** 提示用户需要回退 explore 补充功能点描述

### Requirement: 阶段门控包含 RELOAD 步骤

每个阶段的门控检查 SHALL 在检查文件存在性之后、进入核心执行流程之前，增加 RELOAD 步骤，强制执行基础信息文件的重读。门控检查 SHALL 按子变更类型区分适用性。

#### Scenario: 门控检查增强

- **WHEN** 任何阶段 Skill 进入执行流程
- **THEN** 门控检查 SHALL 在原有的文件存在性检查之后，增加 RELOAD 步骤
- **AND** RELOAD 步骤 SHALL 按照钩子配置表中该阶段定义的 RELOAD 清单，重新读取所有基础信息文件的最新内容
- **AND** RELOAD 步骤 SHALL 在阶段核心逻辑执行之前完成

#### Scenario: RELOAD 步骤阻塞

- **WHEN** RELOAD 步骤中某文件不存在或无法读取
- **THEN** SHALL 标记当前阶段为 ❌ 阻塞
- **AND** SHALL 提示缺失的文件路径
- **AND** SHALL NOT 使用过时的缓存内容继续执行

#### Scenario: RELOAD 与存在性检查的关系

- **WHEN** 现有门控检查已验证文件存在
- **THEN** RELOAD 步骤 SHALL 在存在性检查之后执行
- **AND** RELOAD 专注于读取最新内容（非检查存在性）
- **AND** 若文件在检查后被删除（极端情况），RELOAD 失败 SHALL 触发阻塞

## ADDED by phase-artifact-verification-and-input-alignment

### Requirement: Plan 阶段入口门控增强

系统 SHALL 在 plan 阶段入口门控中增加以下检查项。

#### Scenario: CONTEXT.md 存在性检查
- **WHEN** 进入 plan 阶段 [全部]
- **THEN** 门控 SHALL 检查 CONTEXT.md 文件存在
- **AND** 不存在时 SHALL 提示「缺少项目级领域词汇表，请先完成设计探索阶段」

#### Scenario: functional-designs/ 存在性检查
- **WHEN** 进入 plan 阶段 [全部]
- **THEN** 门控 SHALL 检查 functional-designs/index.md 存在
- **AND** 不存在时 SHALL 提示「缺少功能设计文档，请先完成设计探索阶段」

#### Scenario: api-tests/ 存在性检查
- **WHEN** 进入 plan 阶段 [全部]
- **THEN** 门控 SHALL 检查 api-tests/index.md 存在
- **AND** 不存在时 SHALL 提示「缺少接口测试用例，请先完成详细设计阶段」

#### Scenario: e2e-tests/ 条件存在性检查
- **WHEN** 进入 plan 阶段 [前端SC + 前后端项目]
- **THEN** 门控 SHALL 检查 e2e-tests/index.md 存在
- **AND** 不存在时 SHALL 提示「缺少 E2E 测试用例，请先完成详细设计阶段」
- **AND** [后端子变更] SHALL 跳过此检查

### Requirement: Code 阶段入口门控增强

系统 SHALL 在 code 阶段入口门控中增加子变更类型判断和前端输入源检查。

#### Scenario: 子变更类型判断分支
- **WHEN** 进入 code 阶段
- **THEN** 系统 SHALL 读取 detailed-design.md 中子变更划分章节确定当前子变更类型
- **AND** SHALL 根据子变更类型选择对应的门控检查项

#### Scenario: 前端子变更 prototype/* 强制检查
- **WHEN** 进入 code 阶段 [前端SC]
- **THEN** 门控 SHALL 检查 prototype/index.html 存在
- **AND** SHALL 检查 prototype/design-tokens.css 存在
- **AND** SHALL 检查 prototype/element-coverage-tree.md 存在
- **AND** 任一文件缺失 SHALL 阻塞编码，提示「前端子变更缺少原型核心产物」

#### Scenario: CONTEXT.md 存在性检查
- **WHEN** 进入 code 阶段 [全部]
- **THEN** 门控 SHALL 检查 CONTEXT.md 存在
- **AND** 不存在时 SHALL 提示「缺少项目级领域词汇表，代码命名无法对齐」

### Requirement: E2E 测试阶段入口门控增强

系统 SHALL 在 e2e-test 阶段入口门控中增加 element-coverage-tree.md 检查。

#### Scenario: element-coverage-tree.md 存在性检查
- **WHEN** 进入 e2e-test 阶段 [前端项目]
- **THEN** 门控 SHALL 检查 element-coverage-tree.md 存在（prototype/ 或 e2e-tests/ 目录下）
- **AND** 不存在时 SHALL 提示「缺少元素覆盖树，请重新执行详细设计阶段生成」
- **AND** [纯后端项目] SHALL 跳过此检查

### Requirement: 集成测试入口设计产物回溯验证

系统 SHALL 在 integration-test 阶段入口门控中增加设计阶段产物完整性快速检查。

#### Scenario: 设计产物回溯验证
- **WHEN** 进入 integration-test 阶段 [全部]
- **THEN** 门控 SHALL 快速检查 functional-designs/index.md 和 detailed-design.md 存在且非空
- **AND** [前后端项目 + 原型未跳过] SHALL 检查 prototype/index.html 存在
- **AND** 缺失时 SHALL 提示「设计阶段产物不完整，请先执行 kflow-verify 诊断」

### Requirement: 门控规则显式标注 SC 类型适用性

系统 SHALL 对所有门控规则显式标注适用子变更类型。

#### Scenario: 门控规则标注格式
- **WHEN** 门控规则被定义或修改
- **THEN** 每条规则 SHALL 标注适用性：`[全部]` / `[后端子变更]` / `[前端子变更]` / `[前端项目]` / `[纯后端项目]`
- **AND** 标注 SHALL 用于门控执行时判断是否应用该规则

## ADDED by frontend-implementation-and-phase-guards

### Requirement: 归档阶段禁止自动流转

系统 SHALL 确保归档阶段不因前置阶段完成而自动触发，MUST 用户显式确认后方可进入。

#### Scenario: 审计通过后不自动调度归档

- **WHEN** kflow-audit 阶段完成且审计通过
- **THEN** 系统 SHALL NOT 自动调用 kflow-archive
- **AND** 系统 SHALL 通过 AskUserQuestion 获取用户显式确认
- **AND** Archive 是 KFlow 体系中唯一禁止自动流转的阶段

#### Scenario: 归档确认后正常流转

- **WHEN** 用户显式确认进入归档
- **THEN** 系统 SHALL 正常进入 kflow-archive 阶段
- **AND** 按现有归档流程执行

### Requirement: 前端子变更依赖 API 契约规则

系统 SHALL 定义前端子变更的特殊依赖规则：依赖 API 契约（design 阶段已定义）而非后端子变更编码完成。

#### Scenario: 前端子变更的启动依赖判定

- **WHEN** 系统检查前端子变更的启动依赖
- **THEN** 依赖条件 SHALL 判定为：detailed-design.md 中对应 API 契约章节存在且状态为 ✅ 完成
- **AND** SHALL NOT 要求后端子变更编码状态为 ✅ 完成
- **AND** 前端子变更可与后端子变更并行启动

#### Scenario: 前端子变更使用 mock 数据开发

- **WHEN** 前端子变更进入编码阶段
- **AND** 后端子变更编码尚未完成
- **THEN** 前端子变更 SHALL 基于 API 契约使用 mock 数据进行开发
- **AND** 后端编码完成后执行集成对接（替换 mock 为真实 API）
