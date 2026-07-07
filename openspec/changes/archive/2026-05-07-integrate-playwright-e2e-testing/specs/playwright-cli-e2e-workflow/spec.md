## ADDED Requirements

### Requirement: E2E 测试使用 playwright-cli snapshot+ref 模式

系统 SHALL 使用 playwright-cli 的 snapshot+ref 系统作为 E2E 测试中元素定位的主要方法。

#### Scenario: 获取页面 snapshot
- **WHEN** agent 导航到目标页面后
- **THEN** agent 执行 `playwright-cli snapshot` 获取带有 ref 编号的元素列表
- **AND** 每个可交互元素被分配唯一 ref（如 e15 [button "登录"]）

#### Scenario: 使用 ref 执行交互
- **WHEN** agent 需要与页面元素交互
- **THEN** agent 使用 snapshot 中获取的 ref 编号（如 `playwright-cli click e15`）
- **AND** 不要求 agent 手工编写 CSS 选择器

#### Scenario: ref 无效时降级
- **WHEN** 页面动态变化导致 ref 失效
- **THEN** agent 重新执行 `playwright-cli snapshot` 获取最新 ref
- **AND** 如 ref 重新获取仍失败，使用 `getByRole()` 或 `getByTestId()` 作为备用定位方式

### Requirement: E2E 测试决策树

系统 SHALL 在 E2E 测试开始前按决策树选择执行路径。

#### Scenario: 静态 HTML 路径
- **WHEN** 被测试页面为静态 HTML 文件（非动态应用）
- **THEN** agent 使用 `playwright-cli open file:///path/to/page.html` 直接打开
- **AND** 无需启动开发服务器

#### Scenario: 动态应用且服务未运行
- **WHEN** 被测试页面为动态应用且服务未在运行
- **THEN** agent 将服务启动请求上报变更级 agent
- **AND** 变更级 agent 使用 with_server.py 启动服务后通知子变更 agent 继续

#### Scenario: 动态应用且服务已运行
- **WHEN** 被测试页面为动态应用且服务已在运行
- **THEN** agent 使用 `playwright-cli open {url}` 连接到已运行的服务
- **AND** 执行 `playwright-cli run-code "async page => { await page.waitForLoadState('networkidle'); }"` 等待页面完全加载
- **AND** 然后执行 snapshot 获取元素 ref

### Requirement: 测试决策树中的网络等待

系统 SHALL 在动态应用测试中，等待 `networkidle` 后再检查 DOM。

#### Scenario: 动态应用先等待后检查
- **WHEN** agent 在动态应用中导航到新页面
- **THEN** agent 必须先执行 `page.waitForLoadState('networkidle')`
- **AND** 然后再执行 `playwright-cli snapshot` 或 `playwright-cli screenshot`

#### Scenario: 静态 HTML 无需等待
- **WHEN** agent 在静态 HTML 页面中导航
- **THEN** agent 直接执行 snapshot，无需等待 networkidle

### Requirement: 健康评分数据采集映射

系统 SHALL 通过 playwright-cli 命令采集健康评分所需的各维度数据。

#### Scenario: 控制台错误采集
- **WHEN** E2E 测试执行完成
- **THEN** agent 执行 `playwright-cli console` 获取控制台日志
- **AND** 统计 [error] 和 [warning] 类型消息数量
- **AND** 每条 error 扣 10 分，每条 warning 扣 5 分

#### Scenario: 性能响应采集
- **WHEN** 健康评分需要性能数据
- **THEN** agent 执行 `playwright-cli --raw eval "JSON.stringify(performance.timing)"`
- **AND** 计算 `loadEventEnd - navigationStart` 作为页面加载时间
- **AND** 加载时间 < 2s 满分，每超 1s 扣 20 分

#### Scenario: 视觉一致性采集
- **WHEN** 健康评分需要视觉数据
- **THEN** agent 执行 `playwright-cli screenshot` 获取页面截图
- **AND** 如 prototype.pen 存在，与原型截图进行对比
- **AND** 如 prototype.pen 不存在，视觉一致性标记为 N/A

