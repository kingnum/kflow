# Design

## Context

动机见 proposal.md 的 Why。以下只列影响实现取舍的现状约束。

**版本规则的分散现状**。版本管理规则当前分布在四处：`openspec/specs/unified-version/`（版本值来源、自增判定、文档头规则）、`openspec/specs/version-tracking/`（SKILL.md 字段、同步脚本、打包校验、消费方查看）、`openspec/specs/version-field-removal-rule/`（审计告警）、`CLAUDE.md`（自增级别示例）。四处中三处对 SKILL.md 是否含 `version:` 给出要求，其中两处要求「无」、一处要求「有」。

**实现现状与规格的对照**。

| 环节 | 实现 | 状态 |
|------|------|------|
| 版本值来源 | `VERSION` 文件（首行 `0.18.0`） | 与规格一致 |
| SKILL.md 字段 | 18 个文件均含 `version: 0.18.0` | 与规格「有」一致，与规格「无」相反 |
| 同步脚本 | `scripts/sync-version.sh`，扫描根 `$REPO_ROOT/skills` | 正确 |
| 打包脚本 | `scripts/package-skills.sh`，扫描根 `$REPO_ROOT/.claude/skills` | **错误** |
| 审计校验 | `skills/kflow-audit/` 无版本字段检查 | 无实现 |
| zip 提交 | `targets/` 被 `.gitignore` 排除；`ba0a5e8` 未提交 zip | 与规格「纳入提交」相反 |

**目录职责**。`skills/` 是仓库内实现目录（纳入版本控制，18 个 kflow-* Skill）；`.claude/skills/` 是运行期注册目录（被 `.gitignore` 的 `.claude/` 规则忽略，仅含 `skill-creator` 与 `to-spec`）。`2026-07-04-skill-self-contained-refactor` 的 proposal 第 13 行已明确该分工：「开发仓库中使用 `skills/<skill-name>/references/xxx.md`，由打包脚本处理路径适配」。

**规格与脚本的失败模式**。`package-skills.sh` 的扫描循环与版本一致性校验循环共用同一份扫描结果。扫描根错误使两个循环都匹配空集合：打包产出仅含 `VERSION.txt` 的 zip，一致性校验则打印「✓ 所有 SKILL.md version 与 VERSION 一致」。失败被报告为成功。

## Goals / Non-Goals

**Goals:**

- 版本管理规则收敛到单一能力，使「SKILL.md 是否含 `version:`」在规格集合中只有唯一答案。
- 让版本相关处理在归档后有唯一且可执行的顺序依据，不再依赖人工记忆。
- 使打包前的版本一致性校验从「形式存在」变为「实质生效」。
- 消除三处已被证实与仓库实际状态相反的规格表述（SKILL.md 移除版本字段 ×2、zip 纳入提交、`.claude/skills` 扫描根）。
- 移除已不存在的 `kflow-skills-auditor` 在规格与打包脚本中残留的排除规则，使打包规则不指向不存在的对象。

**Non-Goals:**

- 不改变目录职责划分——`skills/` 与 `.claude/skills/` 的分工维持不变，仅修正指向后者的错误引用。
- 不新增版本号本身的能力（如版本比较、兼容性范围、CHANGELOG 生成）。
- 不改写任何已归档变更的提案或规格增量——归档记录是历史事实。
- 不改写 `README.md` 的既有版本历史条目，仅修正目录结构速查中的过期计数。
- 不改写已归档变更中涉及 `kflow-skills-auditor` 的历史记录（审查记录、排除名单等），即使该 Skill 已不存在。

## Decisions

### 决策 1：收敛为单一能力，而非定点修补冲突需求

**选择**：`version-tracking` 与 `version-field-removal-rule` 两个能力整体移除，有效需求并入 `unified-version`。

**理由**：矛盾的成因不是某一条需求写错，而是同一主题被三份规格并行承载——任一份演进时另两份不会被告知。已归档的 `2026-09-30-remove-kflow-shared-residue` 正是同类问题的前例（集中式目录移除后，18 个规格仍描述旧布局）。定点修补只能消除当下的矛盾，不能阻止下一次分叉。

**考虑过的替代方案**：

- *保留双规格、显式划分职责*（本能力管版本值与自增判定，版本追踪能力管字段机制）。改动面更小，但版本字段规则与版本值规则天然耦合——字段值就是版本值，「谁定义字段是否存在」无法在两个能力间干净切分，仍留有分叉面。已否决。
- *仅删除冲突的两条需求，其余不动*。最小改动，但 `version-tracking` 与 `unified-version` 会在 SKILL.md 字段上重复定义同一规则，违反 CLAUDE.md「同一规则不出现两次」的 Token 效率要求。已否决。

### 决策 2：保留能力 ID `unified-version`，不改名为 `version-management`

**选择**：合并后的能力继续使用路径 `openspec/specs/unified-version/`。

