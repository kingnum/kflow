# prototype-playwright-5round-verification Specification (Delta)

## MODIFIED Requirements

### Requirement: 5 轮子代理串行 Playwright 验证

系统 SHALL 在导航合理性验证（6.3 节）完成后，执行 5 轮 Playwright 全覆盖验证，每轮启动一个独立子代理执行全部 5 项检查。系统 SHALL 确保 playwright 运行时环境隔离到 `.kflow-runtime/playwright/`，工作目录固定为项目根目录。

#### Scenario: 每轮子代理启动

- **WHEN** 进入 Playwright 验证（6.4 节）
- **THEN** 系统 SHALL 串行启动 5 个子代理，每轮子代理类型为 `Agent(subagent_type="claude")`
- **AND** 每个子代理 SHALL 使用 `/playwright-cli` 执行全部 5 项 Playwright 检查
- **AND** 子代理工作目录 SHALL 固定为项目根目录
- **AND** 原型 HTML 文件 SHALL 通过 `docs/changes/{change}/prototype/index.html` 相对路径引用
- **AND** 每轮子代理完成后，主 Agent SHALL 读取其报告并修复发现问题
- **AND** 修复完成后 SHALL 启动下一轮子代理

#### Scenario: 5 轮强制执行

- **WHEN** Playwright 验证执行中
- **THEN** 系统 SHALL 完成全部 5 轮子代理验证
- **AND** SHALL NOT 因中间某轮无新问题而提前终止
- **AND** 即使连续多轮无新问题也必须完成全部 5 轮

## ADDED Requirements

### Requirement: playwright 运行时隔离

系统 SHALL 确保 prototype-design VERIFY §6.4 的 Playwright 验证中，playwright npm 包和浏览器二进制使用 `.kflow-runtime/playwright/` 下的安装，不在 `prototype/` 目录下产生任何运行时文件。

#### Scenario: 验证完成后 prototype/ 目录保持纯净

- **WHEN** 全部 5 轮 Playwright 验证完成
- **THEN** `prototype/` 目录 SHALL NOT 包含以下文件/目录：
  - `node_modules/`
  - `package.json`
  - `package-lock.json`
- **AND** 若发现上述文件，SHALL 在 POST_HOOK BROWSER_CLEANUP 中清理

#### Scenario: playwright 安装路径

- **WHEN** Playwright 验证子代理需要使用 playwright
- **THEN** 系统 SHALL 使用 `.kflow-runtime/playwright/node_modules/.bin/playwright` 或 `.kflow-runtime/playwright/node_modules/playwright`
- **AND** SHALL NOT 在 `prototype/` 目录下执行 `npm install playwright`
