# Proposal

## Why

**项目类型是仓库级不变量，却被当成变更级变量反复重算。**

1. **重复打扰**：`kflow-explore` 每次创建变更都执行 TYPEDET（重扫项目根目录）+ CONFIRM（AskUserQuestion 让用户确认项目类型）。项目类型在一个仓库内是稳定的，用户开 10 个变更就要回答 10 次完全相同的问题，而这 10 次答案必然一致。
2. **记录已存在却不被读取**：`kflow-init` 早在初始化时就检测过项目类型，并写入两处项目级记录——CLAUDE.md「项目画像」表的「项目类型」行，与 `docs/toolchain.md` 头部的「项目类型」字段。变更创建链路（`kflow-guide`、`kflow-explore`）完全无视这两处记录，重新扫描后还要再问用户一遍。
3. **答案已在 AI 上下文中**：CLAUDE.md 由 Claude Code 每次会话自动加载，探索阶段 AI 手里已经握着项目类型，却转头向用户提问——这是"信息可得却不使用"的典型浪费。
4. **确认本身有价值，只是不该重复**：自动检测并不可靠（历史记录见 `docs/designs/examples/skill-suggestion.md` 记录 3：前后端分离、前端在独立仓库的项目被判为"纯后端"，由用户纠正）。所以确认动作不能取消，但应**只发生一次**。
5. **漂移无安全阀**：项目会演进（纯后端项目后来新增前端工程），项目级记录会过期，而现状没有任何机制发现这种漂移。

本次变更把项目类型的**确认动作前移到 init 一次**、**读取改为继承项目级记录**，并为漂移与初始误判各留一个安全阀。

## What Changes

- **确认前移到 init**：`kflow-init` 在 DETECT 之后新增 CONFIRM 步骤，使用 AskUserQuestion 确认一次项目类型（与 init 既有的权限配置、方案选择确认风格一致），结果写入项目级记录。
- **init 侧同样遵守"只问一次"**：re-init 时若项目级记录已存在且重新扫描结果一致 → 静默复用，不重复询问；仅在扫描与记录冲突时才询问。
- **explore 侧改为继承**：`kflow-explore` 步骤 3 TYPEDET 与步骤 4 CONFIRM 由"重扫 + 询问"改写为**三级回落读取**（CLAUDE.md 项目画像 → `docs/toolchain.md` 头部 → 就地检测）＋**静默一致性校验**。一致则静默继承并输出「项目类型: X（继承项目级记录）」；冲突才 AskUserQuestion 复核并可选更新项目级记录。
- **未 init 项目降级自愈**：项目级记录完全缺失时，explore 检测并确认**一次**，补写 `docs/toolchain.md` 头部（不写 CLAUDE.md 项目画像——该区块是 init 整体扫描的产物，残缺区块会与受管 marker 逻辑冲突）；此后该项目的所有变更均静默继承。
- **guide 侧改为读取**：`kflow-guide` 的 NEW CHANGE 创建前指引中，DETECT 步骤由"重新扫描判定"改为"读取项目级记录"，输出标注来源。
- **变更级快照保留、来源改为继承**：`.status.md` 与 `functional-designs/index.md` 的项目类型字段继续保留（变更生命周期内项目类型必须冻结，否则已 `⏭️ 跳过` 的阶段会中途复活），其值来自项目级记录而非重新检测；`index.md` 的「项目类型判断」表由"检测结果"改为"来源 + 静默校验结果 + 判定依据"。
- **新增用户显式覆盖通道**：用户在需求描述中显式声明项目类型（或指出记录有误）时，该声明优先于一切记录与扫描，并触发项目级记录更新。这是初始误判（扫描信号与错误记录一致，比对不出冲突）的唯一逃生舱。
- **消费侧完全不动**：`kflow-design`、`kflow-prototype-design`、`kflow-api-test`、`kflow-e2e-test`、`kflow-verify`、`kflow-audit`、`kflow-archive` 一律只读变更级快照，快照依然有值，其判定逻辑与读取路径 SHALL NOT 变更。

## Capabilities

### New Capabilities

（无）

### Modified Capabilities

- `project-type-detection`: 权威改写本能力的核心行为——「项目类型检测」由"设计探索阶段自动检测"改为"读取项目级记录优先，仅记录缺失时检测"；「项目类型记录」由"记录到 design-explore.md"改为"记录到项目级真源（CLAUDE.md 项目画像 + `docs/toolchain.md` 头部）并继承到变更级快照"；「项目类型确认」由"检测完成即向用户确认"改为"仅 init 首次确认或扫描与记录冲突时确认"。新增三条 Requirement：项目级记录真源与读取优先级（含三级回落）、静默一致性校验（漂移检测）、用户显式覆盖。保留「项目类型影响阶段流转」与「playwright-cli 环境可用性检测」不变。
- `devflow-guide`: 「项目类型判断」Requirement 由"流程指引时判断当前项目类型"改为"读取项目级项目类型记录并据此展示流程"，SHALL NOT 重新扫描判定。
- `init-claude-md-injection`: 「项目画像 section 注入」Requirement 补充「项目类型」字段的用途契约——该字段为项目类型项目级唯一真源，供变更创建链路读取（读取优先级高于 `docs/toolchain.md` 头部同名字段）；并补充 re-init 时记录与扫描一致则静默复用、不重复询问用户的要求。

## Impact

- **运行时 Skill**：`skills/kflow-init/SKILL.md`（步骤 1 DETECT 后新增 CONFIRM、幂等复用规则）、`skills/kflow-explore/SKILL.md`（步骤 3/4 改写为三级回落读取 + 静默校验）、`skills/kflow-guide/SKILL.md`（NEW CHANGE 指引步骤 2 DETECT 改为读取记录）
- **设计文档**：`docs/designs/core-mechanisms/01-project-types.md`（新增「记录与继承」节：真源、优先级、漂移、显式覆盖）、`docs/designs/skills/kflow-init.md`、`docs/designs/skills/kflow-explore.md`、`docs/designs/skills/kflow-guide.md`、`docs/designs/index.md`、`docs/designs/overview.md`、`docs/designs/skills/index.md`（同步"设计探索阶段检测项目类型"的表述）
- **模板**：`docs/designs/templates/changes/{change}/functional-designs/index.md`（「项目类型判断」表字段调整）
- **规格**：`openspec/specs/project-type-detection/`、`openspec/specs/devflow-guide/`、`openspec/specs/init-claude-md-injection/`
- **存量消费方项目**：已在 init 时写入项目级记录的项目，改造后首个变更创建即静默继承（读取侧能命中 CLAUDE.md 项目画像或 `docs/toolchain.md`），无需重新 init；从未 init 且无项目级记录的项目，在首个变更创建时补写一次记录，此后静默
- **不涉及**：`kflow-design`、`kflow-prototype-design`、`kflow-api-test`、`kflow-e2e-test`、`kflow-verify`、`kflow-audit`、`kflow-archive` 的项目类型读取与判定逻辑；变更级 `.status.md` 的快照机制与其「阶段适用性声明」区；历史变更的 `.status.md`（已含项目类型字段，无需迁移）