**理由**：能力重命名会带来两类成本而无收益——归档时新旧 ID 的匹配需要额外处理，且历史提案中对 `unified-version` 的引用会全部失配。该 ID 的语义（统一版本管理）在合并后依然成立：统一的范围从「版本值」扩展到「版本值的全部载体」。

**考虑过的替代方案**：*改名为 `version-management` 并同步修正历史引用*。语义更直白，但需要触碰归档记录，与「不改写归档记录」的既定口径冲突。已否决。

### 决策 3：`version-field-removal-rule` 整体移除，不改写为「审计 version 字段存在且一致」

**选择**：该能力的唯一需求进入 `## REMOVED Requirements`，不做并入。

**理由**：把它改写成「审计 SKILL.md 含且仅含与 `VERSION` 一致的 `version` 字段」看似是物尽其用，实则发明需求——`skills/kflow-audit/` 中从未包含任何版本字段检查，该审计行为无实现、也没有提出过要新增。版本一致性已有可执行的检查者：`package-skills.sh` 在打包前校验，失败即中止且有明确的非零退出路径。为已被脚本覆盖的一致性引入第二处审计，会造出两个事实来源，恰是本次要消除的模式。

**考虑过的替代方案**：*改写为审计需求*。需要同时新增实现（改 `skills/kflow-audit/`），扩大本次范围且与打包校验重复。已否决。

### 决策 4：打包扫描根改为 `skills/`

**选择**：`scripts/package-skills.sh` 的 `SKILLS_DIR` 由 `$REPO_ROOT/.claude/skills` 改为 `$REPO_ROOT/skills`；`skill-packaging` 规格同步修正。

**理由**：三处独立证据指向 `skills/` 才是正确扫描根——

1. 脚本自身的路径重写规则是 `s|skills/$skill_name/|.claude/skills/$skill_name/|g`（第 85、87 行）。该规则把源布局的 `skills/<name>/` 改写为消费方的 `.claude/skills/<name>/`，只有源确实在 `skills/` 时才成立。
2. `2026-07-04-skill-self-contained-refactor` 的 proposal 明确「开发仓库中使用 `skills/<skill-name>/references/xxx.md`，由打包脚本处理路径适配」。
3. `sync-version.sh` 已使用 `$REPO_ROOT/skills` 并正常运行（0.18.0 的 18 处同步即由它完成）。两个脚本扫描根不一致本身就是缺陷信号。

**考虑过的替代方案**：

- *保留 `.claude/skills` 扫描根，新增「把 `skills/` 复制到 `.claude/skills/`」的前置步骤*。会在运行期注册目录里混入仓库交付物，与其职责冲突，且引入需同步的副本。已否决。
- *在 `.claude/skills/` 下建指向 `skills/` 的符号链接*。Windows 上符号链接需要额外权限，且 `.claude/` 被忽略、克隆后不存在。已否决。

### 决策 5：空扫描判定为失败

**选择**：打包扫描未匹配到任何 kflow-* Skill 时，脚本以非零状态退出且不产出 zip。

**理由**：这是本次唯一一处「失败被报告为成功」的位置。仅仅修正扫描根可让当前仓库恢复正常，但一旦目录再被移动、或打包在错误工作目录下执行，同样的静默失败会重现。显式的空集合断言把这类回归从「静默产出空包」变为「响亮失败」。

**考虑过的替代方案**：*仅在版本一致性校验循环中加断言*。只能覆盖校验环节，空包仍会被生成。已否决——断言应位于扫描结果产生处。

### 决策 6：CLAUDE.md 的版本示例改为版本无关表述

**选择**：`CLAUDE.md` 的「版本管理」章节把 `0.17.0` → `0.17.1` / `0.18.0` / `1.0.0` 的字面示例改为相对描述（「patch 位 +1」／「minor 位 +1、patch 归零」／「major 位 +1、其余归零」）。新增的「归档后规则」章节同样不写具体版本号。

**理由**：`ba0a5e8` 的提交内容显示，每次版本递增都要编辑 `CLAUDE.md`（`6 ++---`）。这是「文档级载体不得写具体版本号」这条规则被违反的实例——CLAUDE.md 虽非设计文档，但同属版本管理规则的载体，其字面量使每次递增多一处必改点、也多一处可漏点。相对描述传达同样的判定规则且永久有效。

**考虑过的替代方案**：*保留字面示例并在每次递增时同步*。即现状，已被证明需要人工记忆，且漏改不会产生任何失败信号。已否决。

### 决策 7：zip 产物不纳入提交，修正规格而非配置

**选择**：修改 `skill-packaging` 与 `unified-version` 的措辞，使 zip 明确为本地构建产物；不改 `.gitignore`。

**理由**：`targets/` 与 `target/`、`dist/` 在 `.gitignore` 中同组，表明仓库有意排除构建产物。最近一次版本递增提交 `ba0a5e8` 的 `--stat` 显示只含 `CLAUDE.md`、`README.md`、`VERSION` 与 18 个 SKILL.md，无 zip。配置与实际做法一致，只有规格写反了——应当改规格。把二进制构建产物提交进版本库还会使仓库随每次发布线性膨胀。

