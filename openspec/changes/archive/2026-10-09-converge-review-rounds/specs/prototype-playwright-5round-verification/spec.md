# Spec Delta

## MODIFIED Requirements

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

## ADDED Requirements

### Requirement: Playwright 全覆盖验证轮次（收敛驱动）

系统 SHALL 在审查方式为「子代理自动审查验证」且导航合理性验证（9.1 节）完成后，执行**不少于 1 轮、不超过 5 轮**的 Playwright 全覆盖验证，每轮启动一个独立子代理执行全部 5 项检查；达成收敛终止条件（最近一轮为见证轮）时 SHALL 提前结束。审查方式为「人工审查」时，系统 SHALL NOT 执行 Playwright 验证。系统 SHALL 确保 playwright 运行时环境隔离到 `.kflow-runtime/playwright/`，工作目录固定为项目根目录。

#### Scenario: 前置条件满足时进入 Playwright 验证

- **WHEN** 审查方式为「子代理自动审查验证」且导航合理性验证完成后
- **THEN** 系统 SHALL 进入 Playwright 验证（9.2 节）
- **AND** 系统 SHALL 启动串行子代理验证，轮次不少于 1 轮、不超过 5 轮

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

#### Scenario: 收敛或达上限终止

- **WHEN** Playwright 验证执行中（审查方式为「子代理自动审查验证」）
- **THEN** 最近一轮为零新发现、零修复且报告证明 5 项检查已全量执行的见证轮时，系统 SHALL 终止验证
- **AND** 否则 SHALL 继续下一轮，直至达到轮次上限 5 轮
- **AND** SHALL NOT 因「必须完成全部 5 轮」而继续执行无增量价值的轮次

## REMOVED Requirements

### Requirement: 5 轮子代理串行 Playwright 验证

**Reason**: 轮次模型改为「全局下限 1 + 上限 5 + 收敛终止」后，「5 轮强制执行、不允许提前终止」不再成立。

**Migration**: 由新增的「Playwright 全覆盖验证轮次（收敛驱动）」替代——轮次上限保留为 5，下限为 1，达成见证轮即提前结束。
