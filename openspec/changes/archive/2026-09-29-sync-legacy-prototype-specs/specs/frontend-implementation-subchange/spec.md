## MODIFIED Requirements

### Requirement: 前端功能点任务模板

系统 SHALL 在 plan 阶段为前端子变更生成「原型转译」任务模板，区别于后端 TDD 模板。输入源区 SHALL 仅引用原型核心产物。

#### Scenario: 前端 FP 使用原型转译模板

- **WHEN** kflow-plan 为前端子变更生成 tasks.md
- **THEN** 每个前端 FP 的任务结构 SHALL 包含：输入源（原型页面/设计约束/API 契约）、实现步骤（组件骨架 → 设计令牌注入 → 交互状态 → API 对接 → 原型一致性验证）
- **AND** SHALL NOT 使用后端 TDD 的 Red → Green → Refactor 步骤结构
- **AND** 输入源中的「设计约束」SHALL 引用 `docs/designs/prototypes/design-tokens.css`（`docs/designs/prototypes/manifest.md` 中角色为 tokens 的文件）和变更级 `element-coverage-tree.md`
- **AND** SHALL NOT 引用 prototype-plan/design-prompt.md 或 design-system/MASTER.md

#### Scenario: 后端 FP 继续使用 TDD 模板

- **WHEN** kflow-plan 为后端子变更生成 tasks.md
- **THEN** 每个后端 FP SHALL 使用现有 TDD 任务模板（Red → Green → Refactor）
- **AND** 模板结构不受前端子变更规则影响

### Requirement: 编码阶段前端实现子流程

系统 SHALL 在 kflow-code 中为前端子变更提供专属实现流程，核心产物作为执行输入。

#### Scenario: 前端工程骨架搭建

- **WHEN** 前端子变更进入编码阶段
- **THEN** 第一步 SHALL 搭建工程骨架，包含：脚手架初始化、路由框架（对齐 element-coverage-tree.md 📄 节点）、全局布局组件（Header/Sidebar/Footer）、公共组件库（基于 `docs/designs/prototypes/manifest.md` 中角色为 entry/page 的文件与 `docs/designs/prototypes/components/` 中的复用组件模式提取）、状态管理框架、设计令牌注入（`docs/designs/prototypes/design-tokens.css` → CSS 变量/theme）
- **AND** 工程骨架 SHALL 在所有页面实现之前完成
- **AND** 公共组件库 SHALL 以 `docs/designs/prototypes/manifest.md` 声明文件与 `docs/designs/prototypes/components/` 中的实际复用模式为准，非以 design-system/MASTER.md 为准

#### Scenario: 逐页原型转译

- **WHEN** 工程骨架搭建完成
- **THEN** 系统 SHALL 逐页面读取 `docs/designs/prototypes/screens/*.html`（页面文件由 `docs/designs/prototypes/manifest.md` 页面清单声明）→ 转译为前端框架组件代码
- **AND** 每页面实现 SHALL 覆盖 element-coverage-tree.md 中该页面的所有 🔘 元素和 🎯 状态
- **AND** 样式 SHALL 使用 `docs/designs/prototypes/design-tokens.css` 中定义的 CSS 变量，禁止硬编码颜色值/间距/圆角

#### Scenario: 交互状态覆盖

- **WHEN** 页面组件实现完成
- **THEN** 系统 SHALL 为每个页面实现 element-coverage-tree.md 中定义的全部 🎯 状态：hover/active/focus/disabled/loading/empty/error
- **AND** 弹窗/抽屉的打开和关闭逻辑 SHALL 对齐原型中的操作链定义

#### Scenario: 前端编译验证

- **WHEN** 前端子变更所有页面实现完成
- **THEN** 系统 SHALL 执行前端编译验证（如 tsc --noEmit 或 npm run build）
- **AND** 编译失败 SHALL 阻塞前端子变更的完成

### Requirement: 前端编码输入限定为核心原型产物

系统 SHALL 限定前端子变更编码阶段的输入仅包含原型核心产物，排除过程产物。

#### Scenario: 核心产物白名单
- **WHEN** 前端子变更进入编码阶段
- **THEN** 可引用的原型产物 SHALL 限定为：`docs/designs/prototypes/manifest.md` 中角色为 entry/page/tokens/shared 的文件、变更级 `prototype-changes.md` 声明的本变更改动、变更级 `element-coverage-tree.md`
- **AND** SHALL NOT 读取 prototype-plan/design-prompt.md
- **AND** SHALL NOT 读取 design-system/ 目录下任何文件（含 MASTER.md）

#### Scenario: 公共组件库从原型提取
- **WHEN** 前端编码需要建立公共组件库
- **THEN** 系统 SHALL 从 `docs/designs/prototypes/manifest.md` 中角色为 entry/page 的文件与 `docs/designs/prototypes/components/` 中分析复用组件模式提取组件清单
- **AND** SHALL NOT 依赖 design-system/MASTER.md 作为组件库建立依据
- **AND** 组件样式 SHALL 从 `docs/designs/prototypes/design-tokens.css` 中获得 CSS 变量值
