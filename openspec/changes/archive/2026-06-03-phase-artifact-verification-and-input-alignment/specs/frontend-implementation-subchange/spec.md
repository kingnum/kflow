# frontend-implementation-subchange Delta Spec

## MODIFIED Requirements

### Requirement: 前端实现集中为独立子变更

系统 SHALL 将每个 Change 的所有前端实现集中在一个独立的前端子变更中完成，不拆分到多个后端子变更。前后端混合子变更 SHALL NOT 被创建。

#### Scenario: 前后端项目划分子变更时创建前端子变更

- **WHEN** kflow-design 阶段为前后端项目划分子变更
- **THEN** 系统 SHALL 将所有前端功能点（页面/组件/路由/状态管理/样式）归属到一个独立的前端子变更
- **AND** 后端子变更 SHALL NOT 包含前端实现任务
- **AND** 前端子变更 SHALL NOT 包含后端实现任务
- **AND** SHALL NOT 创建前后端混合子变更

#### Scenario: 纯后端项目不创建前端子变更

- **WHEN** 项目类型为纯后端
- **THEN** 系统 SHALL NOT 创建前端子变更
- **AND** 前端相关内容标记为 ⏭️ 不适用

### Requirement: 前端功能点任务模板

系统 SHALL 在 plan 阶段为前端子变更生成「原型转译」任务模板，区别于后端 TDD 模板。输入源区 SHALL 仅引用原型核心产物。

#### Scenario: 前端 FP 使用原型转译模板

- **WHEN** kflow-plan 为前端子变更生成 tasks.md
- **THEN** 每个前端 FP 的任务结构 SHALL 包含：输入源（原型页面/设计约束/API 契约）、实现步骤（组件骨架 → 设计令牌注入 → 交互状态 → API 对接 → 原型一致性验证）
- **AND** SHALL NOT 使用后端 TDD 的 Red → Green → Refactor 步骤结构
- **AND** 输入源中的「设计约束」SHALL 引用 prototype/design-tokens.css 和 prototype/element-coverage-tree.md
- **AND** SHALL NOT 引用 prototype/design-prompt.md 或 design-system/MASTER.md

#### Scenario: 后端 FP 继续使用 TDD 模板

- **WHEN** kflow-plan 为后端子变更生成 tasks.md
- **THEN** 每个后端 FP SHALL 使用现有 TDD 任务模板（Red → Green → Refactor）
- **AND** 模板结构不受前端子变更规则影响

### Requirement: 编码阶段前端实现子流程

系统 SHALL 在 kflow-code 中为前端子变更提供专属实现流程，核心产物作为执行输入。

#### Scenario: 前端工程骨架搭建

- **WHEN** 前端子变更进入编码阶段
- **THEN** 第一步 SHALL 搭建工程骨架，包含：脚手架初始化、路由框架（对齐 element-coverage-tree.md 📄 节点）、全局布局组件（Header/Sidebar/Footer）、公共组件库（基于 prototype/index.html 中的复用组件模式提取）、状态管理框架、设计令牌注入（design-tokens.css → CSS 变量/theme）
- **AND** 工程骨架 SHALL 在所有页面实现之前完成
- **AND** 公共组件库 SHALL 以 prototype/index.html 中的实际复用模式为准，非以 design-system/MASTER.md 为准

#### Scenario: 逐页原型转译

- **WHEN** 工程骨架搭建完成
- **THEN** 系统 SHALL 逐页面读取 prototype/*.html → 转译为前端框架组件代码
- **AND** 每页面实现 SHALL 覆盖 element-coverage-tree.md 中该页面的所有 🔘 元素和 🎯 状态
- **AND** 样式 SHALL 使用 design-tokens.css 中定义的 CSS 变量，禁止硬编码颜色值/间距/圆角

#### Scenario: 交互状态覆盖

- **WHEN** 页面组件实现完成
- **THEN** 系统 SHALL 为每个页面实现 element-coverage-tree.md 中定义的全部 🎯 状态：hover/active/focus/disabled/loading/empty/error
- **AND** 弹窗/抽屉的打开和关闭逻辑 SHALL 对齐原型中的操作链定义

## ADDED Requirements

### Requirement: 前端子变更 API 契约依赖声明

系统 SHALL 在 detailed-design.md「子变更划分」章节中为前端子变更显式声明「依赖API契约」列表。

#### Scenario: 依赖 API 契约列表
- **WHEN** kflow-design 划分子变更且存在前端子变更
- **THEN** 前端子变更条目 SHALL 包含「依赖API契约」字段
- **AND** 列表每项格式为：`METHOD /path → detailed-design.md §章节`
- **AND** 该列表 SHALL 在 plan 阶段传递给 tasks.md

### Requirement: 前端编码输入限定为核心原型产物

系统 SHALL 限定前端子变更编码阶段的输入仅包含原型核心产物，排除过程产物。

#### Scenario: 核心产物白名单
- **WHEN** 前端子变更进入编码阶段
- **THEN** 可引用的原型产物 SHALL 限定为：prototype/index.html、prototype/design-tokens.css、prototype/element-coverage-tree.md
- **AND** SHALL NOT 读取 prototype/design-prompt.md
- **AND** SHALL NOT 读取 design-system/ 目录下任何文件（含 MASTER.md）

#### Scenario: 公共组件库从原型提取
- **WHEN** 前端编码需要建立公共组件库
- **THEN** 系统 SHALL 从 prototype/index.html 中分析复用组件模式提取组件清单
- **AND** SHALL NOT 依赖 design-system/MASTER.md 作为组件库建立依据
- **AND** 组件样式 SHALL 从 design-tokens.css 中获得 CSS 变量值
