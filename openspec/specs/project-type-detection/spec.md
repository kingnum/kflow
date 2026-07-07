# project-type-detection Specification

## Purpose
Defines project type detection (frontend+backend vs backend-only) and the associated phase flow differences including playwright-cli integration.

## Requirements
### Requirement: 项目类型检测

系统 SHALL 在设计探索阶段自动检测项目类型。

#### Scenario: 检测前端工程标识
- **WHEN** 设计探索阶段执行
- **THEN** 系统扫描项目根目录检测前端工程标识
- **AND** 标识包括：package.json 前端框架依赖、.vue/.tsx/.jsx 文件、vite.config/webpack.config 构建配置

#### Scenario: 判断为前后端项目
- **WHEN** 检测到前端工程标识存在
- **THEN** 系统标记项目类型为"前后端项目"
- **AND** 流程包含原型设计和浏览器自动化测试阶段

#### Scenario: 判断为纯后端项目
- **WHEN** 未检测到前端工程标识
- **THEN** 系统标记项目类型为"纯后端项目"
- **AND** 流程跳过原型设计和浏览器自动化测试阶段

### Requirement: 项目类型记录

系统 SHALL 将项目类型检测结果记录到 design-explore.md。

#### Scenario: 记录项目类型
- **WHEN** 项目类型检测完成
- **THEN** design-explore.md 包含"项目类型: {前后端项目|纯后端项目}"字段

### Requirement: 项目类型确认

系统 SHALL 将检测结果展示给用户确认。

#### Scenario: 用户确认项目类型
- **WHEN** 项目类型检测完成
- **THEN** 系统使用 AskUserQuestion 展示检测结果
- **AND** 用户可确认或手动修正项目类型

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
