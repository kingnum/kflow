## MODIFIED Requirements

### Requirement: Shared repetition model definition file

The system SHALL provide `.claude/skills/kflow-shared/repetition-model.md` as the single source of truth for repetition mode execution specifications, including complexity formula, round enforcement rules (flexible for re-execution), acceptance criteria, subagent prompt specifications, subagent isolation rules, impact-based round decision logic, phase execution history tracking, and verification gate for non-standard repetition. §12 子代理隔离规则 SHALL 包含主 Agent 职责边界硬线声明（调度+验收，SHALL NOT 执行阶段主工作，无例外）和轮次级重试机制（子代理崩溃 → 新建 Agent 重跑该轮，≤3 次重试）。§12.5 权限预配置 SHALL 引用 `kflow-shared/permission-model.md` 而非硬编码权限列表。§12.7 SHALL 定义后台权限失败回退前台子代理机制。

#### Scenario: §12.5 权限预配置引用 permission-model.md

- **WHEN** `kflow-shared/repetition-model.md` §12.5 被读取
- **THEN** §12.5 SHALL 引用 `kflow-shared/permission-model.md` 作为权限声明的 source of truth
- **AND** §12.5 SHALL NOT 硬编码具体的权限列表
- **AND** §12.5 SHALL 说明"kflow-init SHALL 根据 `kflow-shared/permission-model.md` 在目标项目中自动配置权限"

#### Scenario: §12.7 后台权限失败回退前台子代理机制

- **WHEN** `kflow-shared/repetition-model.md` §12.7 被读取
- **THEN** §12.7 SHALL 定义后台子代理权限失败回退前台子代理机制，包含：
  - 权限错误模式检测规则
  - 创建新前台子代理（run_in_background=false）的执行规则
  - 主 Agent SHALL NOT 直接接管执行的硬线声明
  - 回退不计入轮次级重试 3 次上限的计数规则
  - 前台子代理也失败时标记 ⚠️ 阻塞的终止规则

#### Scenario: Subagent prompt references shared file

- **WHEN** an execution-phase Skill constructs a subagent prompt
- **THEN** the prompt SHALL reference `kflow-shared/repetition-model.md` instead of inlining repetition rules

#### Scenario: §12 子代理隔离规则强化

- **WHEN** `kflow-shared/repetition-model.md` §12 被读取
- **THEN** §12 SHALL 包含主 Agent 职责边界硬线声明：主 Agent 职责 = 调度 + 验收，SHALL NOT 直接执行编码/修复/测试/审查/计划等阶段主工作，无例外
- **AND** §12 SHALL 包含轮次级重试规则：某轮子代理崩溃 → 新建 Agent 重跑该轮，最多重试 3 次，全部失败标记 ⚠️ 阻塞
- **AND** §12.2 强制规则表 SHALL 更新重试粒度描述为"轮次级"而非"任务级"
