## Purpose

定义 CLAUDE.md marker 注入机制——kflow-init 向 CLAUDE.md 注入「项目画像」「变更流程强制规则」「Skill 改进建议自动捕获」三个受管 marker 区块，并创建一个不受管的「项目自定义规则」区块，支持幂等更新、版本判据替换与项目自定义内容的保护。

本能力是 CLAUDE.md marker 注入规则的唯一权威定义位置：上述 marker 区块的内容要求、版本判据、替换策略与项目自定义规则区块的保护规则均在此定义，其他能力 SHALL NOT 重复定义同一 marker 的注入规则。

## Requirements

### Requirement: 项目画像 section 注入

kflow-init SHALL 向 CLAUDE.md 注入「项目画像」section，包含项目特定上下文信息。注入使用 `## 项目画像` 作为唯一 marker，支持幂等更新。首次注入或信息变更时替换整个 section。CLAUDE.md 不存在时跳过注入。

该 section 的「项目类型」字段 SHALL 作为项目类型项目级记录的唯一真源，供变更创建链路（kflow-guide、kflow-explore）读取；其读取优先级高于 `docs/toolchain.md` 头部的同名字段。项目类型的检测、确认、继承与消费规则由 `project-type-detection` 能力定义，本能力 SHALL NOT 重复定义。

#### Scenario: 首次注入项目画像

- **WHEN** CLAUDE.md 存在且不包含 `## 项目画像` marker
- **THEN** 系统在 CLAUDE.md 末尾追加项目画像 section
- **AND** section 包含：项目类型、语言、框架、数据库、构建工具、关键目录、入口文件、产品文档状态
- **AND** 标注生成来源和时间戳（`> 来源: kflow-init | 扫描时间: {YYYY-MM-DD HH:MM}`）

#### Scenario: 重复执行 init 时幂等更新项目画像

- **WHEN** CLAUDE.md 已包含 `## 项目画像` marker
- **THEN** 系统重新扫描项目并替换 `## 项目画像` 到下一个 `## ` 之间的内容
- **AND** 更新扫描时间戳
- **AND** 不修改 CLAUDE.md 中其他 section 的内容

#### Scenario: re-init 记录一致时静默沿用项目类型

- **WHEN** CLAUDE.md 已包含「## 项目画像」marker 且项目类型行已有值
- **AND** 重新扫描结果与该值一致
- **THEN** 系统静默沿用该值
- **AND** SHALL NOT 使用 AskUserQuestion 询问项目类型

#### Scenario: re-init 记录冲突时请求裁决项目类型

- **WHEN** CLAUDE.md 已包含「## 项目画像」marker 且项目类型行已有值
- **AND** 重新扫描结果与该值冲突
- **THEN** 系统使用 AskUserQuestion 请求用户裁决
- **AND** 按裁决结果更新项目类型行

#### Scenario: 项目画像字段 — 新项目

- **WHEN** 项目无前端依赖且无源码目录
- **THEN** 技术栈字段标注为"待确定"
- **AND** 关键目录和入口文件标注为"待确定"
- **AND** 产品文档状态全部标注为 ❌ 不存在

#### Scenario: 项目画像字段 — 老项目

- **WHEN** 项目有完整的源码和配置文件
- **THEN** 系统从 package.json 提取语言、框架、构建工具
- **AND** 从目录结构推断关键目录和入口文件
- **AND** 从数据库配置提取数据库类型
- **AND** 检测产品文档存在性并标注状态

### Requirement: 变更流程强制规则 section 扩展

kflow-init SHALL 向 CLAUDE.md 的「变更流程强制规则」section 注入跨 skill 的路由约束、用户接口约定与流程概览。使用现有 marker `## 变更流程强制规则` 幂等更新。该 section SHALL NOT 包含由某个 skill 在自身执行流程中完成的步骤。

#### Scenario: 注入扩展的流程规则

- **WHEN** 执行 kflow-init
- **THEN** 系统在「变更流程强制规则」section 中包含以下规则：
  - 所有变更须先经 `kflow-guide` 流程指引
  - 新变更经 guide 引导后进入 `kflow-explore`
  - 中断恢复使用「继续 {change-name}」
  - 禁止直接调用阶段 Skill 绕过 guide
  - 流程阶段列表
  - 查看状态使用「状态」「进度」关键词
- **AND** 该 section SHALL NOT 包含归档后 git commit 询问、非 git 仓库时的 git init 询问等 skill 内部执行步骤
- **AND** SHALL NOT 包含仓库根 `VERSION` 文件、`scripts/` 下的技能仓库脚本、`targets/` 打包产物或 `README.md` 版本条目

#### Scenario: 已有流程规则的增量更新

- **WHEN** CLAUDE.md 已有「变更流程强制规则」section 但其内容与当前模板版本不一致（含旧版仍含归档后 git commit 询问、版本自增或打包规则的情形）
- **THEN** 系统用当前模板内容替换该 section
- **AND** 替换后的 section SHALL NOT 含上述 git 与版本自增规则
- **AND** 该 section 之外的内容 SHALL NOT 被修改

### Requirement: Marker 版本判据与替换兜底

kflow-init SHALL 以自身 SKILL.md front matter 的 `version` 字段作为所注入 marker section 的模板版本标识。版本来源 SHALL NOT 引用消费方项目中可能不存在的文件（如仓库根 `VERSION` 文件）。

