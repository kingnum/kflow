## Requirements

### Requirement: 服务指引检测

系统 SHALL 在 kflow-init 和 kflow-code 阶段检查 `docs/service-guide.md` 是否存在。

#### Scenario: 服务指引已存在
- **WHEN** docs/service-guide.md 文件存在
- **THEN** 系统直接读取使用配置

#### Scenario: 服务指引不存在
- **WHEN** docs/service-guide.md 文件不存在
- **THEN** 若当前为 kflow-init 老项目逆向分析，系统生成初步草稿
- **AND** 若当前为 kflow-code 编码阶段，系统进入完整生成流程

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

系统 SHALL 合并自动检测结果和用户确认信息生成 `docs/service-guide.md`。

#### Scenario: kflow-init 生成初步草稿
- **WHEN** kflow-init 老项目逆向分析触发 service-guide.md 生成
- **THEN** 系统基于 L1 配置扫描生成 dev 环境初步配置
- **AND** test/staging/prod 环境标注「待后续补充」
- **AND** 文档标注「由 AI 逆向分析生成，待人工审核」

#### Scenario: kflow-code 生成/补充完整文档
- **WHEN** kflow-code 编码阶段检测到 service-guide.md 不存在或为草稿
- **THEN** 系统进入完整生成流程（自动分析 + 用户交互确认）
- **AND** 补充 test/staging/prod 多环境配置
- **AND** 替换草稿标记为正式内容

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

### Requirement: 外部服务依赖识别与询问

系统 SHALL 在 kflow-code 编码阶段生成 service-guide.md 时，自动检测项目的外部服务依赖，并通过 AskUserQuestion 询问用户提供可访问的连接信息。

#### Scenario: 自动识别外部服务依赖

- **WHEN** kflow-code 分析项目结构生成 service-guide.md
- **THEN** 系统 SHALL 扫描项目配置文件（如 application.yml、pom.xml、package.json）识别外部服务依赖
- **AND** 识别内容包括：数据库（MySQL/PostgreSQL/...）、缓存（Redis/...）、消息队列（RabbitMQ/Kafka/...）、对象存储（MinIO/S3/...）
- **AND** 在 service-guide.md 中生成「服务依赖」章节表格

#### Scenario: 询问外部服务连接信息

- **WHEN** 系统识别到至少一个外部服务依赖
- **THEN** 系统 SHALL 通过 AskUserQuestion 向用户展示识别到的依赖列表
- **AND** 逐项询问连接信息（dev 环境主机地址、端口、数据库名/实例名）
- **AND** 用户提供的连接信息 SHALL 写入 service-guide.md「服务依赖」章节

#### Scenario: 无外部服务依赖

- **WHEN** 项目无外部服务依赖（如纯静态前端项目或单进程应用）
- **THEN** 系统 SHALL 在 service-guide.md 中标注「无外部服务依赖」
- **AND** 不触发外部服务连接信息询问

### Requirement: 配置状态标记写入

系统 SHALL 在 kflow-code 完成 service-guide.md 生成后，写入配置状态标记。

#### Scenario: 用户确认后写入已就绪标记

- **WHEN** kflow-code 完成 service-guide.md 生成且用户确认所有配置正确
- **THEN** 系统 SHALL 在 service-guide.md 文件头部写入配置状态标记：`> **配置状态**: ✅ 已就绪`
- **AND** SHALL 写入生成来源标记（区别于 kflow-init 的草稿标记）

#### Scenario: 用户部分确认写入待配置标记

- **WHEN** kflow-code 生成 service-guide.md 过程中用户选择跳过部分配置项
- **THEN** 系统 SHALL 写入配置状态标记：`> **配置状态**: ⏳ 待配置`
- **AND** 标注跳过的配置项，供后续测试阶段 PRE_HOOK 补全