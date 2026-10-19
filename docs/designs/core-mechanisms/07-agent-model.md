# KFlow Skills 核心运行机制

> **版本**: 参见仓库根目录 `VERSION` 文件
> **创建时间**: 2026-04-29
> **更新时间**: 2026-05-17
> 
> **终止模型（当前）**: 审查按执行模型分为三类。**设计类与计划阶段的自审（SELFREV）固定单轮**——主 Agent 写作时按 4 维度签署清单自证（零子代理）→ 1 轮独立子代理验证打假 → 主 Agent 统一修复，不追加确认轮；终止结果 `验证通过` / `验证发现问题({N})`。**单轮类阶段**（接口单元测试 / E2E 测试 / 集成测试）执行单轮全面执行 + 定向重验（仅重跑失败用例，有界重试）。**重复制类阶段**（编码 / 代码审查 / 缺陷修复）沿用重复制循环，每轮全量遍历全部工作项，连续 3 轮无实质进展时停滞升级。变更档位只决定**审查形态与产出深度**，SHALL NOT 决定轮数。审查范围冻结（审查对象集合冻结、审查维度集合封闭）仍适用：冻结范围之外的发现降级为「范围外观察」，不改产物、不计入发现数。权威定义见 `signed-checklist-verification`（签署清单与打假契约）、`convergence-driven-repetition`（审查轮数与范围冻结）与 `agent-iteration-execution`（执行类阶段）能力。参见 `docs/designs/skills/kflow-explore.md`（初判）与 `kflow-design.md`（复核）。
>
> **v2.4.0**: 执行类阶段统一重复制——7 个执行类阶段主执行工作从「Agent 迭代执行+节奏指引」改为「重复制」：每轮全量遍历全部工作项独立执行完整流程，移除节奏指引（前 N 轮重点执行/中间 N 轮细节优化/后 N 轮验证），复杂度评估标注为仅信息展示，保留强制子代理+档位轮次决策（轮次由变更档位决定，回退按影响范围分数叠加）+主 Agent 验收闭环。

> **加载层级**: 基础层
> **适用阶段**: 全部

本文档定义 KFlow Skills 体系的核心运行机制，包括目录结构、状态文件、任务清单、阶段流转规则、回退机制和条件产物引用规范。

---


## 十五、子代理执行模型

> **版本**: 1.8.0 新增

> 完整规范参见 `各执行类 skill 的 references/repetition.md`

### 15.1 概述

执行类阶段按执行模型分为两类：

**单轮类阶段**（接口单元测试 / E2E 测试 / 集成测试）：SHALL 在一轮内遍历全部工作项执行完整流程，SHALL NOT 执行第二轮全量审查；发现失败项时走**定向重验**——仅重跑失败用例、不重跑全量，属有界重试。定向重验 SHALL NOT 使用轮次循环判据，且与已移除的 `recheck-round` 语义不同：`recheck-round` 指审查循环到达终止点后追加的复核轮（因依赖已废除的轮数上限而被移除），定向重验触发于测试失败后的修复动作。

**重复制类阶段**（编码 `kflow-code` / 代码审查 `kflow-code-review` / 缺陷修复 `kflow-bug-fix`）：沿用重复制子代理循环。每轮遍历全部工作项独立执行完整流程，禁止按轮次分段分配工作重点；当某轮无新发现且无可执行工作时返回执行报告（须证明全部工作项已完成全量遍历），SHALL NOT 为凑轮次而执行无增量价值的轮次；连续 3 轮无实质进展（同一问题项反复出现）时返回执行报告并标注停滞缘由，升级用户（记录 `docs/skill-suggestion.md` + AskUserQuestion + 可标记 ⚠️ 阻塞）。

kflow-plan 阶段的产物自审由 `plan-self-review` 能力承载，不适用本节模型；设计类阶段（explore / prototype-design / design）的自审见 §16。

