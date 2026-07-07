## Purpose

定义 CLAUDE.md 双层 marker 注入机制——kflow-init 向 CLAUDE.md 注入「项目画像」section 与扩展的「变更流程强制规则」section，支持幂等更新。

## Requirements

### Requirement: 项目画像 section 注入

kflow-init SHALL 向 CLAUDE.md 注入「项目画像」section，包含项目特定上下文信息。注入使用 `## 项目画像` 作为唯一 marker，支持幂等更新。首次注入或信息变更时替换整个 section。CLAUDE.md 不存在时跳过注入。

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

kflow-init SHALL 在「变更流程强制规则」section 中新增 git 相关规则。使用现有 marker `## 变更流程强制规则` 幂等更新。

#### Scenario: 注入扩展的流程规则

- **WHEN** 执行 kflow-init
- **THEN** 系统在「变更流程强制规则」section 中包含以下 git 规则：
  - 首次 init 时，若目录非 git 仓库，询问是否执行 git init
  - 归档完成后，询问是否将当前变更及相关文件提交 git

#### Scenario: 已有流程规则的增量更新

- **WHEN** CLAUDE.md 已有「变更流程强制规则」section 但不含 git 规则或 git 规则过时
- **THEN** 系统替换为包含最新 git 规则（2 条询问式）的版本
- **AND** 保留原有非 git 规则的内容结构

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
