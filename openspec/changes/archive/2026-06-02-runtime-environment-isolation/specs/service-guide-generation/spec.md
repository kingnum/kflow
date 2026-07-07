# service-guide-generation Specification (Delta)

## ADDED Requirements

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
