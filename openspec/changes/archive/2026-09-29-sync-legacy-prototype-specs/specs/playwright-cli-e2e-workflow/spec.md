## MODIFIED Requirements

### Requirement: 无原型时使用 playwright-cli 探索生成元素覆盖树

系统 SHALL 在 kflow-design 阶段无产品级原型（`docs/designs/prototypes/manifest.md` 不存在）时，通过 playwright-cli 逐页探索实际运行的前端页面，自动生成 element-coverage-tree.md。

#### Scenario: 探索前获取页面路由

- **WHEN** kflow-design 阶段检测到 `docs/designs/prototypes/manifest.md` 不存在且为前后端项目
- **THEN** 系统 SHALL 从路由配置文件或前端源码中提取全部页面路径
- **AND** 按路径列表编排逐页探索顺序（从入口页开始 BFS）

#### Scenario: 逐页 playwright-cli snapshot 探索

- **WHEN** 探索子代理对每个页面执行 playwright-cli
- **THEN** 对每个页面 SHALL 依次执行:
  1. `playwright-cli open {url}` — 导航到目标页面
  2. `playwright-cli run-code "await page.waitForLoadState('networkidle')"` — 等待加载完成
  3. `playwright-cli snapshot` — 获取所有可交互元素及 ref

#### Scenario: 探索交互操作产生的动态元素

- **WHEN** 静态 snapshot 完成后
- **THEN** 探索子代理 SHALL 逐个元素执行交互操作:
  - 每个 button: `click` → `snapshot` → 观察新出现的弹窗/下拉/浮窗/Toast → 记录 → `close` 弹窗
  - 每个 input: `focus` → 记录 focus 态 → `fill` 测试值 → 观察校验反馈/建议列表
  - 每个 select: 切换选项 → 观察联动变化
  - 每个 hover 触发元素: hover → 观察 tooltip/popover
- **AND** 操作产生的页面跳转 SHALL 记录目标页面路径后 `go back`

#### Scenario: 探索完成后输出树

- **WHEN** playwright-cli 全部页面探索完成
- **THEN** 系统 SHALL 汇总构建 element-coverage-tree.md
- **AND** 包含页面导航结构、元素清单、交互状态、操作链
- **AND** TC-ID 同步填充（因为探索和用例设计在同一 design 阶段连续完成）
- **AND** 输出到 `e2e-tests/element-coverage-tree.md`