**考虑过的替代方案**：*在 `.gitignore` 中放行 `targets/*.zip`*。需要为「规格说提交」而改变仓库的产物管理策略，代价与收益不成比例。已否决。

### 决策 8：本次不新增 `skip_specs`

**选择**：变更声明 `unified-version`（修改）与 `skill-packaging`（修改）两个能力增量，外加两个能力移除，不设 `skip_specs: true`。

**理由**：本次改变了可观察行为——SKILL.md 的 `version` 字段从「规格要求移除」变为「规格要求存在且一致」，打包的扫描对象与失败条件改变，归档后的处理顺序被固定。这些都需要规格层承载。

## Risks / Trade-offs

**[删除两个能力目录后，历史归档提案中的引用成为悬空指针]** → 不改写归档记录（既定口径：归档记录是历史事实）。影响限于可读性：读者从旧提案跳转到 `openspec/specs/version-tracking/` 会得到 404。缓解方式是在被删除能力的增量文件中写明迁移目标（`unified-version` 的具体需求名），使从归档侧反查有明确落点。

**[`skill-packaging` 的「排除 kflow-skills-auditor」在 `skills/` 下是空操作]** → **已移除**。原判断为「防御性保留：消费方布局下该 Skill 可能存在，删除需消费方环境证据，待确认其不存在后再清理」。用户已确认 `kflow-skills-auditor` 不再存在，触发条件成立，故本次移除规格中的排除条款与其场景、该变更增量中的同款条款，以及 `scripts/package-skills.sh` 的 `EXCLUDE_SKILL` 变量与排除分支。已归档变更中的历史引用不改写。

**[修正扫描根后，首次打包的结果与以往截然不同]** → 以往产出的空包若曾被分发，消费方持有的会是无效包。缓解方式：修正后的首个 zip 应在打包后检查其目录清单（应含 18 个 Skill 目录）再决定是否分发，而不是直接沿用。此检查写入 tasks.md 的验证步骤。

**[合并后 `unified-version` 承载 6 个需求，单文件变长]** → 这是有意的权衡：把同一主题收在一处带来的「读者一次读完即可确定答案」胜过文件更短。若日后确有拆分需要，应沿「版本值 vs 版本载体」切分并同时提供交叉引用，而不是像本次之前那样无声明地并行演进。

**[CLAUDE.md 的版本示例去掉字面量后，读者可能需要自行举一反三]** → 相对描述（「minor 位 +1、patch 归零」）已完整表达规则，字面量不增加信息量。且 CLAUDE.md 的读者是 AI 与项目维护者，规则的可执行性优先于示例的直观性。

## Migration Plan

本次为规格与文档层的收敛，无运行时数据迁移。

实施顺序：

1. 修正 `scripts/package-skills.sh`（扫描根 + 空集合断言）。先改实现，使后续验证有可用的检查者。
2. 重写 `openspec/specs/unified-version/spec.md`，删除 `openspec/specs/version-tracking/` 与 `openspec/specs/version-field-removal-rule/`。
3. 修正 `openspec/specs/skill-packaging/spec.md`。
4. 更新 `CLAUDE.md`（新增「归档后规则」章节、版本管理章节改为版本无关表述、SKILL.md 版本字段规则对齐规格措辞）。
5. 同步三处流程副本：`skills/kflow-init/SKILL.md` 注入规则 Marker 2 第 7 条、`docs/designs/skills/kflow-init.md` 同段源文本、`docs/designs/core-mechanisms/08-governance.md` §18.5 第 2 条。
6. 修正 `docs/designs/skills/kflow-archive.md`、`docs/designs/skills/kflow-init.md` 的页头计数与 `README.md` 目录结构速查的过期计数。

**流程副本的一致性约束**。上述第 4、5 步涉及同一份「归档后流程」的四处载体：规格（`unified-version`）、`CLAUDE.md`（本仓库自身的规则）、`skills/kflow-init/SKILL.md` 的注入模板（分发到消费项目的规则）、`08-governance.md`（设计文档层）。四者措辞须一致，且注入模板描述的是**消费项目**的处境——消费项目的 Skills 位于 `.claude/skills/`，其 `VERSION` 与打包脚本随 Skills 一同分发，故模板中的版本自增与打包步骤对消费项目同样成立。

**回滚策略**：本次改动集中在规格与文档，且实现侧的扫描根修正有明确的前后对比（0 个 Skill vs 18 个 Skill）。若修正后打包结果异常，`git revert` 对应提交即可；无外部依赖或数据状态需要复原。

## Open Questions

无。三处规格-实现矛盾（SKILL.md 版本字段、打包扫描根、zip 提交口径）的处置均已在决策 1~7 中确定，无遗留的待定项。
