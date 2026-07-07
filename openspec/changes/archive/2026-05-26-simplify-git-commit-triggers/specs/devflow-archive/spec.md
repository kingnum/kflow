## MODIFIED Requirements

### Requirement: 归档后 git commit

kflow-archive SHALL 在归档流程完成后分析归档内容、生成一行摘要、通过 AskUserQuestion 询问用户是否提交。详见 `post-archive-git-commit` spec。

#### Scenario: 归档完成后询问提交

- **WHEN** 归档流程完成（文件移动、索引更新均已完成）
- **THEN** 系统从归档目录读取变更摘要
- **AND** 生成一行中文提交信息（格式：`归档变更 {name}: {一行摘要}`）
- **AND** 使用 AskUserQuestion 询问用户「确认提交」「修改提交信息」或「跳过本次提交」
- **AND** 用户确认后执行 `git add -A` 和 `git commit -m "{提交信息}"`

#### Scenario: 归档提交失败不阻塞归档

- **WHEN** git commit 执行失败（如无变更、git 配置问题）
- **THEN** 系统提示失败原因
- **AND** 归档操作本身不受影响
- **AND** 提示用户手动提交

#### Scenario: 用户选择跳过提交

- **WHEN** 用户选择「跳过本次提交」
- **THEN** 系统跳过 COMMIT 步骤
- **AND** 输出提醒：归档内容尚未提交

## REMOVED Requirements

### Requirement: 版本自增与打包步骤

**Reason**: 版本自增判定和 `scripts/package-skills.sh` 打包是项目级 CI/CD 机制（kflow-devflow-skills 开发仓库自身），被前一变更错误注入到 `kflow-archive` Skill 中。它们保留在 CLAUDE.md 项目规则中，不属于通用 Skill 功能。

**Migration**: 无需迁移——版本自增+打包逻辑始终在 CLAUDE.md 中正确存在，仅从 kflow-archive SKILL.md 中移除。
