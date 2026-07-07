---
stage: 编码
skill: kflow-code
version: 1.0.0
created_at: 2026-05-06
template_for: migrations/migration-log.md
template_description: 数据库迁移记录模板，记录迁移脚本执行情况（序号、文件、子变更、执行时间、执行人、状态、回滚状态）。由 kflow-code 在涉及数据模型变更的编码阶段创建和更新，服务刷新同步点执行迁移时追加记录。
---

# 数据库迁移记录

| 序号 | 迁移文件 | 子变更 | 执行时间 | 执行人 | 状态 | 回滚状态 |
|------|---------|--------|---------|--------|------|---------|
| {序号} | {序号}_{子变更}_{描述}.sql | {subchange} | {YYYY-MM-DD HH:MM} | Agent | {✅ 成功 / ❌ 失败} | {未回滚 / 已回滚} |
