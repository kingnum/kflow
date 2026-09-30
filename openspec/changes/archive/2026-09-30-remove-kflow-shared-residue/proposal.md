# Proposal

## Why

`.claude/skills/kflow-shared/` 集中式目录已在 `2026-07-04-skill-self-contained-refactor` 中移除，其内容按引用次数分发到各 skill 的 `references/`：`repetition-model.md` → 8 份 `references/repetition.md`、`self-review.md` → 3 份 `references/self-review.md`、`gate-rules.md` → `references/gates.md`、`state-values.md` → 9 份 `references/state-values.md`、`phase-hooks.md` → 各 `references/hooks.md`、`service-lifecycle.md` → 各 `references/service-lifecycle.md`、`scripts/with_server.py` → `kflow-code/scripts/`、`permission-model.md` → `kflow-init/references/`、`recovery-protocol.md` → `kflow-resume/references/`、`archive-rules.md` → `kflow-archive/references/`。

但那次重构只改了实现层，规格层与文档层留下大批残留。23 个规格提到 `kflow-shared`，其中仅 5 个是重构后的正确表述（`skill-self-contained`、`phase-hooks`、`phase-self-review`、`execution-repetition-mode`、`layered-context-loading` 的「不得存在 / 不得引用」），其余 18 个仍在描述已经不存在的集中式布局。

现状的具体后果：

- **规格集合内部自相矛盾。** `shared-repetition-model` 与 `shared-self-review` 要求集中式文件作为唯一事实来源，而 `execution-repetition-mode` 与 `phase-self-review` 明确要求「不得存在集中文件」。`phase-file-reload` 的「RELOAD 清单由共享钩子文件统一定义」与 `phase-hooks` 的「不得引用 `kflow-shared/phase-hooks.md`」同样直接冲突。
- **规格不可信。** 读者无法从规格判断当前布局是哪种，新人按过期规格操作会去找不存在的路径。
- **一处规格被实现违反。** `layered-context-loading` 要求「加载指令 SHALL NOT 引用 `kflow-shared/`」，但 9 个 SKILL.md 与 `07-agent-model.md` §17 仍写着「kflow-shared 分层加载（基础层 + 执行层）」——实际列出的路径是正确的 per-skill 路径，只是标签未改。该措辞会随 skill 打包分发到消费项目。
- **README 当前状态描述失效。** 目录结构速查仍画出 `kflow-shared/` 子树，FAQ 有「kflow-shared 是什么？」条目，两个文档链接指向不存在的路径。

已核对：所有 per-skill 迁移目标文件均存在（`kflow-code/scripts/with_server.py`、`kflow-init/references/permission-model.md`、`kflow-resume/references/recovery-protocol.md`、`kflow-archive/references/archive-rules.md`、各 `references/{repetition,self-review,gates,state-values,hooks,service-lifecycle}.md`）。因此这次清理不改变任何运行时行为，只让规格与文档回到与实现一致的描述。

## What Changes

**整体移除 6 个纯集中式规格**

`shared-archive-rules`、`shared-gate-rules`、`shared-recovery-protocol`、`shared-repetition-model`、`shared-self-review`、`shared-state-values` 的全部需求进入 `## REMOVED Requirements`，随后删除对应的规格目录。理由：这些能力的目标（集中式文件作为唯一事实来源）已被 `skill-self-contained` 定义的 per-skill 结构取代，且其中两项与现行规格直接矛盾。

**修正 12 个规格的失效引用与错误前提**

- 路径修正（`kflow-shared/x.md` → per-skill 路径）：`centralized-service-management`、`kflow-permission-model`、`resume-five-question-summary`、`two-level-checkpoint`、`archive-product-summary`、`devflow-archive`、`skill-packaging`、`port-conflict-detection`、`subagent-enforcement-notice`、`subagent-isolation-rule`、`background-permission-fallback`
- 需求整体替换：`phase-file-reload` 的「RELOAD 清单由共享钩子文件统一定义」进入 `## REMOVED Requirements`（与 `phase-hooks` 矛盾），`skill-packaging` 的「打包范围与排除规则」进入 `## REMOVED Requirements` 并替换为「打包范围与排除规则（自包含 Skill 目录）」（其场景名本身以 `kflow-shared` 命名）
- 每个修正后的需求追加一条「不依赖集中式目录」的场景，使回归可被检查

**修正实现层与文档层措辞**

