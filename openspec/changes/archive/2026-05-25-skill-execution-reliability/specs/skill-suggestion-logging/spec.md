## MODIFIED Requirements

### Requirement: 错误场景记录

系统 SHALL 将流程指引的错误场景以及 AI 对话中特定触发模式记录到 docs/skill-suggestion.md。

#### Scenario: 用户纠正指引方向

- **WHEN** 用户指出指引方向错误
- **THEN** 系统记录触发场景、用户反馈、改进建议

#### Scenario: 用户报告指引错误

- **WHEN** 用户报告指引结果与预期不符
- **THEN** 系统记录错误现象、预期行为、改进建议

#### Scenario: Skill 执行异常

- **WHEN** Skill 执行结果与预期不符
- **THEN** 系统记录异常现象、预期行为、影响范围

#### Scenario: AI 阻塞模式自动捕获

- **WHEN** AI 回复中出现「因...无法...」模式（如"因服务未启动无法执行测试"）
- **THEN** 系统 SHALL 记录阻塞原因和失败的执行路径到 skill-suggestion.md
- **AND** 记录内容包含：触发场景（AI 回复上下文）、阻塞原因、改进建议

#### Scenario: AI 因果链模式自动捕获

- **WHEN** AI 回复中出现「因...导致...」模式（如"因设计错误导致测试全部失败"）
- **THEN** 系统 SHALL 记录因果链和受影响的阶段到 skill-suggestion.md
- **AND** 记录内容包含：因果链描述、受影响阶段、改进建议

#### Scenario: 用户纠正后 AI 附和自动捕获

- **WHEN** 用户纠正 AI 的行为或判断后，AI 回复中包含「你说得对」、「你是对的」、「确实如此」等附和内容
- **THEN** 系统 SHALL 记录用户的纠正内容（不是 AI 的附和）到 skill-suggestion.md
- **AND** 记录内容包含：用户纠正的具体内容、AI 之前的错误行为、改进建议
- **AND** 如果纠正内容涉及业务功能问题（如"这个功能应该是先验证邮箱再登录"）， SHALL 同时记录为缺陷参考信息
