## Purpose

定义变更级集成测试阶段的执行规范和修复循环机制，通过 kflow-integration-test Skill 统一执行。
## Requirements
### Requirement: 变更级集成测试阶段

系统 SHALL 在所有子变更编码和测试完成后、归档前，执行变更级集成测试。集成测试通过 `kflow-integration-test` Skill 执行。

#### Scenario: 集成测试触发条件
- **WHEN** 所有子变更的接口单元测试和E2E测试（前后端项目）均通过
- **AND** 变更级服务刷新已完成并通过
- **THEN** 系统进入集成测试阶段
- **AND** 执行入口为 `kflow-integration-test` Skill

#### Scenario: 前后端项目集成测试
- **WHEN** 项目类型为前后端项目
- **THEN** 集成测试包含跨子变更 API 调用链验证和数据一致性验证
- **AND** 可通过浏览器或接口调用方式执行

#### Scenario: 纯后端项目集成测试
- **WHEN** 项目类型为纯后端项目
- **THEN** 集成测试聚焦 API 间调用链和数据一致性验证
- **AND** 使用接口调用执行，不涉及浏览器

### Requirement: 集成测试用例生成

系统 SHALL 基于各子变更 detailed-design.md 中定义的接口契约自动生成集成测试用例。

#### Scenario: 集成测试用例来源
- **WHEN** 进入集成测试阶段
- **THEN** 系统读取变更级 detailed-design.md 中各子变更的"与其他子变更的接口"章节
- **AND** 自动生成集成测试用例文档 integration-tests.md
- **AND** 每个跨子变更接口契约至少一个测试用例

#### Scenario: 集成测试用例格式
- **WHEN** 集成测试用例生成
- **THEN** 每个用例包含依赖链、测试步骤、预期结果、验证的契约内容

### Requirement: 集成测试门控

系统 SHALL 将集成测试通过作为归档的必要条件。

#### Scenario: 集成测试通过
- **WHEN** 集成测试全部用例通过
- **THEN** 系统输出 `test-reports/integration/summary.md` 标记"集成测试通过"
- **AND** 变更可以进入审计和归档阶段

#### Scenario: 集成测试失败进入修复循环
- **WHEN** 集成测试有用例失败
- **THEN** 系统在 `kflow-integration-test` 内部执行四分法根因分类
- **AND** 接口实现错误或测试用例错误进入变更级修复循环
- **AND** 修复后自动触发新一轮集成测试
- **AND** 接口契约错误更新契约后联动修订受影响子变更
- **AND** 架构设计错误触发设计阶段回退
- **AND** 连续 3 轮同一用例失败自动触发架构评估

### Requirement: 集成测试多轮缺陷修复循环

系统 SHALL 在集成测试失败时支持多轮缺陷修复再测试循环。

#### Scenario: 修复后重新集成测试
- **WHEN** 变更级缺陷修复完成
- **THEN** 系统自动触发新一轮集成测试
- **AND** 输出新的测试轮次报告 round-{n}.md

#### Scenario: 多轮循环收敛
- **WHEN** 集成测试经过 N 轮修复后全部用例通过
- **THEN** 系统输出 summary.md 标记"集成测试通过"
- **AND** 记录总轮次数和各轮修复历史

#### Scenario: 修复报告记录
- **WHEN** 集成测试某轮次失败
- **THEN** 修复报告输出到 test-reports/integration/fix-reports/ 目录

### Requirement: 集成测试缺陷修复内聚

系统 SHALL 在 `kflow-integration-test` Skill 内聚处理集成测试失败，不跳转到外部缺陷修复 Skill。

#### Scenario: 修复报告输出路径
- **WHEN** 集成测试修复执行
- **THEN** 修复报告输出到 `test-reports/integration/fix-reports/`
- **AND** 修复完成后自动返回集成测试

#### Scenario: 修复循环收敛
- **WHEN** 集成测试经过 N 轮修复后全部用例通过
- **THEN** 系统输出 `summary.md` 标记"集成测试通过"
- **AND** 记录总轮次数和各轮修复历史

