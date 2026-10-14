# Spec Delta

## MODIFIED Requirements

### Requirement: 用户意图识别

系统 SHALL 根据用户输入关键词按优先级规则自动识别意图并引导对应阶段。支持从用户输入解析变更标识名称（kebab-case），按匹配模式路由到对应处理分支。

#### Scenario: 多关键词优先级裁决

- **WHEN** 用户输入同时命中多个优先级的关键词
- **THEN** 系统按优先级从高到低裁决：修复类 > 测试类 > 归档类 > 流程类 > 创建类
- **AND** 路由到最高优先级匹配的 Skill

#### Scenario: 活跃变更自动路由

- **WHEN** 用户输入为继续类关键词（继续、下一步、接着）且存在活跃变更
- **THEN** 系统忽略其他关键词命中
- **AND** 直接路由到活跃变更的当前阶段

#### Scenario: 明确阶段名称直接匹配

- **WHEN** 用户输入包含明确的 Skill 名称或阶段名称
- **THEN** 系统直接路由到对应 Skill
- **AND** 跳过关键词优先级裁决

#### Scenario: 无法识别意图

- **WHEN** 用户输入无法匹配任何关键词
- **THEN** 系统显示全套流程概览供用户选择

#### Scenario: RESUME 模式识别（新增）

- **WHEN** 用户输入匹配「恢复/resume + 变更名称」（如"恢复 add-user-auth"、"resume add-user-auth"）
- **THEN** 系统提取变更名称并调用 `kflow-resume` Skill
- **AND** 「继续 + 变更名称」SHALL NOT 触发本路由，其由轻量推进路径处理

#### Scenario: 轻量推进模式识别

- **WHEN** 用户输入匹配「继续 + 变更名称」（如"继续 add-user-auth"）
- **THEN** 系统提取变更名称，读取 `docs/changes/{change-name}/.status.md`
- **AND** 按阶段衔接决策表直接调度目标阶段 Skill
- **AND** SHALL NOT 调用 `kflow-resume`
- **AND** SHALL NOT 执行产物完整性二次校验、五问题摘要与服务恢复检测

#### Scenario: 定向指引模式识别（新增）

- **WHEN** 用户输入匹配「指引/引导/guide + 变更名称」（如"指引 add-user-auth"）
- **THEN** 系统提取变更名称并输出针对该变更的定向指引

#### Scenario: 无变更名 RESUME（新增）

- **WHEN** 用户输入为"恢复"或"resume"（无变更名）
- **THEN** 系统自动选择活跃变更并调用 `kflow-resume`
- **AND** 当存在多个活跃变更时，列出所有活跃变更供用户选择

#### Scenario: 无变更名持续推进

- **WHEN** 用户输入为"继续"（无变更名）且存在活跃变更
- **THEN** 存在单个活跃变更时，系统自动选择该变更并执行轻量推进
- **AND** 存在多个活跃变更时，列出所有活跃变更供用户选择

## REMOVED Requirements

### Requirement: NEW CHANGE 创建前指引

**Reason**: 与 `kflow-explore` 的能力完全重复。`kflow-explore` 的 INIT 步骤（变更命名与目录创建）、CLASSIFY 步骤（变更类型分类）、TIER 步骤（档位初判）、CONTEXT 步骤（活跃变更情况）已完整覆盖创建前指引的全部内容，且 `kflow-explore` 的 description 已声明其为 all changes 的入口点。该指引只输出预览、不产生产物、不构成必经关卡，作为流程中继节点只会增加往返开销。

**Migration**: 新变更意图直接由 `kflow-explore` 承接。用户不再经过创建前指引，变更命名、类型分类、档位初判与冲突预检均在 `kflow-explore` 内完成。原先依赖该指引输出的用户，改由 `kflow-explore` 的对应步骤输出。

### Requirement: 变更类型分类

**Reason**: 该能力由 `kflow-explore` 的 CLASSIFY 步骤（判断变更粒度：产品级/功能需求级/功能缺陷级）实现，guide 侧的分类仅用于创建前指引输出，随创建前指引一并移除。

**Migration**: 变更类型分类由 `kflow-explore` 的 CLASSIFY 步骤承担。

### Requirement: 变更名称建议

**Reason**: 该能力由 `kflow-explore` 的 INIT 步骤实现（按变更类型确定命名前缀并生成 kebab-case 名称），guide 侧的建议仅用于创建前指引输出，随创建前指引一并移除。

**Migration**: 变更名称确定由 `kflow-explore` 的 INIT 步骤承担。
