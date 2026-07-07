## ADDED Requirements

### Requirement: 功能设计索引包含修订记录不重复

functional-designs/index.md SHALL 仅包含一张修订记录表，不再包含独立的需求变更记录表。

#### Scenario: 合并后的修订记录表

- **WHEN** functional-designs/index.md 被创建或修订
- **THEN** SHALL 仅包含"八、修订记录"节
- **AND** 表 SHALL 包含列：版本、日期、修订类型、修订内容、影响功能点、触发阶段
- **AND** 修订类型枚举 SHALL 包含"需求变更"以区分需求层面的变更

#### Scenario: 不再包含独立的需求变更记录

- **WHEN** functional-designs/index.md 被生成
- **THEN** SHALL NOT 包含独立的"需求变更记录"节
- **AND** 原需求变更记录的内容 SHALL 纳入统一修订记录表

## MODIFIED Requirements

无现有需求被修改。
