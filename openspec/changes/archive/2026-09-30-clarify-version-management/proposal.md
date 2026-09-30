# Proposal

## Why

版本管理规则当前被拆成三份规格各自演进，对同一个问题给出了**相反**的要求：

| 来源 | 对「SKILL.md 是否该含 `version:` 字段」的表述 |
|------|------------------------------------------|
| `unified-version`「SKILL.md 版本字段移除」 | SHALL **移除** frontmatter 中的独立 `version:` 字段 |
| `unified-version`「Single version source for all documents」 | SKILL.md frontmatter **SHALL NOT** contain `version:` field |
| `version-field-removal-rule` | `kflow-skills-auditor` SHALL 对存在的 `version:` 字段输出 WARN |
| `version-tracking` | 每个 SKILL.md front matter **SHALL include** a `version` field |
| CLAUDE.md | 每个 SKILL.md front matter **须包含** `version` 字段 |
| 实现（18 个 SKILL.md + `sync-version.sh` + `package-skills.sh`） | 均含 `version:` 字段 |

三份规格中两份要求「有」、两份要求「无」，且 `version-field-removal-rule` 的执法者 `kflow-skills-auditor` 根本不在本仓库（`.claude/skills/` 下只有 `skill-creator` 与 `to-spec`），该规格既与现行口径相反、也无实现可验证。读者无法从规格判断当前布局是哪种，新人照过期规格操作会把现有 18 个 SKILL.md 判为违规。

同时，「版本管理」的规则**没有正式载体**：CLAUDE.md 第 33 行声明「由 CLAUDE.md 的归档后规则和流程自动驱动」，但 CLAUDE.md 中并不存在该章节；`skill-packaging` 规格要求「CLAUDE.md SHALL 包含 `/opsx:archive` 完成后的打包规则」，该需求同样未落地。结果是自增判定、同步、README 更新、打包、提交的**先后顺序无据可依**，只能依赖每次归档时的人工记忆。

排查中还发现一个使上述顺序失去意义的实现缺陷：`scripts/package-skills.sh:9` 的扫描根为 `$REPO_ROOT/.claude/skills`，而 18 个 kflow-* Skills 实际位于 `$REPO_ROOT/skills`（该目录在 `.gitignore` 中被忽略，其下只有 `skill-creator`/`to-spec`）。后果是打包循环匹配零个 Skill、静默产出仅含 `VERSION.txt` 的空包，并且**版本一致性校验因遍历空集合而空转通过**（打印「✓ 所有 SKILL.md version 与 VERSION 一致」）。该一致性校验正是本次要并入 `unified-version` 的需求之一——若不修，合并后的规格将要求一项永远不可能失败、也永远不可能生效的校验。

三份规格并存的前提下，任何单点修补都会在下一次演进中再次分叉。因此本次不做定点修补，而是把版本管理收敛为**一份**规格。

## What Changes

**收敛为单一版本管理能力**

- `version-tracking` 与 `version-field-removal-rule` 两个能力整体移除，其有效需求并入 `unified-version`。版本管理规则此后仅由 `unified-version` 一份规格定义。
- `unified-version` 明确「版本管理规则 SHALL NOT 被他处重复定义」，杜绝再次分叉。

**修正 `unified-version` 中与实现相反的两处需求**

- 「SKILL.md 版本字段移除」需求删除——该需求要求移除的字段正是现行机制（`sync-version.sh` 写入、`package-skills.sh` 校验、消费方 `grep` 查看）所依赖的载体。
- 「Single version source for all documents」中「SKILL.md frontmatter SHALL NOT contain `version:` field」子句删除，替换为明确的**载体分层规则**：`VERSION` 文件为唯一事实来源，SKILL.md 承载同步副本，设计文档头部不写具体版本号。
- 过期计数「16 个运行时 Skills」修正为 18 个（并以机制性措辞表述，避免再次随 Skills 数量变动而失效）。

**明确版本载体分层**

- 仓库级：`VERSION` 文件（首行三段式 `major.minor.patch`），唯一事实来源。
- Skill 级：每个 `skills/kflow-*/SKILL.md` front matter 含 `version:` 字段，值须等于 `VERSION`，由 `scripts/sync-version.sh` 批量同步；消费方通过 `grep '^version:'` 查看已安装版本。
- 文档级：设计文档与核心机制文档头部不写具体版本号，标注「版本: 参见仓库根目录 `VERSION` 文件」。
- 禁止条款：任何载体 SHALL NOT 持有独立于 `VERSION` 的版本值。

**明确自增级别判定**

- minor：新增 Skill、新增阶段、或核心运行机制变更。
- patch：Bug 修复、文档更新、重构、或 `references/` 文件变更，且不涉及新增 Skill 或核心机制。
- 无法判定时默认 patch 并提示用户复核。
- major 位手动确认（`Major 版本手动确认` 需求）为现行有效规则，本次不修改，仅与上述三级判定并列陈述以形成完整的自增口径。

**明确归档后流程顺序（此前无规格载体）**

以 SHALL 级需求固定顺序：归档完成 → 判定自增级别 → 更新 `VERSION` → 运行 `scripts/sync-version.sh` 同步全部 SKILL.md → 更新 README 版本行与版本更新说明条目 → 运行 `scripts/package-skills.sh` 打包 → git commit。步骤失败按各自规则处理，SHALL NOT 阻塞归档本身。

**修正包产物与提交口径的矛盾**