**审查范围冻结**：审查对象集合由主 Agent 从阶段产物既有内容生成并冻结，审查维度限于该阶段固定枚举；子代理 SHALL NOT 扩大审查对象集合、SHALL NOT 新增审查维度、SHALL NOT 借审查之名新增功能点/字段/章节/分支。冻结范围之外的发现降级为「范围外观察」——不修改产物、不计入发现数。审查对象集合 MAY 因阶段输入变化（如回退重执行新增受影响项）由主 Agent 更新。

**工作量分片上限**：单个子代理承担的工作量 SHALL NOT 超过 **3 个功能点**或 **10 个 TDD 步骤**。超出该上限的工作 SHALL 被拆分为多个子代理按序执行——前一个子代理返回并落盘后，由主 Agent 启动后一个子代理承接剩余工作；子代理在完其所分配工作量前判断剩余工作需另行承接时，SHALL 落盘当前进度并返回，说明剩余工作范围，主 Agent SHALL 启动新子代理承接，SHALL NOT 在主 Agent 上下文中继续。

> **仅重复制类阶段**（编码 / 代码审查 / 缺陷修复）适用本上限；单轮类测试阶段（接口单元测试 / E2E 测试 / 集成测试）的输入工作项已在设计阶段拆为用例级，超限场景由「按测试用例分片」自然覆盖，SHALL NOT 额外套用功能点计数。分片 SHALL NOT 改变「每轮遍历全部工作项」的既有要求——分片仅决定单次子代理调用的工作量边界，该轮次的遍历范围仍为阶段工作项全集。

> **工作量上限与轮数上限的口径区分**：二者是两类不同的约束，SHALL NOT 混用。工作量上限约束**单个子代理承担的功能点数或 TDD 步数**，是允许且强制的要求；轮数上限约束**阶段的执行轮次**，属 prompt 禁止项（见下）。工作量上限 SHALL NOT 被表述为「最多执行 N 轮」。

**档位语义**：变更档位由设计面分数（`功能点数 × 1 + 接口契约变更数 × 1.5 + 数据模型变更数 × 2`）派生，只决定**审查形态**（轻量单 Agent 串行覆盖全部视角 / 标准两视角并行）与产出深度，SHALL NOT 决定轮数。复核阶段的硬升档（数据迁移、破坏性契约变更、跨变更契约影响）不可拒绝；软升档默认保持当前档位并仅在新增下游测试阶段时提示。变更级 `.status.md` 不含「变更档位」字段，或读取到历史变更遗留的 `完整` 取值时，按 `标准` 档确定审查形态与产出深度。

**验证门控**：受影响项 100% 覆盖（回退重执行场景，存在受影响项清单时）+ 产物完整性；两项全部通过方验收通过。

**主 Agent 验收**：以「执行报告完整（含全量遍历证明）+ 阶段产物齐全 + traceability 覆盖率达标 + 无 TODO/TBD/{待填写} 占位符」为通过条件；单轮类阶段另须定向重验全部通过。SHALL NOT 以轮次数量作为通过或拒收依据。验收发现子代理引入冻结范围之外的新内容时 SHALL 拒收并要求其在冻结范围内重新执行。

`执行轮次` 字段格式为 `{N} 轮`（无分母，下限 1 轮）；读取侧遇到历史 `{N} / {上限}` 形式时取分子、忽略分母。

> 完整规范（复杂度公式、轮次执行细节、prompt 规范、工作量分片、审查范围冻结、验证门控）参见 `各执行类 skill 的 references/repetition.md`；权威定义见 `agent-iteration-execution` 能力

### 15.2 轮间摘要传递

> **版本**: 2.6.0 新增

