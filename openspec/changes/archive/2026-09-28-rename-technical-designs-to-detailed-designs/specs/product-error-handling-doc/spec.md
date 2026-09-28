## MODIFIED Requirements

### Requirement: 产品级错误处理设计文档

系统 SHALL 维护产品级错误处理设计文档 `docs/designs/detailed-designs/error-handling.md`，汇总所有错误场景和处理策略。

#### Scenario: init LEGACY 预生成骨架

- **WHEN** kflow-init LEGACY 模式执行逆向分析
- **THEN** 系统从 L3 源码语义扫描中提取已有错误码和异常处理
- **AND** 写入 `docs/designs/detailed-designs/error-handling.md` 草稿
- **AND** 标注"由 AI 逆向分析生成，待人工审核"

#### Scenario: archive 合并更新

- **WHEN** 归档变更时 detailed-design.md 包含错误处理设计章节
- **THEN** 系统将变更级错误处理合并到产品级 error-handling.md
- **AND** 已存在的错误场景更新来源标注，不存在的追加
