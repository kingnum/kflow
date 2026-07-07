## ADDED Requirements

### Requirement: 新变更前 git 状态检查

kflow-guide SHALL 在引导用户进入新变更流程前，检查 git 工作区状态。有未提交变更时进入分析-总结-确认-提交流程。

#### Scenario: 工作区干净时直接进入引导

- **WHEN** 用户请求开始新变更
- **AND** `git status --porcelain` 返回空
- **THEN** 系统直接进入正常的意图识别和变更创建引导流程
- **AND** 不展示 git 相关提示

#### Scenario: 有未提交变更时触发分析

- **WHEN** 用户请求开始新变更
- **AND** `git status --porcelain` 有输出（存在未暂存或未提交的变更）
- **THEN** 系统暂停引导流程
- **AND** 进入变更分析步骤

#### Scenario: 首次使用无提交历史

- **WHEN** 用户请求开始新变更
- **AND** 项目尚无任何 git 提交（`git rev-parse HEAD` 失败）
- **THEN** 系统提示"项目尚无提交记录，建议先执行初始提交"
- **AND** 不强制要求提交，允许继续

### Requirement: 变更内容分析

系统 SHALL 通过 `git diff` 分析未提交变更的范围和性质，推断变更类型以生成准确的提交摘要。

#### Scenario: 分析变更文件范围

- **WHEN** 检测到未提交变更
- **THEN** 系统执行 `git diff --stat` 获取变更文件列表和行数统计
- **AND** 执行 `git diff` 获取具体变更内容（限制前 200 行）

#### Scenario: 推断变更性质 — 归档类

- **WHEN** 变更文件路径包含 `docs/archive/` 前缀
- **THEN** 系统识别为"归档变更"类型
- **AND** 从路径提取变更名称（如 `docs/archive/2026-05-14-add-2fa/` → `add-2fa`）

#### Scenario: 推断变更性质 — 产品文档类

- **WHEN** 变更文件路径包含 `docs/designs/domains/` 或 `docs/designs/*.md`
- **THEN** 系统识别为"产品文档更新"类型

#### Scenario: 推断变更性质 — 代码变更类

- **WHEN** 变更文件路径不匹配任何已知文档模式
- **THEN** 系统识别为"代码变更"类型
- **AND** 从文件路径中提取模块名作为摘要关键词

### Requirement: 提交信息生成与确认

系统 SHALL 基于变更分析结果生成一行中文摘要，通过 AskUserQuestion 提示用户确认、修改或跳过。

#### Scenario: 生成一行摘要并展示

- **WHEN** 变更分析完成
- **THEN** 系统按格式 `{动词}: {一行中文摘要}` 生成提交信息
- **AND** 展示：提交信息预览 + 变更文件列表概要
- **AND** 使用 AskUserQuestion 提供三个选项：
  - 「确认提交」— 以预览信息执行 git commit
  - 「修改提交信息」— 用户自行输入提交信息后提交
  - 「跳过本次提交」— 不提交，继续进入变更流程（记录 checkpoint）

#### Scenario: 用户确认后执行提交

- **WHEN** 用户选择「确认提交」
- **THEN** 系统执行 `git add -A`
- **AND** 执行 `git commit -m "{提交信息}"`
- **AND** 提交成功后进入正常引导流程

#### Scenario: 用户选择跳过

- **WHEN** 用户选择「跳过本次提交」
- **THEN** 系统不执行 commit
- **AND** 记录未提交提醒到当前活跃变更的 checkpoint
- **AND** 继续进入正常引导流程

### Requirement: 提交信息格式规范

系统 SHALL 使用简洁的一行中文摘要作为 git commit 信息，不要求多行格式。

#### Scenario: 归档变更类提交

- **WHEN** 变更性质为归档类
- **THEN** 提交信息格式为 `归档变更 {name}: {一行摘要}`
- **AND** 如 `归档变更 add-2fa: 新增双因素认证，更新认证域文档`

#### Scenario: 代码/文档变更类提交

- **WHEN** 变更性质为代码或文档类且非归档
- **THEN** 提交信息格式为 `{动词}: {一行摘要}`
- **AND** 动词从：新增、修复、更新、重构、移除 中选择
