# Spec Delta

## MODIFIED Requirements

### Requirement: 档位决定每轮审查强度而非轮数

变更档位 SHALL 决定审查的**审查形态**（`轻量` 单 Agent 串行覆盖全部视角 / `标准` 两视角并行）与产出深度，以及验证报告的输出深度。档位 SHALL NOT 决定审查轮数——全部档位的审查轮数恒为单轮。系统 SHALL NOT 存在四视角并行等第三形态。

#### Scenario: 档位不决定轮数

- **WHEN** 任一阶段的单轮验证启动
- **THEN** 系统 SHALL NOT 因变更档位而调整审查轮数
- **AND** 审查轮数 SHALL 恒为 1

#### Scenario: 档位决定每轮审查强度

- **WHEN** 变更档位为 `轻量`
- **THEN** 审查 SHALL 由单个 Agent 串行覆盖全部视角的检查项
- **AND** 检查项 SHALL NOT 因单 Agent 而缩减

#### Scenario: 标准档两视角审查

- **WHEN** 变更档位为 `标准`
- **THEN** 审查 SHALL 由两个 Agent 并行执行（业务+技术视角 / 安全+质量视角）
- **AND** 检查项 SHALL NOT 因合并为两个 Agent 而缩减

#### Scenario: 档位缺失时的处理

- **WHEN** 变更级 `.status.md` 不含 `变更档位` 字段，或读取到的历史取值为 `完整`
- **THEN** 系统 SHALL 按 `标准` 档确定审查形态与产出深度