轮间摘要 SHALL 仅由**重复制类阶段**（编码 / 代码审查 / 缺陷修复）使用；设计类阶段自审、kflow-plan 自审与测试三阶段（接口单元测试 / E2E 测试 / 集成测试）SHALL NOT 使用。重复制类阶段每轮子代理返回后，主 Agent 从审查报告/产物差异中提取轮间摘要（已修复问题/未解决问题/覆盖率变化/**范围外观察**/本轮建议关注），注入下一轮子代理 prompt，使后期轮次可优化注意力分配（已修复项快速回归/未解决项重点分析/未涉及项全量兜底）。摘要仅优化注意力分配，不跳过任何工作项，全量遍历兜底始终保留；摘要 SHALL NOT 承载跨轮累积的修复清单——修复由该阶段自身的执行报告追踪。**范围外观察**字段承载冻结范围之外的发现，使后续轮次不重复发现同一范围外内容；字段为空时 SHALL 记为「（空）」。

> 完整规范参见 `各执行类 skill 的 references/repetition.md` §13

### 15.3 子代理隔离规则强化

> **版本**: 2.7.0 新增（变更 enforce-subagent-execution），2.8.0 新增后台权限失败回退（变更 portable-permission-propagation），2.9.0 硬线升级为工具级强制（变更 optimize-context-budget）

§12 强化内容：
- **主 Agent 职责边界硬线**：执行类阶段主 Agent 职责 = 调度 + 验收，SHALL NOT 直接执行阶段主工作（编码/修复/测试/审查/计划等），无例外
- **硬线由阶段感知的工具级门控强制实施**：硬线 SHALL NOT 仅依赖 SKILL.md 中的声明性约束——声明性约束已实测被违反（执行类阶段主 Agent 自行 `Edit` 生产代码、自行运行多轮 `pytest`，单会话产生 169~254 次 `Bash`、66~215 次 `Edit`）。硬线 SHALL 由 `main-agent-execution-gating` 能力提供的 `PreToolUse` 门控强制实施：由变更级 `.status.md` 的当前阶段字段判定是否执行类阶段，据此拒绝主 Agent 的越界 `Edit`/`Write` 与长输出构建测试命令。门控的判定来源、白名单与黑名单命令模式见该能力；无法判定当前阶段时放行（门控的目的是降低上下文消耗，不是安全边界）
- **轮次级重试**：某轮子代理崩溃 → 新建 Agent 重跑该轮（≤3 次重试），全部失败标记 ⚠️ 阻塞
- **后台权限失败回退前台子代理**：后台子代理因权限问题失败时，主 Agent SHALL 创建新的前台子代理（run_in_background=false）重新执行，SHALL NOT 直接接管，回退不计入轮次级重试 3 次上限
- **权限预配置**：由 kflow-init 根据 `kflow-init 的 references/permission-model.md` 自动配置，取代手动预配置
- **双写强制**：集中定义在 `各执行类 skill 的 references/repetition.md` §12，各执行类阶段 SKILL.md 内联规则框

> **门控拒绝不等于流程阻塞**：门控拒绝一次工具调用时，主 Agent SHALL 转而创建子代理执行该工作，SHALL NOT 将拒绝视为阻塞或据此中止流程。拒绝原因（`permissionDecisionReason`）为**指导性内容**，回传给主 Agent 作为改派子代理的依据。门控拒绝记录 SHALL 可观测，供审计阶段核验职责边界遵守情况（参见 `08-governance.md`）。

> 完整规范参见 `各执行类 skill 的 references/repetition.md` §12；门控机制权威定义见 `main-agent-execution-gating` 能力

## 十六、自审机制

> **版本**: 1.10.0 新增

> 完整规范参见 `各设计类 skill 的 references/self-review.md`

### 16.1 概述

kflow-explore、kflow-prototype-design、kflow-design、kflow-plan 四个阶段在产物初稿完成后执行自审（self-review）。自审固定为**单轮**：SHALL NOT 预置轮数上限，SHALL NOT 执行第二轮，SHALL NOT 存在 0 轮豁免路径。变更档位只决定**审查形态与产出深度**，SHALL NOT 决定轮数。

单轮由三个环节构成：

