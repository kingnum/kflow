## Context

KFlow Skills 是公司内部开发流程的阶段门控技能体系，目前包含 14 个 Skill。这次变更的系统上下文：

- **当前体系**：Change → Subchange 层级 + 阶段门控（`.status.md` 门控检查）
- **设计文档**：`docs/designs/skills/*.md` 定义各 Skill 规格
- **模板文件**：`docs/templates/` 提供状态文件、任务清单等模板
- **问题**：matpocock-skills 中多个成熟方法论未被吸收，调试、领域建模、TDD 层面存在方法论空白

## Goals / Non-Goals

**Goals:**
- 将 diagnose 的系统化调试方法论集成到 kflow-bug-fix 的 DISCOVER 步骤
- 建立项目级 CONTEXT.md 领域词汇表基础设施（构建 + 消费链）
- 在 kflow-design 阶段引入 ADR 架构决策记录机制
- 将 tdd 的测试哲学（vertical slice、反模式警告、检查清单）注入 kflow-code
- 在子变更划分中引入 HITL/AFK 分类
- 缺陷修复后增加 post-mortem 检查点，将架构洞察传递给 kflow-audit

**Non-Goals:**
- 不创建新的独立 Skill，所有增强内聚到现有 Skill 中
- 不改变现有阶段门控机制的核心逻辑
- 不引入 mattpocock-skills 的 issue tracker 集成（setup/triage/to-issues/zoom-out/prototype）
- 不修改 docs/templates/ 中的模板文件

## Decisions

### 决策 1：Feedback Loop 集成方式

**选择**：在 kflow-bug-fix 的 DISCOVER 步骤中内联引入 diagnose 的 Phase 1-3，而非创建独立 Skill

**替代方案**：创建 `kflow-diagnose` 独立 Skill
- 缺点：增加 Skill 数量，与 bug-fix 的 DISCOVER 步骤职责重叠
- 优点：可独立使用
- 结论：diagnose 的价值在于"构建反馈循环 → 复现 → 假设"，这是 bug-fix 的天然前置步骤，内聚优于拆分

**集成架构**：
```
DISCOVER（增强后）:
  1a. BUILD LOOP → 10 种方法优先级排序（自动化优先）
  1b. REPRODUCE → 确认失败模式一致，多轮复现
  1c. HYPOTHESISE → 生成 3-5 个可证伪假设，展示给用户
```

### 决策 2：CONTEXT.md 构建和消费链

**选择**：项目级 `CONTEXT.md` + kflow-init（检测）+ kflow-explore（增补）

**格式**：采用 grill-with-docs 的 CONTEXT-FORMAT.md 格式：
```markdown
# CONTEXT — {项目名} 领域词汇表

## {领域术语1}
- **定义**: ...
- **别名**: （可选，代码中出现的变体名）
- **边界**: 明确什么不是这个概念
```

**消费链**：
```
explore 构建 → design 引用审查 → plan 用于任务描述 → code 用于命名 → review 用于审查报告
```

### 决策 3：ADR 机制设计

**选择**：在 kflow-design 阶段按三条件过滤创建，每变更上限控制

**三条件**（来自 grill-with-docs）：
1. 难以逆转 — 改主意成本高
2. 缺上下文会奇怪 — 未来读者会问"为什么这么做？"
3. 真正做了权衡 — 有替代方案，选了其中一个

**上限**：
- 功能需求级变更 ≤ 2 个 ADR
- 产品级变更 ≤ 5 个 ADR
- 功能缺陷级变更通常 0 个 ADR

**过期条件**：每个 ADR 必须标注何时重新审视

**ADR 文件格式**（来自 grill-with-docs 的 ADR-FORMAT.md）：
```markdown
# ADR-{序号}: {标题}

**日期**: YYYY-MM-DD
**状态**: 提议 | 接受 | 废弃 | 取代
**过期条件**: {何时应重新评估此决策}

## 背景

## 决策

## 后果

## 替代方案
```

### 决策 4：TDD 增强方式

**选择**：在 kflow-code 的 TDD 循环段落注入哲学内容，保持现有 RED → GREEN → REFACTOR 结构

**新增内容**：
- Tracer Bullet 说明（第一个 RED→GREEN 证明端到端路径可用）
- 水平切片反模式警告框（先写所有测试 = 测试假想行为 = 不可靠测试）
- 每周期检查清单（测试描述行为 / 仅用公共接口 / 内部重构后不失败 / 代码最小 / 无投机功能）
- REFACTOR 增加"深化模块"引用（指向 `improve-codebase-architecture` 的接口深度概念）

### 决策 5：HITL/AFK 分类与 ralph-loop 集成

**选择**：在子变更划分结果表格中增加"执行类型"列

**分类定义**：
| 类型 | 含义 | 执行方式 |
|------|------|---------|
| AFK | 无人工决策点，编码+测试全自动 | ralph-loop 自动迭代 |
| HITL | 含架构选择/设计确认/UI方向等决策点 | Agent 执行到决策点 → AskUserQuestion 暂停 → 确认后继续 |

**与 ralph-loop 协作**：AFK 子变更直接启动 ralph-loop；HITL 子变更的 ralph-loop 在决策点暂停等待用户。

### 决策 6：Post-mortem 与 kflow-audit 的关联

**选择**：在 kflow-bug-fix 的 REPORT 步骤后增加轻量 post-mortem 检查点，架构改进建议记录到 fix-report 的"关联建议"字段，leadl-audit 归档评估时读取汇总。

**不采用**：创建独立 post-mortem 阶段 — 过于重，与 bug-fix 的自然流程不匹配。

## Risks / Trade-offs

| 风险 | 缓解措施 |
|------|---------|
| CONTEXT.md 在创建初期不完整，后续 Skill 引用空文件 | kflow-explore 增补流程强制检查新术语是否已录入 |
| ADR 可能过度创建导致噪音 | 三条件过滤 + 每变更上限 + 过期条件三重约束 |
| Feedback loop 自动化方法部分失败 | 10 种方法优先级排序确保自动方法优先尝试，失败时降级 |
| HITL 子变更过多导致频繁暂停影响效率 | 设计阶段标注 HITL 时可提示用户减少决策点 |
| TDD 检查清单增加编码负担 | 检查清单以 ralph-loop 自检形式内嵌，不增加人工步骤 |
