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
