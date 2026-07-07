## MODIFIED Requirements

### Requirement: 环境能力发现

系统 SHALL 在项目启动时发现当前上下文可用的 MCP servers 和 Skills，并扫描项目画像信息写入 CLAUDE.md。

#### Scenario: 发现已连接 MCP

- **WHEN** 执行 kflow-init
- **THEN** 系统扫描当前会话可用的 MCP 工具前缀（如 mcp__pencil__*）
- **AND** 列出所有可用 MCP servers 及其能力

#### Scenario: 发现已安装 Skills

- **WHEN** 执行 kflow-init
- **THEN** 系统扫描 .claude/skills/ 目录
- **AND** 列出所有已安装 Skills

#### Scenario: 未安装推荐工具

- **WHEN** 发现原型设计或 E2E 测试所需工具缺失
- **THEN** 系统输出安装建议
- **AND** 提示用户安装推荐工具

#### Scenario: 扫描项目画像信息（新增）

- **WHEN** 执行 kflow-init
- **THEN** 系统扫描项目类型、技术栈、目录结构、入口文件、产品文档状态
- **AND** 将扫描结果写入 CLAUDE.md 的「项目画像」section
- **AND** 重新执行时重新扫描并幂等更新

## ADDED Requirements

### Requirement: 项目画像注入

kflow-init SHALL 向 CLAUDE.md 注入「项目画像」section，包含项目类型、技术栈摘要、源码结构、关键入口文件、产品文档状态。使用 marker 机制支持幂等更新。详见 `init-claude-md-injection` spec。

### Requirement: 老项目逆向分析

kflow-init SHALL 在检测到产品文档缺失时，询问用户是否通过代码逆向扫描生成产品级文档草稿。详见 `init-legacy-reverse-analysis` spec。

### Requirement: 变更流程规则注入扩展

kflow-init SHALL 在向 CLAUDE.md 注入「变更流程强制规则」section 时，包含 git commit 相关规则（归档后提交、新变更前提交、首次 init 后提交）。

### Requirement: 首次 init 后 git commit

kflow-init SHALL 在完成首次项目初始化（生成产品文档或 toolchain.md）后执行 git commit。
