# subchange-type-validation Specification

## Purpose

定义 design 阶段子变更划分的类型一致性自动校验——同一子变更内所有 FP 的类型必须相同，混合则阻塞流程。

## ADDED Requirements

### Requirement: 子变更类型一致性校验

design 阶段 DIVIDE 步骤完成后，系统 SHALL 对每个子变更执行类型一致性校验——提取该子变更包含的所有 FP，读取 functional-designs/index.md 中每个 FP 的类型，验证类型是否全部一致。

#### Scenario: 类型一致通过

- **WHEN** 子变更包含的所有 FP 类型均为「后端」
- **THEN** 系统 SHALL 自动标记该子变更类型为「后端子变更」
- **AND** 校验通过，允许进入下一阶段

#### Scenario: 类型一致通过（前端）

- **WHEN** 子变更包含的所有 FP 类型均为「前端」
- **THEN** 系统 SHALL 自动标记该子变更类型为「前端子变更」
- **AND** 校验通过，允许进入下一阶段

#### Scenario: 类型不一致阻塞

- **WHEN** 子变更同时包含类型为「后端」和「前端」的 FP
- **THEN** 系统 SHALL 标记该子变更为「混合子变更」
- **AND** SHALL 阻塞后续流程（不输出到子变更划分结果表）
- **AND** SHALL 提示用户：「子变更 {name} 包含后端 FP（{fp-list}）和前端 FP（{fp-list}），请拆分为独立子变更」

#### Scenario: 子变更类型列自动推断

- **WHEN** 类型一致性校验通过
- **THEN** 子变更划分结果表的「类型」列 SHALL 由系统自动填写（= 包含 FP 的统一类型）
- **AND** SHALL NOT 由人工手动填写

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
