## MODIFIED Requirements

### Requirement: 原型通过后自动提取设计规格

系统 SHALL 在原型设计阶段用户确认通过后，从实际原型 HTML 文件中生成统一的元素覆盖树 `prototype/element-coverage-tree.md`，替代原有的 design-tokens.css、element-spec.md 和 nav-tree.md 三项独立产物中的后两项。

#### Scenario: 从原型 HTML 自动提取 design-tokens.css

- **WHEN** 原型设计阶段用户确认通过
- **THEN** 系统扫描 prototype/ 目录下所有 .html 文件
- **AND** 提取 :root { ... } 中的 CSS 变量声明
- **AND** 提取内联 style 中出现的颜色值、font-size、border-radius、box-shadow 等样式值
- **AND** 去重、排序、归类后输出到 prototype/design-tokens.css
- **AND** 在文件头部标注提取来源（原型版本、生成时间、自动提取）

#### Scenario: 从原型 HTML 自动生成 element-coverage-tree.md

- **WHEN** 原型设计阶段用户确认通过
- **THEN** 系统从 prototype/ 目录下所有 .html 文件中提取页面结构和交互元素
- **AND** 生成 prototype/element-coverage-tree.md，包含：页面导航结构（📄）、交互元素清单（🔘/📝/📊）、交互状态（🎯 hover/focus/loading/empty/error/disabled）、操作链（💬 弹窗/浮窗/🔗 页面跳转）
- **AND** TC-ID 列初始为空，待 design 阶段填充
- **AND** 文件头部标注生成时间戳和来源（prototype-design 阶段自动生成）

#### Scenario: 原型迭代后重新生成

- **WHEN** 原型设计阶段用户确认通过后又进入修订循环
- **AND** 新一轮用户确认通过
- **THEN** 系统重新执行 design-tokens.css 和 element-coverage-tree.md 的生成
- **AND** 覆盖旧版本文件
- **AND** 若 design 阶段已填充 TC-ID，SHALL 通过 AskUserQuestion 确认是否保留已有映射

#### Scenario: 用户跳过原型设计时不生成

- **WHEN** 原型设计阶段被跳过（⏭️ 跳过）
- **THEN** 系统不生成 design-tokens.css 和 element-coverage-tree.md
- **AND** 后续 code 和 code-review 阶段不执行原型对账

### Requirement: 编码阶段引用原型 spec 文件

系统 SHALL 在编码阶段子代理的 prompt 中注入原型 spec 文件作为实现约束，仅当这些文件存在时。

#### Scenario: 前端编码约束——设计令牌

- **WHEN** prototype/design-tokens.css 存在
- **AND** kflow-code 阶段子代理开始执行
- **THEN** 子代理 prompt 中注入约束: "必须使用 prototype/design-tokens.css 中定义的 CSS 变量，禁止在源码中硬编码颜色值/间距/圆角"
- **AND** 子代理在实现前端样式时引用该文件中的变量值

#### Scenario: 前端编码约束——元素覆盖

- **WHEN** prototype/element-coverage-tree.md 存在
- **AND** kflow-code 阶段子代理开始执行
- **THEN** 子代理 prompt 中注入约束: "必须实现 prototype/element-coverage-tree.md 中定义的所有元素及其状态（按钮/表单/弹窗/浮窗/交互状态）"
- **AND** 子代理在实现完成后自行对照元素覆盖树验证元素覆盖

#### Scenario: 前端编码约束——路由覆盖

- **WHEN** prototype/element-coverage-tree.md 存在
- **AND** kflow-code 阶段子代理开始执行
- **THEN** 子代理 prompt 中注入约束: "路由结构必须覆盖 element-coverage-tree.md 中 📄 页面节点的所有页面"
- **AND** 子代理在实现完成后自行验证路由配置

#### Scenario: 原型 spec 文件不存在时不注入

- **WHEN** prototype/design-tokens.css 和 element-coverage-tree.md 均不存在
- **THEN** 编码阶段不注入上述约束
- **AND** 子代理按正常流程执行，不受影响

### Requirement: 代码审查阶段执行原型对账

系统 SHALL 在代码审查阶段从源码中机械提取实际使用的元素和样式值，与 element-coverage-tree.md 对账。

#### Scenario: 硬编码颜色值检测

- **WHEN** kflow-code-review 阶段执行
- **AND** prototype/design-tokens.css 存在
- **THEN** 系统使用 Grep 从源码中提取所有硬编码颜色值（#xxx、rgb()、rgba()、hsl()）
- **AND** 与 design-tokens.css 中的 CSS 变量值进行比对
- **AND** 源码中硬编码的颜色值在 design-tokens.css 中有对应变量时，标记为 ❌ "应使用 var(--xxx) 替代硬编码"
- **AND** 源码中使用了 var(--xxx) 的，标记为 ✅

#### Scenario: 元素覆盖对账

- **WHEN** kflow-code-review 阶段执行
- **AND** prototype/element-coverage-tree.md 存在
- **THEN** 系统读取 element-coverage-tree.md 中的按钮/表单/弹窗/浮窗元素清单
- **AND** 使用 Grep 在源码中逐项搜索对应名称
- **AND** 缺失项标记为 ❌ "element-coverage-tree 中定义了 {元素名}，源码中未找到"
- **AND** 多余项（源码中有但树中无）记录但不阻塞

#### Scenario: 路由覆盖对账

- **WHEN** kflow-code-review 阶段执行
- **AND** prototype/element-coverage-tree.md 存在
- **THEN** 系统读取 element-coverage-tree.md 中 📄 页面节点列表
- **AND** 提取前端路由配置文件中的所有路径
- **AND** 未覆盖的页标记为 ❌ "元素覆盖树中定义了页面 {page}，路由配置中未找到"

#### Scenario: 对账结果输出

- **WHEN** 原型对账完成
- **THEN** 系统将对账结果写入代码审查报告
- **AND** 包含：设计令牌使用统计、元素覆盖率、路由覆盖率
- **AND** 元素覆盖率 < 100% 时标记为审查缺陷
- **AND** 设计令牌硬编码数 > 0 时标记为审查建议

## REMOVED Requirements

### Requirement: 从原型 HTML 自动提取 element-spec.md

**Reason**: element-spec.md 的信息（按钮/表单/弹窗清单）是 element-coverage-tree.md 的子集，后者还额外包含交互状态、操作链和 TC-ID 映射。维护两个文件会造成信息冗余和不一致。

**Migration**: 所有读取 prototype/element-spec.md 的流程改为读取 prototype/element-coverage-tree.md，从树中提取对应的元素清单信息。code-review 阶段的元素覆盖对账逻辑同步更新。

### Requirement: 从原型 HTML 自动提取 nav-tree.md

**Reason**: nav-tree.md 的信息（页面可达关系）已合并到 element-coverage-tree.md 的 📄 页面节点层。单一文件统一管理页面结构和元素覆盖，避免分散。

**Migration**: 所有读取 prototype/nav-tree.md 的流程改为读取 prototype/element-coverage-tree.md，从树的 📄 页面节点中提取页面列表和导航关系。code-review 阶段的路由覆盖对账逻辑同步更新。