1. **主 Agent 签署自证（零子代理）**——主 Agent 在写作时按本阶段 4 个固定维度逐项填写「维度 / 自证结论 / 证据锚点」。证据锚点 SHALL 指向产物内的具体位置（章节号、功能点 ID、接口 ID、用例 ID 或表名之一）；锚点为空、或指向产物中不存在的内容时，该维度的签署 SHALL 判定为不成立。自证过程中发现某维度不通过时，SHALL 先行修复该产物并重新完成该维度自证。
2. **单轮独立子代理验证**——主 Agent 启动一个验证子代理（拥有独立上下文）。子代理执行契约强制为：**先独立遍历产物形成自身 4 维度结论（此阶段 SHALL NOT 读取签署清单，防锚定）→ 再逐项对照签署清单打假 → 输出验证报告**。执行顺序反转时该轮结果 SHALL NOT 被接受。子代理 SHALL NOT 修改任何产物（只报告）。
3. **主 Agent 统一修复**——主 Agent 按验证结论统一修复全部发现项，生成「本阶段修复清单」随产物交付下游。SHALL NOT 追加确认轮；修复结果由下游的交叉审查（设计类）或下游阶段验证。

各阶段维度：explore 为完整性 / 闭环性 / 必要性 / 清晰性；prototype 为覆盖性 / 一致性 / 可用性 / 完整性（覆盖性为第一优先级）；design 为一致性 / 完备性 / 可行性 / 可测性；plan 为计划阶段 4 个定制维度（任务覆盖完整性 / DoD 验收标准正确性 / HITL 标注准确性 / 任务粒度合理性）。审查对象集合由主 Agent 从阶段产物既有内容生成并冻结，审查维度集合封闭。

**终止结果**：单轮验证零发现且无签署不成立项时写入 `验证通过`；存在发现项或签署不成立项时写入 `验证发现问题({N})`，N 为该阶段发现总数。终止结果 SHALL 写入变更级 `.status.md`。读取侧遇到历史变更遗留的 `收敛` 取值 SHALL 归并为 `验证通过`，其余历史取值 SHALL 归并为 `验证发现问题`。

**审查范围冻结与范围外观察**：冻结范围之外的发现 SHALL NOT 触发产物修改、SHALL NOT 计入验证发现数，记为「范围外观察」写入验证报告的「范围外观察」小节（为空时记「（空）」），由主 Agent 在阶段终止时汇总并向用户提示。子代理引入冻结范围之外的新内容时，主 Agent SHALL 拒收该轮、要求其在冻结范围内重新验证，并将越界事实记录到 `docs/skill-suggestion.md`。

**评分语义**：验证报告 SHALL NOT 输出各维度 0–10 评分与不达标项清单。评分原为 `完整` 档专属的**报告输出深度**要求，本就不参与终止判定（单轮验证无论评分高低均在单轮结束时终止，发现项由主 Agent 统一修复）；档位枚举二值化后该触发条件不复存在，若改为对全部变更无条件生效，等同于给全部变更加一层无条件评分产出，与审计去除评分的既定方向相悖。

**子代理异常**：验证子代理意外停止、报错退出或返回不完整结果时，主代理 MUST 分析原因后重新创建新的子代理，SHALL NOT 在主 Agent 上下文中接管其未完成的工作；最多重试 3 次，全部失败后标记 ⚠️ 阻塞并提示用户。

**kflow-prototype-design 例外**：该阶段仅在该变更选择「子代理自动审查验证」审查方式时执行自审；选择「人工审查」时完全跳过 SELFREV，不启动任何验证子代理，直接进入用户评审 REVIEW 步骤。该跳过属**流程分支**，SHALL NOT 被视为 0 轮豁免。

