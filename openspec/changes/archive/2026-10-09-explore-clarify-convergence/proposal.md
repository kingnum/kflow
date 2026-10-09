# Proposal

## Why

kflow-explore 的 CLARIFY 步骤以「五域覆盖清单（页面结构 / 可执行操作 / 表单项 / 业务规则 / 业务流程）+ 流程顺序」作为完成标志，**没有任何收敛判据**——无法判定「需求是否已澄清充分」，因而可以在仍留有未决歧义的情况下进入 SPLIT。既有自审只检查产物的完整性/闭环性/必要性/清晰性，不检查「歧义是否已被消解」，且越界处理规则显式允许带着「待补充」标记继续流转。

同时，本次核对发现仓库存在**两处不可解析的外部格式依赖**，违反 `skill-self-contained` 的「Zero external dependency after installation」：

| 位置 | 现状 |
|------|------|
| `openspec/specs/domain-glossary/spec.md:67` | 「`CONTEXT.md` SHALL 遵循 `grill-with-docs` 的 CONTEXT-FORMAT.md 格式定义」——该技能未安装，全仓无承载该格式的 KFlow 自属文件 |
| `openspec/specs/adr-records/spec.md:27` | 「每个 ADR SHALL 遵循 `grill-with-docs` 的 ADR-FORMAT.md 格式」 |

且 `skills/kflow-explore/references/context-template.md` **已存在**——CONTEXT.md 的格式实际有两个来源，其中一个不可解析。本变更修复其中的 CONTEXT.md 一侧；ADR 一侧属 `kflow-design`/归档阶段，另立变更处理。

## What Changes

- **新增需求收敛硬门**：kflow-explore 进入 SPLIT 之前，**未决问题清单 SHALL 为 ∅**；清单中每一项必须被「消解」或**显式降级**为 `待补充` 并记录理由。门是硬的——存在未处理项时不得进入 SPLIT
- **消歧路径限定**：消解一项歧义 SHALL 通过澄清提问、`CONTEXT.md` 术语精确化或事实查库完成；**SHALL NOT 以扩增功能设计内容（新增功能点、字段、章节或分支）的方式消除歧义**
- **非必要不增加**：需求探索 SHALL NOT 为假想分支或将来需求预留功能点、字段与章节——歧义要**收敛成一个确定答案**，而不是**铺开成多个可能**
- **提问纪律**：可查证的事实项自动解析（不占用用户注意力），仅决策项提交用户；一次只提交一项决策
- **CONTEXT.md 格式权威内部化**：`domain-glossary` 的「CONTEXT.md 格式」requirement 由引用外部技能格式文件改为引用 KFlow 自有的 `kflow-explore/references/context-template.md`
- **BREAKING**：进入 SPLIT 的门槛由「流程顺序走完」变为「未决问题清单为空或已显式降级」

## Capabilities

### New Capabilities

- `requirement-clarification`: 需求澄清的收敛门（未决问题清单归零）、消歧路径限定、内容克制（非必要不增加）与提问纪律

### Modified Capabilities

- `domain-glossary`: 「CONTEXT.md 格式」requirement 改由 KFlow 自有 `kflow-explore/references/context-template.md` 承载，移除对外部技能格式文件的引用

## Impact

**受影响实现**：

- `skills/kflow-explore/SKILL.md`：步骤 6（CLARIFY）新增硬门、未决问题清单与消歧路径；步骤 7（SPLIT）前置条件引用该门；「越界处理」中「带待补充继续流转」的表述须与新门对齐
- `skills/kflow-explore/references/`：新增承载收敛门的规则文件；`context-template.md` 升级为 CONTEXT.md 格式的唯一权威来源
- `docs/designs/skills/kflow-explore.md`：设计文档同步
- `openspec/specs/`：新增 `requirement-clarification`，修改 `domain-glossary`

**行为影响**：

- 需求探索的出口条件从「看起来问完了」变为**可判定**（清单为空）；歧义必须被消解或显式降级，二者都留痕
- 内容量受约束：不得以堆砌功能设计内容来"覆盖"歧义——同时提升明确度与降低复杂度
- 交互量由**真实歧义**决定：清单越短越省，无歧义的简单需求几乎零额外成本，因此**不需要按变更档位分级**
- 消除一处外部依赖，`domain-glossary` 与 explore 实现重新对齐
- 无代码、API、依赖或运行时契约变更
