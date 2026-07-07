## Context

每次子代理冷启动加载全部 9 个核心机制文档（~10K tokens），其中大量内容与当前阶段无关。~80 次调用累计 ~800K tokens 的固定开销。

## Goals / Non-Goals

**Goals:**
- 按阶段类型分层加载核心机制文档和 kflow-shared 文件
- 基础层所有阶段加载，阶段特定层按需加载
- 减少每次子代理调用的固定 Token 开销

**Non-Goals:**
- 不改变任何机制的语义
- 不修改子代理的隔离规则
- 不改变 Skill 的执行流程

## Decisions

### D1: 分层定义

| 层级 | 加载文件 | 适用阶段 | 估算 Tokens |
|------|---------|---------|:-----------:|
| 基础层 | 01-project-types.md（摘要）, kflow-shared/state-values.md（摘要）, kflow-shared/gate-rules.md（仅当前阶段相关门控） | 全部 | ~2,000 |
| 执行层 | kflow-shared/repetition-model.md | plan/code/code-review/api-test/e2e-test/integration-test/bug-fix | +3,000 |
| 服务层 | kflow-shared/service-lifecycle.md, phase-hooks.md（服务相关章节） | api-test/e2e-test/integration-test | +2,000 |
| 创意层 | kflow-shared/self-review.md | explore/prototype-design/design | +2,500 |
| 恢复层 | kflow-shared/recovery-protocol.md | 仅恢复场景 | +1,000 |
| 归档层 | kflow-shared/archive-rules.md | archive | +1,500 |

### D2: 加载清单标注

每个核心机制文档和 kflow-shared 文件头部添加加载层级标注：
```markdown
> **加载层级**: 基础层 | 执行层 | 服务层 | 创意层
> **适用阶段**: 全部 | plan/code/... | ...
```

### D3: 子代理 prompt 构建规范

各阶段 SKILL.md 的子代理 prompt 构建章节更新，列出该阶段需要加载的文件清单。

## Risks / Trade-offs

| 风险 | 缓解 |
|------|------|
| 分层遗漏：子代理缺少必要的上下文 | 基础层始终加载；门控规则按阶段筛选而非完全省略 |
| 标注维护负担：新增文件时忘记标注层级 | kflow-skills-auditor 检查所有核心机制和 kflow-shared 文件必须有加载层级标注 |
