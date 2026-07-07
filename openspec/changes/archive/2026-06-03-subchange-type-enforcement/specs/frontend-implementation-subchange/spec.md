# frontend-implementation-subchange Delta Spec

## ADDED Requirements

### Requirement: 前端子变更编码前 FP 类型校验

前端子变更进入编码阶段前，SHALL 校验子变更内所有 FP 的类型均为「前端」。

#### Scenario: 前端子变更 FP 类型前置校验

- **WHEN** 前端子变更进入 plan 阶段生成 tasks.md
- **THEN** 系统 SHALL 读取 functional-designs/index.md 中该子变更包含的所有 FP 类型
- **AND** 若所有 FP 类型均为「前端」 → 校验通过，正常生成原型转译任务模板
- **AND** 若存在类型为「后端」的 FP → 🟡 警告：「前端子变更 {name} 包含后端 FP: {fp-list}，请回退到 design 阶段重新划分」
- **AND** 警告 SHALL NOT 阻塞 tasks.md 生成（向后兼容），但 SHALL 在 tasks.md 中记录

#### Scenario: 编码阶段再次校验

- **WHEN** 前端子变更进入 code 阶段执行前端实现子流程
- **THEN** 系统 SHALL 再次校验子变更 FP 类型
- **AND** 若存在后端 FP → SHALL 跳过该后端 FP 的任务项（仅实现前端 FP）
- **AND** SHALL 在编码报告中记录被跳过的后端 FP

### Requirement: 后端子变更编码前 FP 类型校验

后端子变更进入编码阶段前，SHALL 校验子变更内所有 FP 的类型均为「后端」。

#### Scenario: 后端子变更 FP 类型前置校验

- **WHEN** 后端子变更进入 plan 阶段生成 tasks.md
- **THEN** 系统 SHALL 读取 functional-designs/index.md 中该子变更包含的所有 FP 类型
- **AND** 若所有 FP 类型均为「后端」 → 校验通过，正常生成 TDD 任务模板
- **AND** 若存在类型为「前端」的 FP → 🟡 警告：「后端子变更 {name} 包含前端 FP: {fp-list}，请回退到 design 阶段重新划分」
- **AND** 警告 SHALL NOT 阻塞 tasks.md 生成（向后兼容），但 SHALL 在 tasks.md 中记录
