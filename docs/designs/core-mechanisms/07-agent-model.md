# KFlow Skills 核心运行机制

> **版本**: 参见仓库根目录 `VERSION` 文件
> **创建时间**: 2026-04-29
> **更新时间**: 2026-05-17
> 
> **变更档位（当前）**: 执行类阶段与设计自审的目标轮次改由变更档位决定——执行类阶段（轻量 1 / 标准 3 / 完整 10），设计自审（轻量 0 / 标准 2 / 完整 10）。「首次一律最大」的两个固定下限（执行类阶段首次执行、设计自审首次执行各自一度固定为 10 轮）已废除，回退重执行取 `max(档位基线, 影响范围分数映射)`。参见 `docs/designs/skills/kflow-explore.md`（初判）与 `kflow-design.md`（复核）。
>
> **v2.4.0**: 执行类阶段统一重复制——7 个执行类阶段主执行工作从「Agent 迭代执行+节奏指引」改为「重复制」：每轮全量遍历全部工作项独立执行完整流程，移除节奏指引（前 N 轮重点执行/中间 N 轮细节优化/后 N 轮验证），复杂度评估标注为仅信息展示，保留强制子代理+档位轮次决策（轮次由变更档位基线决定，回退按影响范围分数叠加）+主 Agent 验收闭环。

> **加载层级**: 基础层
> **适用阶段**: 全部

本文档定义 KFlow Skills 体系的核心运行机制，包括目录结构、状态文件、任务清单、阶段流转规则、回退机制和条件产物引用规范。

---


## 十五、子代理执行模型

> **版本**: 1.8.0 新增

> 完整规范参见 `各执行类 skill 的 references/repetition.md`

### 15.1 概述

执行类阶段（计划/编码/代码审查/接口单元测试/E2E测试/集成测试/缺陷修复）统一采用**档位驱动的重复制**模式：目标轮次由变更档位基线决定，回退重执行取 `max(档位基线, 影响范围分数映射)`。子代理每轮遍历全部工作项独立执行完整流程，禁止按轮次分段分配工作重点。验证门控：受影响项 100% + 全量 ≥1 轮兜底 + 产物完整性。

**档位基线**：

| 变更档位 | 执行类阶段目标轮次 |
|---------|-----------------|
| 轻量 | 1 |
| 标准 | 3 |
| 完整 | 10 |

**回退重执行的叠加规则**：目标轮次 = `max(档位基线, 影响范围分数映射)`，映射为分数 <= 3 映射 1 轮、4~15 映射 3 轮、> 15 映射 10 轮。`.status.md` 中无影响范围分数可用时取档位基线。统一映射表定义于 `tier-driven-repetition` 能力，其他能力 SHALL 引用，不得另行定义数值区间。

> **缺省回退**: 变更级 `.status.md` 不含 `变更档位` 字段时按 `完整` 档处理（等价于历史行为）。
>
> 完整规范（复杂度公式、轮次执行细节、prompt 规范、叠加决策、验证门控）参见 `各执行类 skill 的 references/repetition.md`

### 15.2 轮间摘要传递

> **版本**: 2.6.0 新增

每轮子代理返回后，主 Agent 从自审报告/产物差异中提取轮间摘要（已发现问题/未解决问题/覆盖率变化/本轮建议关注），注入下一轮子代理 prompt，使后期轮次可优化注意力分配（已修复项快速回归/未解决项重点分析/未涉及项全量兜底）。摘要仅优化注意力分配，不跳过任何工作项，全量遍历兜底始终保留。

> 完整规范参见 `各执行类 skill 的 references/repetition.md` §13

### 15.3 子代理隔离规则强化

> **版本**: 2.7.0 新增（变更 enforce-subagent-execution），2.8.0 新增后台权限失败回退（变更 portable-permission-propagation）

