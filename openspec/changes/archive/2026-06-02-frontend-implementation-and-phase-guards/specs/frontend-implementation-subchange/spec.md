## ADDED Requirements

### Requirement: 前端实现集中为独立子变更

系统 SHALL 将每个 Change 的所有前端实现集中在一个独立的前端子变更中完成，不拆分到多个后端子变更。

#### Scenario: 前后端项目划分子变更时创建前端子变更

- **WHEN** kflow-design 阶段为前后端项目划分子变更
- **THEN** 系统 SHALL 将所有前端功能点（页面/组件/路由/状态管理/样式）归属到一个独立的前端子变更
- **AND** 后端子变更 SHALL NOT 包含前端实现任务

#### Scenario: 纯后端项目不创建前端子变更

- **WHEN** 项目类型为纯后端
- **THEN** 系统 SHALL NOT 创建前端子变更
- **AND** 前端相关内容标记为 ⏭️ 不适用

### Requirement: 前端子变更依赖 API 契约而非后端实现

前端子变更 SHALL 依赖 design 阶段定义的 API 契约（路径/参数/返回值/错误码），而非等待后端子变更编码完成。

#### Scenario: 前端子变更的依赖判定

- **WHEN** kflow-plan 生成前端子变更的 tasks.md
- **THEN** 前端子变更的依赖列标注为「依赖 API 契约（detailed-design.md §接口设计）」
- **AND** 依赖状态 SHALL NOT 要求后端子变更状态为「🔄 进行中」或「✅ 完成」

#### Scenario: 前端子变更使用 mock 数据启动

- **WHEN** 前端子变更进入编码阶段
- **AND** 后端子变更尚未完成编码
- **THEN** 前端子变更 SHALL 使用 mock 数据（基于 API 契约）进行开发
- **AND** 后端子变更编码完成后替换 mock 为真实 API

### Requirement: 前端功能点任务模板

系统 SHALL 在 plan 阶段为前端子变更生成「原型转译」任务模板，区别于后端 TDD 模板。

#### Scenario: 前端 FP 使用原型转译模板

- **WHEN** kflow-plan 为前端子变更生成 tasks.md
- **THEN** 每个前端 FP 的任务结构 SHALL 包含：输入源（原型页面/设计约束/API 契约）、实现步骤（组件骨架 → 设计令牌注入 → 交互状态 → API 对接 → 原型一致性验证）
- **AND** SHALL NOT 使用后端 TDD 的 Red → Green → Refactor 步骤结构

#### Scenario: 后端 FP 继续使用 TDD 模板

- **WHEN** kflow-plan 为后端子变更生成 tasks.md
- **THEN** 每个后端 FP SHALL 使用现有 TDD 任务模板（Red → Green → Refactor）
- **AND** 模板结构不受前端子变更规则影响

### Requirement: 编码阶段前端实现子流程

系统 SHALL 在 kflow-code 中为前端子变更提供专属实现流程，覆盖原型到工程代码的完整转译。

#### Scenario: 前端工程骨架搭建

- **WHEN** 前端子变更进入编码阶段
- **THEN** 第一步 SHALL 搭建工程骨架，包含：脚手架初始化、路由框架（对齐 element-coverage-tree.md 📄 节点）、全局布局组件（Header/Sidebar/Footer）、公共组件库（Button/Input/Modal/Table 等，对齐 design-system/MASTER.md）、状态管理框架、设计令牌注入（design-tokens.css → CSS 变量/theme）
- **AND** 工程骨架 SHALL 在所有页面实现之前完成

#### Scenario: 逐页原型转译

- **WHEN** 工程骨架搭建完成
- **THEN** 系统 SHALL 逐页面读取 prototype/*.html → 转译为前端框架组件代码
- **AND** 每页面实现 SHALL 覆盖 element-coverage-tree.md 中该页面的所有 🔘 元素和 🎯 状态
- **AND** 样式 SHALL 使用 design-tokens.css 中定义的 CSS 变量，禁止硬编码颜色值/间距/圆角

#### Scenario: 交互状态覆盖

- **WHEN** 页面组件实现完成
- **THEN** 系统 SHALL 为每个页面实现 element-coverage-tree.md 中定义的全部 🎯 状态：hover/active/focus/disabled/loading/empty/error
- **AND** 弹窗/抽屉的打开和关闭逻辑 SHALL 对齐原型中的操作链定义

#### Scenario: 前端编译验证

- **WHEN** 前端子变更所有页面实现完成
- **THEN** 系统 SHALL 执行前端编译验证（如 tsc --noEmit 或 npm run build）
- **AND** 编译失败 SHALL 阻塞前端子变更的完成

### Requirement: 前端 FP 超过 10 时的拆分

当前端功能点数量超过 10 时，系统 SHALL 允许拆分为「骨架子变更」+ 多个「页面组子变更」。

#### Scenario: 骨架子变更先行

- **WHEN** 前端 FP 数量 > 10
- **THEN** 系统 SHALL 先创建「前端-骨架子变更」，包含：脚手架/路由/布局/组件库/状态管理/设计令牌注入（不计入 10 FP 限制的核心基础设施）
- **AND** 骨架子变更 SHALL 在其他前端页面子变更之前完成

#### Scenario: 页面组子变更串行追加

- **WHEN** 骨架子变更完成
- **THEN** 系统 SHALL 按页面/模块创建串行页面组子变更（每个 ≤ 10 FP）
- **AND** 各页面组子变更 SHALL 在骨架已建立的路由框架和组件库基础上增量添加页面
- **AND** 页面组子变更之间不存在共享文件冲突（各自操作独立的页面组件文件）
