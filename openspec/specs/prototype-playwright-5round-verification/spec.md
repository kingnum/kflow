# prototype-playwright-5round-verification Specification

## Purpose

定义原型设计阶段 Playwright 验证的运行时隔离约束：playwright npm 包与浏览器二进制 SHALL 使用 `.kflow-runtime/playwright/` 下的隔离安装，产品级原型目录 `docs/designs/prototypes/` SHALL NOT 产生任何运行时文件。Playwright 全覆盖检查项、单轮合并验证与不可用降级规则见 `prototype-single-round-verify` 能力。

## Requirements

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
