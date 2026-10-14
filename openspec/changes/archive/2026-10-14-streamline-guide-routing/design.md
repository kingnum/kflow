# Design

## Context

动机见 `proposal.md` - Why。这里只记影响设计决策的现状与约束。

**现状要点**

- 阶段 Skill 的 COMPLETE 步骤只更新 `.status.md` 字段，不发起任何衔接动作，用户必须再输入一句话才能推进。
- `skills/kflow-resume/SKILL.md` 的 DISPATCH 步骤已实现完整的阶段衔接决策表（✅完成递归推进 / 🔄进行中调度当前 / ⚠️需修订回退 / ❌阻塞不调度 / ⏳待开始调度），但该逻辑是 resume 私有实现，未推广到各阶段 Skill。
- `kflow-guide` 的 PARSE 正则「继续/恢复/resume + 变更名」优先级 0，凌驾于 INTENT 关键词表之上，导致「继续」永远走 RESUME 重流程。
- `kflow-explore` 已在 INIT/CLASSIFY/TIER/CONTEXT 四个步骤中实现变更命名、类型分类、档位初判、活跃变更检测，并在 description 中声明为 all changes 的入口点。
- `openspec/specs/intent-priority-rules/` 已规定「继续类关键词 → 直接路由到活跃变更的当前阶段」，与实现（走 RESUME）存在既有偏差。

**项目约束**

- `skills/kflow-*/SKILL.md` 内容语言为英文；`openspec/specs/` 与 `docs/designs/` 为中文。
- Skill 自包含：辅助规则放各 skill 的 `references/` 子目录，skill 安装后零外部依赖，不得依赖消费方项目中不存在的 `docs/designs/`。
- Token 效率：同一规则不得出现两次。
- `scripts/sync-references.sh` 对同名 references 文件做跨 skill 一致性校验，校验清单为硬编码数组。
- `scripts/validate-injection-scope.sh` 扫描 kflow-init 注入模板，命中开发态词汇即非零退出。

## Goals / Non-Goals

**Goals:**

- 消除流程执行期间回 `kflow-guide` 的往返，使正常变更可连续执行到底。
- 让阶段衔接成为默认行为，而非需要用户显式发起的操作。
- 使「推进」与「恢复」两个语义各有唯一入口，不再互相干扰。
- 把 `kflow-guide` 的职责收敛到「状态查看 / 断点恢复 / 流程概览 / 设计修订分流」四项。

**Non-Goals:**

- 不改变各阶段自身的入口门控、自审机制与产物白名单。
- 不削弱 `kflow-resume` 的中断恢复能力——产物完整性二次校验、五问题摘要、优先级链断点定位、服务恢复检测全部保留。
- 不重构 `kflow-explore` 的变更创建能力（已自足）。
- 不取消归档的显式发起要求。
- 不引入存量项目的自动版本检测机制（见 Risks）。

## Decisions

### D1：阶段衔接决策表的承载位置 —— 共享 references 副本

**决策**：新增 `references/phase-transition.md`，由各阶段 Skill 各持一份副本；各 SKILL.md 的 COMPLETE 步骤以一句引用指向它。该文件加入 `scripts/sync-references.sh` 的 `REF_FILES` 校验清单。

**理由**：决策表必须能被消费方项目的 Skill 读到，因此不能只写在 `docs/designs/`（消费方不存在该目录）；而内联到 9 个 SKILL.md 会产生 9 份副本、违反「同一规则不出现两次」。共享 references 副本是项目既定模式（`repetition.md`、`gates.md`、`state-values.md` 等 6 个文件已采用），且 `sync-references.sh` 提供跨副本一致性保障。Claude Code 按需加载 references，不占常驻上下文。

**替代方案**：
- 内联到各 SKILL.md —— 否决，token 冗余且易漂移。
- 新建独立 Skill 承载 —— 否决，阶段衔接是步骤而非阶段，引入 Skill 反而增加一层往返。
- 放入 `kflow-guide/references/` 由其他 skill 引用 —— 否决，破坏 skill 自包含约束。

### D2：推进与恢复的路由拆分

**决策**：`kflow-guide` 的 PARSE 正则拆为两条独立分支：

| 输入模式 | 路由 | 执行内容 |
|---------|------|---------|
| `/(?:恢复\|resume)\s+([a-z0-9-]+)/` | RESUME 路由 → `kflow-resume` | 优先级链读状态 → 断点定位 → 门控验证（含产物完整性二次校验）→ 五问题摘要 → 服务检测 → 调度 |
| `/继续\s+([a-z0-9-]+)/` | 轻量推进 → 读 `.status.md` → 执行衔接决策 | 直接调度目标阶段 Skill |

**理由**：「继续」在日常语义中表达「往下走」，「恢复」表达「中断后回来」，两者对状态校验深度的需求不同。当前实现把两者合一且绑定到重流程，是反直觉的。拆分后每条路径语义单一，且轻量推进与阶段自动衔接复用同一决策表，无新逻辑。

