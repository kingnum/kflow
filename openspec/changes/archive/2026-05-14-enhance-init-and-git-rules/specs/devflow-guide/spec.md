## ADDED Requirements

### Requirement: 新变更前 git commit 检查

kflow-guide SHALL 在引导用户进入新变更流程前，检查 git 工作区状态。有未提交变更时分析变更性质、生成一行摘要、提示用户确认提交或跳过。详见 `pre-change-git-commit` spec。

#### Scenario: 新变更前检测到未提交变更

- **WHEN** 用户请求开始新变更
- **AND** `git status --porcelain` 有输出
- **THEN** 系统暂停引导流程
- **AND** 分析未提交变更的范围和性质（通过 `git diff --stat` 和 `git diff`）
- **AND** 基于文件路径推断变更类型（归档类/产品文档类/代码变更类）
- **AND** 生成一行中文摘要提交信息
- **AND** 使用 AskUserQuestion 提示用户「确认提交」「修改提交信息」或「跳过本次提交」

#### Scenario: 用户确认提交后继续引导

- **WHEN** 用户选择「确认提交」或「修改提交信息」后提交
- **AND** git commit 成功
- **THEN** 系统继续进入正常的意图识别和变更创建引导流程

#### Scenario: 用户跳过提交后继续引导

- **WHEN** 用户选择「跳过本次提交」
- **THEN** 系统记录未提交提醒到 checkpoint
- **AND** 继续进入正常引导流程
