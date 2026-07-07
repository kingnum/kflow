## ADDED Requirements

### Requirement: 服务指引检测

系统 SHALL 在编码阶段检查 docs/service-guide.md 是否存在。

#### Scenario: 服务指引已存在
- **WHEN** docs/service-guide.md 文件存在
- **THEN** 系统直接读取使用配置

#### Scenario: 服务指引不存在
- **WHEN** docs/service-guide.md 文件不存在
- **THEN** 系统进入生成流程

### Requirement: 项目结构自动分析

系统 SHALL 自动分析项目结构推断服务启动配置。

#### Scenario: 检测项目类型
- **WHEN** 生成服务指引
- **THEN** 系统扫描项目根目录检测项目类型标识文件
- **AND** 根据检测结果推断启动命令

#### Scenario: Java 项目检测
- **WHEN** 存在 pom.xml 或 build.gradle
- **THEN** 系统推断项目类型为 Java/Spring Boot
- **AND** 推断启动命令为 mvn spring-boot:run 或 gradle bootRun

#### Scenario: Node 项目检测
- **WHEN** 存在 package.json 且包含前端框架依赖
- **THEN** 系统推断项目类型为 Node.js
- **AND** 推断启动命令为 npm run dev 或 npm start

### Requirement: 用户交互确认

系统 SHALL 使用 AskUserQuestion 确认或获取服务配置信息。

#### Scenario: 确认启动命令
- **WHEN** 自动分析完成
- **THEN** 系统展示推断结果并请求用户确认

#### Scenario: 获取补充信息
- **WHEN** 用户确认需要补充
- **THEN** 系统询问服务端口、数据库连接、测试账号、健康检查接口等信息

### Requirement: 服务指引生成

系统 SHALL 合并自动检测结果和用户确认信息生成 docs/service-guide.md。

#### Scenario: 生成服务指引文档
- **WHEN** 信息收集完成
- **THEN** 系统生成 docs/service-guide.md 文档
- **AND** 文档包含项目类型、启动命令、编译构建、测试执行、端口环境等配置

### Requirement: 服务指引更新

系统 SHALL 支持在编码过程中更新服务指引。

#### Scenario: 配置错误更新
- **WHEN** 编码过程中发现配置错误
- **THEN** 系统提示用户确认并更新 docs/service-guide.md

#### Scenario: 启动失败分析更新
- **WHEN** 服务启动失败
- **THEN** 系统分析原因并更新配置