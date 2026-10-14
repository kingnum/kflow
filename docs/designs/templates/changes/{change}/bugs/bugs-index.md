---
version: 1.1.0
created_at: 2026-06-16
---

# 问题登记索引：{change-name}

> **版本**: 1.1.0
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
| 快车道缺陷 | {fast_lane_count} |

---

## 二、问题列表

| ID | 标题 | 严重度 | 源头阶段 | 路由目标 | 修复通道 | 状态 | 登记时间 | 详情文件 |
|----|------|--------|---------|---------|---------|------|---------|---------|
| BUG-{NNN} | {标题} | {🔴 阻塞 / 🟡 警告 / 🔵 建议} | {L1/L2/L3/L4} | {explore REVISION/prototype-design REVISION/design REVISION/缺陷修复快车道} | {REVISION/快车道/— 不适用} | {待处理/处理中/已解决/已关闭/已挂起} | {YYYY-MM-DD HH:MM} | [bug-NNN-NNN.md](bug-NNN-NNN.md#bug-nnn) |

**列定义**：

| 列 | 取值 | 说明 |
|----|------|------|
| 源层阶段 | `L1` / `L2` / `L3` / `L4` | 四层溯源诊断的问题源头层级 |
| 路由目标 | `explore REVISION` / `prototype-design REVISION` / `design REVISION` / `缺陷修复快车道` | L1/L2/L3 回退到对应阶段的 REVISION 模式；L4 进入缺陷修复快车道 |
| 修复通道 | `REVISION` / `快车道` / `— 不适用` | **快车道缺陷的区分标记**——`快车道` 表示该缺陷由 L4 结论进入缺陷修复快车道，持有缺陷级状态文件 `bugs/fix/{BUG-ID}/bugfix-status.md`；`— 不适用` 表示尚未路由 |
| 状态 | `待处理` / `处理中` / `已解决` / `已关闭` / `已挂起` | 与 `bug-registration` 的缺陷状态流转一致；快车道缺陷在快速收口校验全部通过后由 `kflow-bug-fix` 更新为 `已解决`，收口校验未通过时保持 `处理中` |

> **状态列的「已解决」写入条件**: 常规路径为 bug-fix 修复验证通过；快车道路径为**定向验证通过且快速收口校验项全部满足**。两条路径的写入动作均只更新本表状态列与对应问题详情，SHALL NOT 修改变更级 `.status.md` 的阶段状态字段。

---

## 三、分页

| 分页文件 | BUG ID 范围 | 问题数 |
|---------|------------|--------|
| [bug-001-020.md](bug-001-020.md) | BUG-001 ~ BUG-020 | {n} |