#### Scenario: marker 版本与当前模板版本一致

- **WHEN** CLAUDE.md 中 marker 区块标注的版本等于 kflow-init 当前的 `version` 字段值
- **THEN** 系统 SHALL 仅更新该区块的时间戳
- **AND** SHALL NOT 替换区块内容

#### Scenario: marker 版本与当前模板版本不一致

- **WHEN** CLAUDE.md 中 marker 区块标注的版本不等于 kflow-init 当前的 `version` 字段值
- **THEN** 系统 SHALL 用当前模板内容全量替换该区块内容

#### Scenario: marker 版本缺失或无法解析

- **WHEN** CLAUDE.md 中 marker 区块未标注版本，或其版本值无法解析
- **THEN** 系统 SHALL 判定该区块与当前模板版本不同
- **AND** SHALL 用当前模板内容全量替换该区块内容

### Requirement: 项目自定义规则区块保护

kflow-init SHALL 为项目自行维护的规则提供独立 marker 区块 `## 项目自定义规则`。该区块 SHALL NOT 纳入 kflow-init 的模板替换范围。

#### Scenario: 首次注入创建项目自定义区块

- **WHEN** 执行 kflow-init 且 CLAUDE.md 不含 `## 项目自定义规则` marker
- **THEN** 系统 SHALL 在 CLAUDE.md 中创建该区块
- **AND** 区块内 SHALL 标注该区块由项目自行维护、kflow-init 不覆盖其内容

#### Scenario: re-init 不覆盖项目自定义规则

- **WHEN** 执行 kflow-init 且 CLAUDE.md 已含 `## 项目自定义规则` marker
- **THEN** 系统 SHALL NOT 修改该区块内容
- **AND** SHALL NOT 因模板版本变化而替换或删除该区块
- **AND** 用户在框架管理区块之外新增的内容 SHALL NOT 被删除

### Requirement: Skill 改进建议自动捕获 marker 注入

kflow-init SHALL 向 CLAUDE.md 注入 `## Skill 改进建议自动捕获` section，定义 AI 对话中的三种触发模式。使用 `## Skill 改进建议自动捕获` 作为唯一 marker 幂等更新。

#### Scenario: 注入自动捕获规则

- **WHEN** 执行 kflow-init
- **AND** CLAUDE.md 不存在 `## Skill 改进建议自动捕获` marker
- **THEN** 系统在 CLAUDE.md 中追加该 section
- **AND** section 内容 SHALL 定义三种触发模式和处理规则：
  - 「因...无法...」→ 记录阻塞原因和失败的执行路径
  - 「因...导致...」→ 记录因果链和受影响的阶段
  - 用户纠正后 AI 回复中的「你说得对」等附和 → 记录用户的纠正内容
- **AND** 标注来源为 kflow-init 和注入时间戳

#### Scenario: 自动捕获规则已存在的幂等更新

- **WHEN** CLAUDE.md 已包含 `## Skill 改进建议自动捕获` marker
- **THEN** 系统 SHALL NOT 重复追加该 section
- **AND** SHALL 按 marker 版本判据决定是否更新该 section 内容

### Requirement: 产品文档状态检测

系统 SHALL 在注入项目画像时检测产品文档的存在状态，并在 re-init 时重新扫描更新。

#### Scenario: 检测产品文档

- **WHEN** 执行 kflow-init
- **THEN** 系统检测以下文件的存在性：
  - `CONTEXT.md`（项目根目录）
  - `docs/designs/index.md`（产品设计入口）
  - `docs/designs/domains/`（领域文档目录，统计文件数）
  - `docs/designs/architecture.md`（架构全景）
  - `docs/designs/data-model.md`（数据模型）
  - `docs/designs/api-catalog.md`（API 目录）
  - `docs/designs/nfr-baseline.md`（NFR 基线）
- **AND** 每个文件标注 ✅ 已就绪 或 ❌ 不存在

#### Scenario: Re-init 更新产品文档状态

- **WHEN** 用户重新执行 kflow-init
- **THEN** 系统重新扫描产品文档状态
- **AND** 更新项目画像 section 中的状态标记
- **AND** 领域文档数量反映最新实际数量

### Requirement: 首次 init 时 git 仓库检测

kflow-init SHALL 在完成首次项目初始化后，检测当前目录是否为 git 仓库，若非仓库则询问用户是否执行 git init。

#### Scenario: 目录已是 git 仓库

- **WHEN** kflow-init 完成初始化流程
- **AND** `git rev-parse --git-dir` 成功
- **THEN** 系统跳过 git 初始化
- **AND** 直接进入 COMPLETE 步骤

#### Scenario: 目录非 git 仓库时询问

- **WHEN** kflow-init 完成初始化流程
- **AND** `git rev-parse --git-dir` 失败
- **THEN** 系统使用 AskUserQuestion 询问用户是否执行 git init
- **AND** 提供「初始化 git 仓库」和「跳过」两个选项

#### Scenario: 用户选择初始化

- **WHEN** 用户选择「初始化 git 仓库」
- **THEN** 系统执行 `git init`
- **AND** git init 失败不阻塞 init 流程

#### Scenario: 用户选择跳过

- **WHEN** 用户选择「跳过」
- **THEN** 系统不执行 git init
- **AND** 提示用户可后续手动初始化
