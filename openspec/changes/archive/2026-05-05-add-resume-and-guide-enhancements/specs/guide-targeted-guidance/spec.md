# guide-targeted-guidance

## Purpose

定义 kflow-guide 的定向指引增强——支持从用户输入解析变更标识名称，实现定向指引、NEW CHANGE 指引（类型分类+命名建议+冲突预检）和 RESUME 路由。

## ADDED Requirements

### Requirement: 变更标识名称解析

kflow-guide SHALL 从用户输入中解析变更标识名称（kebab-case），并按匹配模式路由到对应处理分支。

#### Scenario: 识别 RESUME 模式

- **WHEN** 用户输入匹配正则 `/继续|恢复|resume\s+([a-z0-9-]+)/`
- **THEN** 系统提取变更名称并路由到 `kflow-resume` Skill
- **AND** 将变更名称作为参数传递给 resume

#### Scenario: 识别定向指引模式

- **WHEN** 用户输入匹配正则 `/指引|引导|guide\s+([a-z0-9-]+)/`
- **THEN** 系统提取变更名称并读取该变更的状态信息
- **AND** 输出针对该变更的定向指引

#### Scenario: 无变更名匹配

- **WHEN** 用户输入不包含变更名称模式
- **THEN** 系统走现有逻辑（扫描所有活跃变更）

### Requirement: NEW CHANGE 指引

kflow-guide SHALL 在用户表达新变更意图时提供创建前指引，不创建任何文件。

#### Scenario: 分类变更类型

- **WHEN** 用户表达新变更意图（如"做一个用户认证功能"）
- **THEN** 系统根据语义分析自动判断变更类型为产品需求、功能需求或功能缺陷
- **AND** 将判断结果告知用户

#### Scenario: 建议变更名称

- **WHEN** 变更类型确定
- **THEN** 系统根据需求描述自动生成 kebab-case 格式的变更名称建议
- **AND** 名称格式为「动词-名词」（如 `add-user-auth`、`fix-login-bug`）

#### Scenario: 跨变更冲突预检

- **WHEN** 变更名称和类型确定
- **THEN** 系统扫描 `docs/changes/` 下所有活跃变更的 functional-design.md 功能点清单
- **AND** 对新变更与已有变更进行功能重叠度语义比对
- **AND** 如有重叠，提示用户可能存在冲突，询问是否继续

#### Scenario: 检测项目类型

- **WHEN** 新变更指引开始
- **THEN** 系统自动检测项目类型（前后端项目或纯后端项目）
- **AND** 根据项目类型确定适用的阶段流程（9 阶段或 7 阶段）

#### Scenario: 输出下一步建议

- **WHEN** 完成类型分类、命名建议、冲突预检
- **THEN** 系统输出下一步操作建议（"请使用 kflow-explore 开始设计探索"）
- **AND** 不创建任何文件或目录

### Requirement: 定向变更指引输出

kflow-guide SHALL 为指定变更输出包含当前状态、进度、可用操作和流程位置的定向指引。

#### Scenario: 输出变更定向指引

- **WHEN** 用户请求对特定变更的指引（"指引 add-user-auth"）
- **THEN** 系统读取该变更的 .status.md 和子变更状态
- **AND** 输出变更基本信息（描述、类型、当前阶段、进度）
- **AND** 输出流程位置图（✅/🔄/⏳ 标注）
- **AND** 输出可用操作建议（当前应使用的 Skill）

#### Scenario: 变更不存在

- **WHEN** 用户指定的变更名称在 `docs/changes/` 下不存在
- **THEN** 系统提示变更不存在并列出当前活跃变更供参考

### Requirement: RESUME 路由

kflow-guide SHALL 在识别到 RESUME 模式时直接调用 `kflow-resume` Skill。

#### Scenario: 有变更名的 resume

- **WHEN** 用户输入"继续 add-user-auth"
- **THEN** 系统解析出变更名 `add-user-auth`
- **AND** 调用 `kflow-resume` 并传入变更名称

#### Scenario: 无变更名的 resume

- **WHEN** 用户输入"继续"且存在单个活跃变更
- **THEN** 系统自动选择该变更并调用 `kflow-resume`

#### Scenario: 无变更名且多个活跃变更

- **WHEN** 用户输入"继续"且存在多个活跃变更
- **THEN** 系统列出所有活跃变更供用户选择
- **AND** 用户选择后调用 `kflow-resume`

### Requirement: 新变更引导完整性

kflow-guide SHALL 确保新变更引导输出的完整性，包含变更类型、建议名称、冲突预检结果、项目类型、适用流程阶段、下一步建议。

#### Scenario: 完整的新变更引导输出

- **WHEN** 用户输入不指定变更名的创建类关键词（"新功能"、"修复Bug"等）
- **THEN** 系统输出包含变更类型、建议名称、冲突预检结果、项目类型、适用流程阶段、下一步建议的完整引导信息
- **AND** 下一步建议明确指向 `kflow-explore`
