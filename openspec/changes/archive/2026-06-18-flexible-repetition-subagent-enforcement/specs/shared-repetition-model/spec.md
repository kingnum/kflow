## MODIFIED Requirements

### Requirement: Shared repetition model definition file
The system SHALL provide `.claude/skills/kflow-shared/repetition-model.md` as the single source of truth for repetition mode execution specifications, including complexity formula, round enforcement rules (flexible for re-execution), acceptance criteria, subagent prompt specifications, subagent isolation rules, impact-based round decision logic, phase execution history tracking, and verification gate for non-standard repetition. §12 子代理隔离规则 SHALL 包含主 Agent 职责边界硬线声明（调度+验收，SHALL NOT 执行阶段主工作，无例外）和轮次级重试机制（子代理崩溃 → 新建 Agent 重跑该轮，≤3 次重试）。

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

### Requirement: Flexible round decision logic

The shared repetition model SHALL include logic for determining repetition rounds based on execution history and impact scope score.

#### Scenario: Round decision added to shared model

- **WHEN** `kflow-shared/repetition-model.md` is read
- **THEN** it SHALL contain a new section on "Flexible Round Decision" that defines:
  - First execution: 10 rounds (standard)
  - Re-execution after rollback: rounds determined by impact scope score
  - Score 1-5: max(3, ceil(score)) rounds
  - Score 6-15: max(5, ceil(score/2)) rounds
  - Score >15: 10 rounds

#### Scenario: Verification gate in shared model

- **WHEN** `kflow-shared/repetition-model.md` flexible round section is read
- **THEN** it SHALL include verification gate requirements for non-standard repetition:
  - Affected items: 100% coverage verification
  - Full sweep: at least 1 round complete traversal
  - Product integrity: all required outputs exist

### Requirement: Phase execution history tracking in shared model

The shared repetition model SHALL define the format and usage of phase execution history tracking.

#### Scenario: Execution history format defined

- **WHEN** `kflow-shared/repetition-model.md` is read
- **THEN** it SHALL define the "Phase Execution History" table format:
  - Phase name, Execution count, Last execution type, Rounds completed, Impact scope score, Notes
- **AND** it SHALL define the "Recent Revision Info" section format:
  - Revision trigger, Source phase, Timestamp, Content summary, Affected items, Impact score, Recommended rounds

### Requirement: Impact scope score reading mechanism

The shared repetition model SHALL define how execution phases read and use impact scope score from .status.md.

#### Scenario: Score reading on phase start

- **WHEN** an execution phase starts
- **THEN** the main Agent SHALL read .status.md "Recent Revision Info" section
- **AND** extract the impact scope score
- **AND** use the score to determine round count per the flexible round decision logic

### Requirement: Core mechanism doc references shared file
`07-agent-model.md` §15 SHALL retain only a brief overview (≤5 lines) and a reference to `kflow-shared/repetition-model.md`. The full content SHALL be removed from the core mechanism doc.

#### Scenario: No duplicate content
- **WHEN** `07-agent-model.md` is read
- **THEN** §15 SHALL NOT contain the full complexity formula, round enforcement details, or prompt specifications — these SHALL only exist in `kflow-shared/repetition-model.md`

### Requirement: Skill design docs reference shared file
All execution-phase Skill design documents (kflow-code.md, kflow-code-review.md, kflow-api-test.md, kflow-e2e-test.md, kflow-integration-test.md) SHALL replace their inline repetition mode sections with a reference to `kflow-shared/repetition-model.md` plus phase-specific parameters only.

#### Scenario: Skill design doc redundancy eliminated
- **WHEN** kflow-code.md repetition section is read
- **THEN** it SHALL contain only: (1) a reference to `kflow-shared/repetition-model.md`, (2) phase-specific complexity weights, (3) phase-specific work item definitions, (4) phase-specific output requirements
