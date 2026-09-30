# Design

## Context

本变更触及 KFlow 原型设计阶段的三个阶段机制（工具链选择、验证审查、原型归属）以及一条跨阶段的规格—实现断裂。动机见 `proposal.md`。

约束：

- **KFlow 支持多个活跃变更并存**（`skills/kflow-guide/SKILL.md:126`：`>1 个活跃变更 → 列出所有活跃变更供用户选择`）。任何"所有变更共用一份资源"的设计都必须回答并发写入问题。
- **`docs/designs/` 已是产品级设计文档根目录**，下辖 `functional-designs/`、`detailed-designs/`、`changelog.md`。`02-directory-structure.md:136` 已画出 `docs/designs/prototypes/`，但没有任何规格或实现引用它。
- **原型是纯 HTML/CSS/JS，无编译步骤**。阶段钩子类型表中 prototype-design 是 `🔶 浏览器`，`编译验证` 是 code 阶段专属（`skills/kflow-prototype-design/references/hooks.md:16-22`）。
- **`design-review-tiering` 已建立"首次/非首次创建"分级机制**，以 `docs/CONTEXT.md` 存在 且 `docs/designs/detailed-designs/` 非空 为判定信号，覆盖 explore / prototype-design / design 三阶段的 SELFREV。

## Goals / Non-Goals

**Goals:**

- 消除原型设计阶段的重复询问与重复扫描。
- 把原型阶段的必做验证成本从"最多约 27 个子代理串行"降到"零子代理"，重验证改为用户可选。
- 建立产品级原型的**唯一真相源**，并使该真相源在多活跃变更下可并发、可回滚、可审计。
- 消除原型在"是否合并到产品级"上的规格—实现矛盾。

**Non-Goals:**

- 不改变 explore / design / plan 三阶段的 SELFREV 规则（`design-review-tiering`、`subagent-self-review` 中这三部分保持原样）。
- 不改变 explore 完成后"是否进入原型设计"的决策门控（`prototype-decision-gate` 不动）。
- 不改变原型的离线自包含约束（`prototype-offline-constraint` 不动）。
- 不改变 OPTIMIZE 步骤的提示词优化与用户确认机制（`prototype-prompt-optimization` 不动）。
- 不把原型阶段改造为 git worktree 或分支隔离模型。

## Decisions

### D1 产品级原型目录采用 `docs/designs/prototypes/`

**选择**：`docs/designs/prototypes/`。废弃规格层现存的 `docs/prototype/` 写法。

**理由**：产品级设计文档已统一在 `docs/designs/` 下按类型目录化（`functional-designs/`、`detailed-designs/`），原型作为第三类产品级设计资产应归位同层。`02-directory-structure.md:136` 已经画了这条路径，追认它比新造一条路径代价更低——只需修改规格层，不需修改目录规范。

**备选**：
- `docs/prototype/`（规格层现状）——需要在 `docs/` 根下新建第二类产品级设计目录，与 `docs/designs/` 语义重叠，且违反 `02-directory-structure.md` 既有约定。
- `docs/designs/prototype/`（单数）——与 `functional-designs/`、`detailed-designs/` 的复数命名风格不一致。

### D2 变更直写产品级目录，用"改动清单 + 改动前快照"提供隔离

**选择**：模型 B。变更直接写 `docs/designs/prototypes/`；变更级维护 `prototype-changes.md`（改动清单 + 改动前哈希）与 `prototype-backup/`（改动前副本）。

**理由**：用户诉求是"所有变更共用一份原型目录，避免复制"。多活跃变更下，无隔离的直写会导致静默覆盖且无法回滚。改动清单提供审计与冲突检测依据，改动前快照提供回滚能力，两者成本都在文件复制量级（原型 HTML 文件量级可控）。

**备选**：
- **模型 A：无隔离直写**。最简单、零复制，但多活跃变更互相污染，变更放弃无法回滚（只能靠 git），同文件写入静默覆盖。在 KFlow 明确支持多活跃变更的前提下不可接受。
- **模型 C：产品级基线 + 变更级工作副本（自动复制 + 归档合并）**。隔离最干净、回滚最简单（删目录），且复用既有 `archive-design-merge` 设计的意图。但它保留了用户明确要消除的"复制往返"，且产品级与变更级可能长期分叉。

### D3 并发写入检测依据改动前哈希

**选择**：`prototype-changes.md` 每条改动记录携带"改动前哈希"。写入产品级原型前比对当前文件哈希与记录中的改动前哈希，不一致则判定为并发修改。

**理由**：产品级目录是共享资源，两个活跃变更修改同一屏幕时，后写者会静默覆盖先写者。哈希比对是唯一能在写入**前**发现该情况且不引入额外协调服务的机制。

**备选**：
- 文件锁 / 变更互斥——需要跨会话状态，KFlow 无此类运行时。
- 仅比对 mtime——时间戳可被复制、检出等操作篡改，不可靠。

### D4 构建门控采用纯静态检查，不含浏览器冒烟