`skill-packaging` 要求「打包完成后将 zip 产物纳入 git commit」，但 zip 落在 `targets/`，该目录在 `.gitignore` 中被排除；最近一次版本递增提交（`ba0a5e8`）也确实未包含 zip，只含 `CLAUDE.md`/`README.md`/`VERSION`/18 个 SKILL.md。规格要求与仓库配置、实际做法三者不一致。修正为：zip 为本地构建产物，不纳入提交；流程中第 6 步只提交版本变更文件。

**修正打包扫描根（使一致性校验真正生效）**

- **BREAKING**：`package-skills.sh` 扫描根由 `.claude/skills` 改为 `skills/`；`skill-packaging` 规格中「扫描 `.claude/skills/kflow-*`」的表述同步修正为「扫描 `skills/kflow-*`（仓库内实现目录）」。
- 打包前版本一致性校验因此从「空转通过」变为真实生效；Skill 数量为 0 时 SHALL 判定为失败而非成功。

**版本规则载体变为版本无关**

- CLAUDE.md 补齐缺失的「归档后规则」章节，陈述流程顺序与自增判定，并去掉 `skill-packaging` 与该章节之间的规格-文档断裂。
- CLAUDE.md 的版本示例由字面量（`0.17.0` → `0.18.0`）改为相对描述（「minor 位 +1，patch 归零」），使该章节不再需要每次版本递增时人工编辑——当前它在每次递增中都被改动，是「版本值散落在文档中」的残留。

**移除已不存在的 `kflow-skills-auditor` 残留**

`kflow-skills-auditor` 已不存在（本次经确认）。`skill-packaging` 规格、本变更的规格增量与 `scripts/package-skills.sh` 中仍保留针对它的排除条款，规则指向一个不存在的对象，且因扫描根内不存在该目录而恒为空操作、无从验证。本次移除三处排除条款：规格与增量中的「排除 `kflow-skills-auditor`」表述、增量中的同款场景，以及脚本的 `EXCLUDE_SKILL` 变量与排除分支。已归档变更中涉及它的历史记录不改写——归档记录是历史事实。

## Capabilities

### New Capabilities

无。本次为既有版本管理能力的收敛与修正，不引入新能力；打包能力的扫描根修正属既有能力的需求修正。

### Modified Capabilities

- `unified-version`: 版本管理规则的唯一载体。删除两处与实现相反的需求（SKILL.md 移除 version 字段、SKILL.md 不得含 version 字段）；新增版本载体分层规则、归档后流程顺序、版本规则唯一性条款；修正过期的 Skills 计数；并入原 `version-tracking` 的 SKILL.md 字段同步与打包一致性校验需求，以及原 `version-field-removal-rule` 中被判为有效的部分（无——该规格的审计要求随执法者 `kflow-skills-auditor` 不在仓库内而整体作废，不并入）。
- `skill-packaging`: 打包扫描范围由 `.claude/skills/kflow-*` 修正为 `skills/kflow-*`；新增「扫描结果为空时打包失败」场景，使版本一致性校验不再空转；移除已不存在的 `kflow-skills-auditor` 排除条款与其场景。

### Removed Capabilities

- `version-tracking`: 全部需求并入 `unified-version`。
- `version-field-removal-rule`: 整体移除。其唯一需求（审计 SKILL.md 不得含 `version:` 字段）与现行载体分层规则相反，且执法者 `kflow-skills-auditor` 已不存在，无实现可验证。

## Impact

- `openspec/specs/unified-version/spec.md` — 重写（4 个需求 → 6 个需求）
- `openspec/specs/version-tracking/` — 删除目录
- `openspec/specs/version-field-removal-rule/` — 删除目录
- `openspec/specs/skill-packaging/spec.md` — 修改扫描范围需求与打包触发时机需求；新增空结果失败、扫描根、路径重写、同步未完成不打包等场景；zip 产物与 git commit 的关系修正为「不纳入提交」
- `scripts/package-skills.sh` — 扫描根修正 + 空结果失败保护 + 移除 `EXCLUDE_SKILL`（`kflow-skills-auditor`）及其排除分支 + 接入 front matter 阻断式门控
- `scripts/validate-frontmatter.py` — 新增：打包前置的 front matter 校验（YAML 可解析、`name`/`description` 必填、`name` 与目录名一致、`version` 与 `VERSION` 一致、含中文触发词），并覆盖 `.claude/skills/*` 与设计规格的 `yaml` 代码块
- `CLAUDE.md` — 新增「归档后规则」章节；「版本管理」章节改为版本无关表述；SKILL.md 版本字段规则与规格措辞对齐
- `skills/kflow-init/SKILL.md` — 注入目标项目的「变更流程强制规则」Marker 2 第 7 条：版本流程补入 SKILL.md 版本同步环节，去掉 `targets/` 纳入提交的表述（设计文档 → SKILL.md 同步）
- `docs/designs/skills/kflow-init.md` — 同上注入规则的源文本同步
- `docs/designs/core-mechanisms/08-governance.md` — §18.5 归档后规则第 2 条补全版本流程顺序
- `docs/designs/skills/kflow-archive.md`、`docs/designs/skills/kflow-init.md` — 页头「16 个运行时 Skills 共享版本号」修正
- `README.md` — 目录结构速查中的过期 Skills 计数修正（变更历史条目不改写）
- `.claude/skills/` 与 `skills/` 的路径差异不改动——`skills/` 为仓库内实现目录，`.claude/skills/` 为运行期注册目录，本次仅修正脚本与规格的扫描目标，不改变目录职责划分
