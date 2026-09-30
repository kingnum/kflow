# Design

## Context

参见 `proposal.md` 的 Why。以下约束决定了实现方式：

**重构已完成，清理只是让描述追上实现。** `2026-07-04-skill-self-contained-refactor` 已把集中式目录的内容按引用次数分发到各 skill 的 `references/`，并且这 11 个分发副本（8 份 `repetition.md`、3 份 `self-review.md`）在本仓库中属于「执行层 / 创意层」的现行结构。本变更不触碰这些内容，只修正引用它们的描述。

**验证器的场景名约束。** `openspec validate` 要求 `## MODIFIED Requirements` 块保留原规格中的全部场景名（存档时 MODIFIED 整体替换该需求块，验证器拒绝静默丢场景）。因此当某个场景名本身以 `kflow-shared` 命名时，无法用 MODIFIED 达成目的。

**CLI 不支持删除能力。** `openspec spec` 只有 `show` / `list` / `validate`，没有删除子命令。

**但 archive 会删除空规格目录。** 已通过先例验证：`2026-05-17-replace-ralph-loop-with-agent-iteration` 把 `ralph-loop-subagent-execution` 的全部需求写入 `## REMOVED Requirements`，其 tasks.md 中**没有**任何删除 `openspec/specs/ralph-loop-subagent-execution/` 的任务，而该目录现已不存在（`ls openspec/specs/ | grep -i ralph` 无输出）。因此归档动作自身承担目录删除，任务清单不需要也不应该包含这一步。

**`README.md` 含两类 `kflow-shared` 提及。** 一类描述当前状态（目录结构速查、FAQ、文档链接、钩子规范表述），另一类是变更历史条目（记录过去某个版本做过什么）。

## Goals / Non-Goals

**Goals:**

- 使 `openspec/specs/` 内部一致——不再存在「某个能力要求集中式目录、另一个能力禁止集中式目录」的对立。
- 使规格与文档中出现的每个路径都能在仓库中解析到真实文件。
- 消除实现层违反 `layered-context-loading` 的措辞。
- 保持零运行时行为变更。

**Non-Goals:**

- 不重新设计 per-skill 布局。
- 不合并重复需求（`phase-file-reload` 与 `archive-product-summary` 各有一条 `module-summary.md` RELOAD 需求；`phase-file-reload` 内部两条同义需求）——去重是独立问题，本变更只修正来源路径。
- 不改写 `README.md` 的变更历史条目。
- 不处理未纳入版本控制的 `.claude/settings.local.json.bak`。

## Decisions

### 决策 1：6 个 `shared-*` 规格整体移除，而非改写

**未采用**的方案是把它们的需求改写为 per-skill 表述。

理由：改写会制造与 `skill-self-contained` 重复的第七处关于 per-skill 布局的描述——而这次清理的起因正是「同一事实存在多份互相漂移的描述」。这 6 个能力的共同目标是「集中式文件作为唯一事实来源」，目标本身已被 `skill-self-contained` 的「Shared file distribution by reference count」与「references content is phase-specific」取代。移除后，per-skill 布局只有 `skill-self-contained` 一处定义。

其中 `shared-repetition-model` 与 `shared-self-review` 的移除额外解决了与 `execution-repetition-mode`、`phase-self-review` 的直接矛盾。

每条移除的需求都在 `**Reason**` 中写明移除原因、在 `**Migration**` 中写明去向，使「为什么删」与「现在去哪找」可追溯。

### 决策 2：场景名含 `kflow-shared` 的需求改用 REMOVED + ADDED

受验证器的场景名约束，两处需求无法用 MODIFIED 达成目标：

| 规格 | 需求 | 原场景名 | 处理 |
|------|------|---------|------|
| `skill-packaging` | 打包范围与排除规则 | `kflow-shared 包含运行时脚本`、`ZIP 包中 kflow-shared 结构` | REMOVED + ADDED「打包范围与排除规则（自包含 Skill 目录）」 |
| `phase-file-reload` | RELOAD 清单由共享钩子文件统一定义 | `集中式 RELOAD 清单` | REMOVED（无替代需求，与 `phase-hooks` 矛盾） |

其余 10 个路径修正规格的场景名均不含 `kflow-shared`，可正常使用 MODIFIED 并保留全部原场景名。

### 决策 3：措辞替换保留层级概念，删除借用的目录名

实现层与文档层的原文是「kflow-shared 分层加载（基础层 + 执行层）」。替换为「分层加载（基础层 + 执行层）」。

**未采用**的方案是保留「kflow-shared」作为层级方案的名称。理由：该名称借用一个已不存在的目录，是本次清理要消除的混淆源；而「分层」这一概念由 `layered-context-loading` 定义，与任何目录无关。替换后，读者查「分层加载」会落到该能力，查路径会落到各 skill 的 `references/`。

