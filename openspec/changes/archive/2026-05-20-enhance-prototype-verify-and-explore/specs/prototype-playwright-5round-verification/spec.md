# prototype-playwright-5round-verification Specification

## Purpose

定义原型设计阶段 VERIFY 步骤中升级后的 Playwright 5 轮全覆盖验证（6.4 节），替代原有"最小点击测试"，每轮子代理完整执行全部 5 项检查。

## ADDED Requirements

### Requirement: 5 轮子代理串行 Playwright 验证

系统 SHALL 在导航合理性验证（6.3 节）完成后，执行 5 轮 Playwright 全覆盖验证，每轮启动一个独立子代理执行全部 5 项检查。

#### Scenario: 每轮子代理启动

- **WHEN** 进入 Playwright 验证（6.4 节）
- **THEN** 系统 SHALL 串行启动 5 个子代理，每轮子代理类型为 `Agent(subagent_type="claude")`
- **AND** 每个子代理 SHALL 使用 `/playwright-cli` 执行全部 5 项 Playwright 检查
- **AND** 每轮子代理完成后，主 Agent SHALL 读取其报告并修复发现问题
- **AND** 修复完成后 SHALL 启动下一轮子代理

#### Scenario: 5 轮强制执行

- **WHEN** Playwright 验证执行中
- **THEN** 系统 SHALL 完成全部 5 轮子代理验证
- **AND** SHALL NOT 因中间某轮无新问题而提前终止
- **AND** 即使连续多轮无新问题也必须完成全部 5 轮

### Requirement: 每轮 Playwright 验证检查项

每轮 Playwright 验证子代理 SHALL 执行以下全部 5 项检查。

#### Scenario: 页面可达性扫描

- **WHEN** 子代理执行 Playwright 验证
- **THEN** 子代理 SHALL 从 `prototype/index.html` 出发 BFS 遍历所有 `<a>` 链接
- **AND** 对每个页面验证加载成功（HTTP 200 或无 pageerror）
- **AND** 验证每个页面 `pageerror` 数量 = 0
- **AND** 输出页面可达性矩阵

#### Scenario: 按钮/链接全覆盖点击

- **WHEN** 子代理执行 Playwright 验证
- **THEN** 子代理 SHALL 穷举每个页面的所有 `<button>` 和 `<a>` 元素
- **AND** 逐个点击每个元素，验证有响应（页面跳转/弹窗打开/状态变更/控制台无错误）
- **AND** 对 `disabled` 状态按钮验证其不可点击
- **AND** 输出按钮/链接覆盖清单

#### Scenario: 表单全覆盖

- **WHEN** 子代理执行 Playwright 验证
- **THEN** 子代理 SHALL 对每个表单执行空提交验证（校验提示是否正确显示）
- **AND** 对每个表单执行合法数据提交验证（提交行为是否正确）
- **AND** 对每个表单执行取消/重置操作验证
- **AND** 输出表单覆盖清单

#### Scenario: 弹窗/抽屉全覆盖

- **WHEN** 子代理执行 Playwright 验证
- **THEN** 子代理 SHALL 对每个弹窗/抽屉验证所有打开方式
- **AND** 对每个弹窗/抽屉验证所有关闭方式（确认/取消/点击遮罩/Esc）
- **AND** 对弹窗内的表单和按钮按上述规则验证
- **AND** 输出弹窗覆盖清单

#### Scenario: 端到端业务流程

- **WHEN** 子代理执行 Playwright 验证
- **THEN** 子代理 SHALL 按 `prototype/design-prompt.md` 中定义的业务流程脚本逐条走通
- **AND** 验证每个流程无 JS 错误、无交互断点、无死胡同
- **AND** 输出流程通过清单

### Requirement: Playwright 验证报告

每轮子代理 SHALL 输出验证报告到指定路径。

#### Scenario: 报告输出

- **WHEN** 子代理完成一轮 Playwright 验证
- **THEN** 子代理 SHALL 保存报告到 `prototype/playwright-check-round-{N}.md`（N 为轮次 1-5）
- **AND** 报告 SHALL 包含 5 项检查各自的结果、pageerror 统计、发现问题和建议修复

### Requirement: Playwright 不可用降级

当 Playwright 不可用时，系统 SHALL 降级为手动检查。

#### Scenario: 降级处理

- **WHEN** Playwright CLI 不可用
- **THEN** 主 Agent 在子代理 prompt 中指示降级为手动文件分析
- **AND** 在验证报告中记录降级原因
- **AND** 报告标注 "Playwright 不可用 — 降级为手动检查"