- 9 个 SKILL.md（plan/code/code-review/api-test/e2e-test/integration-test/bug-fix/design/explore）与 `07-agent-model.md` §17：将「kflow-shared 分层加载」标签改为层级名称本身（基础层 / 执行层 / 服务层 / 创意层），不再借用已不存在的目录名。
- `README.md`：修正目录结构速查（`kflow-shared/` 子树 → 各 skill 的 `references/` 与 `kflow-code/scripts/`）、删除或改写 FAQ 中「kflow-shared 是什么？」条目、修正两个失效文档链接、修正「阶段钩子统一引用 `kflow-shared/phase-hooks.md`」的表述。
- `README.md` 的**变更历史条目不改写**——那些条目记录的是历史事实（当时确实存在该目录、当时确实做过那些改动），改写会破坏变更记录的准确性。

## Capabilities

### New Capabilities

无。本次变更为规格与文档的一致性修正，不引入新能力。

### Modified Capabilities

**整体移除全部需求（6 个，delta 仅含 `## REMOVED Requirements`）**

- `shared-archive-rules`: 全部需求移除，归档规则改由 `kflow-archive/references/archive-rules.md` 承载
- `shared-gate-rules`: 全部需求移除，门控规则改由各 skill 的 `references/gates.md` 承载
- `shared-recovery-protocol`: 全部需求移除，恢复协议改由 `kflow-resume/references/recovery-protocol.md` 承载
- `shared-repetition-model`: 全部需求移除，重复制规范改由各执行类 skill 的 `references/repetition.md` 承载（与 `execution-repetition-mode` 的矛盾随之消除）
- `shared-self-review`: 全部需求移除，自审规范改由三个设计类 skill 的 `references/self-review.md` 承载（与 `phase-self-review` 的矛盾随之消除）
- `shared-state-values`: 全部需求移除，状态值定义改由各 skill 的 `references/state-values.md` 承载

**修正失效引用与错误前提（12 个）**

- `centralized-service-management`: `with_server.py` 路径改为 `skills/kflow-code/scripts/with_server.py`
- `kflow-permission-model`: 权限声明路径改为 `skills/kflow-init/references/permission-model.md`
- `resume-five-question-summary`: 恢复协议引用路径改为 per-skill
- `two-level-checkpoint`: 恢复协议单一来源改为 per-skill
- `devflow-archive`: 归档条件单一来源改为 `skills/kflow-archive/references/archive-rules.md`
- `archive-product-summary`: RELOAD 清单来源改为各阶段自身的 `references/hooks.md`
- `phase-file-reload`: 移除与 `phase-hooks` 矛盾的集中式 RELOAD 清单需求；另两项 RELOAD 清单需求的来源改为 per-skill
- `skill-packaging`: 打包范围需求整体移除并替换为自包含版本；ZIP 结构需求改为自包含描述
- `port-conflict-detection`: 端口检测脚本路径改为 per-skill
- `subagent-enforcement-notice`: §12 引用与权限声明路径改为 per-skill
- `subagent-isolation-rule`: 规则定义位置、规则框引用形式、权限声明路径改为 per-skill
- `background-permission-fallback`: §12 引用改为各执行类 skill 自身的 `references/repetition.md`

## Impact

**规格层**：18 个既有能力的增量（6 个全量移除、12 个修正），无新增能力。

**实现层**：9 个 `SKILL.md` 的措辞修正（`kflow-plan`、`kflow-code`、`kflow-code-review`、`kflow-api-test`、`kflow-e2e-test`、`kflow-integration-test`、`kflow-bug-fix`、`kflow-design`、`kflow-explore`）。无逻辑变更、无路径变更、无需同步 `references/` 内容。

**设计文档层**：`docs/designs/core-mechanisms/07-agent-model.md` §17 的措辞修正。`06-recovery.md`、`04-gates-and-transitions.md` 的引用目标需核对（其对集中式文件的引用由本变更的规格修正界定为 per-skill）。

**项目文档层**：`README.md` 的目录结构速查、FAQ 条目、文档链接、钩子规范表述。变更历史条目不改写。

**行为影响**：无。这是纯一致性修正——所有被修正的引用目标都已经存在，只是规格与文档仍指向旧位置。不涉及数据迁移。

**非目标**：

- 不重新设计 per-skill 布局（`skill-self-contained` 定义的结构已完成，本变更只让描述与之一致）。
- 不改写 `README.md` 的变更历史条目——历史记录应保持当时的事实。
- 不处理 `.claude/settings.local.json.bak`（未纳入版本控制的本地备份文件，其中的 `cp skills/kflow-shared/...` 权限条目是历史残留，不影响交付物）。
- 不合并 `phase-file-reload` 与 `archive-product-summary` 中重复的 `module-summary.md` RELOAD 需求，也不合并 `phase-file-reload` 内部的两条同义需求——去重是另一个独立问题，本变更只修正其来源路径。
