---
template_for: .claude/skills/{skill-name}/SKILL.md
template_type: 阶段 Skill 通用模板
version: 1.0.0
created_at: 2026-05-28
---

# {skill-name}（{阶段中文名}）

> **版本**: 1.0.0
> **阶段**: {阶段名称}
> **阶段钩子引用**: `各 skill 的 references/hooks.md`（{需要服务/不需要服务}，RELOAD: {RELOAD 清单}）

---

## 基本信息

```yaml
name: {skill-name}
description: {阶段中文名} - {简要描述}。阶段钩子引用 `各 skill 的 references/hooks.md`（{需要服务/不需要服务}，RELOAD: {RELOAD 清单}）。
license: MIT
triggers:
  - {中文触发词1}
  - {中文触发词2}
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Agent
  - AskUserQuestion
```

---

## 输入要求

| 产物 | 图例 | 说明 |
|------|------|------|
| {输入产物1} | ✅ 必须 | {说明} |
| {输入产物2} | 🔶 条件 | {说明} |

---

## 输出产物

| 产物 | 文件 | 模板 | 图例 | 内容要求 |
|------|------|------|------|---------|
| {输出产物1} | {文件路径} | {模板路径} | ✅ 必须 | {内容要求} |

---

## 执行流程

```
{阶段名称}阶段流程:

┌─────────────────────────────────────────────────────────────┐
│                      {WORKFLOW NAME}                         │
├─────────────────────────────────────────────────────────────┤
│  1. PRE_HOOK  → 引用 `各 skill 的 references/hooks.md` {阶段} 阶段 PRE_HOOK  │
│  │   ├── CHECK_STATE → 验证前置阶段状态                       │
│  │   ├── RELOAD → 重读 {RELOAD 清单}                          │
│  │   └── {服务相关步骤：不需要服务 / CHECK_PORTS→STOP_STALE→COMPILE→MIGRATE→START→HEALTH_CHECK} │
│  2. {核心步骤1} → {描述}                                      │
│  3. {核心步骤2} → {描述}                                      │
│  4. {核心步骤3} → {描述}                                      │
│  N. POST_HOOK → 引用 `各 skill 的 references/hooks.md` {阶段} 阶段 POST_HOOK │
│  │   ├── {服务相关步骤：不需要服务→跳过 / STOP_SERVICE→VERIFY_STOP→BROWSER_CLEANUP} │
│  │   └── UPDATE_STATE → 更新 .status.md                       │
└─────────────────────────────────────────────────────────────┘
```

---

## 与其他 Skill 的关系

- **前置阶段**：{前置 Skill}
- **后置阶段**：{后置 Skill}
- **触发来源**：{调用来源}
- **输出给**：{输出目标}

---

## 反馈机制

如果在使用本 Skill 过程中发现问题或有优化建议，请记录到 `docs/skill-suggestion.md` 文件中。