替换范围：9 个 SKILL.md（`kflow-plan`、`kflow-code`、`kflow-code-review`、`kflow-api-test`、`kflow-e2e-test`、`kflow-integration-test`、`kflow-bug-fix`、`kflow-design`、`kflow-explore`）与 `docs/designs/core-mechanisms/07-agent-model.md` §17。

### 决策 4：每个修正需求追加一条「不依赖集中式目录」场景

在 12 个路径修正规格中，为每个被修正的需求补一条新场景，断言引用目标为 per-skill 路径且不依赖 `kflow-shared/`。

理由：本次清理的验收本质是「grep 不到失效引用」。把该断言写成规格场景，使回归检查有规格依据，而不是依赖一次性的 grep。这也符合本变更的目的——让规格能反映真实状态。

### 决策 5：README 变更历史条目不改写

只修正描述当前状态的段落（目录结构速查的 `kflow-shared/` 子树、FAQ 的「kflow-shared 是什么？」条目、两个失效文档链接、阶段钩子规范表述）。

理由：变更历史条目记录的是历史事实——当时确实存在该目录、当时确实做过那些改动。改写会让变更记录失真，且会让后续读者无法理解为什么会有这次清理。这与仓库既有的 `docs/designs/*.md` 保留「版本变更说明」的做法一致。

**代价与应对**：README 中会继续存在「kflow-shared」字符串，使 grep 校验出现假阳性。应对方式是把例外写进验证任务（排除变更历史区段），而非放宽整个检查。

### 决策 6：不删除规格目录，交给归档动作

已由先例验证 `openspec archive` 会删除需求被全部移除的规格目录。任务清单中不包含删除步骤。

理由：任务若在归档前删除目录，归档时无法找到对应的主规格来应用 delta，会导致归档失败。把目录删除留给归档动作，顺序天然正确。这条同时满足仓库对 tasks.md 的约束（不含归档相关的元工作流任务）。

## Risks / Trade-offs

- **移除 6 个能力可能丢掉其中独有的需求** → 已逐条核对：`shared-repetition-model` 的 6 条需求中，轮次决策与执行历史追踪同 `flexible-repetition-mode`、影响分数读取同 `triage-impact-assessment`/`tier-driven-repetition`，其余两条是「引用集中式文件」本身；`shared-gate-rules` 的 `Internal duplication eliminated` 在集中式文件消失后失去对象；其余 4 个能力的 2 条需求结构相同（定义文件 + 引用替换）。全部去向记入 `**Migration**`。
- **规格目录删除后，历史归档变更中的 delta 引用失效** → 归档条目是历史记录，其 delta 文件独立存在，不依赖主规格目录。`ralph-loop-subagent-execution` 的归档 delta 至今可读即为先例。
- **README 历史条目保留 `kflow-shared` 会让 grep 校验假阳性** → 决策 5 的例外规则；验证任务显式排除变更历史区段与 `.bak` 文件。
- **替换措辞后读者不知去何处查「分层加载」** → 替换为引用 `layered-context-loading` 能力，而非留空。
- **移除需求的原正文在归档后不可从规格检索** → `## REMOVED Requirements` 保留 Reason 与 Migration（去向可查），原正文可从 git 历史恢复。本变更不含不可逆的信息丢失。
- **`devflow-archive` 被三个变更触及**（`add-change-tier` 未涉及，但本变更与 `add-lightweight-change-flow` 都改了 `devflow-audit`）→ 已核对：本变更只改 `devflow-archive`，与 `add-lightweight-change-flow` 改的 `devflow-audit` 不同规格，无重叠。

## Migration Plan

无数据迁移。无运行时行为变更。

改动落地顺序：

1. `openspec/specs/` 下 18 个增量（6 个全量移除、12 个修正）——本变更的 delta。
2. `docs/designs/core-mechanisms/07-agent-model.md` §17 的分层加载措辞修正。
3. 9 个 `skills/*/SKILL.md` 的分层加载措辞修正。
4. `README.md` 的当前状态描述修正（目录结构速查、FAQ、文档链接、钩子规范表述）。
5. 全仓库残留校验（含例外规则）。

回滚策略：6 个被移除的规格可从 git 历史恢复其完整正文；12 个修正为路径替换，逆向替换即可。无不可逆改动。

**与其他变更的顺序**：与 `add-change-tier`、`add-lightweight-change-flow` 无规格重叠，可独立于二者落地。

## Open Questions

无。移除范围、场景名受限需求的处理方式、措辞替换目标、README 改写边界、规格目录删除的归属均已在设计中确定为可执行步骤。
