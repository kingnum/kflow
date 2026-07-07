# prototype-to-code-consistency Specification

## Requirements

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
- **AND** SHALL 同步更新 `prototype/index.md` 中的文件清单和版本号

#### Scenario: 用户跳过原型设计时不生成

- **WHEN** 原型设计阶段被跳过（⏭️ 跳过）
- **THEN** 系统不生成 design-tokens.css 和 element-coverage-tree.md
- **AND** 后续 code 和 code-review 阶段不执行原型对账

### Requirement: 编码阶段前端子变更使用原型作为执行输入

系统 SHALL 在前端子变更编码阶段，通过读取 `prototype/index.md` 原型产物清单动态获取原型文件列表，将清单中声明的原型产物作为前端转译流程的必需输入，而非硬编码具体文件路径。

#### Scenario: 前端工程骨架搭建时读取原型产物

- **WHEN** 前端子变更进入编码阶段的「工程骨架搭建」
- **THEN** 系统 SHALL 读取 `prototype/index.md` 获取原型产物清单
- **AND** 从清单中获取元素覆盖树文件路径（角色为 coverage）→ 搭建路由框架
- **AND** 从清单中获取设计令牌文件路径（角色为 tokens）→ 注入 CSS 变量/theme 系统
- **AND** 从清单中获取入口文件路径（角色为 entry）的全局布局 → 实现 Header/Sidebar/Footer 布局组件
- **AND** 公共组件库 SHALL 从入口文件的 HTML 结构中提取复用模式

#### Scenario: 逐页转译时读取对应原型页面

- **WHEN** 前端子变更进入编码阶段的「逐页转译」
- **THEN** 系统 SHALL 从 `prototype/index.md` 的页面清单中获取各页面对应的 HTML 文件路径
- **AND** 对每个页面：读取对应的 HTML 文件 → 识别交互元素和状态 → 转译为前端框架组件
- **AND** 从元素覆盖树文件中读取该页面的 🔘 元素清单和 🎯 状态清单 → 逐项实现
- **AND** 样式 SHALL 使用设计令牌文件中定义的 CSS 变量

#### Scenario: 原型产物缺失时的处理

- **WHEN** 前端子变更进入编码阶段
- **AND** `prototype/index.md` 不存在
- **THEN** 门控检查 SHALL 标记 ⚠️ 阻塞
- **WHEN** `prototype/index.md` 存在但清单中部分角色文件缺失（如缺少 tokens 角色文件）
- **THEN** 系统 SHALL 对缺失角色执行降级处理：存在则作为输入，不存在则跳过对应步骤
- **AND** 入口文件（角色为 entry）缺失时 SHALL 标记 ⚠️ 阻塞

### Requirement: 代码审查阶段执行原型对账

系统 SHALL 在代码审查阶段从 `prototype/index.md` 获取原型产物清单，基于清单中声明的文件路径执行原型对账。

#### Scenario: 硬编码颜色值检测

- **WHEN** kflow-code-review 阶段执行
- **AND** `prototype/index.md` 存在且清单中包含角色为 tokens 的文件
- **THEN** 系统读取清单中该 tokens 文件的内容
- **AND** 使用 Grep 从源码中提取所有硬编码颜色值（#xxx、rgb()、rgba()、hsl()）
- **AND** 与 tokens 文件中的 CSS 变量值进行比对
- **AND** 源码中硬编码的颜色值在 tokens 文件中有对应变量时，标记为 ❌ "应使用 var(--xxx) 替代硬编码"
- **AND** 源码中使用了 var(--xxx) 的，标记为 ✅

#### Scenario: 元素覆盖对账

- **WHEN** kflow-code-review 阶段执行
- **AND** `prototype/index.md` 存在且清单中包含角色为 coverage 的文件
- **THEN** 系统读取清单中该 coverage 文件中的按钮/表单/弹窗/浮窗元素清单
- **AND** 使用 Grep 在源码中逐项搜索对应名称
- **AND** 缺失项标记为 ❌ "元素覆盖树中定义了 {元素名}，源码中未找到"
- **AND** 多余项（源码中有但树中无）记录但不阻塞

#### Scenario: 路由覆盖对账

- **WHEN** kflow-code-review 阶段执行
- **AND** `prototype/index.md` 存在且清单中包含角色为 coverage 的文件
- **THEN** 系统读取清单中该 coverage 文件中 📄 页面节点列表
- **AND** 提取前端路由配置文件中的所有路径
- **AND** 未覆盖的页标记为 ❌ "元素覆盖树中定义了页面 {page}，路由配置中未找到"

#### Scenario: 对账结果输出

- **WHEN** 原型对账完成
- **THEN** 系统将对账结果写入代码审查报告
- **AND** 包含：设计令牌使用统计、元素覆盖率、路由覆盖率
- **AND** 元素覆盖率 < 100% 时标记为审查缺陷
- **AND** 设计令牌硬编码数 > 0 时标记为审查建议

## ADDED by subchange-type-enforcement

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
- **AND** 发现 ≥ 3 次硬编码颜色值时 SHALL 标记：「后端SC 含疑似内联样式代码，请确认」
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
