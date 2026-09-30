# Tasks

## 1. 实现层措辞修正（设计文档 → SKILL.md 同步）

- [x] 1.1 修正 7 个执行类 SKILL.md 的分层加载措辞：`skills/kflow-plan`、`kflow-code`、`kflow-code-review`、`kflow-api-test`、`kflow-e2e-test`、`kflow-integration-test`、`kflow-bug-fix` 的 SKILL.md 中「kflow-shared 分层加载（基础层 + 执行层）」改为「分层加载（基础层 + 执行层）」。验证：grep 这 7 个文件无「kflow-shared」命中，且其列出的 references 路径仍为各 skill 自身路径。
- [x] 1.2 修正 2 个设计类 SKILL.md 的分层加载措辞：`skills/kflow-design/SKILL.md` 与 `skills/kflow-explore/SKILL.md` 中「kflow-shared 文件」「kflow-shared 分层加载」改为「分层加载」表述。验证：grep 这两个文件无「kflow-shared」命中，且第 1.1 条列出的三份 references 文件仍被引用。
- [x] 1.3 修正 `docs/designs/core-mechanisms/07-agent-model.md` §17：将「按阶段类型分层加载 kflow-shared 文件」改为「按阶段类型分层加载各 skill 的 `references/` 文件」，并将「kflow-shared 文件头部标注」改为「`references/` 文件头部标注」。验证：grep 该文件无「kflow-shared」命中，且 §17.1 的层级表与 `layered-context-loading` 能力一致。
- [x] 1.4 核对 `layered-context-loading` 能力的合规性：确认修正后，该能力「No reference to kflow-shared in loading instructions」场景在全部 skill 与核心机制文档中成立。验证：grep 全仓库 `skills/` 与 `docs/` 的加载指令语境无「kflow-shared」命中。

## 2. 项目文档修正

- [x] 2.1 修正 `README.md` 的目录结构速查：删除 `kflow-shared/` 子树，替换为各 skill 自包含的 `references/` 结构说明与 `kflow-code/scripts/with_server.py` 的位置。验证：速查区块不含 `kflow-shared/`，且列出的路径在仓库中存在。
- [x] 2.2 修正 `README.md` 的 FAQ「kflow-shared 是什么？」条目：改写为描述各 skill 通过自身 `references/hooks.md` 与 `references/service-lifecycle.md` 接入钩子机制，不再提及共享目录。验证：该条目不含 `kflow-shared`，且表述与 `phase-hooks`、`skill-self-contained` 一致。
- [x] 2.3 修正 `README.md` 的「阶段钩子」段落（约第 298 行）：「统一引用 `kflow-shared/phase-hooks.md`」改为「统一引用各阶段自身的 `references/hooks.md`」。验证：该段落不含 `kflow-shared`。
- [x] 2.4 修正 `README.md` 的两个失效文档链接（约第 345、346 行）：原指向 `.claude/skills/kflow-shared/phase-hooks.md` 与 `service-lifecycle.md` 的链接改为指向实际存在的路径或删除链接条目。验证：README 中所有 markdown 链接的目标路径在仓库中存在。
- [x] 2.5 核对 `README.md` 变更历史区段：确认其中提及 `kflow-shared` 的条目属于历史记录，保持原样不改写。验证：变更历史区段的条目数量与内容未变，且其 `kflow-shared` 命中被记为设计决策 5 的已知例外。

## 3. 设计文档层核对

- [x] 3.1 核对 `docs/designs/core-mechanisms/06-recovery.md` 与 `docs/designs/skills/kflow-resume.md` 的恢复协议引用目标。验证：两者均指向 `kflow-resume` 的 `references/recovery-protocol.md`，且该文件存在；无 `kflow-shared` 命中。
- [x] 3.2 核对 `docs/designs/core-mechanisms/04-gates-and-transitions.md` §6.3 与 `docs/designs/skills/kflow-archive.md` 的归档规则引用目标。验证：两者均指向 `kflow-archive` 的 `references/archive-rules.md`，且该文件存在；无 `kflow-shared` 命中。
- [x] 3.3 核对 `docs/designs/skills/kflow-init.md` 与 `docs/designs/skills/kflow-api-test.md`、`kflow-e2e-test.md`、`kflow-integration-test.md` 中对权限声明与服务脚本的引用目标。验证：分别指向 `kflow-init/references/permission-model.md` 与 `kflow-code/scripts/with_server.py`，且这些文件存在。

## 4. 全仓库残留校验

- [ ] 4.1 校验 `openspec/specs/` 无失效引用：grep 全部规格文件，确认已无「作为唯一权威文件」「唯一事实来源」句式指向 `kflow-shared/`，且修正后的 12 个规格中的引用目标均在仓库中存在。验证：grep 输出的 `kflow-shared` 命中仅来自本变更的 delta 文件（`openspec/changes/remove-kflow-shared-residue/specs/`，其中提及为对照说明）与历史归档 delta。
- [x] 4.2 校验 `skills/` 与 `docs/` 无残留：grep 排除 `openspec/`，确认唯一残留在 `README.md` 变更历史区段（已知例外）与 `.claude/settings.local.json.bak`（未纳入版本控制，非目标）。验证：grep 输出与例外清单完全一致，无其他命中。
- [x] 4.3 校验「不依赖集中式目录」断言：逐条核对本变更 12 个修正规格新增的场景所断言的路径，确认每个路径都解析到仓库中的真实文件。验证：逐条对照的结论均为存在。
- [x] 4.4 运行 `openspec validate remove-kflow-shared-residue` 与 `openspec validate --specs`（如支持），确认本变更的增量与全部主规格均通过校验。验证：命令输出 valid，且无规格因需求被移除而报结构错误。

## 5. 归档后校验

- [ ] 5.1 确认 6 个被移除能力的规格目录已由归档动作删除，且 12 个修正能力的规格已更新为增量内容。验证：`ls openspec/specs/ | grep '^shared-'` 的残留项与第 5.2 条一致。
- [x] 5.2 确认 `shared-concern-ownership` 与 `shared-type-directory` 未被误删：这两个能力描述的是「共享关切归属规则」与「共享类型目录」的领域概念，与 `kflow-shared/` 目录无关，不在移除范围内。验证：两个规格目录仍存在且需求数未变。
- [x] 5.3 确认 `shared-gate-rules`、`shared-state-values` 等被移除能力的需求去向在本变更 delta 的 `**Migration**` 中均可查。验证：6 个 delta 文件的 REMOVED 块每条需求均含 `**Reason**` 与 `**Migration**`。
