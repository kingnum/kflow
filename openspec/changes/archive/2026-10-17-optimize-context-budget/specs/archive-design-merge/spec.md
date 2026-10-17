# Spec Delta

## MODIFIED Requirements

### Requirement: 变更记录维护

系统 SHALL 在归档时更新 changelog.md，并同时执行产品级文档的修订记录留存边界。

#### Scenario: 追加变更记录
- **WHEN** 归档完成
- **THEN** changelog.md 追加一条记录
- **AND** 记录包含归档日期、变更名称、涉及功能模块、主要变更摘要

#### Scenario: changelog 按年归档
- **WHEN** changelog.md 超过 500 行或年末
- **THEN** 系统将旧记录归档到 changelog-{year}.md
- **AND** changelog.md 仅保留当前年记录

#### Scenario: 合并时裁剪产品级文档的修订记录
- **WHEN** 归档的合并步骤写入任一产品级文档
- **THEN** 该文档头部的修订记录 SHALL 被裁剪至保留最近 3 条
- **AND** 被移出的记录 SHALL 追加到 changelog.md 的对应变更条目下
- **AND** 该文档的当前版本号 SHALL 保持为全部修订的累积结果

#### Scenario: 合并时维护章节索引与触发拆分
- **WHEN** 归档合并改变了某产品级文档的章节结构或体积
- **THEN** 该文档的章节索引 SHALL 被同步更新
- **AND** 体积跨越分片阈值时 SHALL 触发拆分，并在同一步完成引用更新与索引建立

#### Scenario: 合并裁剪不改变实质内容
- **WHEN** 归档的合并步骤执行裁剪
- **THEN** 产品级文档的正文内容 SHALL NOT 被改写或删减
- **AND** 仅修订记录的位置发生变更

#### Scenario: 变更级产物的修订记录同步裁剪
- **WHEN** 变更归档完成
- **THEN** 该变更产物的修订记录超出保留条数的部分 SHALL 移入该变更目录下的 `revision-history.md`
- **AND** 移出记录 SHALL 按产物文件分组组织
