## Purpose

定义流程指引 Skill 的意图识别、活跃变更检测和跨变更冲突检测功能。
## Requirements
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

### Requirement: 项目类型判断

系统 SHALL 在流程指引时判断当前项目类型。

#### Scenario: 前后端项目
- **WHEN** 项目包含前端工程
- **THEN** 流程包含原型设计和浏览器自动化测试阶段

#### Scenario: 纯后端项目
- **WHEN** 项目不包含前端工程
- **THEN** 流程跳过原型设计和浏览器自动化测试阶段

### Requirement: 流程概览显示

系统 SHALL 提供全套开发流程概览供用户查看，显示正确的阶段数量。

#### Scenario: 显示前后端项目流程
- **WHEN** 用户请求查看流程且项目类型为前后端项目
- **THEN** 系统显示 9 阶段流程：设计探索 → 原型设计(可选) → 详细设计 → 计划 → 编码 → 代码审查 → 接口单元测试 → E2E 测试 → 集成测试(含修复) → 归档
- **AND** 标注原型设计为可选阶段

#### Scenario: 显示纯后端项目流程
- **WHEN** 用户请求查看流程且项目类型为纯后端项目
- **THEN** 系统显示 7 阶段流程：设计探索 → 详细设计 → 计划 → 编码 → 代码审查 → 接口单元测试 → 集成测试(含修复) → 归档
- **AND** 标注跳过原型设计和 E2E 测试

### Requirement: 指引错误记录

系统 SHALL 将用户纠正的指引错误记录到 skill-suggestion.md。

#### Scenario: 用户纠正指引
- **WHEN** 用户指出指引方向错误或纠正意图识别结果
- **THEN** 系统记录错误场景、用户反馈、改进建议到 docs/skill-suggestion.md

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

## ADDED by phase-artifact-verification-and-input-alignment

### Requirement: kflow-verify 路由入口

kflow-guide SHALL 支持 kflow-verify Skill 的路由识别和调用。

#### Scenario: 诊断触发词识别
- **WHEN** 用户输入包含「诊断/验证产物/检查产物/产物完整性/输入源检查/verify」等关键词
- **THEN** kflow-guide SHALL 识别为 kflow-verify 调用意图
- **AND** 路由到 kflow-verify Skill

#### Scenario: 带变更名的诊断
- **WHEN** 用户输入「诊断 {change-name}」或「验证 {change-name} 产物」
- **THEN** kflow-guide SHALL 提取变更名称
- **AND** 调用 kflow-verify 对指定变更执行诊断

#### Scenario: 无变更名诊断
- **WHEN** 用户输入「诊断产物」且存在单个活跃变更
- **THEN** kflow-guide SHALL 自动选择该变更
- **AND** 调用 kflow-verify 执行诊断
- **AND** 多个活跃变更时列出供用户选择

### Requirement: kflow-verify 纳入流程概览

kflow-guide 的流程概览 SHALL 包含 kflow-verify 作为独立诊断工具的说明。

#### Scenario: 流程概览显示 verify
- **WHEN** 用户请求查看流程概览
- **THEN** 系统 SHALL 在流程末尾（audit 之前）显示 kflow-verify 作为独立诊断工具
- **AND** 标注为「独立诊断（非流程阶段），可随时调用诊断产物完整性」

## ADDED by design-change-record

### Requirement: 设计修订意图集中检测与分流

kflow-guide SHALL 在 PARSE 阶段检测用户的设计修订意图并分流到对应设计 Skill。

#### Scenario: 检测设计修订触发词

- **WHEN** 用户输入包含"功能设计需调整/原型需调整/详细设计需调整/接口设计要改/修改设计/调整设计/设计要改"等关键词
- **THEN** kflow-guide SHALL 进入 DESIGN_REVISION 模式
- **AND** 解析关键词确定目标设计目录：含"功能"/"需求" → functional-designs，含"原型"/"UI"/"交互" → prototype，含"详细"/"接口"/"架构" → detailed-design

#### Scenario: 分流到目标设计 Skill

- **WHEN** 设计修订目标确定
- **THEN** kflow-guide SHALL 唤醒对应设计 Skill：functional-designs → kflow-explore（REVISION）、prototype → kflow-prototype-design（REVISION）、detailed-design → kflow-design（REVISION）

#### Scenario: 设计修订完成后返回

- **WHEN** 目标设计 Skill 完成修订
- **THEN** kflow-guide SHALL 更新目标目录 index.md 的修订记录（版本号递增 + 追加行）
- **AND** SHALL 更新 .status.md 的设计修订同步追踪表（追加行）
- **AND** SHALL 通过 AskUserQuestion 询问用户：「设计修订完成。是否立即回退并重新执行受影响阶段？」选项：确认回退 / 暂缓继续

### Requirement: DESIGN_REVISION 触发词维护在 kflow-guide

设计修订触发词 SHALL 仅维护在 kflow-guide 的 description 和 SKILL.md 中，不分散到各阶段 Skill。

#### Scenario: 阶段 Skill 不含设计修订触发词

- **WHEN** 任意阶段 Skill 的 SKILL.md description 被编写或更新
- **THEN** description SHALL 仅包含该阶段自身的触发词
- **AND** SHALL NOT 包含指向其他阶段的触发词或设计修订触发词

