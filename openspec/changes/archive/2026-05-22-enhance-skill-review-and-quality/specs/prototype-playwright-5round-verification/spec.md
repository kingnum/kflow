## MODIFIED Requirements

### Requirement: Playwright 验证报告

每轮子代理 SHALL 输出验证报告到指定路径。

#### Scenario: 报告输出
- **WHEN** 子代理完成一轮 Playwright 验证
- **THEN** 子代理 SHALL 保存报告到 `self-reviews/prototype/playwright-check/round-{N}.md`（N 为轮次 1-5）
- **AND** 报告 SHALL 包含 5 项检查各自的结果、pageerror 统计、发现问题和建议修复
