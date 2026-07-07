## ADDED Requirements

### Requirement: 用户意图识别

系统 SHALL 根据用户输入关键词自动识别意图并引导对应阶段。

#### Scenario: 识别新变更意图
- **WHEN** 用户输入包含"新功能"、"开始"、"创建"、"开发"等关键词
- **THEN** 系统引导进入设计探索阶段

#### Scenario: 识别测试意图
- **WHEN** 用户输入包含"测试"、"QA"、"验收"、"E2E"等关键词
- **THEN** 系统引导进入浏览器自动化测试阶段

#### Scenario: 识别修复意图
- **WHEN** 用户输入包含"修复"、"Bug"、"缺陷"、"问题"等关键词
- **THEN** 系统引导进入缺陷修复阶段

#### Scenario: 识别状态查看意图
- **WHEN** 用户输入包含"状态"、"进度"、"查看"、"总结"等关键词
- **THEN** 系统调用状态总结 Skill

#### Scenario: 无法识别意图
- **WHEN** 用户输入无法匹配任何关键词
- **THEN** 系统显示全套流程概览供用户选择

### Requirement: 活跃变更检测

系统 SHALL 自动扫描 docs/changes/ 目录识别活跃变更。

#### Scenario: 无活跃变更
- **WHEN** docs/changes/ 下无未归档变更
- **THEN** 系统引导创建新变更

#### Scenario: 单个活跃变更
- **WHEN** 存在单个未归档变更
- **THEN** 系统自动选择该变更并继续当前阶段

#### Scenario: 多个活跃变更
- **WHEN** 存在多个未归档变更
- **THEN** 系统列出变更供用户选择

### Requirement: 项目类型判断

系统 SHALL 在流程指引时判断当前项目类型。

#### Scenario: 前后端项目
- **WHEN** 项目包含前端工程
- **THEN** 流程包含原型设计和浏览器自动化测试阶段

#### Scenario: 纯后端项目
- **WHEN** 项目不包含前端工程
- **THEN** 流程跳过原型设计和浏览器自动化测试阶段

### Requirement: 流程概览显示

系统 SHALL 提供全套开发流程概览供用户查看。

#### Scenario: 显示流程概览
- **WHEN** 用户请求查看流程或意图无法识别
- **THEN** 系统显示阶段顺序图和各阶段 Skill 功能说明

### Requirement: 指引错误记录

系统 SHALL 将用户纠正的指引错误记录到 skill-suggestion.md。

#### Scenario: 用户纠正指引
- **WHEN** 用户指出指引方向错误或纠正意图识别结果
- **THEN** 系统记录错误场景、用户反馈、改进建议到 docs/skill-suggestion.md