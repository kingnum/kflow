## MODIFIED Requirements

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

#### Scenario: 草稿阶段仅 dev 环境完整

- **WHEN** kflow-init 生成 service-guide.md 草稿
- **THEN** dev 环境配置从 L1 扫描填充
- **AND** test/staging/prod 环境标注「待后续补充」
- **AND** kflow-code 阶段补充完整