**替代方案**：
- 给 RESUME 加参数控制深度 —— 否决，让单一 Skill 承担两种深度会使职责不清，且用户仍需记忆参数。
- 同一入口按状态自动判轻重 —— 否决，判据无法可靠区分「用户刚从断线回来」与「用户只是想让流程往下走」，误判代价高。

**注意**：`resume-plan-mode-bypass` 能力要求两条路径都不被 Plan Mode 拦截，需同步更新该能力的三条 requirement。

### D3：衔接决策表的单一真源

**决策**：`kflow-resume` 的 DISPATCH 步骤改为引用与各阶段 Skill 相同的 `references/phase-transition.md`，不再维护私有副本。

**理由**：决策表原本是 resume 私有实现，提取为通用规则后若不改 resume 侧，会产生两份会漂移的规则，违反 Token 效率原则。

### D4：guide description 触发词的收敛边界

**决策**：从 `kflow-guide` 的 description 中移除「做、添加、实现、搭建」四个新工作意图动词；**保留**「修复、Bug、缺陷」及其上下文判断。

**理由**：新工作意图已完全移交 `kflow-explore`（其 description 已声明入口地位），guide 侧保留只会造成误触发。但修复类意图不同——`intent-priority-rules` 规定的「有活跃 bug-fix 子阶段 → `kflow-bug-fix`，否则 → `kflow-bug-triage`」上下文判断仍是 guide 的职责，且 `kflow-bug-triage` 的 description 未覆盖「修复」这一动词，移除后会出现意图无承接的缺口。

### D5：自动衔接与人工门控的边界

**决策**：自动衔接免除的**仅为**「提示用户输入推进指令」这一步。阶段自身定义的人工门控（原型设计决策门控、详细设计用户评审、原型用户评审、审计用户验收门控）继续正常执行。

**理由**：用户诉求是「不要每次推进都手打一句话」，而非「跳过所有确认」。把门控一并跳过会越过设计方案确认、原型确认、验收确认等必要节点，属于超出诉求范围的改动。

**实现要点**：门控询问在 COMPLETE 之前或之内发生，衔接决策在门控通过之后执行。

### D6：归档阶段的硬性闸口

**决策**：衔接决策的推进目标 SHALL NOT 包含归档阶段。审计阶段完成后停止自动衔接，提示用户可发起归档但不自动调用 `kflow-archive`。

**理由**：与 `docs/designs/core-mechanisms/04-gates-and-transitions.md` §6.7「Archive 禁止自动流转」保持一致。归档是不可逆的流程终点，必须由用户显式发起。

## Risks / Trade-offs

- **[存量项目旧规则残留]** 消费方 CLAUDE.md 中的旧规则不会自动消失，未 re-init 的项目行为不变 → 在 `README.md` 的版本更新说明中明示「本次升级需重跑 `/kflow-init`」；不引入自动检测机制，避免变更范围扩散。
- **[轻量推进跳过产物完整性校验]** 「继续」路径不执行 resume 的 GATE 二次校验 → 由目标阶段 Skill 自有的入口门控兜底（各 skill 的 `references/gates.md` 已含产物存在性与前置阶段状态检查）。
- **[9 份 references 副本漂移]** `phase-transition.md` 在多 skill 间复制 → 纳入 `sync-references.sh` 的 `REF_FILES` 校验清单，纳入后由脚本检出不一致。
- **[移除 guide 新工作触发词后意图落空]** 用户说「做个 XXX」时不再命中 guide → `kflow-explore` 的 description 已声明 `Entry point for all changes` 并覆盖「开始新需求/设计探索/功能设计/需求澄清」触发词，由它承接；需在实现后验证 explore 触发词对「做/添加/实现」类表述的覆盖度。
- **[自动衔接与用户预期冲突]** 部分用户可能希望在阶段间停顿以便审阅 → 阶段产物均有自审与门控，且用户随时可中断；如实际反馈强烈，可将自动衔接降级为可配置项（本次不做）。
- **[既有 spec 偏差的修正面]** `intent-priority-rules` 中「继续类关键词 → 直接路由到当前阶段」原本就与实现不符，本次修正会使该能力的行为首次与实现对齐 → 无迁移成本，属修正而非破坏。

## Migration Plan

**实现顺序**（详见 `tasks.md`）

1. 新增 `references/phase-transition.md` 并把各阶段 Skill 的 COMPLETE 步骤指向它
2. 改写 `kflow-guide`：PARSE 正则拆分、INTENT 关键词表、description 触发词、删除 NEW CHANGE 指引与意图识别中的新变更分支
3. 改写 `kflow-init` 的 Marker 2 注入模板
4. 收敛 `kflow-resume` 的 DISPATCH 引用与 triggers
5. 同步设计文档、主 spec 的 Purpose、README

**Rollback**

纯文本产物变更，无数据迁移。回滚方式为 `git revert` 对应提交；已 re-init 的消费方项目需再次 re-init 以恢复旧规则文本。

**消费方动作**

升级后需重跑 `/kflow-init`，由 marker 版本判据替换「变更流程强制规则」section。不重跑则消费方行为保持原样（旧规则继续生效），不会因升级本身产生破坏。
