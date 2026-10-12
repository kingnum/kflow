# Spec Delta

## MODIFIED Requirements

### Requirement: Playwright 全覆盖验证轮次（收敛驱动）

系统 SHALL 在审查方式为「子代理自动审查验证」且导航合理性验证（9.1 节）完成后，执行**不少于 1 轮、不超过 5 轮**的 Playwright 全覆盖验证，每轮启动一个独立子代理执行全部 5 项检查；达成收敛终止条件（最近一轮为见证轮）时 SHALL 提前结束。到达终止点且累积未复核修复清单非空时，系统 SHALL 追加 1 轮复检轮，该轮 SHALL NOT 消耗 1–5 轮的轮次上限，且 SHALL 最多追加 1 轮。审查方式为「人工审查」时，系统 SHALL NOT 执行 Playwright 验证，SHALL NOT 追加复检轮。系统 SHALL 确保 playwright 运行时环境隔离到 `.kflow-runtime/playwright/`，工作目录固定为项目根目录。

#### Scenario: 前置条件满足时进入 Playwright 验证

- **WHEN** 审查方式为「子代理自动审查验证」且导航合理性验证完成后
- **THEN** 系统 SHALL 进入 Playwright 验证（9.2 节）
- **AND** 系统 SHALL 启动串行子代理验证，轮次不少于 1 轮、不超过 5 轮

#### Scenario: 人工审查路径跳过 Playwright 验证

- **WHEN** 用户选择的审查方式为「人工审查」
- **THEN** 系统 SHALL NOT 执行 Playwright 验证
- **AND** SHALL NOT 启动 Playwright 验证子代理
- **AND** SHALL NOT 追加复检轮
- **AND** 系统 SHALL 直接进入用户评审（REVIEW）

#### Scenario: 每轮子代理启动

- **WHEN** 进入 Playwright 验证（9.2 节）
- **THEN** 系统 SHALL 串行启动子代理，每轮子代理类型为 `Agent(subagent_type="claude")`
- **AND** 每个子代理 SHALL 使用 `/playwright-cli` 执行全部 5 项 Playwright 检查
- **AND** 子代理工作目录 SHALL 固定为项目根目录
- **AND** 原型 HTML 文件 SHALL 通过 `docs/designs/prototypes/index.html` 相对路径引用
- **AND** 每轮子代理完成后，主 Agent SHALL 读取其报告并修复发现问题

#### Scenario: 收敛或达上限终止

- **WHEN** Playwright 验证执行中（审查方式为「子代理自动审查验证」）
- **THEN** 最近一轮为零新发现、零修复且报告证明 5 项检查已全量执行的见证轮时，系统 SHALL 终止验证
- **AND** 否则 SHALL 继续下一轮，直至达到轮次上限 5 轮
- **AND** SHALL NOT 因「必须完成全部 5 轮」而继续执行无增量价值的轮次

#### Scenario: 终止点清单非空时追加复检轮

- **WHEN** Playwright 验证到达终止点（最近一轮为见证轮，或已达到轮次上限 5 轮）
- **AND** 累积未复核修复清单非空
- **THEN** 系统 SHALL 追加 1 轮复检轮
- **AND** 该轮 SHALL NOT 计入 1–5 轮的轮次上限
- **AND** 该轮 SHALL 逐项复核清单内全部修复，并证明 5 项检查已完成全量遍历

#### Scenario: 复检轮通过后终止

- **WHEN** 复检轮零新发现、零修复、证明 5 项检查全量遍历且清单内全部修复逐项复核通过
- **THEN** 系统 SHALL 终止 Playwright 验证
- **AND** 终止原因 SHALL 记录为 `收敛（复检轮）`

#### Scenario: 复检轮未通过后终止

- **WHEN** 复检轮未满足通过判据
- **THEN** 系统 SHALL 终止 Playwright 验证
- **AND** 终止原因 SHALL 记录为 `达上限`
- **AND** 系统 SHALL 进入非收敛分支

### Requirement: Playwright 验证报告

每轮子代理 SHALL 输出验证报告到指定路径。

#### Scenario: 报告输出

- **WHEN** 子代理完成一轮 Playwright 验证
- **THEN** 子代理 SHALL 保存报告到 `self-reviews/prototype/playwright-check/round-{N}.md`（N 为轮次 1-5）
- **AND** 报告 SHALL 包含 5 项检查各自的结果、pageerror 统计、发现问题和建议修复

#### Scenario: 复检轮报告输出

- **WHEN** 子代理完成复检轮
- **THEN** 子代理 SHALL 保存报告到 `self-reviews/prototype/playwright-check/round-recheck.md`
- **AND** 该报告 SHALL 明确标注其为复检轮
- **AND** 该报告 SHALL 包含清单内每一项修复的逐项复核结果与全量遍历证明
