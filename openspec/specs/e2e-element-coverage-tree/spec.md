# e2e-element-coverage-tree Specification

## Requirements

### Requirement: 统一元素覆盖树产物

系统 SHALL 在变更级维护一份树状结构的元素覆盖文件 `element-coverage-tree.md`，合并页面导航结构、交互元素清单、交互状态、操作驱动的动态链路（浮窗/弹窗/页面跳转）、及 E2E 测试场景 ID 映射。

#### Scenario: 有原型时树落在 prototype/ 目录

- **WHEN** prototype/index.html 存在
- **THEN** 元素覆盖树 SHALL 存储在 `prototype/element-coverage-tree.md`
- **AND** e2e-tests/index.md SHALL 通过文件引用链接指向该文件

#### Scenario: 无原型但前端项目存在时树落在 e2e-tests/ 目录

- **WHEN** prototype/index.html 不存在
- **AND** 项目类型为前后端项目
- **THEN** 元素覆盖树 SHALL 存储在 `e2e-tests/element-coverage-tree.md`
- **AND** 树通过 playwright-cli 逐页探索实际前端页面生成

#### Scenario: 纯后端项目不生成树

- **WHEN** 项目类型为纯后端项目
- **THEN** 系统 SHALL NOT 生成 element-coverage-tree.md
- **AND** E2E 测试阶段按现有逻辑标记为 ⏭️ 跳过

### Requirement: 树结构包含四层节点与操作链

元素覆盖树 SHALL 采用「页面 → 区域 → 元素 → 状态」四层结构，状态节点下 SHALL 支持挂载操作驱动的动态链路（浮窗/弹窗/下拉/Toast/页面跳转）。

#### Scenario: 树的基本结构

- **WHEN** 生成元素覆盖树
- **THEN** 树 SHALL 以页面（📄）为根节点
- **AND** 页面下 SHALL 包含区域（🏗️）作为组织层
- **AND** 区域下 SHALL 列出所有可交互元素（🔘/📝/📊 等）
- **AND** 每个元素下 SHALL 列出其交互状态（🎯）
- **AND** TC-ID 列在状态节点上的 SHALL 映射为 `→ <TC-ID>` 格式

#### Scenario: 操作链——按钮产生浮窗

- **WHEN** 某个按钮点击后会产生弹窗或下拉
- **THEN** 树 SHALL 在该按钮的状态节点下以 💬 标识嵌套浮窗
- **AND** 浮窗内的所有可交互元素 SHALL 完整列出并挂载 TC-ID
- **AND** 浮窗的关闭方式（确认/取消/遮罩/Esc）SHALL 分别挂载 TC-ID

#### Scenario: 操作链——页面跳转

- **WHEN** 某个操作导致页面跳转
- **THEN** 树 SHALL 以 🔗 标识跳转关系
- **AND** 跳转目标页面 SHALL 在树中独立存在
- **AND** 跳转前后的关联通过 🔗 → 📄 符号表达

#### Scenario: 条件出现的区域

- **WHEN** 页面中的某些区域仅在特定条件下出现（如选中行后出现批量操作栏）
- **THEN** 树 SHALL 在区域节点上标注触发条件
- **AND** 区域内元素 SHALL 挂载对应的 TC-ID

#### Scenario: 全局浮窗/Toast

- **WHEN** 页面存在全局级别的通知、Toast 或模态对话框
- **THEN** 树 SHALL 在页面根节点下以 💬 列出
- **AND** 每个全局浮窗的所有状态（成功/失败/警告）SHALL 挂载 TC-ID

### Requirement: 有原型时通过静态解析生成树

