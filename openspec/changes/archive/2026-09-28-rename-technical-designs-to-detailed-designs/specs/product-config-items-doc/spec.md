## MODIFIED Requirements

### Requirement: 产品级配置项设计文档

系统 SHALL 维护产品级配置项设计文档 `docs/designs/detailed-designs/config-items.md`，汇总所有环境配置项定义。

#### Scenario: init LEGACY 预生成骨架

- **WHEN** kflow-init LEGACY 模式执行逆向分析
- **THEN** 系统从 L1 配置文件扫描中提取已知配置项
- **AND** 写入 `docs/designs/detailed-designs/config-items.md` 草稿
- **AND** 标注"由 AI 逆向分析生成，待人工审核"

#### Scenario: archive 合并更新

- **WHEN** 归档变更时 detailed-design.md 包含配置项设计章节
- **THEN** 系统将变更级配置项合并到产品级 config-items.md
- **AND** 已存在的配置项更新来源标注，不存在的追加
