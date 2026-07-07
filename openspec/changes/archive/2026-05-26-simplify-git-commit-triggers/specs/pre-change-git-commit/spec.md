## REMOVED Requirements

### Requirement: 新变更前 git 状态检查

**Reason**: Git commit 触发点简化为仅 2 个（init 询问 git init + 归档后询问 commit）。新变更前的 git 检查属于过度干预，用户应有自主控制节奏的权利。

**Migration**: 用户可在开始新变更前自行通过 `git status` 检查工作区状态并决定是否提交。无自动替代机制。

### Requirement: 变更内容分析

**Reason**: 随「新变更前 git 状态检查」一同移除。分析-总结-确认-提交流程不再存在。

**Migration**: 无需迁移。

### Requirement: 提交信息生成与确认

**Reason**: 随「新变更前 git 状态检查」一同移除。

**Migration**: 无需迁移。

### Requirement: 提交信息格式规范

**Reason**: 随「新变更前 git 状态检查」一同移除。代码/文档变更类的 `{动词}: {摘要}` 格式不再使用。

**Migration**: 提交信息格式仅保留归档后 commit 的 `归档变更 {name}: {摘要}` 格式，定义在 `post-archive-git-commit` spec 中。
