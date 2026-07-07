## REMOVED Requirements

### Requirement: 执行类阶段统一使用 ralph-loop 子代理

**Reason**: ralph-loop Stop Hook 循环机制被 Agent 原生迭代能力取代（见 `agent-iteration-execution` spec）。
**Migration**: 所有执行类阶段改用 Agent 迭代执行模式，`/ralph-loop --max-iterations {N}` 替换为 `Agent(description, prompt, run_in_background)`。

### Requirement: 复杂度评估机制

**Reason**: 复杂度评估逻辑保留，但结果用途从 "ralph-loop --max-iterations" 改为 Agent prompt 中的节奏指引。
**Migration**: 复杂度公式不变（功能点数 × 1 + 接口数 × 1.5 + 场景数 × 2），结果嵌入 Agent prompt 作为 pacing guidance。

### Requirement: COMPLETED 完成承诺

**Reason**: Agent 原生执行时自然返回，不再需要 `<promise>COMPLETED</promise>` 标签供外部 Hook 检测。
**Migration**: Agent 完成任务后自然返回验收报告。主 Agent 验收逻辑不变。

### Requirement: 主 Agent 验收

**Reason**: 验收逻辑完全保留，仅术语从 "ralph-loop 子代理" 改为 "Agent 迭代子代理"。
**Migration**: 验收条件不变（产物完整性、覆盖率=100%、无占位符），验收不通过流程不变（skill-suggestion.md + AskUserQuestion）。

### Requirement: ralph-loop 子代理提示词规范

**Reason**: prompt 构建规范保留核心内容，术语更新。
**Migration**: prompt 仍包含阶段目标、输入引用、traceability.md 列、迭代指令。新增复杂度节奏指引。
