# devflow-guide Specification

## Purpose

定义流程指引 Skill 的职责范围：用户意图识别与优先级裁决、活跃变更检测与变更名定位、项目类型判断、流程概览展示、断点恢复与轻量推进的路由分流，以及指引错误记录。

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

### Requirement: 项目类型判断

系统 SHALL 在流程指引时读取项目级项目类型记录，并据此展示适用流程阶段。SHALL NOT 在流程指引中重新扫描判定项目类型。项目级记录的读取优先级与降级规则由 `project-type-detection` 能力定义，本能力 SHALL NOT 重复定义。

#### Scenario: 前后端项目
- **WHEN** 读取到的项目类型为前后端项目
- **THEN** 流程包含原型设计和浏览器自动化测试阶段

#### Scenario: 纯后端项目
- **WHEN** 读取到的项目类型为纯后端项目
- **THEN** 流程跳过原型设计和浏览器自动化测试阶段

#### Scenario: 项目级记录缺失时的指引
- **WHEN** 项目级记录不存在
- **THEN** 系统执行扫描检测并在指引输出中展示检测结果
- **AND** 标注该结果待变更创建阶段确认与补写
- **AND** SHALL NOT 在指引阶段创建或修改任何文件

### Requirement: 流程概览显示

系统 SHALL 提供全套开发流程概览供用户查看，显示正确的阶段数量，并在变更档位为 `轻量` 时按阶段适用性声明标注不适用阶段。

#### Scenario: 显示前后端项目流程
- **WHEN** 用户请求查看流程且项目类型为前后端项目
- **THEN** 系统显示 9 阶段流程：设计探索 → 原型设计(可选) → 详细设计 → 计划 → 编码 → 代码审查 → 接口单元测试 → E2E 测试 → 集成测试(含修复) → 归档
- **AND** 标注原型设计为可选阶段

#### Scenario: 显示纯后端项目流程
- **WHEN** 用户请求查看流程且项目类型为纯后端项目
- **THEN** 系统显示 7 阶段流程：设计探索 → 详细设计 → 计划 → 编码 → 代码审查 → 接口单元测试 → 集成测试(含修复) → 归档
- **AND** 标注跳过原型设计和 E2E 测试

#### Scenario: 轻量档流程概览标注不适用阶段
- **WHEN** 用户请求查看流程 且 当前活跃变更的档位为 `轻量`
- **AND** 该变更已生成阶段适用性声明
- **THEN** 流程概览 SHALL 将声明为不适用的阶段标注为 `⏭️ 不适用`
- **AND** SHALL 显示实际执行的阶段集合
- **AND** SHALL NOT 将不适用阶段计入实际阶段数量

#### Scenario: 轻量档未生成适用性声明时的概览
- **WHEN** 用户请求查看流程 且 当前活跃变更的档位为 `轻量`
- **AND** 该变更尚未生成阶段适用性声明
- **THEN** 流程概览 SHALL 显示完整阶段集合
- **AND** SHALL 标注「接口单元测试与 E2E 测试将在详细设计后按适用性判定」

#### Scenario: 标准档与完整档流程概览
- **WHEN** 用户请求查看流程 且 当前活跃变更的档位为 `标准`，或其 `.status.md` 中读取到历史遗留的 `变更档位 = 完整`
- **THEN** 流程概览 SHALL 按项目类型显示完整阶段集合
- **AND** SHALL NOT 标注本能力引入的档位裁剪
- **AND** SHALL NOT 显示第三档位的专属标注

### Requirement: 指引错误记录

系统 SHALL 将用户纠正的指引错误记录到 skill-suggestion.md。

#### Scenario: 用户纠正指引
- **WHEN** 用户指出指引方向错误或纠正意图识别结果
- **THEN** 系统记录错误场景、用户反馈、改进建议到 docs/skill-suggestion.md

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


### Requirement: kflow-doc-optimize 路由入口

kflow-guide SHALL 支持 `kflow-doc-optimize` Skill 的路由识别和调用，且该路由 SHALL NOT 被视为变更流程的一环。

#### Scenario: 文档优化触发词识别

- **WHEN** 用户输入包含「文档优化 / 文档瘦身 / 拆分文档 / 清理修订记录 / 文档体积」等关键词
- **THEN** kflow-guide SHALL 识别为 `kflow-doc-optimize` 调用意图
- **AND** 路由到该 Skill

#### Scenario: 无活跃变更时仍可路由

- **WHEN** 用户表达文档优化意图且项目中没有活跃变更
- **THEN** kflow-guide SHALL 仍然路由到 `kflow-doc-optimize`
- **AND** SHALL NOT 因缺少活跃变更而中止或要求先创建变更

#### Scenario: 优化意图与流程意图的区分

- **WHEN** 用户输入同时含变更名与优化意图
- **THEN** kflow-guide SHALL 优先按变更名模式路由（「恢复/resume + 变更名」或「继续 + 变更名」）
- **AND** SHALL NOT 将优化意图误判为对应变更的阶段推进

### Requirement: kflow-doc-optimize 纳入流程概览

kflow-guide 的流程概览 SHALL 包含 `kflow-doc-optimize` 作为独立维护工具的说明。

#### Scenario: 流程概览显示文档优化

- **WHEN** 用户请求查看流程概览
- **THEN** 系统 SHALL 显示 `kflow-doc-optimize` 作为独立维护工具
- **AND** 标注为「独立维护（非流程阶段），可随时调用优化存量文档的修订记录与体积」

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
