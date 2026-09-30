## RENAMED Requirements

- FROM: `### Requirement: prototype/ 目录纯净性保证`
- TO: `### Requirement: docs/designs/prototypes/ 目录纯净性保证`

## MODIFIED Requirements

### Requirement: playwright 运行时隔离

系统 SHALL 将 playwright npm 包和浏览器二进制安装到 `.kflow-runtime/playwright/`，确保 `/playwright-cli` 调用不发生在 `docs/designs/prototypes/` 或其他设计文档目录下。

#### Scenario: playwright 安装检测

- **WHEN** 🔶 浏览器 类型阶段的 PRE_HOOK 执行
- **THEN** 系统 SHALL 检测 `.kflow-runtime/playwright/node_modules/playwright` 是否存在
- **AND** 若不存在，SHALL 执行 `cd .kflow-runtime/playwright && npm init -y && npm install playwright && npx playwright install chromium`

#### Scenario: playwright 已安装跳过安装

- **WHEN** `.kflow-runtime/playwright/node_modules/playwright` 已存在
- **THEN** 系统 SHALL 跳过 playwright 安装步骤
- **AND** 直接使用已有的 playwright 安装

### Requirement: /playwright-cli 工作目录约束

系统 SHALL 确保 `/playwright-cli` 的调用上下文中，shell 工作目录为项目根目录，HTML 文件通过相对项目根的路径引用。

#### Scenario: prototype-design VERIFY 步骤调用 playwright-cli

- **WHEN** prototype-design VERIFY §6.4 步骤的子代理启动
- **THEN** 系统 SHALL 在子代理 prompt 中明确指示：工作目录固定为项目根目录
- **AND** 原型 HTML 文件通过 `docs/designs/prototypes/index.html` 相对路径引用
- **AND** SHALL NOT 在 `docs/designs/prototypes/` 目录下执行 `npm install` 或 `npx playwright`

#### Scenario: e2e-test 调用 playwright-cli

- **WHEN** e2e-test 阶段使用 `/playwright-cli` 打开应用 URL 或 file:// 路径
- **THEN** 系统 SHALL 确保 playwright 使用 `.kflow-runtime/playwright/` 下的安装
- **AND** shell 工作目录 SHALL 为项目根目录

#### Scenario: 交互式调试调用 playwright-cli

- **WHEN** 用户在原型设计或前端编码过程中使用 `/playwright-cli` 进行问题分析
- **THEN** 系统 SHALL 确保 playwright 使用 `.kflow-runtime/playwright/` 下的安装
- **AND** SHALL NOT 在 `docs/designs/prototypes/` 等设计文档目录下触发 npm install

### Requirement: docs/designs/prototypes/ 目录纯净性保证

系统 SHALL 确保产品级原型目录 `docs/designs/prototypes/` 仅包含设计文档和原型 HTML 文件，不包含任何运行时环境文件。

#### Scenario: 产品级原型目录不包含运行时文件

- **WHEN** prototype-design 阶段 VERIFY 步骤完成
- **THEN** `docs/designs/prototypes/` 目录 SHALL NOT 包含以下文件/目录：
  - `node_modules/`
  - `package.json`
  - `package-lock.json`
- **AND** 若发现上述文件，SHALL 视为违规并清理

#### Scenario: BROWSER_CLEANUP 不依赖产品级原型目录

- **WHEN** POST_HOOK 执行 BROWSER_CLEANUP 步骤
- **THEN** `playwright-cli kill-all` SHALL 从项目根目录执行
- **AND** SHALL NOT 在 `docs/designs/prototypes/` 目录下产生任何残留文件
