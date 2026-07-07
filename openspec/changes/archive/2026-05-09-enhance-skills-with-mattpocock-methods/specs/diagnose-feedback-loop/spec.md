## ADDED Requirements

### Requirement: Feedback Loop 构建

系统 SHALL 在缺陷修复的 DISCOVER 步骤中，按优先级尝试构建可自动运行的缺陷反馈循环。反馈循环 SHALL 是一个快速、确定性、Agent 可运行的 pass/fail 信号，用于验证缺陷是否存在及修复是否有效。

#### Scenario: 自动反馈循环构建优先级

- **WHEN** Agent 进入 kflow-bug-fix 的 DISCOVER 步骤
- **THEN** 按以下优先级尝试构建 feedback loop：1) 失败测试 at nearest seam，2) Curl/HTTP 脚本 against dev server，3) CLI 调用 with fixture 输入 diff snapshot，4) Headless browser 脚本（Playwright/Puppeteer），5) Replay captured trace，6) Throwaway harness（minimal subsystem），7) Property/Fuzz loop（1000 random inputs），8) Bisection harness（git bisect run），9) Differential loop（old vs new version diff），10) HITL bash script（last resort）
- **AND** 优先使用高优先级方法，失败后降级尝试

#### Scenario: Feedback loop 迭代优化

- **WHEN** 一个 feedback loop 已构建
- **THEN** 系统 SHALL 尝试优化 loop 的：速度（缓存 setup、跳过无关 init）、信号清晰度（断言具体症状）、确定性（固定时间、随机种子、文件系统隔离）
- **AND** 2 秒确定性 loop 优于 30 秒不稳定 loop

#### Scenario: 无法构建 Feedback Loop

- **WHEN** 所有 10 种方法均无法构建有效 feedback loop
- **THEN** 系统 SHALL 停止并明确列出已尝试方法
- **AND** 请求用户提供：a) 可复现环境访问权限，b) 捕获的 artifact（HAR 文件、日志 dump、core dump、带时间戳的屏幕录制），c) 添加临时生产 instrumentation 的授权
- **AND** 禁止不通过 feedback loop 直接进入假设阶段

### Requirement: 非确定性缺陷复现率提升

系统 SHALL 对非确定性缺陷提供复现率提升策略，而非追求 100% 复现。

#### Scenario: 非确定性缺陷处理

- **WHEN** 缺陷不能 100% 复现
- **THEN** 系统 SHALL 采用以下策略提升复现率：loop 触发 100×、并行化、增加压力、缩小时间窗口、注入 sleeps
- **AND** 复现率 ≥ 50% 视为可调试
- **AND** 复现率 < 1% 视为不可调试，转向"无法构建 loop"流程

### Requirement: 可证伪多假设生成

系统 SHALL 在复现缺陷后生成 3-5 个可证伪假设，展示给用户后按排序测试。

#### Scenario: 假设生成和展示

- **WHEN** 缺陷已复现
- **THEN** 系统 SHALL 生成 3-5 个排序假设
- **AND** 每个假设 SHALL 使用格式："如果 <X> 是原因，则 <改变 Y> 会让 bug 消失 / <改变 Z> 会让它更严重"
- **AND** 无法给出可证伪预测的假设视为"感觉"，应丢弃或锐化
- **AND** 排序列表 SHALL 展示给用户以获取领域知识重排序

#### Scenario: 单变量假设测试

- **WHEN** 假设列表已确认
- **THEN** 每次 SHALL 仅改变一个变量进行测试
- **AND** 测试结果 SHALL 映射到对应假设的预测

### Requirement: Regression Test at Correct Seam

系统 SHALL 在修复前评估是否存在正确的 seam 用于回归测试，并在不存在正确 seam 时标记为发现本身。

#### Scenario: Seam 正确性评估

- **WHEN** 修复方案已确定
- **THEN** 系统 SHALL 评估：该 seam 是否能锻炼真实 bug 模式
- **AND** 如果 seam 太浅（single-caller 测试无法复制触发 bug 的调用链），SHALL 标记"无正确 seam"作为发现并记录到 fix-report
- **AND** 如果存在正确 seam，SHALL 先写回归测试确认失败，再应用修复，再确认通过

#### Scenario: 原始场景验证

- **WHEN** 修复完成且回归测试通过
- **THEN** 系统 SHALL 重新运行 Phase 1 构建的 feedback loop
- **AND** 确认原始（未最小化）场景不再复现缺陷
