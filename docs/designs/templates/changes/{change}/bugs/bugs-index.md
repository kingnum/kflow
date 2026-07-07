---
version: 1.0.0
created_at: 2026-06-16
---

# 问题登记索引：{change-name}

> **版本**: 1.0.0
> **创建时间**: {YYYY-MM-DD}
> **关联变更**: {change-name}

---

## 一、统计

| 统计项 | 值 |
|--------|---|
| 总问题数 | {total} |
| 🔴 阻塞 | {b_count} |
| 🟡 警告 | {w_count} |
| 🔵 建议 | {s_count} |
| 待处理 | {pending_count} |
| 处理中 | {in_progress_count} |
| 已解决 | {resolved_count} |
| 已关闭 | {closed_count} |
| 已挂起 | {suspended_count} |

---

## 二、问题列表

| ID | 标题 | 严重度 | 源头阶段 | 路由目标 | 状态 | 登记时间 | 详情文件 |
|----|------|--------|---------|---------|------|---------|---------|
| BUG-{NNN} | {标题} | {🔴 阻塞 / 🟡 警告 / 🔵 建议} | {L1/L2/L3/L4} | {explore REVISION/prototype-design REVISION/design REVISION/kflow-bug-fix} | {待处理/处理中/已解决/已关闭/已挂起} | {YYYY-MM-DD HH:MM} | [bug-NNN-NNN.md](bug-NNN-NNN.md#bug-nnn) |

---

## 三、分页

| 分页文件 | BUG ID 范围 | 问题数 |
|---------|------------|--------|
| [bug-001-020.md](bug-001-020.md) | BUG-001 ~ BUG-020 | {n} |
