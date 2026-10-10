# Spec Delta

## REMOVED Requirements

### Requirement: 变更流程强制规则 section 扩展

**Reason**: 本能力与 `init-claude-md-injection` 重复定义了同一 CLAUDE.md marker 区块的注入规则，同一 marker 的内容要求由两个能力分别规定，导致规则变更时两处定义易失去同步；本次作用域泄漏（注入模板中混入技能开发仓库特有的版本自增与打包流程）正是因该重复定义而未被发现。

此外该需求中的 git 规则要求已被判定为作用域错误：归档后 git commit 询问、非 git 仓库时的 git init 询问均为 skill 在自身执行流程中完成的步骤，分别由 `kflow-archive` 的归档流程与 `kflow-init` 的 git 仓库检测步骤承载，不属于消费方 CLAUDE.md 的强制规则。

该需求中的「Skill 改进建议自动捕获」注入要求与 `skill-suggestion-logging` 的记录规范及 `init-claude-md-injection` 的 marker 注入机制重叠。

**Migration**: CLAUDE.md marker 注入规则收敛至 `init-claude-md-injection`，由其统一承载「变更流程强制规则」「Skill 改进建议自动捕获」「项目自定义规则」三个 marker 的注入、版本判据与替换策略；阻塞模式、因果链模式、用户纠正附和模式的记录规范由 `skill-suggestion-logging` 承载；归档后 git commit 行为由 `post-archive-git-commit` 承载。本能力保留工具推荐矩阵 — 原型设计阶段多方案要求，该要求在本需求移除后不受影响。
