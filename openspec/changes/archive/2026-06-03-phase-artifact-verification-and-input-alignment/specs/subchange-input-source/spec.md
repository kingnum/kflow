# subchange-input-source Specification

## Purpose
定义子变更输入源规范——后端子变更与前端子变更的输入源定义、前端子变更原型核心产物限定、各阶段 Skill 输入表「适用SC类型」列。

## ADDED Requirements

### Requirement: 子变更类型严格二分
系统 SHALL 将子变更类型限定为「后端子变更」或「前端子变更」，禁止创建前后端混合子变更。

#### Scenario: 后端子变更判定
- **WHEN** 子变更包含的全部功能点均为后端 FP（API 实现/服务逻辑/数据模型/数据库操作/业务规则）
- **THEN** 系统 SHALL 标记该子变更为「后端子变更」
- **AND** SHALL NOT 包含前端 FP

#### Scenario: 前端子变更判定
- **WHEN** 子变更包含的全部功能点均为前端 FP（页面/组件/路由/状态管理/样式/CSS 变量注入）
- **THEN** 系统 SHALL 标记该子变更为「前端子变更」
- **AND** SHALL NOT 包含后端 FP

#### Scenario: 混合子变更拒绝
- **WHEN** 子变更同时包含后端 FP 和前端 FP
- **THEN** 系统 SHALL 拒绝此划分
- **AND** 提示将前后端 FP 拆分到两个独立子变更

### Requirement: 后端子变更输入源
系统 SHALL 为后端子变更定义以下必选输入源。

#### Scenario: 后端子变更 plan 阶段输入
- **WHEN** kflow-plan 为后端子变更生成 tasks.md
- **THEN** 输入源 SHALL 包含：functional-designs/（业务规则与功能点）、detailed-design.md（数据模型章节 + 接口设计章节 + NFR 章节）、api-tests/（接口测试用例）、CONTEXT.md（命名对齐）、traceability.md（覆盖追踪）
- **AND** SHALL NOT 包含 prototype/ 系列文件

#### Scenario: 后端子变更 code 阶段输入
- **WHEN** kflow-code 为后端子变更执行编码
- **THEN** 输入源 SHALL 包含：functional-designs/（业务规则验证）、detailed-design.md（实现规格）、api-tests/（TDD 测试来源）、CONTEXT.md（代码命名）、tasks.md（任务清单）、service-guide.md（编译/运行配置）
- **AND** SHALL NOT 包含 prototype/ 系列文件

### Requirement: 前端子变更输入源
系统 SHALL 为前端子变更定义以下输入源，限定核心原型产物，排除过程产物。

#### Scenario: 前端子变更 plan 阶段输入
- **WHEN** kflow-plan 为前端子变更生成 tasks.md
- **THEN** 输入源 SHALL 包含 prototype/index.html（页面结构）、prototype/design-tokens.css（设计令牌）、prototype/element-coverage-tree.md（元素清单和状态）、detailed-design.md（仅 API 契约章节）、functional-designs/（业务规则和表单项定义）、traceability.md
- **AND** SHALL NOT 将 prototype/design-prompt.md 作为输入源
- **AND** SHALL NOT 将 design-system/MASTER.md 作为输入源

#### Scenario: 前端子变更 code 阶段输入
- **WHEN** kflow-code 为前端子变更执行编码
- **THEN** 输入源 SHALL 包含 prototype/index.html（转译目标）、prototype/design-tokens.css（CSS 变量注入）、prototype/element-coverage-tree.md（元素和状态覆盖清单）、detailed-design.md（API 契约与 mock 数据依据）、tasks.md（原型转译模板）、CONTEXT.md（组件命名）
- **AND** SHALL NOT 将 prototype/design-prompt.md 或 design-system/MASTER.md 作为执行输入
- **AND** 设计令牌注入 SHALL 以 design-tokens.css 中的 CSS 变量值为准

#### Scenario: 前端子变更过程产物排除
- **WHEN** 前端子变更编码阶段引用原型产物
- **THEN** 系统 SHALL 仅使用核心产物：index.html、design-tokens.css、element-coverage-tree.md
- **AND** SHALL NOT 读取 prototype/design-prompt.md（AIGC 提示词文件）
- **AND** SHALL NOT 读取 design-system/ 目录下文件（含 MASTER.md，设计系统说明文档）
- **AND** design-tokens.css 是设计令牌的唯一真实来源

### Requirement: 各阶段 Skill 输入表增加适用 SC 类型列
系统 SHALL 在所有阶段 Skill 设计文档的「输入要求」表中增加「适用SC类型」列。

#### Scenario: 输入表格式
- **WHEN** 阶段 Skill 设计文档定义输入要求
- **THEN** 输入表 SHALL 包含列：产物、文件、图例、适用SC类型、说明
- **AND** 「适用SC类型」列取值为：全部 / 后端子变更 / 前端子变更

#### Scenario: 条件产物标注
- **WHEN** 某产物仅适用于特定子变更类型
- **THEN** 「适用SC类型」列 SHALL 明确标注子变更类型
- **AND** 图例 SHALL 使用 🔶 条件
