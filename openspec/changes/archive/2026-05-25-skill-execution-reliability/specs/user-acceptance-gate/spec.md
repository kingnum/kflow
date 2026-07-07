## ADDED Requirements

### Requirement: 集成测试通过后用户验收确认

系统 SHALL 在集成测试全部通过且审计通过后、归档之前，启动服务并要求用户访问确认功能符合预期。

#### Scenario: 用户确认通过

- **WHEN** 集成测试状态为「✅ 完成」且审计状态为「✅ 完成」
- **AND** 系统按 `docs/service-guide.md` 启动服务并通过健康检查
- **AND** 系统通过 AskUserQuestion 展示服务地址和测试摘要，提供「确认通过，可以归档」和「还有问题，需要修复」两个选项
- **AND** 用户选择「确认通过，可以归档」
- **THEN** 系统标记用户验收为「✅ 已确认」
- **AND** 系统进入归档阶段（kflow-archive）

#### Scenario: 用户确认不通过

- **WHEN** 用户选择「还有问题，需要修复」
- **THEN** 系统 SHALL 通过 AskUserQuestion 或开放式输入收集用户描述的具体问题
- **AND** 系统创建缺陷记录并路由到 kflow-bug-fix 进行修复
- **AND** 系统 SHALL NOT 将此问题记录到 skill-suggestion.md（这是功能缺陷，非 Skill 执行问题）
- **AND** bug-fix 完成后重新执行测试 → 审计 → 用户验收确认循环

#### Scenario: 用户跳过确认

- **WHEN** AskUserQuestion 提供「跳过确认，直接归档」选项（第三个选项）
- **AND** 用户选择该选项
- **THEN** 系统 SHALL 直接进入归档阶段
- **AND** 系统在 .status.md 用户验收记录中标记「⏭️ 用户跳过」

### Requirement: 用户验收确认门控

系统 SHALL 在归档阶段的门控检查中验证用户验收确认状态。

#### Scenario: 归档门控检查用户验收

- **WHEN** 系统检查进入归档阶段的门控条件
- **THEN** 系统 SHALL 检查 .status.md 中「用户验收确认」状态
- **AND** 状态为「✅ 已确认」或「⏭️ 用户跳过」→ 门控放行
- **AND** 状态为「⏳ 待确认」或未设置 → 门控失败，提示先完成用户验收确认

### Requirement: 用户验收服务启动

系统 SHALL 在发起用户验收确认前自动启动服务，而非假设服务已运行。

#### Scenario: 服务启动流程

- **WHEN** 系统准备发起用户验收确认
- **THEN** 系统 SHALL 按 `docs/service-guide.md` 中的启动命令启动服务
- **AND** 系统 SHALL 等待服务端口可访问（健康检查通过）
- **AND** 系统 SHALL 输出服务访问地址（如 `http://localhost:{port}`）
- **AND** 服务启动失败 → 标记「❌ 阻塞」并提示用户手动启动
