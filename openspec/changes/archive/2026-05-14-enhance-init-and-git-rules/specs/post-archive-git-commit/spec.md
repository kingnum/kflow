## ADDED Requirements

### Requirement: 归档后自动分析生成提交信息

kflow-archive SHALL 在归档流程的 COMPLETE 步骤之后，分析本次归档涉及的变更内容并生成一行摘要提交信息。

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

### Requirement: 归档后执行 git commit

kflow-archive SHALL 在生成提交信息后执行 git add 和 git commit。

#### Scenario: 正常执行归档提交

- **WHEN** 提交信息生成完成
- **THEN** 系统执行 `git add -A`
- **AND** 执行 `git commit -m "{提交信息}"`
- **AND** 验证提交成功（`git status` 确认干净）

#### Scenario: 归档提交失败处理

- **WHEN** git commit 执行失败（如无变更内容、git 配置问题）
- **THEN** 系统提示用户提交失败原因
- **AND** 归档操作本身不受影响（已完成的文件移动和索引更新保留）
- **AND** 提示用户手动提交

#### Scenario: 用户明确要求不提交

- **WHEN** 用户在归档前指明不进行 git commit
- **THEN** 系统跳过 COMMIT 步骤
- **AND** 输出提醒：归档内容尚未提交
