# Proposal

## Why

对需求探索阶段（kflow-explore）产物 `functional-designs/` 按「目标用户 / 核心功能 / 用户流程 / 页面结构原型 / 优先级 / 解决问题 / 非功能需求」七项内容覆盖度核查后发现两项缺口：

1. **用户视角非功能期望无捕获点**：NFR 完全后置到详细设计阶段（kflow-design 的 NFR 章节）由 AI 直接给出技术目标值，用户层面的期望输入（如"列表加载应在 2 秒内可交互"）在整个流程中没有记录位置，需求输入链断裂。
2. **页面结构无变更级承载**：页面信息仅以「所属页面与菜单」散落在各功能点中，没有页面清单与页面级结构描述；视觉原型归属可选的 kflow-prototype-design（轻量档不主动询问、纯后端项目跳过），一旦跳过原型设计，整个变更流程不存在任何页面结构记录。

## What Changes

- `functional-designs/index.md` §一 变更概述新增**「非功能期望」小节**：用户视角、业务语言描述（性能感受 / 安全与合规 / 可用性 / 兼容性等开放维度），每条期望关联功能点；无显式期望时整节标注「本变更无特殊非功能期望」（沿用结构性章节不省略规则）
- `functional-designs/index.md` 新增**「页面清单」章节**：页面 × 菜单路径 × 类型（新建/修改/复用）× 区块级文字结构描述 × 涉及功能点；置于「功能结构树」之后，后续章节顺延重编号；纯后端项目或无前端 FP 时标注「本变更无涉及页面」
- **CLARIFY 遍历域由五域扩为六域**：候选清单生成域新增「非功能期望」，收敛门与空清单凭据说明同步扩展
- **kflow-design NFR 步骤新增输入说明**：NFR 章节以探索阶段「非功能期望」小节为需求输入，将用户视角期望转译为可度量技术目标值（消费闭环）
- **自审完整性检查新增检查项**：「页面清单与各 FP 所属页面一致（无孤页、无漏页）」
- **轻量档配套**：页面清单保留简表（结构描述可并为一句）；非功能期望无则标「无」；不新增流程步骤
- **阶段边界澄清**：非功能期望 SHALL 使用业务语言，SHALL NOT 定义技术目标值（并发数、P95 指标等技术定义仍属 design 阶段 NFR 章节）

## Capabilities

### New Capabilities

（无）

### Modified Capabilities

- `functional-design-content`: 新增两条 Requirement——变更概述包含「非功能期望」小节（业务语言、关联功能点、无期望标注规则）；功能设计索引包含「页面清单」章节（页面级结构承载、与各 FP 页面归属一致性、纯后端标注规则）
- `requirement-clarification`: 「需求澄清收敛硬门」的候选来源场景由五个内容域扩为六个（新增非功能期望域），空清单凭据说明同步扩展
- `nfr-requirements`: 「详细设计包含 NFR 章节」新增输入来源场景——NFR 章节以探索阶段非功能期望为需求输入进行转译
- `phase-boundary-enforcement`: 「阶段内容禁止越界」的 explore 场景——用户视角聚焦清单纳入非功能期望与页面清单，并显式约束非功能期望为业务语言输入、不含技术目标值

## Impact

- `docs/designs/skills/kflow-explore.md`：输出产物内容要求、CLARIFY（6b 域清单、6c 收敛门候选域）、OUTPUT 步骤、自审完整性检查表、域内内容表
- `docs/designs/skills/kflow-design.md`：NFR 步骤输入说明（一行）
- `docs/designs/templates/changes/{change}/functional-designs/index.md`：§一 新增小节、新增「页面清单」章节、后续章节重编号
- `skills/kflow-explore/SKILL.md`、`skills/kflow-design/SKILL.md`：设计文档 → SKILL.md 同步
- `skills/kflow-explore/references/clarify-convergence.md`（五域→六域）、`references/self-review-dimensions.md`（完整性检查项）——explore 专属 references，直接编辑，不涉及 references-src/ 共享切片
- 纯后端场景：非功能期望小节适用（纯后端也有性能/安全期望），页面清单章节标注「无」；apply 阶段核查纯后端简化模板是否需同步章节编号
- 版本影响：触及 `requirement-clarification` 能力行为，归档时预计 minor 位 +1（由归档后规则判定）
