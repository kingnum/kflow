# prototype-to-code-consistency Delta Spec

## ADDED Requirements

### Requirement: 后端子变更代码审查越界检测

kflow-code-review 在对后端子变更执行审查时，SHALL 增加跨层越界检测——检测源码中是否存在前端代码特征。

#### Scenario: 后端SC 前端文件检测

- **WHEN** code-review 对后端子变更执行审查
- **THEN** 系统 SHALL 检查子变更源码目录中是否存在 `.tsx`/`.jsx`/`.vue`/`.svelte` 文件
- **AND** 检查是否存在 `.css`/`.scss`/`.less` 样式文件（排除全局样式文件如 `globals.css`）
- **AND** 发现前端文件时 SHALL 在审查报告「跨层一致性」章节标记 ⚠️
- **AND** 标记为审查建议，不阻塞审查通过

#### Scenario: 后端SC 硬编码样式检测

- **WHEN** code-review 对后端子变更执行审查
- **AND** 后端子变更源码为 TypeScript/JavaScript 文件
- **THEN** 系统 SHALL grep 检测硬编码颜色值（`#[0-9a-fA-F]{3,6}` 或 `rgb(`）
- **AND** 发现 ≥ 3 次硬编码颜色值时 SHALL 标记：「后端SC 含疑似内联样式代码，请确认'
- **AND** 标记为审查建议

### Requirement: 前端子变更代码审查越界检测

kflow-code-review 在对前端子变更执行审查时，SHALL 增加跨层越界检测——检测源码中是否存在后端代码特征。

#### Scenario: 前端SC 后端逻辑检测

- **WHEN** code-review 对前端子变更执行审查
- **THEN** 系统 SHALL 检查子变更源码目录中是否存在数据库迁移脚本
- **AND** 检查是否存在 ORM 模型定义
- **AND** 检查是否存在服务端路由注册语句
- **AND** 发现后端代码时 SHALL 在审查报告「跨层一致性」章节标记 ⚠️
- **AND** 标记为审查建议，不阻塞审查通过

#### Scenario: 越界检测执行顺序

- **WHEN** code-review 阶段启动
- **THEN** 跨层越界检测 SHALL 在原型对账（步骤 3.5）之前执行
- **AND** 审查报告 SHALL 包含「跨层一致性」章节，位于原型对账章节之前
- **AND** 原型对账 SHALL 仅在前端子变更时执行（不受越界检测结果影响）
