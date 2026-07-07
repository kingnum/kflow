## MODIFIED Requirements

### Requirement: 归档后自动分析生成提交信息

kflow-archive SHALL 在归档流程完成后分析本次归档涉及的变更内容并生成一行摘要提交信息。

#### Scenario: 分析归档变更内容

- **WHEN** 归档流程完成（MOVE、UPDATE、INDEX 步骤均已执行）
- **THEN** 系统从归档目录 `docs/archive/{YYYY-MM-DD}-{change}/` 读取变更的功能设计和技术设计摘要
- **AND** 从产品文档变更中提取受影响的设计域
- **AND** 生成一行中文摘要

#### Scenario: 已完成的归档生成摘要

- **WHEN** 归档的变更为已完成状态
- **THEN** 提交信息格式为 `归档变更 {name}: {一行摘要}`
- **AND** 摘要概括变更的核心功能或修复内容
- **AND** 如涉及产品文档更新，摘要中包含受影响的设计域

#### Scenario: 未完成归档生成摘要

- **WHEN** 归档的变更为未完成状态
- **THEN** 提交信息格式为 `归档变更 {name}(未完成): {一行摘要}`
- **AND** 摘要包含归档原因

### Requirement: 归档后询问是否提交

kflow-archive SHALL 在生成提交信息后，通过 AskUserQuestion 询问用户是否执行 git commit，而非自动强制执行。

#### Scenario: 询问用户是否提交

- **WHEN** 提交信息生成完成
- **THEN** 系统使用 AskUserQuestion 展示提交信息预览和变更文件列表概要
- **AND** 提供三个选项：
  - 「确认提交」— 执行 git add -A && git commit -m "{提交信息}"
  - 「修改提交信息」— 用户输入修改后的信息后提交
  - 「跳过本次提交」— 不提交，输出提醒

#### Scenario: 用户确认后执行提交

- **WHEN** 用户选择「确认提交」或「修改提交信息」
- **THEN** 系统执行 `git add -A`
- **AND** 执行 `git commit -m "{提交信息}"`
- **AND** 验证提交成功（`git status` 确认干净）

#### Scenario: 提交失败处理

- **WHEN** git commit 执行失败（如无变更内容、git 配置问题）
- **THEN** 系统提示用户提交失败原因
- **AND** 归档操作本身不受影响（已完成的文件移动和索引更新保留）
- **AND** 提示用户手动提交

#### Scenario: 用户跳过提交

- **WHEN** 用户选择「跳过本次提交」
- **THEN** 系统跳过 COMMIT 步骤
- **AND** 输出提醒：归档内容尚未提交，请适时手动提交
