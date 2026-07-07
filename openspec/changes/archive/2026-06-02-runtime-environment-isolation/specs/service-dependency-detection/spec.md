# service-dependency-detection Specification

## Purpose

定义测试阶段首次运行服务时的 service-guide.md 就绪检测机制，包括存在性检测、内容完整性验证、外部服务依赖连接信息收集与持久化。确保测试阶段 PRE_HOOK 中 READ_SERVICE_GUIDE 步骤在服务启动前完成配置就绪验证，缺失信息通过 AskUserQuestion 收集并持久化，后续会话自动跳过。

## ADDED Requirements

### Requirement: service-guide.md 就绪状态检测

系统 SHALL 在测试阶段（api-test / e2e-test / integration-test）PRE_HOOK 的 READ_SERVICE_GUIDE 步骤中检测 `docs/service-guide.md` 的就绪状态，包括存在性和内容完整性。

#### Scenario: service-guide.md 不存在

- **WHEN** READ_SERVICE_GUIDE 步骤执行时 `docs/service-guide.md` 文件不存在
- **THEN** 系统 SHALL 进入全量配置收集流程
- **AND** 通过 AskUserQuestion 收集项目类型、启动命令、端口、数据库连接等全部信息
- **AND** 基于用户输入和模板生成 `docs/service-guide.md`

#### Scenario: service-guide.md 存在且内容完整

- **WHEN** READ_SERVICE_GUIDE 步骤执行时 `docs/service-guide.md` 存在
- **AND** dev 环境启动命令不为模板占位符
- **AND** dev 环境端口值为有效数字
- **AND** 配置状态标记为「✅ 已就绪」
- **THEN** 系统 SHALL 直接读取使用，跳过配置询问

#### Scenario: service-guide.md 存在但内容不完整

- **WHEN** READ_SERVICE_GUIDE 步骤执行时 `docs/service-guide.md` 存在
- **AND** dev 环境配置存在模板占位符（如 `{命令}`、`{端口}`）或缺失必填值
- **THEN** 系统 SHALL 进入增量配置收集流程
- **AND** 仅询问缺失的配置项，不重复询问已填写的项

### Requirement: 外部服务依赖识别与询问

系统 SHALL 解析 service-guide.md 中「服务依赖」章节，自动识别外部服务依赖，首次检测到新依赖时通过 AskUserQuestion 询问用户提供可访问的连接信息。

#### Scenario: 识别外部服务依赖

- **WHEN** READ_SERVICE_GUIDE 步骤验证 service-guide.md 内容
- **THEN** 系统 SHALL 解析「服务依赖」章节表格
- **AND** 提取所有服务名称和对应 dev 环境连接地址
- **AND** 标记连接地址为非 `localhost`/`127.0.0.1` 且非环境变量占位符（`${...}`）的条目为「需确认的外部服务」

#### Scenario: 首次检测到外部服务依赖

- **WHEN** 系统识别到外部服务依赖
- **AND** 该依赖的连接信息在之前未被确认过
- **THEN** 系统 SHALL 通过 AskUserQuestion 向用户展示依赖列表
- **AND** 询问用户确认或修改连接信息（主机/端口/凭证）
- **AND** 用户确认后 SHALL 将最终连接信息持久化到 service-guide.md

#### Scenario: 外部服务依赖已确认

- **WHEN** 系统识别到外部服务依赖
- **AND** 该依赖的连接信息已被用户确认过（配置状态标记为「✅ 已就绪」）
- **THEN** 系统 SHALL 跳过询问，直接使用已持久化的连接信息

#### Scenario: 无外部服务依赖

- **WHEN** service-guide.md 中无「服务依赖」章节或该章节为空
- **THEN** 系统 SHALL 直接使用已有配置，不触发外部服务询问

### Requirement: 配置状态标记与持久化

系统 SHALL 在 service-guide.md 中使用配置状态标记，区分「已就绪」和「待配置」状态，实现一次配置后续会话自动跳过。

#### Scenario: 首次配置完成后写入状态标记

- **WHEN** 用户完成全部缺失配置项的填写
- **THEN** 系统 SHALL 在 service-guide.md 文件头部写入配置状态标记：`> **配置状态**: ✅ 已就绪 ({确认日期})`
- **AND** SHALL 写入上次检测时间戳：`> **上次检测**: {ISO 8601 时间戳}`

#### Scenario: 后续会话检测到已就绪标记

- **WHEN** READ_SERVICE_GUIDE 步骤执行时
- **AND** service-guide.md 存在且配置状态标记为「✅ 已就绪」
- **AND** 内容完整性验证通过
- **THEN** 系统 SHALL 跳过所有配置询问
- **AND** 直接使用已持久化的配置启动服务

#### Scenario: 用户修改配置后标记过期

- **WHEN** 用户手动修改 service-guide.md 中已被确认的配置项
- **THEN** 系统 SHALL 在下次 READ_SERVICE_GUIDE 时检测到内容变化
- **AND** 将配置状态更新为「⏳ 待确认」
- **AND** 重新触发完整性验证和增量询问

#### Scenario: 用户选择稍后配置

- **WHEN** AskUserQuestion 询问配置信息时
- **AND** 用户选择「稍后配置」
- **THEN** 系统 SHALL 保持配置状态为「⏳ 待配置」
- **AND** SHALL ❌ 阻塞当前测试阶段，不继续执行
- **AND** 输出提示：「服务配置未完成，请补充后重新进入测试阶段」
