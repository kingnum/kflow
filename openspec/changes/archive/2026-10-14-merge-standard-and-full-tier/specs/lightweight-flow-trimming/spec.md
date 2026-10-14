# Spec Delta

## MODIFIED Requirements

### Requirement: 轻量档阶段适用性声明

变更档位为 `轻量` 时，kflow-design SHALL 在 DIVIDE 步骤之后逐阶段判定接口单元测试、E2E测试、集成测试三个阶段的适用性，并将声明写入变更级 `.status.md` 的阶段状态表。声明 SHALL 为显式记录，使「因不适用而跳过」与「遗漏产物」可区分。

#### Scenario: 生成适用性声明

- **WHEN** 变更档位为 `轻量` 且 kflow-design 完成 DIVIDE 步骤
- **THEN** 系统 SHALL 判定接口单元测试、E2E测试、集成测试三个阶段的适用性
- **AND** SHALL 将每个阶段的判定结果写入变更级 `.status.md` 阶段状态表

#### Scenario: 非轻量档不生成适用性声明

- **WHEN** 变更档位为 `标准`
- **THEN** 系统 SHALL NOT 生成阶段适用性声明
- **AND** 接口单元测试、E2E测试、集成测试三个阶段 SHALL 按该档位的既有规则执行

### Requirement: 裁剪仅适用于轻量档

阶段裁剪 SHALL 仅适用于变更档位为 `轻量` 的变更。`标准` 档变更的阶段集合 SHALL 维持既有规则不变，纯后端项目跳过 E2E测试的既有规则 SHALL 不受本能力影响。

#### Scenario: 标准档与完整档不受裁剪影响

- **WHEN** 变更档位为 `标准`，或读取到的历史取值为 `完整`（按 `标准` 处理）
- **THEN** 接口单元测试、E2E测试、集成测试 SHALL 按该档位的既有规则执行
- **AND** 不因本能力新增的适用性判定而跳过

#### Scenario: 纯后端项目的既有跳过规则保持

- **WHEN** 项目类型为纯后端项目
- **THEN** E2E测试 SHALL 按既有规则标记为 `⏭️` 跳过
- **AND** 该跳过与变更档位无关
