## MODIFIED Requirements

### Requirement: Shared repetition model definition file

The system SHALL provide `.claude/skills/kflow-shared/repetition-model.md` as the single source of truth for repetition mode execution specifications, including complexity formula, 10-round enforcement rules, acceptance criteria, subagent prompt specifications, and subagent isolation rules. §12 子代理隔离规则 SHALL 包含主 Agent 职责边界硬线声明（调度+验收，SHALL NOT 执行阶段主工作，无例外）和轮次级重试机制（子代理崩溃 → 新建 Agent 重跑该轮，≤3 次重试）。

#### Scenario: New file creation

- **WHEN** the change is applied
- **THEN** `kflow-shared/repetition-model.md` SHALL exist containing all content from `07-agent-model.md` §15 (complexity formula, round enforcement, acceptance criteria, prompt specifications, subagent isolation rules)

#### Scenario: Subagent prompt references shared file

- **WHEN** an execution-phase Skill constructs a subagent prompt
- **THEN** the prompt SHALL reference `kflow-shared/repetition-model.md` instead of inlining repetition rules

#### Scenario: §12 子代理隔离规则强化

- **WHEN** `kflow-shared/repetition-model.md` §12 被读取
- **THEN** §12 SHALL 包含主 Agent 职责边界硬线声明：主 Agent 职责 = 调度 + 验收，SHALL NOT 直接执行编码/修复/测试/审查/计划等阶段主工作，无例外
- **AND** §12 SHALL 包含轮次级重试规则：某轮子代理崩溃 → 新建 Agent 重跑该轮，最多重试 3 次，全部失败标记 ⚠️ 阻塞
- **AND** §12.2 强制规则表 SHALL 更新重试粒度描述为"轮次级"而非"任务级"

### Requirement: Core mechanism doc references shared file

`07-agent-model.md` §15 SHALL retain only a brief overview (≤5 lines) and a reference to `kflow-shared/repetition-model.md`. The full content SHALL be removed from the core mechanism doc.

#### Scenario: No duplicate content

- **WHEN** `07-agent-model.md` is read
- **THEN** §15 SHALL NOT contain the full complexity formula, round enforcement details, or prompt specifications — these SHALL only exist in `kflow-shared/repetition-model.md`
