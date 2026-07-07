# devflow-guide Delta Spec

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

- **WHEN** 用户输入匹配「继续/恢复/resume + 变更名称」（如"继续 add-user-auth"）
- **THEN** 系统提取变更名称并调用 `kflow-resume` Skill

#### Scenario: 定向指引模式识别（新增）

- **WHEN** 用户输入匹配「指引/引导/guide + 变更名称」（如"指引 add-user-auth"）
- **THEN** 系统提取变更名称并输出针对该变更的定向指引

#### Scenario: 无变更名 RESUME（新增）

- **WHEN** 用户输入"继续"且存在单个活跃变更
- **THEN** 系统自动选择该变更并调用 `kflow-resume`
- **AND** 当存在多个活跃变更时，列出所有活跃变更供用户选择

### Requirement: 活跃变更检测

系统 SHALL 自动扫描 docs/changes/ 目录识别活跃变更。支持指定变更名称时直接定位。

#### Scenario: 无活跃变更

- **WHEN** docs/changes/ 下无未归档变更
- **THEN** 系统引导创建新变更

#### Scenario: 单个活跃变更

- **WHEN** 存在单个未归档变更
- **THEN** 系统自动选择该变更并继续当前阶段

#### Scenario: 多个活跃变更

- **WHEN** 存在多个未归档变更
- **THEN** 系统列出变更供用户选择

#### Scenario: 指定变更名称定位（新增）

- **WHEN** 用户输入包含变更标识名称（如"指引 add-user-auth"）
- **THEN** 系统直接定位到 `docs/changes/add-user-auth/` 目录
- **AND** 读取该变更的 .status.md 输出定向状态信息
- **AND** 无匹配时提示变更不存在并列出活跃变更

## ADDED Requirements

### Requirement: NEW CHANGE 创建前指引

kflow-guide SHALL 在用户表达新变更意图时提供创建前指引，包含类型分类、命名建议、冲突预检和下一步建议，不创建任何文件。

#### Scenario: 新功能变更指引

- **WHEN** 用户输入新功能意图（如"做一个用户认证功能"）
- **THEN** 系统自动判断变更类型为「功能需求」
- **AND** 自动检测项目类型
- **AND** 自动建议 kebab-case 变更名称（如 `add-user-auth`）
- **AND** 执行跨变更冲突预检
- **AND** 输出下一步建议指向 `kflow-explore`

#### Scenario: 缺陷修复变更指引

- **WHEN** 用户输入修复意图（如"修复登录 Bug"）
- **THEN** 系统自动判断变更类型为「功能缺陷」
- **AND** 自动建议 kebab-case 变更名称（如 `fix-login-bug`）
- **AND** 执行跨变更冲突预检
- **AND** 输出下一步建议指向 `kflow-explore`

#### Scenario: 产品需求变更指引

- **WHEN** 用户输入平台级意图（如"搭建电商平台"）
- **THEN** 系统自动判断变更类型为「产品需求」
- **AND** 自动建议变更名称
- **AND** 提醒产品需求可能需要拆分为多个变更
- **AND** 输出下一步建议指向 `kflow-explore`

#### Scenario: 跨变更冲突预检有重叠

- **WHEN** 新变更的功能意图与已有活跃变更的功能点存在语义重叠
- **THEN** 系统提示可能的功能冲突
- **AND** 列出冲突的活跃变更名称和功能点
- **AND** 询问用户是否仍要继续

### Requirement: 变更类型分类

kflow-guide SHALL 根据用户需求描述的语义自动判断变更类型。

#### Scenario: 功能需求分类

- **WHEN** 用户输入包含「添加/新增/实现/开发/做/增加」等关键词
- **THEN** 系统分类为「功能需求」
- **AND** 后续流程为标准流程（渐进式流程中的功能需求级）

#### Scenario: 功能缺陷分类

- **WHEN** 用户输入包含「修复/Bug/问题/报错/异常/修」等关键词
- **THEN** 系统分类为「功能缺陷」
- **AND** 后续流程为简化流程（渐进式流程中的功能缺陷级）

#### Scenario: 产品需求分类

- **WHEN** 用户输入包含「搭建/创建平台/系统/完整/产品」等关键词
- **THEN** 系统分类为「产品需求」
- **AND** 后续流程为完整流程（渐进式流程中的产品级）

### Requirement: 变更名称建议

kflow-guide SHALL 基于用户需求描述自动生成 kebab-case 格式的变更名称建议。

#### Scenario: 新功能命名

- **WHEN** 变更类型为功能需求且用户描述为"添加用户认证功能"
- **THEN** 系统建议变更名称 `add-user-auth`

#### Scenario: 缺陷修复命名

- **WHEN** 变更类型为功能缺陷且用户描述为"修复登录页面报错"
- **THEN** 系统建议变更名称 `fix-login-error`

#### Scenario: 产品需求命名

- **WHEN** 变更类型为产品需求且用户描述为"搭建电商平台"
- **THEN** 系统建议变更名称 `ecommerce-platform`
