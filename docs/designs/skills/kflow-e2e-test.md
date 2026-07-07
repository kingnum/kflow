# kflow-e2e-test（E2E 浏览器自动化测试阶段）

> **版本**: 参见仓库根目录 `VERSION` 文件
> **阶段**: 浏览器自动化测试（前后端项目必须阶段，子变更级）

---

## 基本信息

```yaml
name: kflow-e2e-test
description: E2E 浏览器自动化测试阶段 - 使用 playwright-cli snapshot+ref 模式执行 E2E 测试。集成测试决策树（静态 HTML/动态应用/服务器状态）、健康评分数据采集映射、测试代码自动生成（generated-test.spec.ts）、网络 Mock 错误测试。仅适用于前后端项目，纯后端项目跳过。依赖前置 kflow-api-test（接口单元测试）。多轮测试报告输出。阶段钩子引用 `skills/kflow-e2e-test/references/hooks.md`（每轮前 STOP→编译→迁移→START→健康检查，每轮后 STOP+浏览器清理）。/E2E 测试/QA 测试/功能测试/浏览器自动化测试/playwright
license: MIT
triggers:
  - E2E 测试
  - QA 测试
  - 功能测试
  - 浏览器自动化测试
  - playwright
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Agent
```

---

## 门控检查

> **机制说明**：门控规则定义在 [core-mechanisms/03-status-and-tasks.md](../core-mechanisms/03-status-and-tasks.md#34-门控规则)

进入浏览器自动化测试阶段前检查：
- .status.md 存在
- 项目类型 = 前后端项目（纯后端项目跳过此阶段）
- 编码状态 = ✅ 完成（含代码审查通过）
- 接口单元测试状态 = ✅ 完成（由 `kflow-api-test` 执行）
- traceability.md「接口测试」列覆盖率 = 100%
- 子变更代码审查报告存在 (test-reports/review/code-review.md)
- docs/service-guide.md 存在（服务启动配置可用）

---

## 项目类型判断

| 项目类型 | 阶段处理 |
|---------|---------|
| 前后端项目 | 必须执行浏览器自动化测试阶段 |
| 纯后端项目 | ⏭️ 跳过此阶段（接口单元测试由 `kflow-api-test` 覆盖） |

---

## 输入要求

| 产物 | 图例 | 说明 |
|------|------|------|
| 变更级 e2e-tests/ | ✅ 必须 | E2E 测试用例文档 |
| 变更级 detailed-design.md | ✅ 必须 | 统一详细设计（NFR 章节用于性能评分参考） |
| docs/service-guide.md | ✅ 必须 | 服务启动配置（多环境） |
| prototype/index.md | 🔶 条件 | 原型清单入口，用于视觉一致性对比（从清单获取页面文件路径） |
| element-coverage-tree.md | 🔶 条件 | 元素覆盖树（前后端项目 + 文件存在时），用于元素触达率统计和回归检测。有原型时位于 prototype/ 目录，无原型时位于 e2e-tests/ 目录 |

---

## 输出产物

| 产物 | 文件 | 模板 | 图例 | 内容要求 |
|------|------|------|------|---------|
| E2E测试轮次报告 | subchanges/*/test-reports/e2e/round-{n}.md | [E2E测试轮次报告](../../templates/subchanges/{subchange}/e2e-round-report.md) | ✅ 必须 | 测试用例执行结果 |
| E2E测试总结文档 | subchanges/*/test-reports/e2e/summary.md | [E2E测试总结](../../templates/subchanges/{subchange}/e2e-summary.md) | ✅ 必须 | 各轮次统计、健康评分、是否通过 |
| 自动生成测试代码 | subchanges/{subchange}/test-reports/e2e/generated-test.spec.ts | N/A（Playwright TypeScript） | 🔶 条件（通过率≥80%时收集） | playwright-cli 交互过程中被动收集的测试代码，仅当本轮测试通过率 ≥80% 时保存为回归资产 |
| 状态文件更新 | subchanges/*/.status.md | [子变更状态文件](../../templates/subchanges/{subchange}/subchange-status.md) | ✅ 必须 | 标记子变更测试阶段状态 |
| 变更状态更新 | .status.md | [变更级状态文件](../../templates/changes/{change}/change-status.md) | ✅ 必须 | 更新子变更进度矩阵 |

---

## 执行流程

```
E2E 测试阶段流程 (playwright-cli 驱动):

┌─────────────────────────────────────────────────────────────┐
│                   E2E TEST WORKFLOW                           │
├─────────────────────────────────────────────────────────────┤
│  1. PRE_HOOK  → 引用 `skills/kflow-e2e-test/references/hooks.md` e2e-test 阶段 PRE_HOOK │
│  │   ├── CHECK_STATE → 验证前置阶段状态                       │
│  │   ├── RELOAD → 重读 service-guide.md, e2e-tests/, detailed-design.md, element-coverage-tree.md(条件), prototype/(条件), .status.md │
│  │   ├── CHECK_PORTS → 检测前后端端口占用                     │
│  │   ├── STOP_STALE → 停止残留服务                            │
│  │   ├── COMPILE → 前后端编译                                 │
│  │   ├── MIGRATE → 执行未执行的迁移脚本                       │
│  │   ├── START_SERVICE → with_server.py --daemon 启动前后端服务 │
│  │   └── HEALTH_CHECK → /health + /db-health + 前端 /health   │
│  2. CHECK     → 门控检查（前置阶段 + 服务刷新门控）          │
│  2. TYPECHECK → 确认项目类型为前后端项目                      │
│  │   └── 纯后端项目 → 标记 ⏭️ 跳过                            │
│  3. WAIT_SYNC → 等待变更级 agent 编译重启完成                 │
│  │   └── 变更级 agent 执行: 停止→编译→迁移→启动→健康检查     │
│  │   └── 收到「服务就绪，开始 Round N」信号后继续            │
│  4. DECIDE    → 按决策树选择执行路径（见决策树章节）          │
│  │   ├── 静态 HTML → playwright-cli open file:///path        │
│  │   ├── 动态应用 + 服务已运行 → playwright-cli open {url}   │
│  │   └── 动态应用 + 服务未运行 → 上报变更级 → 等待恢复       │
│  5. SESSION   → 管理浏览器会话（见会话管理章节）               │
│  │   ├── playwright-cli open {url} → 创建会话                │
│  │   ├── playwright-cli run-code "page.waitForLoadState()"   │
│  │   └── playwright-cli snapshot → 获取元素 ref 编号         │
│  6. EXECUTE   → 执行测试用例（使用 playwright-cli 命令）     │
│  │   ├── 按 ref 执行交互: click/fill/type/press              │
│  │   ├── 网络 Mock 错误场景: route/unroute                   │
│  │   ├── 采集健康评分数据: console/eval/screenshot           │
│  │   ├── 收集交互代码 → generated-test.spec.ts（被动收集，仅通过率≥80%时保存）│
│  │   └── 记录执行结果                                        │
│  7. EVALUATE  → 评估测试结果 + 健康评分                       │
│  │   ├── 全部通过 → 输出 summary.md                           │
│  │   │   ├── 其他子变更未完成 → 标记 ⏸️ 等待同步             │
│  │   │   └── 所有子变更完成 → 标记完成                        │
│  │   └── 有失败 → 提示进入缺陷修复阶段                        │
│  8. FIX       → (缺陷修复阶段处理，含根因分类路由)            │
│  9. CLEANUP   → 关闭浏览器会话                                │
│  │   ├── playwright-cli close → 关闭当前会话                  │
│  │   └── playwright-cli kill-all → 清理残留（如需要）        │
│  10. ROUND N  → 等待变更级同步 → 执行后续轮次测试             │
│  11. SUMMARY  → 输出测试总结文档 + 健康评分                   │
│  12. NEXT     → 选择下一个子变更测试（按依赖顺序）             │
│  │   └────────────────────────────────────────────────────── │
│  │   所有子变更测试完成后                                     │
│  │   └────────────────────────────────────────────────────── │
│  13. INTEGRATE → 准备进入变更级集成测试                        │
│ 14. POST_HOOK → 引用 `skills/kflow-e2e-test/references/hooks.md` e2e-test 阶段 POST_HOOK │
│  │   ├── STOP_SERVICE → with_server.py --stop-all 停止前后端服务 │
│  │   ├── VERIFY_STOP → 验证端口已释放                          │
│  │   ├── BROWSER_CLEANUP → playwright-cli kill-all            │
│  │   └── UPDATE_STATE → 更新 .status.md + 清理 .service-state.json │
└─────────────────────────────────────────────────────────────┘
```

### 子变更 agent 服务使用约束

> 完整规范参见 `skills/kflow-e2e-test/references/service-lifecycle.md`

子变更 agent 为纯消费者，不管理服务生命周期。连接已知端口使用服务，不执行启停/编译/迁移操作。

### 服务不可用上报

> 完整规范参见 `skills/kflow-e2e-test/references/service-lifecycle.md`

服务不可用时上报变更级 agent，标记当前测试用例为「阻塞等待服务恢复」，等待服务恢复后继续。

---

## E2E 测试决策树

测试执行前按以下决策树选择路径：

```
E2E 测试决策树:

被测页面类型？
    │
    ├── 静态 HTML 文件
    │   └── playwright-cli open file:///path/to/page.html
    │       └── 直接执行 snapshot → 无需启动服务器
    │
    └── 动态应用
        │
        ├── 服务已在运行？
        │   ├── YES → playwright-cli open {url}
        │   │   └── playwright-cli run-code "async page => { await page.waitForLoadState('networkidle'); }"
        │   │   └── playwright-cli snapshot → 获取元素 ref
        │   │
        │   └── NO → 上报变更级 agent 启动服务
        │       └── 等待「服务就绪」信号
        │       └── 走「服务已运行」路径
        │
        └── 服务器状态检查？
            └── playwright-cli run-code "async page => { const r = await page.request.get('/health'); return r.status(); }"
```

| 分支 | 触发条件 | playwright-cli 命令 | 说明 |
|------|---------|-------------------|------|
| 静态 HTML | 被测页面为 .html 文件，无动态后端 | `open file:///path/to/page.html` | 无需启动开发服务器 |
| 动态应用 + 服务已运行 | 动态应用，端口可连接 | `open {url}` + `run-code "waitForLoadState('networkidle')"` | 先等待网络空闲再 snapshot |
| 动态应用 + 服务未运行 | 动态应用，端口无响应 | 上报变更级 → 等待恢复 → 走「服务已运行」路径 | 子变更 agent 不自行启动服务 |

---

## 元素定位方法

### 主要方法：snapshot + ref

playwright-cli 的 snapshot 命令自动为页面中每个可交互元素分配唯一的 ref 编号。这是元素定位的主要方法。

```
工作流:
1. playwright-cli open {url}                    # 导航到目标页面
2. playwright-cli run-code "await page.waitForLoadState('networkidle');"
3. playwright-cli snapshot                      # 获取带有 ref 的元素列表
   → 输出示例:
     e15 [button "登录"]
     e22 [input "用户名"]
     e28 [a "忘记密码"]
4. playwright-cli click e15                     # 使用 ref 执行交互
5. playwright-cli fill e22 "testuser"           # 填充表单
```

### 备用方法：getByRole / getByTestId

当 snapshot ref 因页面动态变化失效时使用备用方法：

| 场景 | 方法 | 示例 |
|------|------|------|
| ref 失效（页面动态变化） | 重新 snapshot 获取最新 ref | `playwright-cli snapshot` |
| ref 再次失效 | `getByRole()` | `playwright-cli run-code "await page.getByRole('button', {name: '登录'}).click()"` |
| 组件有 data-testid | `getByTestId()` | `playwright-cli run-code "await page.getByTestId('submit-btn').click()"` |

---

## 健康评分数据采集映射

健康评分各维度通过 playwright-cli 命令采集原始数据：

| 评分维度 | 数据源 | playwright-cli 命令 | 评分规则 |
|---------|--------|-------------------|---------|
| 功能完整性 | 测试用例执行结果 | 统计 ✅/❌ 用例数 | 通过数/总数 × 100 |
| 控制台错误 | 浏览器控制台 | `playwright-cli console` | 每条 [error] 扣 10 分，每条 [warning] 扣 5 分 |
| 性能响应 | performance.timing | `playwright-cli --raw eval "JSON.stringify(performance.timing)"` | `loadEventEnd - navigationStart` < 2s 满分，每超 1s 扣 20 分 |
| 视觉一致性 | 页面截图 + prototype/index.md | `playwright-cli screenshot` | 与原型清单中声明的页面文件对比；原型缺失时为 N/A |
| 可访问性 | ARIA 属性检测 | `playwright-cli --raw eval "JSON.stringify(Array.from(document.querySelectorAll('[role],[aria-*]')).map(e => ({tag: e.tagName, role: e.getAttribute('role'), aria: Array.from(e.attributes).filter(a=>a.name.startsWith('aria-')).map(a=>a.name)})))"` | 统计 [role] 和 [aria-*] 属性数量，覆盖率评分 |
| 元素覆盖率 | element-coverage-tree.md 触达节点数/总节点数 | 对照树中 TC-ID 映射统计触达状态 | 触达率 × 100；树不存在时为 N/A（可选维度，树存在时启用） |

### 视觉一致性评分条件化

| 条件 | 处理方式 |
|------|---------|
| prototype/index.md 存在 | ✅ 以原型清单为基准对比视觉一致性 |
| prototype/index.md 不存在（原型设计 ⏭️ 跳过） | 视觉一致性评分标记为 N/A，总分权重重新分配 |

---

## 测试代码自动生成

playwright-cli 每次交互命令会自动输出对应的 Playwright TypeScript 代码。agent 在测试过程中**被动收集**这些代码片段，组装为完整的测试文件。

### 禁止主动编写测试脚本

**铁律**：agent 禁止在任何阶段主动编写或修改 .spec.ts 测试脚本文件。必须使用 `playwright-cli snapshot → 获取 ref → click/fill ref` 的交互模式。generated-test.spec.ts 仅作为交互成功的副产品被动收集生成。

### 收集流程（可选，通过率≥80%时触发）

```
1. 执行 playwright-cli 交互命令（click, fill, type 等）
   → playwright-cli 自动输出 TypeScript 代码
2. 被动收集所有交互代码片段
3. 当本轮测试通过率 ≥80% 时：
   组装为完整的 Playwright 测试文件:
   import { test, expect } from '@playwright/test';
   test('{test-name}', async ({ page }) => {
     // 收集的交互代码
   });
   保存到 subchanges/{subchange}/test-reports/e2e/generated-test.spec.ts
4. 当本轮测试通过率 <80% 时：
   → 跳过收集，专注修复
```

### 使用方式

- **当前子变更下一轮测试**：如 generated-test.spec.ts 存在，直接运行 `npx playwright test generated-test.spec.ts` 跳过元素侦查
- **归档时**：如文件存在，随变更归档到 `docs/archive/`，不合并到产品级文档 `docs/designs/`
- **后续变更**：从 playwright-cli snapshot 重新生成，不依赖旧的选择器

---

## 网络 Mock 错误测试

使用 playwright-cli 的 route 命令模拟后端异常，覆盖 Error Path 测试场景。

### 命令使用

| 场景 | 命令 | 说明 |
|------|------|------|
| 模拟 API 500 错误 | `playwright-cli route "{api_url}" --status=500` | 模拟后端异常响应 |
| 模拟自定义响应 | `playwright-cli route "{api_url}" --body='{"mock": true}'` | 返回指定 mock 数据 |
| 模拟网络超时 | `playwright-cli route "{api_url}" --abort` | 模拟网络中断 |
| 清除 Mock | `playwright-cli unroute "{api_url}"` | 恢复正常 API 调用 |

### 使用流程

```
1. 设置 Mock: playwright-cli route "/api/users" --status=500
2. 执行触发 API 调用的前端操作
3. 验证前端显示正确的错误提示
4. 截图记录: playwright-cli screenshot
5. 清除 Mock: playwright-cli unroute "/api/users"
```

---

## 浏览器会话管理

### 生命周期

| 阶段 | 命令 | 说明 |
|------|------|------|
| 创建会话 | `playwright-cli open {url}` | 创建浏览器会话，默认 headless 模式 |
| 页面导航 | `playwright-cli goto {url}` | 同一会话内切换页面，保持登录状态和 cookie |
| 关闭会话 | `playwright-cli close` | 测试完成或中断时关闭当前会话 |
| 强制清理 | `playwright-cli kill-all` | 清理所有残留的浏览器进程 |

### 会话管理规则

- 同一子变更内测试多个关联页面时，在同一会话中使用 `goto` 导航，保持登录状态
- 每个子变更测试完成后必须 `close` 当前会话
- 崩溃恢复时先执行 `kill-all` 清理残留，再重新 `open`
- 禁止在非 headless 模式下运行（headless 为默认行为）

---

## 崩溃恢复

> 完整规范参见 `skills/kflow-e2e-test/references/service-lifecycle.md`

服务崩溃时子变更 agent 检测并上报，变更级 agent 执行 playwright-cli kill-all + 编译重启流程，恢复后通知子变更 agent 从断点继续。

---

## 常见陷阱

| 序号 | 陷阱 | 错误做法 | 正确做法 |
|------|------|---------|---------|
| 1 | 过早检查 DOM | 导航后立即 snapshot | 先 `waitForLoadState('networkidle')` 再 snapshot |
| 2 | 忘记关闭浏览器 | 测试完成后不关闭会话 | 每轮测试后 `playwright-cli close` |
| 3 | 硬编码选择器 | 手工编写 CSS/XPath 选择器 | 优先使用 snapshot ref，备用 getByRole/getByTestId |
| 4 | 忽略弹窗 | 不处理 alert/confirm/dialog | `playwright-cli run-code "page.on('dialog', d => d.dismiss())"` |
| 5 | 不捕获控制台 | 不检查浏览器控制台错误 | 每轮测试后 `playwright-cli console` 采集错误 |
| 6 | 会话残留 | 多个子变更间不复用 clean session | 每个子变更测试结束时 `close`，必要时 `kill-all` |
| 7 | 非 Headless 模式 | 使用 `--headed` 标志运行 | 默认 headless 模式；视觉调试时才临时用 `--headed` |
| 8 | 子代理自行换工具 | 模型 API 报错后改用 Bash 直接执行 Playwright | 禁止子代理自行更换测试工具或使用 Bash 替代 playwright-cli；遇到 API 报错应阻塞+上报变更级 agent，等待恢复或 AskUserQuestion 确认 |
| 9 | 忽略元素覆盖树 | element-coverage-tree.md 存在但未加载直接执行测试 | RELOAD 步骤必须加载元素覆盖树（如存在），每轮测试后对照树标记触达状态并输出触达率统计 |

---

## 上下文管理

- **快照优先于截图**：优先使用 `playwright-cli snapshot` 获取文本结构（轻量），仅在需要视觉对比时使用 `playwright-cli screenshot`
- **增量轮次报告**：每轮报告仅记录本轮新增的成败变化，不重复完整用例清单
- **选择性读取**：读取 detailed-design.md 时仅提取当前子变更相关的 NFR 章节

---

## 测试报告格式

### 测试轮次报告

```markdown
# 测试轮次报告：Round {n}

## 基本信息
- **测试时间**: {YYYY-MM-DD HH:MM}
- **测试轮次**: {n}
- **子变更**: {subchange-name}
- **项目类型**: 前后端项目
- **测试用例数**: {总数}
- **通过**: {通过数}
- **失败**: {失败数}
- **跳过**: {跳过数}

## 测试环境

| 环境项 | 值 | 说明 |
|--------|---|------|
| 服务地址 | http://localhost:{port} | 测试服务地址 |
| 浏览器 | Chrome/Firefox | 测试浏览器 |
| 测试账号 | {账号信息} | 测试使用的账号 |

## 测试用例执行结果

| 序号 | 用例ID | 用例描述 | 执行结果 | 备注 |
|------|--------|----------|----------|------|
| 1 | TC-001 | {描述} | ✅ 通过 | - |
| 2 | TC-002 | {描述} | ❌ 失败 | {失败原因} |

## 失败用例详情

### TC-002: {用例描述}

- **预期结果**: {预期}
- **实际结果**: {实际}
- **失败原因**: {原因分析}
- **截图**: {截图路径}

## 健康评分

| 维度 | 分数 | 说明 |
|------|------|------|
| 功能完整性 | {score}/100 | 核心功能通过率 |
| 控制台错误 | {score}/100 | JavaScript 错误数量 |
| 视觉一致性 | {score}/100 | 与原型对比 {或 N/A} |
| 性能响应 | {score}/100 | 页面加载时间 |
| 可访问性 | {score}/100 | ARIA 标签、键盘导航 |
| 元素覆盖率 | {score}/100 | element-coverage-tree 触达率 {或 N/A} |

> 如 prototype/index.md 不存在（原型设计 ⏭️ 跳过），视觉一致性标记为 N/A。
> 如 element-coverage-tree.md 不存在（纯后端项目或旧变更），元素覆盖率标记为 N/A。
```

### 测试总结文档

```markdown
# E2E 测试总结：{change-name} / {subchange-name}

## 基本信息
- **测试完成时间**: {YYYY-MM-DD HH:MM}
- **总轮次**: N（N 由弹性轮次决策确定）
- **项目类型**: 前后端项目
- **测试用例总数**: {N}
- **最终通过率**: {百分比}%

## 各轮次统计

| 轮次 | 用例通过率 | 元素触达率 | 健康评分 | 备注 |
|------|-----------|-----------|---------|------|
| Round 1 | {百分比}% | {百分比}% | {score} | |
| Round 2 | {百分比}% | {百分比}% | {score} | |
| ... | ... | ... | ... | |
| Round N | {百分比}% | {百分比}% | {score} | |

## 元素触达率趋势

| 轮次 | 预期元素数 | 实际触达 | 触达率 | 未触达原因 |
|------|-----------|---------|--------|-----------|
| Round 1 | {N} | {M} | {百分比}% | — |
| Round 2 | {N} | {M} | {百分比}% | bug: {n}, service: {m} |
| ... | ... | ... | ... | ... |
| Round N | {N} | {M} | {百分比}% | — |

> 若趋势线持续低于 100%，SHALL 标记为阻塞（不得释放门控）。
> 若 element-coverage-tree.md 不存在，此章节省略。

## 健康评分汇总

| 维度 | Round 1 | Round 5 | Round N | 趋势 |
|------|---------|---------|----------|------|
| 功能完整性 | {score} | {score} | {score} | {趋势} |
| 控制台错误 | {score} | {score} | {score} | {趋势} |
| 视觉一致性 | {score} | {score} | {score} | {趋势} |
| 性能响应 | {score} | {score} | {score} | {趋势} |
| 可访问性 | {score} | {score} | {score} | {趋势} |
| 元素覆盖率 | {score} | {score} | {score} | {趋势} |

## 结论
- [ ] 所有轮次完成（N/N，N 由弹性轮次决策确定）
- [ ] 最终用例通过率 ≥ 100%
- [ ] 元素触达率 = 100%（树存在时）
- [ ] 健康评分各维度达标
- [ ] E2E 测试阶段通过
```

---

## 元素触达率统计

> **版本**: 3.0.0 新增

每轮 E2E 测试执行完成后，子代理 SHALL 对照元素覆盖树统计实际触达的元素，并在轮次报告中输出触达率。

### 触达率统计流程

```
1. 本轮全部测试用例执行完成后:
   a. 读取 element-coverage-tree.md（来源：有原型时 prototype/ 目录，无原型时 e2e-tests/ 目录）
   b. 解析树中所有 TC-ID 映射，生成「TC-ID → 元素树路径」索引表
2. 对照本轮已执行的测试用例:
   ├── TC-ID 已执行且通过 → 对应树节点标记为 ✅
   └── TC-ID 未执行或执行失败 → 对应树节点标记为 ❌
3. 计算:
   ├── 预期元素数: 树中所有 🎯 状态节点总数 (N)
   ├── 实际触达数: ✅ 节点数 (M)
   └── 触达率 = M / N × 100%
```

### 未触达元素原因分类

| 原因分类 | 标识 | 说明 | 处理方式 |
|---------|------|------|---------|
| 测试用例执行失败 | `bug` | 功能缺陷导致测试不通过 | 进入缺陷修复循环 |
| 服务异常 | `service` | API 不可用或服务崩溃 | 上报变更级 agent |
| 设计遗漏 | `design-gap` | 测试用例设计时遗漏了该元素 | 记录到 skill-suggestion.md，建议回退 design 阶段补充 |

### 元素触达率预期

触达率预期为 100%（每轮都应触达全部元素），与覆盖率语义一致：

```
Round 1:  触达 156/156 → 100% ✅
Round 2:  触达 154/156 → ⚠️ 回归信号
          未触达: [批量删除 button]（批量操作栏未出现，bug）
                  [搜索建议下拉]（/api/suggest 500，service）
...
Round N:  触达 156/156 → 100% ✅ 稳定
```

> **关键**: 多轮测试的目的是发现间歇性 bug 和验证修复不引入回归，不是"分工覆盖元素"。每轮都跑全部用例，每轮都应触达全部元素。

### 元素覆盖树不存在时跳过

当 element-coverage-tree.md 不存在（纯后端项目或旧变更）时，元素触达率统计功能禁用，不影响正常 E2E 测试流程。

---

## 重复制（执行类阶段）

> ⚠ **子代理强制规则**（参见 skills/kflow-e2e-test/references/repetition.md §12）：本阶段（E2E测试）主工作 MUST 通过 Agent 子代理执行，主 Agent 仅负责调度和验收，SHALL NOT 直接执行E2E测试主工作（playwright操作/健康评分/测试代码收集等），无例外。子代理崩溃时轮次级重试（≤3 次），全部失败标记 ⚠️ 阻塞。

E2E 测试阶段属于执行类阶段，采用弹性重复制模式。目标轮次由弹性轮次决策确定（首次执行 10 轮，回退重执行按影响范围分数缩减）。子代理每轮遍历 e2e-tests/ 全部场景，逐条 Playwright 执行。

> 通用规范（复杂度公式、轮次执行细节、prompt 规范、弹性轮次决策、验证门控）参见 `skills/kflow-e2e-test/references/repetition.md`

### 阶段特定参数

- **遍历项**：e2e-tests/ 全部测试场景
- **每轮工作**：逐条 Playwright 执行（snapshot+ref 模式），健康评分数据采集，被动收集交互代码
- **复杂度权重**：接口数 × 1.5 + 场景数 × 2
- **产物要求**：traceability.md「E2E测试」列覆盖率 = 100%，round-{n}.md + summary.md，健康评分各维度已采集

---

## 与其他 Skill 的关系

- **输入来自**：接口单元测试（`kflow-api-test`，子变更级）
- **输出给**：`kflow-bug-fix`（测试失败时）、`kflow-integration-test`（全部子变更通过时）
- **前置阶段**：编码 → 代码审查（`kflow-code-review`）→ 接口单元测试（`kflow-api-test`）
- **后续阶段**：缺陷修复（失败时）或集成测试（通过时）
- **服务管理**：服务生命周期由变更级 agent 独占管理，子变更 agent 为纯消费者
- **项目类型**：仅前后端项目执行，纯后端项目跳过
- **执行模式**：弹性重复制，目标轮次由弹性轮次决策确定（参见 skills/kflow-e2e-test/references/repetition.md §14），复杂度评估仅信息展示，主 Agent 验收闭环

---

## 反馈机制

如果在使用本 Skill 过程中发现问题或有优化建议，请记录到 `docs/skill-suggestion.md` 文件中。