**原型 VERIFY 合并验证**：kflow-prototype-design 的 VERIFY 步骤将导航合理性（5 项）、Playwright 全覆盖（5 项）、UX 规则审查与对比度检测合并为**单轮单报告**，报告固定存放于 `self-reviews/prototype/verify-report.md`，按「导航合理性 / Playwright 全覆盖 / UX 规则审查 / 对比度检测 / 验证结论」强制分区；对比度检测为静态计算，不启动独立子代理；Playwright 不可用时优先执行 `.kflow-runtime/playwright/` 隔离安装引导，安装失败再降级为手动文件分析并在报告对应分区记录原因。BUILD 四项静态门控保持不变（主 Agent 直接执行、零子代理）。权威定义见 `prototype-single-round-verify` 能力。

> **缺省回退**: 变更级 `.status.md` 不含 `变更档位` 字段，或读取到历史变更遗留的 `完整` 取值时，按 `标准` 档确定审查形态与产出深度。
>
> 签署清单结构、打假契约与终止结果取值的权威定义见 `signed-checklist-verification` 能力；审查轮数与审查范围冻结见 `convergence-driven-repetition` 能力与各设计类 skill 的 references/self-review.md。

## 十七、子代理上下文分层加载

> **版本**: 2.5.0 新增，2.6.0 加载粒度下沉到阶段级并补入切片规则（变更 optimize-context-budget）

子代理冷启动时按阶段分层加载各 skill 的 `references/` 文件，避免全量加载不相关的上下文。每个核心机制文档和 `references/` 文件头部标注了「加载层级」和「适用阶段」。

**加载粒度下沉到阶段级**：层级划分（基础层 / 执行层 / 服务层 / 创意层 / 恢复层 / 归档层）保持不变，但加载清单的粒度由「阶段类型」下沉到**「具体阶段 + 子代理职责」**——同一层级的文件在不同阶段被切片为不同内容，且同一阶段内不同职责的子代理加载的章节亦不同。实测子代理平均加载 46,734 字符的 references，其中约 85% 与本阶段无关，故粒度必须落到阶段级与章节级。

### 17.1 分层定义

| 层级 | 加载文件 | 适用阶段 |
|------|---------|---------|
| 基础层 | `state-values.md`、`gates.md` | 全部 |
| 执行层 | `repetition.md` | plan/code/code-review/api-test/e2e-test/integration-test/bug-fix |
| 服务层 | `service-lifecycle.md`、`hooks.md` | api-test/e2e-test/integration-test（hooks.md 另覆盖 prototype-design/code/audit/archive/bug-fix/bug-triage/design/explore/plan） |
| 创意层 | `self-review.md` | explore/prototype-design/design |
| 恢复层 | `recovery-protocol.md` | 仅恢复场景 |
| 归档层 | `archive-rules.md` | archive |

> 各阶段另加载本阶段的 `phase-transition.md`（阶段衔接决策与调度映射），与钩子机制同属阶段执行基础设施。

### 17.2 各阶段精确加载清单

清单精确到**文件 + 章节级定位**。各 skill 的 `references/` 副本为切片后的结果，下列章节号即该副本内的章节。