§12 强化内容：
- **主 Agent 职责边界硬线**：执行类阶段主 Agent 职责 = 调度 + 验收，SHALL NOT 直接执行阶段主工作（编码/修复/测试/审查/计划等），无例外
- **轮次级重试**：某轮子代理崩溃 → 新建 Agent 重跑该轮（≤3 次重试），全部失败标记 ⚠️ 阻塞
- **后台权限失败回退前台子代理**：后台子代理因权限问题失败时，主 Agent SHALL 创建新的前台子代理（run_in_background=false）重新执行，SHALL NOT 直接接管，回退不计入轮次级重试 3 次上限
- **权限预配置**：由 kflow-init 根据 `kflow-init 的 references/permission-model.md` 自动配置，取代手动预配置
- **双写强制**：集中定义在 `各执行类 skill 的 references/repetition.md` §12，各执行类阶段 SKILL.md 内联规则框

> 完整规范参见 `各执行类 skill 的 references/repetition.md` §12

## 十六、自审机制

> **版本**: 1.10.0 新增

> 完整规范参见 `各设计类 skill 的 references/self-review.md`

### 16.1 概述

kflow-explore、kflow-prototype-design、kflow-design、kflow-plan 四个阶段在产物初稿完成后执行自循环审查（self-review），目标轮次由**变更档位**决定：

| 变更档位 | 设计自审目标轮次 |
|---------|----------------|
| 轻量 | 0（完全跳过自审，改以产物完整性门控替代） |
| 标准 | 2 |
| 完整 | 10 |

每轮由独立子代理串行执行全维度检查，按阶段类型采用不同维度组合（explore: 完整性/闭环性/必要性/清晰性；prototype: 覆盖性/一致性/可用性/完整性；design: 一致性/完备性/可行性/可测性；plan: 计划阶段 4 个定制维度）。

**评分底线仅完整档适用**：完整档每轮输出各维度评分（0-10 量纲），各维度评分均 > 8 方通过，未达标则补审至 10 轮上限；标准档按目标轮次执行，不适用评分底线。

**kflow-prototype-design 例外**：该阶段仅在该变更选择「子代理自动审查验证」审查方式时执行自审；选择「人工审查」时完全跳过 SELFREV，不计算目标轮次、不保留兜底轮次，直接进入用户评审 REVIEW 步骤。

> **缺省回退**: 变更级 `.status.md` 不含 `变更档位` 字段时按 `完整` 档处理（10 轮自审），等价于历史行为。
>
> **已废除**: 自审轮次曾按项目是否已有设计基础做二分（无设计基础时一律取上限、有设计基础时走弹性轮次），该二分及其判定信号（`docs/CONTEXT.md` 存在性与 `docs/designs/detailed-designs/` 非空）已删除。轮次不再取决于项目历史。
>
> 轮次取值与产物门控规则见 `tier-driven-repetition` 能力与各设计类 skill 的 references/self-review.md。

## 十七、子代理上下文分层加载

> **版本**: 2.5.0 新增

子代理冷启动时按阶段类型分层加载各 skill 的 `references/` 文件，避免全量加载不相关的上下文。每个核心机制文档和 `references/` 文件头部标注了「加载层级」和「适用阶段」。

### 17.1 分层定义

| 层级 | 加载文件 | 适用阶段 |
|------|---------|---------|
| 基础层 | state-values.md（摘要）、gate-rules.md（当前阶段相关门控） | 全部 |
| 执行层 | repetition-model.md | plan/code/code-review/api-test/e2e-test/integration-test/bug-fix |
| 服务层 | service-lifecycle.md、phase-hooks.md（服务相关章节） | api-test/e2e-test/integration-test |
| 创意层 | self-review.md | explore/prototype-design/design |
| 恢复层 | recovery-protocol.md | 仅恢复场景 |
| 归档层 | archive-rules.md | archive |

### 17.2 各阶段类型加载清单

| 阶段类型 | 加载层级 | 文件清单 |
|---------|---------|---------|
| 纯执行阶段（plan/code/code-review/bug-fix） | 基础层 + 执行层 | state-values.md + gate-rules.md + repetition-model.md |
| 测试阶段（api-test/e2e-test/integration-test） | 基础层 + 执行层 + 服务层 | state-values.md + gate-rules.md + repetition-model.md + service-lifecycle.md + phase-hooks.md |
| 设计阶段（explore/prototype-design/design） | 基础层 + 创意层 | state-values.md + gate-rules.md + self-review.md |

### 17.3 RELOAD 与分层对齐

子代理执行 RELOAD 步骤时，SHALL 仅重新加载当前已加载层级的文件，不跨层级加载。

---
