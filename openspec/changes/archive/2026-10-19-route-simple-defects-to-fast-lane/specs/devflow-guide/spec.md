# Spec Delta

## MODIFIED Requirements

### Requirement: 活跃变更检测

系统 SHALL 自动扫描 docs/changes/ 目录识别活跃变更。支持指定变更名称时直接定位。当用户意图为缺陷修复时，活跃变更数量 SHALL NOT 成为路由前置条件。

#### Scenario: 无活跃变更

- **WHEN** docs/changes/ 下无未归档变更
- **THEN** 系统 SHALL 按用户意图分流：修复意图（修复、Bug、缺陷）路由到 `kflow-bug-triage`；非修复意图引导创建新变更
- **AND** 修复意图 SHALL NOT 被引导创建新变更

#### Scenario: 单个活跃变更

- **WHEN** 存在单个未归档变更 且 用户意图不是缺陷修复
- **THEN** 系统自动选择该变更并继续当前阶段

#### Scenario: 多个活跃变更

- **WHEN** 存在多个未归档变更 且 用户意图不是缺陷修复
- **THEN** 系统列出变更供用户选择

#### Scenario: 指定变更名称定位（新增）

- **WHEN** 用户输入包含变更标识名称（如“指引 add-user-auth”）
- **THEN** 系统直接定位到 `docs/changes/add-user-auth/` 目录
- **AND** 读取该变更的 .status.md 输出定向状态信息
- **AND** 无匹配时提示变更不存在并列出活跃变更

## ADDED Requirements

### Requirement: 缺陷修复意图路由

系统 SHALL 将修复类意图直接路由到缺陷分诊 Skill，SHALL NOT 以活跃变更数量作为是否创建变更的判定依据。

#### Scenario: 修复意图无活跃变更

- **WHEN** 用户输入命中修复类关键词且不存在活跃 bug-fix
- **THEN** 系统 SHALL 路由到 `kflow-bug-triage`
- **AND** SHALL NOT 路由到 `kflow-explore` 创建变更

#### Scenario: 修复意图有活跃变更

- **WHEN** 用户输入命中修复类关键词且存在活跃变更
- **THEN** 系统 SHALL 路由到 `kflow-bug-triage`
- **AND** triage SHALL 判定缺陷工作区（项目级 / 变更级）
- **AND** SHALL NOT 因存在活跃变更而直接创建新变更

#### Scenario: 流程概览展示缺陷快车道

- **WHEN** 用户请求查看流程概览
- **THEN** 系统 SHALL 显示“缺陷修复快车道”作为独立于变更阶段的路径
- **AND** SHALL 说明简单缺陷无需创建变更
