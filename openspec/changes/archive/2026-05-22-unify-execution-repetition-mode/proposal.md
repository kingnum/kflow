## Why

当前 7 个执行类阶段（plan/code/code-review/api-test/e2e-test/integration-test/bug-fix）均采用「Agent 迭代执行」模式，子代理按复杂度评估生成的「节奏指引」将 10 轮拆分为"前 N 轮重点执行 → 中间优化 → 后 N 轮验证"的增量推进。这种人为预设的节奏分配与实际开发中问题的出现分布不一致——可能在 Round 2 就该发现的问题被推迟到 Round 9 才发现，也可能在"重点执行"轮次中遗漏功能点直到"验证"轮次才暴露。**核心风险**：节奏指引创造了"这部分留给后面轮次"的心理暗示，导致子代理在执行中产生疏忽和遗漏。

## What Changes

- **7 个执行类阶段执行模式统一改为「重复制」**：每轮子代理遍历全部工作项（全部功能点/全部测试用例/全部代码变更），独立执行完整流程，10 轮自然收敛
- **移除节奏指引**：删除「低复杂度前 6 轮重点执行」「中复杂度前 4 轮重点+中间 3 轮优化」等分段策略，不再预设"哪轮做什么"
- **保留复杂度评估（仅信息展示）**：复杂度分仍然计算但不驱动执行行为，仅供主 Agent 验收时作为背景信息
- **保留 Tracer Bullet**：编码阶段首个 RED→GREEN 循环保持 Tracer Bullet 先行，确保端到端路径在首轮即被打通，避免第一轮就出现遗漏
- **保留现有机制**：强制子代理 + 10 轮下限 + 主 Agent 验收闭环 + 轮次计数器全部保留不变
- **每阶段明确定义「每轮工作内容」**：在各自 SKILL.md 和设计规格中写明每轮全量执行的具体内容（遍历哪些工作项、执行什么流程、输出什么产物）
- **core-mechanisms.md §15 更新**：将「Agent 迭代执行模式」章节改写为「重复制（执行类阶段）」

## Capabilities

### New Capabilities

- `execution-repetition-mode`: 执行类阶段重复制——7 个执行类阶段（plan/code/code-review/api-test/e2e-test/integration-test/bug-fix）的主执行工作统一采用重复制模式：子代理每轮遍历全部工作项独立执行完整流程，禁止按轮次分段分配工作重点，通过每轮全量遍历实现自然收敛。每阶段明确定义每轮工作内容。

### Modified Capabilities

- `agent-iteration-execution`: 移除节奏指引——复杂度评估公式和分级阈值保留但改为仅信息展示，不再作为「前 N 轮重点执行/中间 N 轮细节优化/后 N 轮验证」的分段依据。Prompt 中的分阶段目标指令替换为重复制遍历指令。复杂度评估保留但标注为「仅信息展示，不驱动执行行为」。

## Impact

- **Skills (7 个 SKILL.md + 7 个设计规格)**：kflow-plan, kflow-code, kflow-code-review, kflow-api-test, kflow-e2e-test, kflow-integration-test, kflow-bug-fix
- **核心机制**：docs/designs/core-mechanisms.md §15（Agent 迭代执行模式 → 重复制）
- **关联文档**：docs/designs/index.md, docs/designs/overview.md（术语和机制描述同步）
- **Specs**：agent-iteration-execution（修改）、execution-repetition-mode（新增）
- **无破坏性变更**：不影响已归档变更的 .status.md 格式，不影响门控规则，不影响阶段顺序
