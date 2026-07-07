## Context

版本号当前分布在 5 层：VERSION 文件（0.10.0）、核心机制文档头部（2.1.0-2.2.0）、Skill 设计文档头部（1.0.0-3.0.0）、Skill 实现 SKILL.md frontmatter（1.0.0-1.2.0）、章节级变更标注（"v1.8.0 新增"等）。其中 kflow-archive/kflow-init 设计文档已标注"参见 VERSION 文件"，但其他文件各自独立。v2.4.0 变更说明被复制到 6 个不相关文件中。

## Goals / Non-Goals

**Goals:**
- 建立 VERSION 文件为唯一版本源，所有其他位置删除或替换为引用
- kflow-skills-auditor 新增检查项阻止未来再出现独立版本号
- 清理 v2.4.0 误置变更说明

**Non-Goals:**
- 不改变版本号本身（不触发版本自增）
- 不改变打包脚本（已使用 VERSION 文件）
- 不删除章节级变更历史标注（"v1.8.0 新增"是历史注释，不是版本定义）

## Decisions

### D1: 版本引用格式

设计文档和核心机制文档头部统一为：
```markdown
> **版本**: 参见仓库根目录 `VERSION` 文件
```

### D2: SKILL.md frontmatter 处理

移除 `version:` 字段，不替换。frontmatter 仅保留 `name:` 和 `description:`。

### D3: v2.4.0 变更说明清理

| 文件 | 操作 |
|------|------|
| 07-agent-model.md | 保留（v2.4.0 确实修改了此文件的执行模型） |
| 01-project-types.md | 删除 |
| 02-directory-structure.md | 删除 |
| 03-status-and-tasks.md | 删除 |
| 04-gates-and-transitions.md | 删除 |
| 06-recovery.md | 删除 |
| 08-governance.md | 删除 |

### D4: 审计规则

kflow-skills-auditor 新增检查项：
- 如果 SKILL.md frontmatter 包含 `version:` 字段 → WARN
- 建议信息："版本号由 VERSION 文件统一管理，SKILL.md 不应包含独立版本号"

## Risks / Trade-offs

| 风险 | 缓解 |
|------|------|
| 移除版本号后无法快速识别文件对应的产品版本 | 归档时 CHANGELOG 已记录版本与变更的对应关系 |
| 章节级历史标注（"v1.8.0 新增"）可能与 VERSION 文件版本混淆 | 明确区分：章节标注是历史注释（不改），头部版本是产品版本（删除） |
