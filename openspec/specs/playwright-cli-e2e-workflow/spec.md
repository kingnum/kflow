## MODIFIED Requirements

### Requirement: 测试代码自动生成（MODIFIED）

系统 SHALL 在 E2E 测试交互过程中收集 playwright-cli 自动生成的 Playwright TypeScript 代码，但仅在测试通过率 ≥80% 时收集为回归资产。

#### Scenario: 收集交互代码（条件触发）

- **WHEN** agent 执行 playwright-cli 交互命令（fill, click, type 等）
- **THEN** playwright-cli 自动输出对应的 TypeScript 代码
- **AND** agent 收集所有交互代码片段，组装为完整的 Playwright 测试文件
- **AND** 收集行为为被动记录，不得在交互前主动编写测试脚本

#### Scenario: 保存生成代码（可选）

- **WHEN** 测试轮次完成且本轮测试通过率 ≥80%
- **THEN** agent 将收集的代码保存到 `subchanges/{subchange}/test-reports/e2e/generated-test.spec.ts`
- **AND** 下一轮测试可直接运行 `npx playwright test generated-test.spec.ts` 跳过元素侦查
- **AND** 如通过率 <80%，跳过收集，专注修复

#### Scenario: 禁止主动编写测试脚本

- **WHEN** agent 在执行 E2E 测试
- **THEN** agent 禁止在任何阶段主动编写或修改 .spec.ts 测试脚本文件
- **AND** agent 必须使用 playwright-cli snapshot → 获取 ref → click/fill ref 的交互模式
- **AND** generated-test.spec.ts 仅作为交互成功的副产品被动收集生成

#### Scenario: 生成代码归档

- **WHEN** 变更归档
- **THEN** `generated-test.spec.ts` 随变更归档到 `docs/archive/`
- **AND** 不合并到产品级文档 `docs/designs/`

### Requirement: 子代理工具切换禁令

系统 SHALL 禁止子代理在执行 E2E 测试时自行更换测试工具或使用 Bash 直接执行 Playwright 命令替代 playwright-cli。

#### Scenario: 子代理遇到模型 API 报错

- **WHEN** 子代理在执行 playwright-cli 命令时遇到模型 API 报错
- **THEN** 子代理 SHALL NOT 自行改用 Bash 直接执行 Playwright 命令
- **AND** 子代理 SHALL NOT 改用其他测试工具或框架
- **AND** 子代理 SHALL 将错误上报变更级 agent，阻塞等待恢复
- **AND** 如确需使用 playwright-cli 以外的工具，必须 AskUserQuestion 确认

#### Scenario: playwright-cli 不可用时

- **WHEN** 子代理检测到 playwright-cli 命令不可用
- **THEN** 子代理 SHALL NOT 降级为手动文件分析
- **AND** 子代理 SHALL NOT 自行改用其他浏览器自动化工具
- **AND** 子代理 SHALL 上报变更级 agent，提示"playwright-cli 不可用，请安装或确认"
- **AND** 等待用户决策后继续

### Requirement: 每轮 E2E 测试前加载元素覆盖树

系统 SHALL 在 kflow-e2e-test 阶段每轮测试的 RELOAD 步骤中加载 `element-coverage-tree.md`，将树中 TC-ID 映射展开为可追踪的元素清单。

#### Scenario: RELOAD 步骤加载元素覆盖树

- **WHEN** kflow-e2e-test 子代理执行 PRE_HOOK 中的 RELOAD 步骤
- **THEN** RELOAD 清单 SHALL 包含 element-coverage-tree.md（条件：文件存在时）
- **AND** 子代理 SHALL 解析树中的 TC-ID 映射，生成「TC-ID → 元素路径」索引表

#### Scenario: 元素覆盖树不存在时跳过

- **WHEN** element-coverage-tree.md 不存在（纯后端项目或旧变更）
- **THEN** RELOAD 步骤 SHALL 跳过该文件
- **AND** 元素触达率统计功能禁用
- **AND** 不影响正常 E2E 测试流程

### Requirement: 无原型时使用 playwright-cli 探索生成元素覆盖树

系统 SHALL 在 kflow-design 阶段无原型文件时，通过 playwright-cli 逐页探索实际运行的前端页面，自动生成 element-coverage-tree.md。

#### Scenario: 探索前获取页面路由

- **WHEN** kflow-design 阶段检测到 prototype/index.html 不存在且为前后端项目
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

### Requirement: 每轮测试后统计元素触达率

系统 SHALL 在每轮 E2E 测试完成后对照元素覆盖树统计实际触达的元素，并在轮次报告中输出触达率。

#### Scenario: 测试执行后标记触达状态

- **WHEN** 本轮全部测试用例执行完成
- **THEN** 子代理 SHALL 对照 element-coverage-tree.md 中的 TC-ID 映射
- **AND** 将本轮已执行的 TC-ID 对应树节点标记为 ✅
- **AND** 将未执行的 TC-ID 对应树节点标记为 ❌

#### Scenario: 轮次报告中输出元素触达率

- **WHEN** 生成 round-{n}.md
- **THEN** 报告 SHALL 包含「元素触达率」章节:
  - 预期元素数（树中总状态节点数）
  - 实际触达数（✅ 节点数）
  - 触达率百分比
  - 未触达元素清单（含完整树路径: 📄 页面 → 🏗️ 区域 → 🔘 元素 → 🎯 状态）

#### Scenario: 未触达元素原因分类

- **WHEN** 存在未触达元素
- **THEN** 子代理 SHALL 对每个未触达元素分析并标注原因:
  - `bug`: 测试用例执行失败（功能缺陷）
  - `service`: 服务异常或不可用
  - `design-gap`: 测试用例设计遗漏（需回退 design 阶段）
- **AND** 原因标注写入轮次报告的未触达元素清单

#### Scenario: summary.md 中的元素触达率趋势

- **WHEN** 生成 summary.md
- **THEN** 报告 SHALL 包含 10 轮元素触达率趋势表
- **AND** 若某轮触达率 < 100%，SHALL 标注原因和恢复情况
- **AND** 若最终轮触达率 < 100%，SHALL 标记为阻塞（不得释放 E2E 测试门控）
