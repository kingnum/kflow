## Requirements

### Requirement: 数据库迁移目录

系统 SHALL 在变更级目录下创建 migrations/ 目录，存放数据库迁移脚本。

#### Scenario: 迁移目录创建
- **WHEN** 编码阶段涉及数据模型变更
- **THEN** 系统在 docs/changes/{change}/migrations/ 下创建迁移脚本
- **AND** 迁移文件按 {序号}_{子变更}_{描述}.sql 格式命名

### Requirement: 迁移执行与回滚记录

系统 SHALL 维护迁移执行记录和回滚记录。

#### Scenario: 迁移执行记录
- **WHEN** 迁移脚本执行
- **THEN** 在 migration-log.md 中记录序号、迁移文件、所属子变更、执行时间、执行环境、状态

#### Scenario: 迁移回滚记录
- **WHEN** 迁移需要回滚
- **THEN** 在 migration-log.md 的回滚记录区记录迁移序号、回滚时间、原因、影响范围

### Requirement: 编码阶段迁移管理步骤

系统 SHALL 在 TDD 循环的数据层实现中增加迁移管理步骤。

#### Scenario: 数据模型变更时的迁移步骤
- **WHEN** 功能点涉及数据模型变更（新建表/修改字段/新增索引等）
- **THEN** TDD 任务清单中数据层实现步骤包含：编写迁移脚本 → 执行迁移+验证 → 编写回滚脚本
- **AND** 迁移脚本和回滚脚本配对存在
