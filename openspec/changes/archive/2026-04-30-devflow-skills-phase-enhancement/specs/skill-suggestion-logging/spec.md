## ADDED Requirements

### Requirement: 错误场景记录

系统 SHALL 将流程指引的错误场景记录到 docs/skill-suggestion.md。

#### Scenario: 用户纠正指引方向
- **WHEN** 用户指出指引方向错误
- **THEN** 系统记录触发场景、用户反馈、改进建议

#### Scenario: 用户报告指引错误
- **WHEN** 用户报告指引结果与预期不符
- **THEN** 系统记录错误现象、预期行为、改进建议

#### Scenario: Skill 执行异常
- **WHEN** Skill 执行结果与预期不符
- **THEN** 系统记录异常现象、预期行为、影响范围

### Requirement: 记录格式规范

系统 SHALL 使用统一的格式记录优化建议。

#### Scenario: 记录内容格式
- **WHEN** 记录优化建议
- **THEN** 记录包含：发现时间、发现阶段、触发场景、用户反馈、改进建议、状态、优先级

### Requirement: 记录文件位置

系统 SHALL 将优化建议记录保存到 docs/skill-suggestion.md。

#### Scenario: 创建记录文件
- **WHEN** docs/skill-suggestion.md 不存在
- **THEN** 系统创建文件并添加记录

#### Scenario: 追加记录
- **WHEN** docs/skill-suggestion.md 已存在
- **THEN** 系统追加新记录到清单

### Requirement: 记录不主动优化

系统 SHALL 仅记录优化建议，不主动执行 Skill 优化。

#### Scenario: 记录后状态
- **WHEN** 记录完成
- **THEN** 记录状态标记为"待优化"
- **AND** 不触发自动优化流程

### Requirement: 统计汇总

系统 SHALL 在 skill-suggestion.md 中维护记录统计。

#### Scenario: 统计更新
- **WHEN** 新记录添加或状态变更
- **THEN** 统计区域更新待优化、优化中、已优化数量