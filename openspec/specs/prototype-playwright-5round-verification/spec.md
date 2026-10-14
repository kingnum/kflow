# prototype-playwright-5round-verification Specification

## Purpose

定义原型设计阶段 VERIFY 步骤中的 Playwright 全覆盖验证（9.2 节），替代原有"最小点击测试"，子代理串行验证，轮次下限 1、**不预设轮数上限**（纯收敛驱动），以见证轮四项判据收敛终止，每轮子代理完整执行全部 5 项检查；适用审查范围冻结与范围外观察降级。该验证仅在审查方式为「子代理自动审查验证」时执行。

## Requirements

### Requirement: Playwright 全覆盖验证轮次（纯收敛驱动）

系统 SHALL 在审查方式为「子代理自动审查验证」且导航合理性验证（9.1 节）完成后，执行**不预设轮数、纯收敛驱动**的 Playwright 全覆盖验证，每轮启动一个独立子代理执行全部 5 项检查；达成收敛终止条件（最近一轮为满足全部四项判据的见证轮）时 SHALL 终止，SHALL NOT 预置轮数上限。审查方式为「人工审查」时，系统 SHALL NOT 执行 Playwright 验证。系统 SHALL 确保 playwright 运行时环境隔离到 `.kflow-runtime/playwright/`，工作目录固定为项目根目录。

#### Scenario: 前置条件满足时进入 Playwright 验证

- **WHEN** 审查方式为「子代理自动审查验证」且导航合理性验证完成后
- **THEN** 系统 SHALL 进入 Playwright 验证（9.2 节）
- **AND** 系统 SHALL 启动串行子代理验证，轮数由收敛决定，SHALL NOT 预置轮数上限

#### Scenario: 人工审查路径跳过 Playwright 验证

- **WHEN** 用户选择的审查方式为「人工审查」
- **THEN** 系统 SHALL NOT 执行 Playwright 验证
- **AND** SHALL NOT 启动 Playwright 验证子代理
- **AND** 系统 SHALL 直接进入用户评审（REVIEW）

#### Scenario: 每轮子代理启动

- **WHEN** 进入 Playwright 验证（9.2 节）
- **THEN** 系统 SHALL 串行启动子代理，每轮子代理类型为 `Agent(subagent_type="claude")`
- **AND** 每个子代理 SHALL 使用 `/playwright-cli` 执行全部 5 项 Playwright 检查
- **AND** 子代理工作目录 SHALL 固定为项目根目录
- **AND** 原型 HTML 文件 SHALL 通过 `docs/designs/prototypes/index.html` 相对路径引用
- **AND** 每轮子代理完成后，主 Agent SHALL 读取其报告并修复发现问题

#### Scenario: 见证轮达成即终止为收敛

- **WHEN** Playwright 验证执行中，最近一轮同时满足零新发现、零修复、报告证明 5 项检查已完成全量遍历、且累积未复核修复清单内全部条目逐项复核通过
- **THEN** 系统 SHALL 终止 Playwright 验证
- **AND** 终止结果 SHALL 记录为 `收敛`

#### Scenario: 未达成见证轮则继续下一轮

- **WHEN** 最近一轮存在新发现、或存在修复、或未证明 5 项检查全量遍历、或累积未复核修复清单内存在未通过复核的条目
- **THEN** 系统 SHALL 继续下一轮
- **AND** SHALL NOT 因轮次数量而终止
- **AND** SHALL NOT 以任何轮数上限作为终止依据

#### Scenario: 不收敛时终止为未收敛

- **WHEN** Playwright 验证命中不收敛判定（无进展 / 振荡 / 安全丝）
- **THEN** 系统 SHALL 终止 Playwright 验证
- **AND** 终止结果 SHALL 记录为 `未收敛`
- **AND** 系统 SHALL 进入非收敛分支升级用户

### Requirement: 每轮 Playwright 验证检查项

每轮 Playwright 验证子代理 SHALL 执行以下全部 5 项检查。

#### Scenario: 页面可达性扫描

- **WHEN** 子代理执行 Playwright 验证
- **THEN** 子代理 SHALL 从 `docs/designs/prototypes/index.html` 出发 BFS 遍历所有 `<a>` 链接
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
- **THEN** 子代理 SHALL 按变更级 `prototype-plan/design-prompt.md` 中定义的业务流程脚本逐条走通
- **AND** 验证每个流程无 JS 错误、无交互断点、无死胡同
- **AND** 输出流程通过清单

### Requirement: Playwright 验证报告内容与存放

每轮子代理 SHALL 输出验证报告到指定路径。

#### Scenario: 报告输出