| 阶段 | 加载文件（章节级定位） |
|------|---------------------|
| explore | `state-values.md`（§1 阶段流转状态值、§4 变更档位字段）、`gates.md`（§1 门控规则标注约定、§2 阶段正向门控中 explore 条目）、`self-review.md`（explore 4 维度：完整性/闭环性/必要性/清晰性）、`clarify-convergence.md`（全文）、`phase-transition.md`（§2 衔接决策表中 explore 行、§3 explore→design 调度行） |
| prototype-design | `state-values.md`（§1、§3 原型设计阶段审查方式记录字段、§4）、`gates.md`（§1、§2 中 prototype 条目）、`self-review.md`（prototype 4 维度：覆盖性/一致性/可用性/完整性）、`hooks.md`（§二 2.2 浏览器进程阶段、§三 3.2、§四 RELOAD 清单中 prototype 行、§九 浏览器进程管理）、`phase-transition.md`（§2 prototype 行、§3 prototype→design 调度行） |
| design | `state-values.md`（§1、§2 用户评审状态值、§4、§5 阶段适用性声明字段）、`gates.md`（§1、§2 中 design 条目、§3 阶段回退门控中 design 条目）、`self-review.md`（design 4 维度：一致性/完备性/可行性/可测性）、`phase-transition.md`（§2 design 行、§3 design→plan 调度行） |
| plan | `state-values.md`（§1、§4）、`gates.md`（§1、§2 中 plan 条目、§7 HITL 阻塞 plan 入口规则）、`repetition.md`（§1 概述、§2 执行模型核心特征、§3 阶段分类、§8 主 Agent 验收标准、§9 验收失败记录与处理、§10 子代理 prompt 规范、§12 子代理隔离规则）、`hooks.md`（§四 RELOAD 清单中 plan 行、§三 1.1 轻量型 PRE_HOOK）、`phase-transition.md`（§2 plan 行、§3 plan→code 调度行） |
| code | `state-values.md`（§1、§4）、`gates.md`（§1、§2 中 code 条目、§8 编码阶段上游问题决策流程）、`repetition.md`（§1~§5 概述/核心特征/阶段分类/执行流程/复杂度评估、§6 Agent 提前返回处理、§7 Agent 完成判断、§8 主 Agent 验收标准、§9 验收失败记录与处理、§10 子代理 prompt 规范、§12 子代理隔离规则、§13 轮间摘要传递机制）、`hooks.md`（§二 2.3 编译验证阶段、§三 3.3、§四 RELOAD 清单中 code 行、§五 服务生命周期操作步骤中编译验证部分）、`tdd-checklist.md`、`service-guide-template.md`、`phase-transition.md`（§2 code 行、§3 code→code-review 调度行） |
| code-review | `state-values.md`（§1、§4）、`gates.md`（§1、§2 中 code-review 条目、§4 代码审查门控规则、§5 审查闭环验证规则）、`repetition.md`（§1~§3、§7、§8、§9、§10、§12、§13）、`hooks.md`（§四 RELOAD 清单中 code-review 行、§三 1.1）、`phase-transition.md`（§2 code-review 行、§3 code-review→api-test 调度行） |
| api-test | `state-values.md`（§1、§4）、`gates.md`（§1、§2 中 api-test 条目、§3 中 api-test 条目、§6 子变更依赖规则）、`repetition.md`（§1~§3、§7、§8、§9、§10、§12）、`service-lifecycle.md`（全文）、`hooks.md`（§二 2.4 后端服务阶段、§三 3.4、§四 RELOAD 清单中 api-test 行、§六 服务刷新规则、§七 服务停止超时链、§八 端口冲突检测）、`phase-transition.md`（§2 api-test 行、§3 api-test→e2e-test 调度行） |
| e2e-test | `state-values.md`（§1、§4）、`gates.md`（§1、§2 中 e2e-test 条目、§6）、`repetition.md`（§1~§3、§7、§8、§9、§10、§12）、`service-lifecycle.md`（全文）、`hooks.md`（§二 2.5 前后端服务阶段、§三 3.4、§四 RELOAD 清单中 e2e-test 行、§六 服务刷新规则、§七 服务停止超时链、§八 端口冲突检测、§九 浏览器进程管理）、`phase-transition.md`（§2 e2e-test 行、§3 e2e-test→integration-test 调度行） |
| integration-test | `state-values.md`（§1、§4）、`gates.md`（§1、§2 中 integration-test 条目、§6）、`repetition.md`（§1~§3、§7、§8、§9、§10、§12）、`service-lifecycle.md`（全文）、`hooks.md`（§二 2.5、§三 3.4、§四 RELOAD 清单中 integration-test 行、§六~§九）、`phase-transition.md`（§2 integration-test 行、§3 integration-test→audit 调度行、§5 归档闸口） |
| bug-fix | `state-values.md`（§1、§4）、`gates.md`（§1、§2 中 bug-fix 条目、§9 缺陷修复快车道门控规则）、`repetition.md`（§1~§3、§7、§8、§9、§10、§12、§13）、`hooks.md`（§三 2.6 缺陷修复快车道模式、§三 3.5、§四 RELOAD 清单中 bug-fix 行）、`phase-transition.md`（§2 bug-fix 行、§7 停止自动衔接时的用户提示） |
| bug-triage | `gates.md`（§1、§9 缺陷修复快车道门控规则）、`repetition.md`（§1~§3 概述/核心特征/阶段分类）、`hooks.md`（§四 RELOAD 清单中 bug-fix 行、§三 1.1）、`phase-transition.md`（§2 bug-triage 行、§3 bug-triage→bug-fix 调度行） |
| audit | `gates.md`（§1、§2 全阶段正向门控——审计为归档门控）、`hooks.md`（§四 RELOAD 清单中 audit 行、§三 1.1）、`phase-transition.md`（§2 audit 行、§3 audit→archive 调度行、§5 归档闸口） |
| archive | `hooks.md`（§四 RELOAD 清单中 archive 行、§三 1.1）、`archive-rules.md`（全文）、`phase-transition.md`（§2 archive 行、§5 归档闸口） |
| resume | `recovery-protocol.md`（全文）、`phase-transition.md`（§1~§3 概述/衔接决策表/调度映射表） |

