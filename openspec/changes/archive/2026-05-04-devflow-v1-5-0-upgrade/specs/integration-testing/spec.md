## ADDED Requirements

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
- **THEN** 变更级修复报告输出到 test-reports/integration/fix-reports/ 目录
- **AND** 每轮修复对应一个 fix-{timestamp}.md 文件

## MODIFIED Requirements

### Requirement: 集成测试门控

系统 SHALL 将集成测试通过作为归档的必要条件，支持多轮修复后通过。

#### Scenario: 集成测试通过
- **WHEN** 集成测试全部用例通过（无论是第几轮）
- **THEN** 系统输出 summary.md 标记"测试通过"
- **AND** 变更可以进入审计和归档阶段

#### Scenario: 集成测试失败进入修复循环
- **WHEN** 集成测试有用例失败
- **THEN** 系统执行变更级根因分类（接口实现/接口契约/测试用例/架构设计）
- **AND** 接口实现错误或测试用例错误进入变更级修复循环
- **AND** 修复后自动触发新一轮集成测试
- **AND** 接口契约错误更新契约后联动修订受影响子变更
- **AND** 架构设计错误触发设计阶段回退