- **WHEN** 子代理完成一轮 Playwright 验证
- **THEN** 子代理 SHALL 保存报告到 `self-reviews/prototype/playwright-check/round-{N}.md`（N 为收敛实际轮次）
- **AND** 报告 SHALL 包含 5 项检查各自的结果、pageerror 统计、发现问题和建议修复

### Requirement: Playwright 验证适用审查范围冻结与范围外观察

Playwright 全覆盖验证 SHALL 适用审查范围冻结：每轮审查对象集合 SHALL 由主 Agent 在该轮开始时从原型阶段既有产物生成并冻结，审查维度 SHALL 限于该轮固定的 5 项 Playwright 检查。子代理 SHALL NOT 扩大审查对象集合、SHALL NOT 新增检查维度、SHALL NOT 借审查之名新增功能点、字段、章节或分支。子代理在冻结范围之外发现的问题 SHALL 降级为「**范围外观察**」——SHALL NOT 在本轮修复、SHALL NOT 计入本轮新发现数、SHALL NOT 阻断收敛，并 SHALL 写入该轮审查报告的「范围外观察」小节，由主 Agent 在阶段终止时汇总提示。某轮引入范围外新内容时该轮 SHALL NOT 被判定为见证轮。

#### Scenario: 审查对象集合按轮冻结

- **WHEN** 主 Agent 构建某轮 Playwright 验证子代理的 prompt
- **THEN** prompt SHALL 包含由原型阶段既有产物生成的审查对象清单
- **AND** 子代理 SHALL NOT 审查该清单之外的文件、代码或内容
- **AND** 子代理 SHALL NOT 新增审查维度

#### Scenario: 范围外发现降级为范围外观察

- **WHEN** 子代理在冻结范围之外发现问题
- **THEN** 系统 SHALL NOT 修改任何原型产物
- **AND** SHALL NOT 将该问题计入本轮新发现数
- **AND** SHALL NOT 阻断收敛
- **AND** SHALL 将其写入该轮审查报告的「范围外观察」小节

#### Scenario: 范围外发现不计入发现数

- **WHEN** 某轮仅存在范围外发现而无范围内新发现
- **THEN** 本轮的新发现数 SHALL 记为 0
- **AND** 该轮 MAY 构成见证轮（其余三项条件同时满足时）

#### Scenario: 引入范围外新内容的轮次不得判为见证轮

- **WHEN** 某轮的新发现或修改落在冻结的审查对象集合之外
- **THEN** 该轮 SHALL NOT 被判定为见证轮
- **AND** 主 Agent SHALL 拒收该轮
- **AND** SHALL 要求子代理在冻结范围内重新审查该轮

### Requirement: Playwright 不可用降级

当 Playwright 不可用时，系统 SHALL 优先尝试 `.kflow-runtime/playwright/` 安装引导，安装失败后再降级为手动检查。

#### Scenario: 优先隔离安装

- **WHEN** `.kflow-runtime/playwright/node_modules/playwright` 不存在
- **THEN** 系统 SHALL 优先执行安装引导：`cd .kflow-runtime/playwright && npm init -y && npm install playwright && npx playwright install chromium`
- **AND** 安装成功 → 使用隔离安装继续 Playwright 验证

#### Scenario: 降级处理

- **WHEN** Playwright CLI 不可用且 `.kflow-runtime/playwright/` 安装失败
- **THEN** 主 Agent 在子代理 prompt 中指示降级为手动文件分析
- **AND** 在验证报告中记录降级原因
- **AND** 报告标注 "Playwright 不可用 — 降级为手动检查"

### Requirement: playwright 运行时隔离

系统 SHALL 确保 prototype-design VERIFY §9.2 的 Playwright 验证中，playwright npm 包和浏览器二进制使用 `.kflow-runtime/playwright/` 下的安装，不在产品级原型目录 `docs/designs/prototypes/` 下产生任何运行时文件。

#### Scenario: 验证完成后 docs/designs/prototypes/ 目录保持纯净

- **WHEN** Playwright 验证阶段的全部轮次完成
- **THEN** `docs/designs/prototypes/` 目录 SHALL NOT 包含以下文件/目录：
  - `node_modules/`
  - `package.json`
  - `package-lock.json`
- **AND** 若发现上述文件，SHALL 在 POST_HOOK BROWSER_CLEANUP 中清理

#### Scenario: playwright 安装路径

- **WHEN** Playwright 验证子代理需要使用 playwright
- **THEN** 系统 SHALL 使用 `.kflow-runtime/playwright/node_modules/.bin/playwright` 或 `.kflow-runtime/playwright/node_modules/playwright`
- **AND** SHALL NOT 在 `docs/designs/prototypes/` 目录下执行 `npm install playwright`
