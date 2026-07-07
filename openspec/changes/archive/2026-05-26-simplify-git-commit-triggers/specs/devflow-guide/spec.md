## REMOVED Requirements

### Requirement: 新变更前 git commit 检查

**Reason**: Git commit 触发点简化为仅 2 个（init 询问 git init + 归档后询问 commit）。新变更前的强制检查步骤在简化方案中不再需要。

**Migration**: 用户可在开始新变更前自行通过 `git status` 检查工作区状态并决定是否提交。无自动替代机制。

#### Scenario: 新变更前检测到未提交变更

<!-- 删除此 scenario -->

#### Scenario: 用户确认提交后继续引导

<!-- 删除此 scenario -->

#### Scenario: 用户跳过提交后继续引导

<!-- 删除此 scenario -->