#### Scenario: 可访问性采集
- **WHEN** 健康评分需要可访问性数据
- **THEN** agent 执行 `playwright-cli --raw eval` 检测 ARIA 标签和角色属性
- **AND** 统计页面中具有 [role] 或 [aria-*] 属性的元素数量

### Requirement: 测试代码自动生成

系统 SHALL 在 E2E 测试交互过程中收集 playwright-cli 自动生成的 Playwright TypeScript 代码。

#### Scenario: 收集交互代码
- **WHEN** agent 执行 playwright-cli 交互命令（fill, click, type 等）
- **THEN** playwright-cli 自动输出对应的 TypeScript 代码
- **AND** agent 收集所有交互代码片段，组装为完整的 Playwright 测试文件

#### Scenario: 保存生成代码
- **WHEN** 测试轮次完成后
- **THEN** agent 将收集的代码保存到 `subchanges/{subchange}/test-reports/e2e/generated-test.spec.ts`
- **AND** 下一轮测试可直接运行 `npx playwright test generated-test.spec.ts` 跳过元素侦查

#### Scenario: 生成代码仅在子变更级保留
- **WHEN** 变更归档
- **THEN** `generated-test.spec.ts` 随变更归档到 `docs/archive/`
- **AND** 不合并到产品级文档 `docs/designs/`

### Requirement: 网络 Mock 用于错误场景测试

系统 SHALL 支持使用 playwright-cli route 命令模拟后端异常以覆盖 Error Path 测试场景。

#### Scenario: 模拟 API 500 错误
- **WHEN** 测试用例要求验证后端异常时的前端行为
- **THEN** agent 执行 `playwright-cli route "{api_url}" --status=500`
- **AND** 执行触发 API 调用的前端操作
- **AND** 验证前端显示正确的错误提示

#### Scenario: 模拟 API 响应数据
- **WHEN** 测试用例需要特定 API 响应数据
- **THEN** agent 执行 `playwright-cli route "{api_url}" --body='{"mock": true}'`
- **AND** 执行相关前端操作并验证 UI 行为

#### Scenario: 清除 Mock
- **WHEN** 错误场景测试完成
- **THEN** agent 执行 `playwright-cli unroute "{api_url}"` 恢复正常 API 调用

### Requirement: 浏览器会话管理

系统 SHALL 管理 playwright-cli 浏览器会话的完整生命周期。

#### Scenario: 测试前创建会话
- **WHEN** E2E 测试开始
- **THEN** agent 执行 `playwright-cli open {url}` 创建浏览器会话
- **AND** 浏览器以 headless 模式运行（默认行为）

#### Scenario: 测试后关闭会话
- **WHEN** E2E 测试完成或中断
- **THEN** agent 执行 `playwright-cli close` 关闭当前会话
- **AND** 如有残留会话，执行 `playwright-cli kill-all` 强制清理

#### Scenario: 切换测试页面时保持会话
- **WHEN** 同一子变更内需要测试多个关联页面
- **THEN** agent 在同一会话中使用 `playwright-cli goto {url}` 导航
- **AND** 保持登录状态和 cookie 不丢失

### Requirement: 常见陷阱文档

系统 SHALL 在 E2E 测试 Skill 文档中包含常见陷阱和对应的正确做法。

#### Scenario: 陷阱文档内容
- **WHEN** agent 读取 `kflow-e2e-test` Skill 文档
- **THEN** 文档包含「常见陷阱」章节
- **AND** 至少包含：过早检查 DOM / 忘记关闭浏览器 / 硬编码选择器 / 忽略弹窗 / 不捕获控制台 / 会话残留 / 在非 Headless 模式测试

### Requirement: 上下文管理原则

系统 SHALL 在核心机制文档中定义辅助脚本的上下文管理原则。

#### Scenario: 黑盒优先使用脚本
- **WHEN** agent 需要使用辅助脚本（如 with_server.py）
- **THEN** agent 首先执行 `python scripts/{script}.py --help` 了解用法
- **AND** 禁止读取脚本完整源码，除非 `--help` 信息不足且脚本执行报错

#### Scenario: 快照优先于截图
- **WHEN** agent 需要了解页面结构
- **THEN** agent 优先使用 `playwright-cli snapshot` 获取文本快照
- **AND** 仅在需要视觉对比时才使用 `playwright-cli screenshot`
