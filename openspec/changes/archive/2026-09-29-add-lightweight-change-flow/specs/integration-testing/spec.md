# Spec Delta

## MODIFIED Requirements

### Requirement: 变更级集成测试阶段

系统 SHALL 在所有子变更编码和测试完成后、归档前，执行变更级集成测试。集成测试通过 `kflow-integration-test` Skill 执行。变更档位为 `轻量` 时，集成测试 SHALL 按阶段适用性声明条件执行。

#### Scenario: 集成测试触发条件

- **WHEN** 所有子变更的接口单元测试和E2E测试（前后端项目）均通过或已标记为 `⏭️ 不适用`
- **AND** 变更级服务刷新已完成并通过
- **THEN** 系统进入集成测试阶段
- **AND** 执行入口为 `kflow-integration-test` Skill

#### Scenario: 轻量档集成测试被裁剪

- **WHEN** 变更档位为 `轻量`
- **AND** `detailed-design.md` 的接口设计章节无本变更新增或修改的接口条目
- **AND** 跨子变更接口契约章节无本变更条目
- **THEN** 集成测试阶段 SHALL 标记为 `⏭️ 不适用`
- **AND** 系统 SHALL NOT 启动 `kflow-integration-test` Skill
- **AND** 系统 SHALL 直接进入审计阶段

#### Scenario: 轻量档集成测试适用

- **WHEN** 变更档位为 `轻量`
- **AND** `detailed-design.md` 的接口设计章节含本变更新增或修改的接口条目，或跨子变更接口契约章节含本变更条目
- **THEN** 集成测试阶段 SHALL 按轻量档轮次（1 轮）执行

#### Scenario: 前后端项目集成测试

- **WHEN** 项目类型为前后端项目 且 集成测试阶段适用
- **THEN** 集成测试包含跨子变更 API 调用链验证和数据一致性验证
- **AND** 可通过浏览器或接口调用方式执行

#### Scenario: 纯后端项目集成测试

- **WHEN** 项目类型为纯后端项目 且 集成测试阶段适用
- **THEN** 集成测试聚焦 API 间调用链和数据一致性验证
- **AND** 使用接口调用执行，不涉及浏览器

### Requirement: 集成测试门控

系统 SHALL 将集成测试通过作为归档的必要条件。集成测试阶段被合法裁剪时，SHALL 视为门控满足。

#### Scenario: 集成测试通过

- **WHEN** 集成测试全部用例通过
- **THEN** 系统输出 `test-reports/integration/summary.md` 标记"集成测试通过"
- **AND** 变更可以进入审计和归档阶段

#### Scenario: 集成测试阶段被裁剪时门控满足

- **WHEN** 集成测试阶段标记为 `⏭️ 不适用` 且存在对应的阶段适用性声明依据
- **THEN** 归档门控 SHALL 视为满足
- **AND** SHALL NOT 要求 `test-reports/integration/summary.md` 存在
- **AND** SHALL NOT 因缺失该产物而阻塞归档

#### Scenario: 无声明依据的裁剪阻塞

- **WHEN** 集成测试阶段标记为 `⏭️ 不适用` 但变更级 `.status.md` 中无对应的阶段适用性声明依据
- **THEN** 归档门控 SHALL 阻塞并提示缺失裁剪依据

#### Scenario: 集成测试失败进入修复循环

- **WHEN** 集成测试有用例失败
- **THEN** 系统在 `kflow-integration-test` 内部执行四分法根因分类
- **AND** 接口实现错误或测试用例错误进入变更级修复循环
- **AND** 修复后自动触发新一轮集成测试
- **AND** 接口契约错误更新契约后联动修订受影响子变更
- **AND** 架构设计错误触发设计阶段回退
- **AND** 连续 3 轮同一用例失败自动触发架构评估
