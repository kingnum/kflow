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
- **THEN** 集成测试阶段 SHALL 按单轮全面执行 + 定向重验模型执行
- **AND** 执行轮数 SHALL NOT 由变更档位决定

#### Scenario: 前后端项目集成测试

- **WHEN** 项目类型为前后端项目 且 集成测试阶段适用
- **THEN** 集成测试包含跨子变更 API 调用链验证和数据一致性验证
- **AND** 可通过浏览器或接口调用方式执行

#### Scenario: 纯后端项目集成测试

- **WHEN** 项目类型为纯后端项目 且 集成测试阶段适用
- **THEN** 集成测试聚焦 API 间调用链和数据一致性验证
- **AND** 使用接口调用执行，不涉及浏览器
