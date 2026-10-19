# subchange-type-validation Specification

## Purpose

定义 design 阶段子变更划分的类型一致性自动校验——同一子变更内所有 FP 的类型必须相同，混合则阻塞流程。

## Requirements

### Requirement: 子变更类型一致性校验与轻量拆分

design 阶段 DIVIDE 步骤完成后，系统 SHALL 对每个子变更执行类型一致性校验——提取该子变更包含的所有 FP，读取 functional-designs/index.md 中每个 FP 的类型，验证类型是否全部一致。变更档位为 `轻量` 时，类型混合 SHALL 拆分为后端子变更与前端子变更，SHALL NOT 触发升档；变更档位为 `标准` 时，同一子变更内类型混合 SHALL 阻塞。

#### Scenario: 类型一致通过

- **WHEN** 子变更包含的所有 FP 类型均为「后端」
- **THEN** 系统 SHALL 自动标记该子变更类型为「后端子变更」
- **AND** 校验通过，允许进入下一阶段

#### Scenario: 类型一致通过（前端）

- **WHEN** 子变更包含的所有 FP 类型均为「前端」
- **THEN** 系统 SHALL 自动标记该子变更类型为「前端子变更」
- **AND** 校验通过，允许进入下一阶段

#### Scenario: 类型不一致阻塞

- **WHEN** 变更档位为 `标准`
- **AND** 子变更同时包含类型为「后端」和「前端」的 FP
- **THEN** 系统 SHALL 标记该子变更为「混合子变更」
- **AND** SHALL 阻塞后续流程（不输出到子变更划分结果表）
- **AND** SHALL 提示用户：「子变更 {name} 包含后端 FP（{fp-list}）和前端 FP（{fp-list}），请拆分为独立子变更」

#### Scenario: 轻量档类型混合拆分而不升档

- **WHEN** 变更档位为 `轻量`
- **AND** 所含 FP 同时包含类型为「后端」和「前端」的 FP
- **THEN** 系统 SHALL 拆分为 1 个后端子变更与 1 个前端子变更
- **AND** SHALL NOT 将变更档位升为 `标准`
- **AND** SHALL NOT 以类型混合为由阻塞变更

#### Scenario: 轻量档边界升档后由用户确认

- **WHEN** 变更档位为 `轻量`
- **AND** 拆分为 2 个子变更后任一子变更的功能点数超过 10
- **THEN** 系统 SHALL 将变更档位升为 `标准`
- **AND** SHALL 按标准档流程重新划分子变更
- **AND** 升档 SHALL NOT 回退 kflow-explore 阶段

#### Scenario: 子变更类型列自动推断

- **WHEN** 类型一致性校验通过
- **THEN** 子变更划分结果表的「类型」列 SHALL 由系统自动填写（= 包含 FP 的统一类型）
- **AND** SHALL NOT 由人工手动填写

#### Scenario: 轻量档最小划分表

- **WHEN** 轻量档因类型混合拆分为 2 个子变更
- **THEN** 系统 SHALL 使用最小划分表（子变更名称、类型、包含功能点、实现顺序、依赖说明）
- **AND** 前端子变更 SHALL 标注「依赖后端 API 契约」
- **AND** SHALL NOT 执行标准档的完整依赖关系分析

### Requirement: 子变更划分结果增加 FP 类型统计

子变更划分结果表 SHALL 在「功能点数」列中区分后端 FP 和前端 FP 的数量标识。

#### Scenario: 类型统计展示

- **WHEN** 子变更划分结果输出
- **THEN** 「功能点数」列格式为：`{总n}（{后端数量}后端 + {前端数量}前端）`
- **AND** 纯后端或纯前端子变更的统计中非本类型数量为 0

### Requirement: 旧版功能设计文档兼容

当 functional-designs/index.md 缺少 FP 类型列时（旧版文档），系统 SHALL 标记为警告而非阻塞。

#### Scenario: 缺少类型列警告

- **WHEN** DIVIDE 步骤检测到 functional-designs/index.md 的功能点清单缺少「类型」列
- **THEN** 系统 SHALL 标记 🟡 警告：「功能设计文档缺少 FP 类型列，无法执行自动类型校验」
- **AND** SHALL NOT 阻塞子变更划分
- **AND** SHALL 提示用户：「建议重新执行 kflow-explore REVISION 补充 FP 类型标记」
