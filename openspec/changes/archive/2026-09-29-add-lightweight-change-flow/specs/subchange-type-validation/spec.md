# Spec Delta

## MODIFIED Requirements

### Requirement: 子变更类型一致性校验

design 阶段 DIVIDE 步骤完成后，系统 SHALL 对每个子变更执行类型一致性校验——提取该子变更包含的所有 FP，读取 functional-designs/index.md 中每个 FP 的类型，验证类型是否全部一致。变更档位为 `轻量` 时，类型混合 SHALL 触发升档而非阻塞。

#### Scenario: 类型一致通过

- **WHEN** 子变更包含的所有 FP 类型均为「后端」
- **THEN** 系统 SHALL 自动标记该子变更类型为「后端子变更」
- **AND** 校验通过，允许进入下一阶段

#### Scenario: 类型一致通过（前端）

- **WHEN** 子变更包含的所有 FP 类型均为「前端」
- **THEN** 系统 SHALL 自动标记该子变更类型为「前端子变更」
- **AND** 校验通过，允许进入下一阶段

#### Scenario: 类型不一致阻塞

- **WHEN** 变更档位为 `标准` 或 `完整`
- **AND** 子变更同时包含类型为「后端」和「前端」的 FP
- **THEN** 系统 SHALL 标记该子变更为「混合子变更」
- **AND** SHALL 阻塞后续流程（不输出到子变更划分结果表）
- **AND** SHALL 提示用户：「子变更 {name} 包含后端 FP（{fp-list}）和前端 FP（{fp-list}），请拆分为独立子变更」

#### Scenario: 轻量档类型混合触发升档

- **WHEN** 变更档位为 `轻量`
- **AND** 所含 FP 同时包含类型为「后端」和「前端」的 FP
- **THEN** 系统 SHALL 将变更档位升为 `标准`
- **AND** SHALL 按标准档流程重新划分子变更，产出后端子变更与前端子变更
- **AND** SHALL NOT 以类型混合为由阻塞变更

#### Scenario: 轻量档升档后由用户确认

- **WHEN** 轻量档因 FP 类型混合需要升档为 `标准`
- **THEN** 系统 SHALL 通过 AskUserQuestion 告知用户升档原因并请求确认
- **AND** 用户确认后 SHALL 按标准档流程继续
- **AND** SHALL NOT 回退 kflow-explore 阶段

#### Scenario: 子变更类型列自动推断

- **WHEN** 类型一致性校验通过
- **THEN** 子变更划分结果表的「类型」列 SHALL 由系统自动填写（= 包含 FP 的统一类型）
- **AND** SHALL NOT 由人工手动填写
