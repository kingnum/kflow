## MODIFIED Requirements

### Requirement: 项目类型影响阶段流转

系统 SHALL 根据项目类型调整阶段流转规则。前后端项目的 E2E 测试阶段使用 playwright-cli 作为指定的浏览器自动化工具。

#### Scenario: 前后端项目阶段流转
- **WHEN** 项目类型为前后端项目
- **THEN** 详细设计阶段输出 e2e-tests/ 测试用例
- **AND** E2E 测试阶段（kflow-e2e-test）启用，使用 playwright-cli 执行浏览器自动化
- **AND** playwright-cli 的 snapshot+ref 模式作为主要元素定位方法

#### Scenario: 纯后端项目阶段流转
- **WHEN** 项目类型为纯后端项目
- **THEN** 详细设计阶段不输出 e2e-tests/
- **AND** E2E 测试阶段（kflow-e2e-test）标记为 ⏭️ 跳过
- **AND** 编码阶段接口单元测试作为验收标准
- **AND** 集成测试仅使用 API 调用，不涉及浏览器

## ADDED Requirements

### Requirement: playwright-cli 环境可用性检测

系统 SHALL 在项目类型被判定为前后端项目时，检测 playwright-cli 是否可用。

#### Scenario: playwright-cli 已安装
- **WHEN** `npx playwright-cli --version` 返回版本号
- **THEN** 系统标记 playwright-cli 为可用
- **AND** E2E 测试使用 `npx playwright-cli` 命令

#### Scenario: playwright-cli 未安装
- **WHEN** `npx playwright-cli --version` 命令失败
- **THEN** 系统在 `kflow-init` 阶段自动执行 `npm install -g @playwright/cli@latest`
- **AND** 安装完成后验证版本号
- **AND** 安装失败时提示用户手动安装并阻塞 E2E 测试阶段
