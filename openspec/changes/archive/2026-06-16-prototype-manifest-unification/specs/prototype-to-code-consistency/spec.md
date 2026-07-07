## MODIFIED Requirements

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
