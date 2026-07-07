## ADDED Requirements

### Requirement: 归档后 git commit

kflow-archive SHALL 在归档流程完成后分析归档内容、生成一行摘要、执行 git commit。详见 `post-archive-git-commit` spec。

#### Scenario: 归档完成后执行提交

- **WHEN** 归档流程完成（文件移动、索引更新均已完成）
- **THEN** 系统从归档目录读取变更摘要
- **AND** 生成一行中文提交信息（格式：`归档变更 {name}: {一行摘要}`）
- **AND** 执行 `git add -A` 和 `git commit -m "{提交信息}"`
- **AND** 验证提交成功

#### Scenario: 归档提交失败不阻塞归档

- **WHEN** git commit 执行失败（如无变更、git 配置问题）
- **THEN** 系统提示失败原因
- **AND** 归档操作本身不受影响
- **AND** 提示用户手动提交
