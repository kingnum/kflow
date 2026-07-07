# Design: add-resume-and-guide-enhancements

## Context

当前 KFlow Skills 体系采用文档驱动的阶段门控机制。kflow-guide 作为入口 Skill 提供意图识别和活跃变更检测，kflow-init 负责环境初始化。整个系统依赖 .status.md、tasks.md、checkpoint 文件记录执行状态。

但存在两个缺口：
1. **无中断恢复机制**：会话中断后，用户无法在新会话中通过变更名称直接恢复执行。现有 guide 的「继续」关键词仅扫描所有活跃变更，没有「定位断点→输出摘要→调度阶段 Skill」的精确恢复路径。
2. **无定向指引能力**：guide 的黑白扫描模式无法针对特定变更输出定向指引，也没有新变更创建前的预检指引（类型分类、命名建议、冲突预检）。

本次设计基于 explore 阶段的讨论结论，维持以下约束：
- kflow-guide 只做指引，不创建文件
- 变更初始化创建保留在 kflow-explore
- kflow-resume 采用直接调度模式（方式 B）

## Goals / Non-Goals

**Goals:**
- 设计 `kflow-resume` Skill，支持通过变更标识名称精确恢复中断的变更执行，输出恢复摘要后直接调度阶段 Skill
- 增强 `kflow-guide`，支持变更名解析、定向指引、NEW CHANGE 指引（分类+命名建议+冲突预检）、RESUME 路由
- 增强 `kflow-init`，向 CLAUDE.md 注入变更流程强制规则

**Non-Goals:**
- 不修改 checkpoint 文件格式或机制（已有设计满足需求）
- 不修改阶段 Skill 的设计（文档驱动架构天然支持 resume）
- 不修改 kflow-explore 的 INIT 逻辑

## Decisions

### Decision 1: kflow-resume 采用直接调度模式

**选择**: resume 定位断点后直接 invoke 对应阶段 Skill（Skill tool）。

**理由**: 阶段 Skill 从文件（.status.md, tasks.md）读取状态，checkbox 已标记完成的任务会被自然跳过。不需要特殊 "resume mode"。直接调度比「输出建议让用户手动调用」减少一次用户交互。

**Alternatives considered**: 仅输出恢复摘要由用户手动调用——更简单但用户需多操作一步。

### Decision 2: 恢复状态读取优先级链

```
checkpoint/ (精确到步骤) → 子变更 .status.md (子变更阶段) → 变更级 .status.md (变更阶段) → tasks.md (checkbox 状态)
```

**理由**: checkpoint 是最精确的中断点记录，优先采用。fallback 到 .status.md 提供阶段级恢复能力。最差情况下仅靠 tasks.md checkbox 也能恢复。

### Decision 3: kflow-guide 不创建文件

**选择**: guide 的 NEW CHANGE 分支仅输出指引信息（变更类型、建议名称、冲突预检结果、下一步建议），不创建目录或文件。

**理由**: 保持 guide 的「只读指引」职责边界清晰。变更初始化是 kflow-explore 的职责，不应分散到两个 Skill。

### Decision 4: guide 的变更名解析采用正则模式匹配

**选择**: 在意图识别阶段用正则从用户输入中提取变更名称：

```
/继续|恢复|resume\s+([a-z0-9-]+)/ → RESUME 路由
/指引|引导|guide\s+([a-z0-9-]+)/   → 定向指引
```

**理由**: 变更名为 kebab-case（字母+数字+连字符），正则可精确捕获，无需额外 NLP。先匹配带变更名的模式，命中后走对应分支；未命中走现有逻辑。

### Decision 5: CLAUDE.md 注入采用 section marker 幂等策略

**选择**: kflow-init 用 `## 变更流程强制规则` 作为 marker 检测是否已注入。存在则替换，不存在则追加。

**理由**: init 可能被多次调用，需保证幂等。section 级替换避免内容重复累积。

## Risks / Trade-offs

- **[R] checkpoint 过期或缺失** → 回退到 .status.md 阶段级恢复。最差情况仅靠 tasks.md checkbox。均不丢失数据。
- **[R] 用户输入变更名拼写错误** → guide 的正则匹配会失败，回退到现有扫描逻辑列出所有活跃变更供选择。
- **[R] resume 调度的阶段 Skill 因文件状态异常而失败** → 阶段 Skill 自身的门控检查会拦截并报错，resume 不掩盖问题。
- **[R] CLAUDE.md 注入位置冲突** → section marker 方式精确定位，追加模式保证不破坏已有内容。

## Open Questions

- 无。三个设计方向已在 explore 阶段充分讨论并达成一致。
