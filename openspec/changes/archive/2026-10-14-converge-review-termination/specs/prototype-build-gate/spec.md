# Spec Delta

## MODIFIED Requirements

### Requirement: 子代理自动审查验证路径

用户选择"子代理自动审查验证"时，系统 SHALL 执行导航验证、Playwright 验证、UX 规则审查与原型阶段 SELFREV。

#### Scenario: 执行四项自动验证

- **WHEN** 审查方式为"子代理自动审查验证"
- **THEN** 系统 SHALL 依次执行导航验证、Playwright 验证、UX 规则审查（各为下限 1 轮，轮数由收敛决定，达成见证轮即收敛终止）
- **AND** 系统 SHALL 执行对比度检测（WCAG 相对亮度计算，标记 <4.5:1 的颜色对），报告输出到 `self-reviews/prototype/contrast-check/report.md`
- **AND** 系统 SHALL 执行原型阶段 SELFREV（下限 1 轮，轮数由收敛决定）
- **AND** 各项验证 SHALL 串行执行，SHALL NOT 并行启动多个子代理

#### Scenario: 自动验证不通过时修复后继续

- **WHEN** 某一轮自动验证发现问题
- **THEN** 主 Agent SHALL 修复原型产物后启动下一轮
- **AND** 系统 SHALL 在达成见证轮（收敛）后方可进入用户评审（REVIEW）
- **AND** SHALL NOT 以任何轮数上限作为进入用户评审的终止依据