> **同一阶段内按子代理职责细分**：上表为该阶段**子变更主工作子代理**的加载清单。承担审查/验证职责的子代理（交叉审查、单轮验证、审计）SHALL 仅加载其审查维度对应的章节，SHALL NOT 加载执行类章节（如 `repetition.md` 的执行流程与轮间摘要机制）。承担探路/信息收集职责的子代理（如 explore 的澄清子代理）SHALL 仅加载 `clarify-convergence.md` 与本阶段 `state-values.md`。

### 17.3 切片规则

共享 references 文件在分发到各 skill 前 SHALL 按以下规则切片。切片结果由 `scripts/sync-references.sh` 从 `references-src/` 下的权威源按 `references-src/slice-manifest.tsv` 生成——各 skill 的副本 SHALL NOT 逐一手工编辑。

**归属规则**：

| 序号 | 规则 | 说明 |
|------|------|------|
| 1 | 按规则的作用对象阶段归属 | 一条规则服务于哪个阶段，就进入该 skill 的切片。判定依据是该规则**约束的动作发生在哪个阶段**，而非该规则在文档中的位置 |
| 2 | 跨阶段通用规则进入所有相关 skill 的切片 | 门控标注约定（`gates.md` §1）、状态值定义（`state-values.md` §1/§4）、子代理隔离规则（`repetition.md` §12）等被多个阶段共同消费的规则，复制进所有相关 skill 的切片，SHALL NOT 只保留在一处 |
| 3 | 文件头部为全局元信息 | 首个章节号标题之前的内容（版本、来源、加载层级、适用阶段）在任何切片中均保留 |

**降级规则**：

| 序号 | 规则 | 说明 |
|------|------|------|
| 4 | 无法归属时保留全量形态并登记 | 若某规则确实无法归属单一阶段（如跨阶段的调度映射），该 skill 的该文件保留**全量形态**（不切片），并在本节的加载清单中登记该例外与理由。降级后 SHALL NOT 因「无法归属」而删除规则 |

**切片边界争议的处理**：一条规则同时适用于多个阶段时按规则 1 的判定依据归属；确实跨越阶段边界的（如 `phase-transition.md` 的阶段衔接决策表）按规则 4 处理。

### 17.4 RELOAD 与分层对齐

子代理执行 RELOAD 步骤时，SHALL 仅重新加载当前已加载层级的文件，不跨层级加载；重新加载 SHALL 按 §17.2 的章节级定位进行，SHALL NOT 整体读取未变化的文件（按需分片读取规则见 `large-doc-splitting` 能力）。

---