**选择**：BUILD 步骤四项检查全部为主 Agent 可直接执行的静态检查——CDN 外部依赖扫描、交叉引用完整性、必检产物存在、清单与磁盘一致。

**理由**：原型无编译步骤，"构建通过"在本体系中唯一合理的低成本含义就是产物级完整性。四项检查零外部依赖、零子代理、秒级完成，且覆盖了"产物不可用"的主要故障模式（外部依赖残留、断链、必检产物缺失、清单失同步）。运行时错误由后续审查环节覆盖。

**备选**：
- 静态检查 + 浏览器冒烟（逐页打开、pageerror = 0）——能抓运行时错误，但需要 `.kflow-runtime/playwright/` 环境、启动 chromium、编写降级逻辑，成本比静态检查高一个量级，且把可选的重验证成本塞回了必做路径。

### D5 重验证由"无条件强制"改为用户二选一

**选择**：BUILD 通过后通过 AskUserQuestion 询问："人工审查" / "子代理自动审查验证"。前者跳过全部自动验证直接进入 REVIEW；后者执行导航验证 + Playwright 验证 + UX 规则审查 + SELFREV。

**理由**：验证的价值取决于变更规模与用户对原型的信心。KFlow 已有 `design-review-tiering` 的"按需缩放"先例（四视角审查按变更类型分级、SELFREV 按首次/非首次分级），本决策是其自然延伸——把"缩放"的决策权从自动判定扩展到用户显式选择，因为原型质量的主观容忍度是用户私有信息，系统无法从仓库状态推断。

**备选**：
- 保留强制、仅下调轮次——不解决"用户想快速看原型"的场景。
- 提供三选（增加"跳过审查"）——与"人工审查"操作上等价（人工审查即跳过自动验证后由人来看），增加选项无收益。

### D6 "人工审查"路径下 SELFREV 完全跳过

**选择**：不保留兜底轮次。

**理由**：SELFREV 存在的意义是在人看到产物前先把机器能发现的问题收敛掉。若用户已显式选择人工审查（即认领全部审查责任），保留兜底轮次既违背其选择，又使"人工审查"路径的成本优势不成立。

**备选**：保留 1 轮兜底——成本低但语义矛盾：用户选了"人工"，系统仍启动子代理。

### D7 `element-coverage-tree.md` 留变更级，`design-tokens.css` 归产品级

**选择**：元素覆盖树落在 `docs/changes/{change}/element-coverage-tree.md`；设计令牌落在 `docs/designs/prototypes/design-tokens.css`。

**理由**：两者的生命周期不同。元素覆盖树承载 TC-ID 映射，是**变更级**追溯产物，且 design 阶段会在其上追加填充——留在变更级可避免后续变更覆盖前序变更已填的映射。设计令牌是**产品级**设计资产，描述产品整体视觉规范，被 code 与 code-review 阶段消费，且现状本就要求所有原型屏幕通过 `<link rel="stylesheet">` 引用同一份，天然是产品级。

顺带修正一处既存不一致：元素覆盖树当前有三套落点说法（`prototype/` 下、变更根目录、模板根目录），本次统一到变更根目录。

**备选**：元素覆盖树也升产品级——会导致每轮变更覆盖前序 TC-ID 映射，且需重新设计"变更级映射子集"的表达方式，收益不足以抵成本。

### D8 归档语义从"合并"改为"登记"

**选择**：归档时把 `prototype-changes.md` 的改动登记到 `docs/designs/prototypes/manifest.md` 的变更来源列；`prototype-backup/` 随变更目录进 `archive/` 保留。删除 `archive-design-merge` 的 `Scenario: 合并原型设计`。

**理由**：直写模型下，变更在原型设计阶段结束时产品级原型**已经是最终状态**，归档时再"合并"会把同一份内容应用两次。登记动作只维护清单的溯源信息，不搬运产物文件。

**备选**：保留"合并"动作但改为幂等——需要定义幂等语义与去重规则，而直写模型下该动作本身已无对象。

### D9 `TOOLCHAIN` 改为默认复用已锁定工具链

**选择**：读取 `docs/toolchain.md`（含变更级覆盖 `docs/changes/{change}/toolchain.md`）的"原型设计"章节，若已锁定且引用的 Skill 在环境中可用，直接复用且不询问。仅在三种例外下重新选择：无已锁定工具链（首次创建）、已锁定工具链引用的 Skill 环境不可用、用户显式要求更换。

**理由**：`docs/toolchain.md` 本就是项目级、跨变更稳定的配置（由 `kflow-init` 产出）。每次变更重新扫描环境并询问，等于假设工具链是变更级属性——与配置的层级不符。例外条件覆盖了"配置失效"与"用户改变主意"两个真实场景。

**备选**：直接删除 TOOLCHAIN 步骤——会丧失首次创建时的选择能力与工具链失效时的自愈能力。

### D10 修复规格—实现断裂的方式是"删除规格中的原型合并场景"

