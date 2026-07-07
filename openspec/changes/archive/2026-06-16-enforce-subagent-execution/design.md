## Context

当前 KFlow Skills 体系有 7 个执行类阶段采用重复制模式：plan / code / code-review / api-test / e2e-test / integration-test / bug-fix。这些阶段的主工作流程设计为通过 Agent 子代理执行，主 Agent 仅负责调度和验收。

子代理隔离规则已定义在 `repetition-model.md` §12 和 `openspec/specs/subagent-isolation-rule/spec.md`，但存在两个结构性缺陷：

1. **规则隐身**：隔离规则仅存在于共享文档，7 个执行类阶段 SKILL.md 中缺少显式禁令。执行时主 Agent 直接读取的是 SKILL.md，而非共享文档，导致规则在关键时刻不可见。
2. **重试粒度模糊**：当前规则表述为"同一子代理任务最多重试 3 次"，但"任务"粒度不明确——是指整个阶段执行、还是某一轮迭代？需明确为轮次级。

当前 `subagent-isolation-rule` spec 适用阶段清单仅覆盖 5 个阶段（explore/prototype-design/design/plan/code），缺少 code-review/api-test/e2e-test/integration-test/bug-fix。

## Goals / Non-Goals

**Goals:**
- 将子代理强制执行规则从"隐式引用"升级为"双写强制"——集中（共享文档）+ 分散（各 SKILL.md 内联规则框）
- 明确主 Agent 职责边界硬线：调度 + 验收，SHALL NOT 直接执行阶段主工作，无例外
- 细化重试粒度为轮次级：某轮子代理崩溃 → 新建 Agent 重跑该轮（≤3 次重试）
- 补全适用阶段清单至全部 7 个执行类阶段
- 同步更新设计文档和 openspec specs

**Non-Goals:**
- 不改变重复制 10 轮下限机制
- 不改变子代理 prompt 构建规范
- 不改变验收标准
- 不涉及创造性阶段（explore/prototype-design/design/audit/archive）的执行模式

## Decisions

### Decision 1: 规则双写策略（集中 + 分散）

**选择**：方案 B——集中强化 `repetition-model.md` §12 + 各 SKILL.md 内联规则框

**替代方案**：
- 方案 A（仅集中强化）：简洁但 SKILL.md 执行时规则不可见，主 Agent 可能忽略共享文档约束
- 方案 C（仅分散强化）：各 SKILL.md 各自内联完整规则，但与共享文档内容重复且可能不一致

**理由**：SKILL.md 是执行时的直接上下文，规则必须在 SKILL.md 中可见。共享文档作为 single source of truth 提供权威定义，SKILL.md 内联规则框提供执行时可见性。两者引用关系明确：SKILL.md 规则框注明"参见 repetition-model.md §12"。

### Decision 2: SKILL.md 内联规则框格式

**选择**：在每个 SKILL.md 的重复制执行流程章节前，新增独立的 `⚠ 子代理强制规则` 引用框

**格式**：
```
> ⚠ **子代理强制规则**（参见 kflow-shared/repetition-model.md §12）:
> 1. {阶段}主工作 MUST 通过 Agent 子代理执行，主 Agent 仅负责调度和验收
> 2. 主 Agent SHALL NOT 直接执行{阶段}主工作（编码/修复/测试/审查/计划等），无例外
> 3. 子代理崩溃 → 新建 Agent 重跑该轮（≤3 次重试），全部失败标记 ⚠️ 阻塞
```

**理由**：引用框格式在 SKILL.md 中醒目且紧凑，不破坏现有文档结构。三条规则覆盖完整的强制执行→禁止接管→失败重试链路。

### Decision 3: 重试粒度为轮次级

**选择**：重试粒度定义为"轮次级"——某轮子代理异常时，新建 Agent 重跑该轮，而非重启整个阶段

**替代方案**：
- 任务级重试（重启整个阶段）：成本高，已完成的轮次信息丢失
- 子轮级重试（重跑某个工作项）：粒度过细，增加复杂度但收益有限

**理由**：轮次级是重复制的天然边界。每轮有独立的 `.status.md` 轮次计数器，崩溃时主 Agent 知道当前轮次号，新建子代理从该轮继续即可。已完成的轮次产物（traceability.md 更新等）保留，不浪费。

### Decision 4: 适用阶段扩展范围

**选择**：覆盖全部 7 个执行类阶段 + 保留创造性阶段的隔离规则

| 类别 | 阶段 | 子代理强制规则 | 原隔离规则 |
|------|------|--------------|-----------|
| 执行类 | plan | ✅ 新增规则框 | ✅ 保留 |
| 执行类 | code | ✅ 新增规则框 | ✅ 保留 |
| 执行类 | code-review | ✅ 新增规则框 | ✅ 保留 |
| 执行类 | api-test | ✅ 新增规则框 | ✅ 保留 |
| 执行类 | e2e-test | ✅ 新增规则框 | ✅ 保留 |
| 执行类 | integration-test | ✅ 新增规则框 | ✅ 保留 |
| 执行类 | bug-fix | ✅ 新增规则框 | ✅ 保留 |
| 创造性 | explore | — | ✅ 保留（SELFREV） |
| 创造性 | prototype-design | — | ✅ 保留（DESIGN/VERIFY/SELFREV） |
| 创造性 | design | — | ✅ 保留（SELFREV/四视角审查） |

**理由**：创造性阶段的主流程由主 Agent 直连执行，子代理仅用于自审/验证等辅助环节，不适用"主工作 MUST 通过子代理执行"的强制规则。但隔离规则（子代理异常时重新创建、主代理不得接管）仍然适用。

## Risks / Trade-offs

- **[规则冗余] → 可控**：集中+分散双写导致规则在两处存在。缓解：SKILL.md 规则框为引用摘要格式，完整定义仅在 repetition-model.md，更新时以共享文档为准
- **[Token 开销增加] → 可接受**：7 个 SKILL.md 各新增约 5 行规则框，每轮子代理 prompt 增加约 100 token。与子代理独立性保障的收益相比，开销可忽略
- **[严格执行可能阻塞] → 有缓解**：3 次重试全部失败时标记阻塞并提示用户，而非无限重试或降级为主 Agent 接管
