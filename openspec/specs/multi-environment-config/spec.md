## Requirements

### Requirement: 多环境配置支持

系统 SHALL 在 service-guide.md 中支持多环境配置，区分 dev/test/staging/prod 环境。

#### Scenario: 环境概览
- **WHEN** service-guide.md 生成或更新
- **THEN** 包含四环境（dev/test/staging/prod）的概览表
- **AND** 每环境记录用途、数据库类型、服务地址

#### Scenario: 环境特定启动命令
- **WHEN** 不同环境需要不同配置
- **THEN** 每环境记录独立的启动命令（如 `-Dspring.profiles.active=dev`）
- **AND** 配置差异在 service-guide.md 中可见

### Requirement: 草稿阶段仅 dev 环境完整

- **WHEN** kflow-init 生成 service-guide.md 草稿
- **THEN** dev 环境配置从 L1 扫描填充
- **AND** test/staging/prod 环境标注「待后续补充」
- **AND** kflow-code 阶段补充完整

### Requirement: 敏感配置保护

系统 SHALL 禁止在 service-guide.md 中写入明文密码和密钥。

#### Scenario: 敏感信息使用环境变量
- **WHEN** 需要记录数据库密码、API密钥等敏感信息
- **THEN** 使用环境变量占位符（如 `${DB_PASSWORD}`）
- **AND** 实际值存储在 .env 文件中（加入 .gitignore）

#### Scenario: 明文检测
- **WHEN** service-guide.md 生成
- **THEN** 系统检测是否包含疑似明文密码
- **AND** 如检测到，警告并建议改用环境变量

### Requirement: 服务启动前环境验证

系统 SHALL 在编码和测试阶段启动服务前验证目标环境可用。

#### Scenario: 环境准备验证
- **WHEN** kflow-code 或 kflow-e2e-qa 准备启动服务
- **THEN** 检查目标环境配置是否存在
- **AND** 检查数据库是否可连接
- **AND** 检查端口是否可用
- **AND** 全部通过后才启动服务
