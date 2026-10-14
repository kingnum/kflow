# Spec Delta

## MODIFIED Requirements

### Requirement: 变更流程强制规则 section 扩展

kflow-init SHALL 向 CLAUDE.md 的「变更流程强制规则」section 注入跨 skill 的路由约束、用户接口约定与流程概览。使用现有 marker `## 变更流程强制规则` 幂等更新。该 section SHALL NOT 包含由某个 skill 在自身执行流程中完成的步骤。

#### Scenario: 注入扩展的流程规则

- **WHEN** 执行 kflow-init
- **THEN** 系统在「变更流程强制规则」section 中包含以下规则：
  - 新变更由 `kflow-explore` 承接（变更类型分类、命名、档位初判、冲突预检均在该阶段完成）
  - 阶段完成后自动衔接下一阶段，SHALL NOT 提示用户输入推进指令
  - 中断恢复使用「恢复 {change-name}」；「继续 {change-name}」为轻量推进
  - 流程阶段列表
  - 查看状态使用「状态」「进度」关键词
- **AND** 该 section SHALL NOT 要求用户变更先经 `kflow-guide` 流程指引
- **AND** SHALL NOT 禁止直接调用阶段 Skill
- **AND** 该 section SHALL NOT 包含归档后 git commit 询问、非 git 仓库时的 git init 询问等 skill 内部执行步骤
- **AND** SHALL NOT 包含仓库根 `VERSION` 文件、`scripts/` 下的技能仓库脚本、`targets/` 打包产物或 `README.md` 版本条目

#### Scenario: 已有流程规则的增量更新

- **WHEN** CLAUDE.md 已有「变更流程强制规则」section 但其内容与当前模板版本不一致（含旧版仍含归档后 git commit 询问、版本自增或打包规则，或含 guide 前置强制与阶段 Skill 禁用规则的情形）
- **THEN** 系统用当前模板内容替换该 section
- **AND** 替换后的 section SHALL NOT 含上述 git 与版本自增规则
- **AND** SHALL NOT 含要求用户变更先经 `kflow-guide` 或禁止直接调用阶段 Skill 的规则
- **AND** 该 section 之外的内容 SHALL NOT 被修改
