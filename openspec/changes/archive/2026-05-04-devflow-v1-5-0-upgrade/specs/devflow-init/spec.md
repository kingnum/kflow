## ADDED Requirements

### Requirement: 环境能力发现

系统 SHALL 在项目启动时发现当前上下文可用的 MCP servers 和 Skills。

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

### Requirement: 工具链推荐

系统 SHALL 根据项目类型和可用能力推荐工具链方案。

#### Scenario: 原型设计阶段推荐
- **WHEN** 项目类型为前后端项目
- **THEN** 系统首选推荐 pencil MCP 用于原型设计
- **AND** 若无 pencil MCP，建议用户安装

#### Scenario: E2E 测试阶段推荐
- **WHEN** 项目类型为前后端项目
- **THEN** 系统首选推荐 /playwright-cli skill 用于浏览器自动化测试
- **AND** playwright MCP 作为备选方案
- **AND** kflow-browser-rules 不列入推荐

### Requirement: 组合可行性评估

系统 SHALL 评估推荐工具链的组合可行性。

#### Scenario: 兼容性检查
- **WHEN** 多个工具被推荐用于同一阶段
- **THEN** 系统检查工具间是否存在已知冲突
- **AND** 若有冲突，降级推荐不冲突的组合

#### Scenario: 覆盖度检查
- **WHEN** 完成工具推荐
- **THEN** 系统检查每个阶段是否都有工具支撑
- **AND** 标注覆盖度百分比

### Requirement: 工具链方案输出

系统 SHALL 输出 toolchain.md 到项目级目录。

#### Scenario: 输出工具链配置
- **WHEN** 用户确认工具链方案
- **THEN** 系统在项目根目录创建 docs/toolchain.md
- **AND** 文件包含各阶段推荐工具及优先级
- **AND** 文件包含环境能力扫描结果

#### Scenario: 变更级覆盖
- **WHEN** 特定变更需要使用与项目级不同的工具链
- **THEN** 系统支持在变更目录创建 toolchain.md 覆盖项目级配置
- **AND** 变更级配置优先级高于项目级

### Requirement: 多方案输出

系统 SHALL 在工具链存在多种可行组合时输出多方案供用户选择。

#### Scenario: 输出多方案
- **WHEN** 存在多种可行工具组合
- **THEN** 系统输出方案 A（推荐最佳组合）
- **AND** 输出方案 B（备选降级方案）
- **AND** 输出方案 C（最小必须方案）
- **AND** 每个方案标注覆盖度和风险