系统 SHALL 在 prototype-design 阶段用户确认通过后，通过解析 prototype/*.html 文件生成初始元素覆盖树（TC-ID 列为空）。

#### Scenario: 从原型 HTML 提取页面结构

- **WHEN** prototype-design 阶段用户确认通过
- **THEN** 系统扫描 prototype/ 目录下所有 .html 文件
- **AND** 提取所有 `<a href>` 和导航组件引用构建页面导航骨架
- **AND** 页面节点以 📄 标识，标注对应的原型文件名

#### Scenario: 从原型 HTML 提取交互元素

- **WHEN** 解析 prototype/*.html
- **THEN** 系统 SHALL 提取所有可交互元素：`<button>`、`<a>`、`<input>`、`<select>`、`<textarea>`、`<dialog>`、`[role="dialog"]`、`<details>`
- **AND** 每个元素标注类型、文本内容或 aria-label
- **AND** 按 DOM 层级关系组织到页面 → 区域 → 元素结构

#### Scenario: 从原型 HTML 提取交互状态

- **WHEN** 解析 prototype/*.html
- **THEN** 系统 SHALL 扫描样式表和内联 style 中的伪类：`:hover`、`:active`、`:focus`、`:disabled`
- **AND** 扫描 class 命名推测状态：`is-loading`、`is-error`、`is-empty`、`is-disabled`、`is-active`
- **AND** 每个发现的状态作为 🎯 节点挂载到对应元素下

#### Scenario: 从原型 HTML 提取操作链

- **WHEN** 解析 prototype/*.html
- **THEN** 系统 SHALL 扫描 JS 事件绑定：`onclick`、`addEventListener`、`@click`、`onClick`
- **AND** 分析事件处理函数中的 DOM 操作（显示/隐藏弹窗、添加/移除 class、修改 innerHTML）
- **AND** 推断操作触发的动态元素（弹窗/下拉/浮窗）并构建 💬 子树

#### Scenario: 原型迭代后重新生成

- **WHEN** prototype-design 修订模式下用户再次确认通过
- **THEN** 系统 SHALL 重新执行静态解析并覆盖旧的 element-coverage-tree.md
- **AND** 若 design 阶段已填充 TC-ID，SHALL 通过 AskUserQuestion 确认是否保留已有映射

#### Scenario: 初始树 TC-ID 列为空

- **WHEN** prototype-design 阶段生成 element-coverage-tree.md
- **THEN** 所有状态节点上的 TC-ID SHALL 为空（待 design 阶段填充）
- **AND** 文件头部标注生成时间戳和来源（prototype-design 阶段自动生成）

### Requirement: 无原型时通过 playwright-cli 探索生成树

系统 SHALL 在无原型设计的前端项目变更中，通过 playwright-cli 逐页探索实际运行的前端页面，生成元素覆盖树及 TC-ID 映射。

#### Scenario: 探索前获取全部页面路径

- **WHEN** kflow-design §7.1 EXPLORE 执行且 prototype/index.html 不存在
- **AND** 项目类型为前后端项目
- **THEN** 系统 SHALL 读取路由配置文件获取全部页面路径列表
- **AND** 按路由列表逐页探索

#### Scenario: 逐页 playwright-cli 探索

- **WHEN** playwright-cli 探索实际页面
- **THEN** 对每个页面 SHALL 执行: open → waitForLoadState → snapshot 获取静态元素
- **AND** SHALL 逐个按钮 click → snapshot 观察变化（弹窗/下拉/跳转）
- **AND** SHALL 逐个 input focus + fill 测试值 → 观察校验状态和建议列表
- **AND** SHALL 逐个 hover 触发元素 → 观察 tooltip/popover
- **AND** SHALL 表单全覆盖：空提交（观察校验错误元素）→ 合法数据提交（观察成功反馈 + 跳转）

#### Scenario: 探索时监听网络请求

- **WHEN** playwright-cli 探索实际页面
- **THEN** 系统 SHALL 通过 `page.on('response')` 监听所有 API 调用
- **AND** 提取 API 路径列表用于后续 Mock 错误测试场景设计

#### Scenario: 探索完成后生成含 TC-ID 的树

- **WHEN** playwright-cli 探索全部页面完成
- **THEN** 系统 SHALL 汇总构建 element-coverage-tree.md
- **AND** 树中 SHALL 填充 TC-ID（因为在同一 design 阶段连续完成探索和用例设计）
- **AND** 输出到 `e2e-tests/element-coverage-tree.md`

### Requirement: Design 阶段门控——TC-ID 覆盖率 100%

系统 SHALL 在 kflow-design 阶段 §7 E2ETESTS 完成后，验证元素覆盖树中所有状态节点均有 TC-ID 映射，覆盖率为 100% 后方可释放门控。

#### Scenario: TC-ID 覆盖率检查

- **WHEN** kflow-design §7 E2ETESTS 完成
- **THEN** 系统 SHALL 遍历元素覆盖树中所有 🎯 状态节点
- **AND** 验证每个状态节点均有 TC-ID 映射（不为空）
- **AND** 覆盖率 = (有 TC-ID 的状态节点数 / 总状态节点数) × 100%
- **AND** 覆盖率 MUST = 100%

#### Scenario: 覆盖率不足时门控阻塞

- **WHEN** TC-ID 覆盖率 < 100%
- **THEN** 系统 SHALL 输出未覆盖元素清单（页面 → 区域 → 元素 → 状态路径）
- **AND** 门控阻塞，不得释放详细设计阶段完成状态
- **AND** 系统 SHALL 提示 agent 为未覆盖元素补充测试用例

#### Scenario: Design 阶段进入时确认树时效性

- **WHEN** kflow-design 阶段 §7 开始执行
- **AND** element-coverage-tree.md 已存在
- **THEN** 系统 SHALL 读取树的生成时间戳
- **AND** 比对其来源（prototype/index.html 修改时间或前端路由配置）
- **AND** 若来源已更新，SHALL 通过 AskUserQuestion 询问用户是否重新生成树
- **AND** 选项包含：重新生成 / 增量更新 / 保持不变

### Requirement: E2E 测试执行阶段加载树并统计触达率

系统 SHALL 在 kflow-e2e-test 阶段每轮测试前 RELOAD 元素覆盖树，测试执行后将实际触达状态标记到树节点上，并在轮次报告中输出元素触达率统计。

#### Scenario: 每轮测试前加载元素覆盖树

- **WHEN** kflow-e2e-test 子代理开始执行新的一轮测试
- **THEN** RELOAD 步骤 SHALL 加载 `element-coverage-tree.md`
- **AND** 将树中所有 TC-ID 映射展开为可追踪的元素清单

#### Scenario: 测试执行后标记触达状态

- **WHEN** 本轮 E2E 测试全部用例执行完成
- **THEN** 系统 SHALL 对照元素覆盖树，将已执行触达的状态节点标记为 ✅
- **AND** 将未触达的状态节点标记为 ❌
- **AND** 标记结果写入轮次报告 round-{n}.md

#### Scenario: 轮次报告中的元素触达率

- **WHEN** 生成 round-{n}.md
- **THEN** 报告 SHALL 包含元素触达率统计：
  - 预期元素数: {N}
  - 实际触达: {M}
  - 触达率: {M/N * 100}%
  - 未触达元素清单（含页面路径和未触达原因）

#### Scenario: 未触达元素作为回归信号

- **WHEN** 某轮测试元素触达率 < 100%
- **THEN** 系统 SHALL 将每个未触达元素标注原因
- **AND** 原因分类为：测试用例执行失败（bug）/ 服务异常（API 不可用）/ 测试用例设计遗漏
- **AND** 若为设计遗漏，SHALL 记录到 skill-suggestion.md 并建议回退 design 阶段补充

#### Scenario: 最终总结中的元素覆盖率趋势

- **WHEN** 生成 summary.md
- **THEN** 报告 SHALL 包含 10 轮元素触达率趋势
- **AND** 趋势线预期在 100% 稳定（允许因 bug 导致的暂时性下降）
- **AND** 若趋势线持续低于 100%，SHALL 标记为阻塞（不得释放门控）

### Requirement: 废弃 element-spec.md 和 nav-tree.md

系统 SHALL 停止生成 `prototype/element-spec.md` 和 `prototype/nav-tree.md`，其信息由 element-coverage-tree.md 统一承载。

#### Scenario: prototype-design COMPLETE 步骤不再生成旧文件

- **WHEN** prototype-design 阶段 COMPLETE 步骤执行
- **THEN** 系统 SHALL NOT 生成 prototype/element-spec.md
- **AND** 系统 SHALL NOT 生成 prototype/nav-tree.md
- **AND** 系统 SHALL 生成 prototype/element-coverage-tree.md（初始版，TC-ID 为空）

#### Scenario: Code 阶段和 Code-review 阶段的数据源切换

- **WHEN** kflow-code 或 kflow-code-review 阶段执行
- **AND** 之前它们读取 prototype/element-spec.md 或 prototype/nav-tree.md 作为约束
- **THEN** 系统 SHALL 改为读取 prototype/element-coverage-tree.md 作为数据源
- **AND** 元素覆盖对账从树中提取按钮/表单/弹窗清单
- **AND** 路由覆盖对账从树的 📄 页面节点中提取页面列表