**选择**：删除而非改写 `archive-design-merge` 的原型合并场景；同时清理 `kflow-archive` 与 `kflow-prototype-design` 中互相矛盾的表述。

**理由**：现状三方表述为——规格要求合并到 `docs/prototype/`、实现明确不合并、上游原型技能声称归档会合并。直写模型下"合并"这个动作不存在，因此正确做法是删除该场景，而非把它改写为另一种合并方式。`kflow-archive` 中"原型设计（.html 文件）不合并到产品级，保留在变更级归档目录中"这条注意事项也要改写，因为变更级原型副本已不再存在。

### D11 对比度检测归入「子代理自动审查验证」路径

**选择**：原型阶段的对比度检测（WCAG 相对亮度计算，标记 <4.5:1 的颜色对）仅在审查方式为「子代理自动审查验证」时执行，报告输出到 `self-reviews/prototype/contrast-check/report.md`；「人工审查」路径下完全跳过，不保留兜底。

**理由**：原 `VERIFY` §8.6 将对比度检测列为无条件必做项，而本次重构把原型阶段的验证重新划分为"BUILD 唯一必做（四项静态检查）+ 其余验证由用户选择"。对比度检测虽是纯静态计算，但它属于"自动验证"范畴，且 UX 规则审查第 1 条已覆盖对比度阈值判定。归入可选路径既保持与「BUILD 为唯一必做验证」「人工审查跳过全部自动验证」两条口径一致，也不必改动 delta 中「四项检查」的表述。

**备选**：并入 UX 规则审查（失去独立报告）；归入 BUILD 静态检查（需把规格从"四项"改为"五项"，与已定稿的 BUILD 定义冲突）。

### D12 `design-system/MASTER.md` 不供下游阶段消费

**选择**：`docs/designs/prototypes/design-system/MASTER.md` 是原型设计阶段的通用必备产物，其角色为 `process`；下游阶段（plan、code、code-review、e2e-test）SHALL NOT 将其列为输入，设计令牌来源统一为产品级清单中角色为 `tokens` 的 `docs/designs/prototypes/design-tokens.css`。

**理由**：规格层存在一处既存冲突——`prototype-design-system-output` 要求 code/code-review 加载 `MASTER.md`，`prototype-manifest` 的「输入限定规则基于清单声明」则禁止下游读取 `MASTER.md` 与 `process` 角色文件。直写 + 清单模型下，下游只需 `entry/page/tokens/shared` 四类角色；`MASTER.md` 是设计引擎的过程性描述文档，与 `design-tokens.css`（机器可消费的令牌值）职责不同。裁决后二者不再矛盾。

**备选**：以 `prototype-design-system-output` 为准，撤销 `prototype-manifest` 的排除条款——会使 `process` 角色枚举失去意义，且下游需额外处理一份自由格式文档。

## Risks / Trade-offs

- **[产品级原型目录成为所有变更的写入热点]** → 由 D3 的哈希比对在写入前拦截并发覆盖；用户裁决提供三个出口（基于新版本改 / 覆盖 / 人工合并）。
- **[快照累积导致仓库体积增长]** → `prototype-backup/` 随变更进 `archive/`，不常驻活跃路径；单变更的快照仅为被改文件，非全量原型。
- **[用户频繁选择"人工审查"导致原型质量问题后移到 code 阶段]** → 这是用户显式认领的取舍；`code` 阶段对原型问题已有 REVISION 回退入口（`prototype-revision-mode` 入口 B），质量问题不会静默流失。
- **[`docs/designs/prototypes/` 与 `docs/designs/` 下其他目录的写权限语义不完全一致]** → 其他目录由归档阶段写入，原型目录由原型设计阶段写入。这种差异是刻意的（原型在变更生命周期内即生效），已在 `prototype-manifest` 中显式约定写权限归属。
- **[17 个能力增量同时修改 specs，归档时冲突面较大]** → 归档按既有流程逐个 delta 应用；各能力改动互不重叠（详见 `specs/` 下各 delta）。

## Migration Plan

1. **规格与设计文档先行**：本变更的 specs 归档后，`openspec/specs/` 层即为新权威。
2. **设计文档同步**：按 `tasks.md` 更新 `docs/designs/` 下的技能设计文档与核心机制文档。
3. **运行时技能同步**：按 `tasks.md` 更新 `skills/` 下 `SKILL.md` 与 `references/`。
4. **已归档变更**：无需迁移。其 `prototype/` 目录原地保留在 `docs/changes/archive/{...}/` 下。
5. **活跃变更**：若变更级已存在 `prototype/` 目录，需迁移到产品级 `docs/designs/prototypes/` 并生成 `prototype-changes.md`。迁移为手动步骤，在 `tasks.md` 中列为检查项；不涉及已归档变更。
6. **回滚策略**：本变更为文档与技能定义变更，回滚即 `git revert`；不涉及运行时数据迁移。

## Open Questions

无。本次设计涉及的取舍已在探索阶段与用户逐项确认。
