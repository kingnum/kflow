## Why

当前 Git commit 触发点分散在 4 个 Skill 中（kflow-init、kflow-guide、kflow-plan、kflow-archive），形成 5 条以上强制规则，增加执行复杂度和用户心智负担。同时上一个变更 `skill-packaging-and-version-unification` 将项目级机制（版本自增+打包）错误注入到 `kflow-archive` Skill 的设计和运行时中，需纠正。整体简化为仅 2 个询问式触发点。

## What Changes

- **BREAKING**: 删除 `kflow-guide` 的 PRECOMMIT 步骤（新变更前 git 状态检查→分析→总结→确认→提交）
- **BREAKING**: 删除 `kflow-plan` 任务模板中的 Step 8 提交变更步骤及自审中的提交粒度检查项
- **BREAKING**: 删除 `pre-change-git-commit` spec（整个 capability 移除）
- 修正 `kflow-archive`：移除 VERSION + PACKAGE 步骤（纠正 top 变更的错误注入），COMMIT 从强制改为 AskUserQuestion 询问
- 修正 `kflow-init`：删除规则 #9（新变更前检查 git），规则 #10 从「必须 git commit」改为「询问是否 git init」
- CLAUDE.md 中 git 相关强制规则从「必须执行」改为「询问是否执行」，保留版本自增+打包规则（项目级，位置正确）
- 相应更新所有受影响的 openspec specs 和设计文档

## Capabilities

### New Capabilities

（无新增能力——本次为简化和纠正）

### Modified Capabilities

- `post-archive-git-commit`: 从「SHALL 执行 git commit」改为「SHALL 询问用户是否提交」
- `devflow-archive`: 移除 VERSION + PACKAGE 步骤描述，COMMIT 步骤改为询问模式
- `devflow-init`: 规则 #9 删除，#10 从强制 commit 改为询问 git init
- `init-claude-md-injection`: 注入 CLAUDE.md 的 git 规则条款从 3 条改为 2 条
- `devflow-guide`: 删除「新变更前 git commit 检查」requirement
- `plan-self-review`: 删除「提交粒度」检查项

### Removed Capabilities

- `pre-change-git-commit`: 整个 capability 删除（新变更前的 git 检查机制不再存在）

## Impact

- 受影响的运行时 Skill: `kflow-guide`, `kflow-plan`, `kflow-init`, `kflow-archive`
- 受影响的 OpenSpec spec: 7 个（1 删除 + 6 修改）
- 受影响的文档: `docs/designs/core-mechanisms/08-governance.md`, 4 个设计文档
- 不改变版本自增+打包的项目级机制（保留在 CLAUDE.md + scripts/package-skills.sh）
