# Proposal

## Why

`kflow-init` 注入到消费方项目 CLAUDE.md 的「变更流程强制规则」section，混入了不属于该 section 职责的内容：

1. **作用域泄漏**：规则 7 写入了 KFlow Skills **开发仓库**特有的元工作流——读取 `VERSION`、判定版本自增级别、运行 `scripts/sync-version.sh`、更新 `README.md` 版本条目、运行 `scripts/package-skills.sh` 打包为 `targets/*.zip`。消费方项目不存在 `VERSION`、`scripts/`、`targets/`，该规则无法执行，且与本仓库 `/opsx:archive` 的归档后规则完全错配。
2. **职责错位**：规则 7、8 描述的是 `kflow-archive` 步骤 11 COMMIT 与 `kflow-init` 步骤 13 GITINIT 的 **skill 内部执行步骤**，属于各 SKILL.md 的职责；写入消费方 CLAUDE.md 构成双重定义，且与规范副本（`post-archive-git-commit`）不一致。
3. **实现偏离规格**：`post-archive-git-commit` 与 `init-claude-md-injection` 的原始要求均只含「归档后询问是否提交」「非 git 仓库时询问 git init」，从未要求版本自增与打包。泄漏发生在设计文档（`docs/designs/skills/kflow-init.md`、`08-governance.md`）被照抄进运行时模板的链路中。
4. **存量污染无法自愈**：「变更流程强制规则」Marker 的版本判据是「参见 VERSION 文件」，消费方读不到该文件，判据悬空 → 即使修正模板，`re-init` 也可能判定为无变化而不替换，存量消费方 CLAUDE.md 中的错误规则将长期滞留。

该 section 应只承载**跨 skill 的路由约束与用户接口约定**；skill 内部执行细节归各 SKILL.md。本次修正同时为注入模板建立作用域守卫，防止同类泄漏复发。

## What Changes

- 从 `kflow-init` 注入模板的「变更流程强制规则」中**移除规则 7（归档后 git commit + 版本自增 + 打包）与规则 8（首次 init 时询问 git init）**，section 收敛为 6 条路由约束/用户接口/流程概览规则。
- **移除**「变更流程强制规则」section 头部对 VERSION 文件的悬空引用；Marker 版本判据改用 `kflow-init` 自身 front matter 的 `version` 字段。
- **Marker 替换判据增加兜底**：marker 版本缺失或无法解析时，视为与当前版本不同，执行全量替换——确保含旧规则的存量消费方 CLAUDE.md 在 `re-init` 时被覆盖。
- **框架规则与项目自定义规则分离**：`kflow-init` 只替换自己管理的 marker 区块，为项目自定义规则提供独立 marker 区块，`re-init` 不覆盖项目自行维护的内容。
- **新增注入模板作用域守卫校验**：校验 `kflow-init` 注入消费方 CLAUDE.md 的模板内容不含技能开发仓库特有词汇（`scripts/`、`targets/`、`VERSION` 文件、README 版本条目等）。
- **规格去重**：`devflow-init` 与 `init-claude-md-injection` 重复定义了同一「变更流程强制规则 section 扩展」Requirement，权威收敛至 `init-claude-md-injection`，`devflow-init` 侧不再重复定义注入规则。
- **设计文档同步**：`docs/designs/skills/kflow-init.md` 与 `docs/designs/core-mechanisms/08-governance.md` 中的同款注入模板与 git 规则描述同步修正。
- 保持不动：`kflow-archive` 的归档后 git commit 行为、`kflow-init` 步骤 13 的 git 仓库检测行为、`unified-version` 与 `skill-packaging` 的本仓库元工作流规则。

## Capabilities

### New Capabilities

- `injection-scope-guard`: KFlow 注入模板作用域守卫——定义并校验 `kflow-init` 注入消费方 CLAUDE.md 的模板内容仅包含消费态规则，不含技能开发仓库特有的路径、脚本与流程词汇，覆盖校验对象、校验项、失败处理与校验落点。

### Modified Capabilities

- `init-claude-md-injection`: 「变更流程强制规则 section 扩展」Requirement 移除注入 git 规则的要求，改为只承载路由约束与用户接口约定；新增 Marker 版本判据（以 `kflow-init` front matter `version` 为准，含无法解析时全量替换的兜底）与项目自定义规则区块不被覆盖的要求；Purpose 中的「双层 marker」表述与实现的三层 marker 对齐。
- `devflow-init`: 移除与 `init-claude-md-injection` 重复的「变更流程强制规则 section 扩展」Requirement 中注入 git 规则的部分，收敛为对该能力的引用，保留本能力独有的工具推荐矩阵与 GAP 检测要求。

## Impact

- **运行时模板**：`skills/kflow-init/SKILL.md`（步骤 11 INJECT 的 Marker 2 模板、幂等策略的版本判据与替换条件、section 边界识别）
- **设计文档**：`docs/designs/skills/kflow-init.md`、`docs/designs/core-mechanisms/08-governance.md`
- **规格**：`openspec/specs/init-claude-md-injection/`、`openspec/specs/devflow-init/`、新增 `openspec/specs/injection-scope-guard/`
- **校验脚本**：`scripts/` 下的注入模板作用域校验（作为既有校验脚本模式的扩展）
- **存量消费方项目**：CLAUDE.md 中已注入的「变更流程强制规则」section 在下次 `kflow-init`（re-init）时被替换为修正版本，错误规则随之清除；项目自定义内容不受影响
- **不涉及**：`kflow-archive`、`post-archive-git-commit`、`unified-version`、`skill-packaging` 的行为与规格
