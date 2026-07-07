---
status: {in_progress|paused|blocked}
branch: {feature/xxx}
timestamp: {YYYY-MM-DDTHH:MM:SS}
files_modified:
  - {文件路径1}
  - {文件路径2}
checkpoint_type: {manual|auto}
---

# Checkpoint: {YYYY-MM-DD HH:MM:SS}

## 恢复信息

- **变更**: {change-name}
- **子变更**: {subchange-name}（子变更级阶段时填写）
- **当前阶段**: {阶段名称}
- **当前状态**: {in_progress|paused|blocked}
- **Git 分支**: {branch-name}

## 已完成任务

- [x] {任务描述}
- [x] {任务描述}

## 待执行任务

- [ ] {任务描述}
- [ ] {任务描述}

## 修改文件

| 文件 | 变更类型 | 说明 |
|------|---------|------|
| {file} | {新增/修改/删除} | {说明} |

## 注意事项

{需要特别记录的信息，如已知问题、待确认项、中断原因等}
