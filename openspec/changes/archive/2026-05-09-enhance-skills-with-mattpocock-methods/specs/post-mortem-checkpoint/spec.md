## ADDED Requirements

### Requirement: Post-mortem 检查点

系统 SHALL 在缺陷修复完成、本地验证通过后执行 post-mortem 检查点，回答"什么可以防止此缺陷发生"。

#### Scenario: Post-mortem 触发

- **WHEN** kflow-bug-fix 的修复已完成、本地验证通过
- **THEN** 系统 SHALL 在 REPORT 步骤之后执行 post-mortem 检查点
- **AND** post-mortem SHALL 回答以下问题：此缺陷的根本原因为何未被早期阶段捕获？是否存在架构改进可以防止同类缺陷？

#### Scenario: 架构改进建议传递

- **WHEN** post-mortem 发现架构层面的改进机会（如"缺少正确的测试 seam"、"模块耦合导致变更波及"）
- **THEN** 系统 SHALL 将改进建议写入 fix-report 的"关联建议"字段
- **AND** kflow-audit 在归档评估时 SHALL 读取所有子变更 fix-report 的关联建议并汇总

#### Scenario: 无架构改进

- **WHEN** post-mortem 未发现架构层面的改进机会
- **THEN** 系统 SHALL 简要记录"无架构改进建议"
- **AND** post-mortem 检查点仍然完成

### Requirement: 调试日志清理

系统 SHALL 在缺陷修复完成后清理所有调试 instrumentation。

#### Scenario: 日志清理检查

- **WHEN** post-mortem 检查点完成
- **THEN** 系统 SHALL 确认所有调试日志已清理
- **AND** 所有 throwaway prototype 已删除或移动到标记位置
- **AND** 修复中使用的临时文件已清理

### Requirement: 修复假设记录

缺陷修复报告中 SHALL 记录最终被验证正确的假设，供未来调试参考。

#### Scenario: 假设记录

- **WHEN** 修复已完成
- **THEN** fix-report SHALL 包含"最终正确的假设"字段
- **AND** 说明为什么该假设是正确的
- **AND** 说明如果有备选假设，为什么它们被排除
