## Why

当前版本定义分散在多个位置：VERSION 文件（产品版本 0.10.0）、核心机制文档（各自独立版本 2.1.0-2.2.0）、Skill 设计文档（各自独立版本 1.0.0-3.0.0）、Skill 实现 SKILL.md（frontmatter 版本 1.0.0-1.2.0）。部分文件（kflow-archive/kflow-init 设计文档）已标注"参见 VERSION 文件"，但其他文件各自为政。v2.4.0 变更说明被复制到 6 个不相关的核心机制文件头部。版本号混乱导致维护困难、同步遗漏。

## What Changes

- 统一所有版本定义到 `VERSION` 文件为唯一产品版本源
- 移除核心机制文档头部的独立版本号，替换为"版本: 参见 VERSION 文件"
- 移除 Skill 设计文档头部的独立版本号，替换为"版本: 参见 VERSION 文件"
- 移除 Skill 实现 SKILL.md frontmatter 中的 `version:` 字段
- 清理 v2.4.0 变更说明在 6 个不相关核心机制文件中的误置复制，仅保留在实际发生变更的 `07-agent-model.md` 中
- `kflow-skills-auditor` 新增检查项：SKILL.md 不应包含 `version:` 字段

## Capabilities

### New Capabilities
- `version-field-removal-rule`: kflow-skills-auditor 新增审计规则——SKILL.md frontmatter 中不应包含 version 字段

### Modified Capabilities
- `unified-version`: 扩展统一版本管理范围，从仅 SKILL.md 扩展到覆盖所有设计文档和核心机制文档
- `skill-packaging`: 打包脚本版本号读取逻辑不受影响（已使用 VERSION 文件）

## Impact

- **VERSION 文件**: 不变（已是唯一产品版本源）
- **核心机制文档 (9 文件)**: 移除头部独立版本号，清理 v2.4.0 误置变更说明
- **Skill 设计文档 (18 文件)**: 移除头部独立版本号
- **Skill 实现 SKILL.md (18 文件)**: 移除 frontmatter version 字段
- **kflow-skills-auditor**: 新增 version 字段检查规则
- **scripts/package-skills.sh**: 不受影响（已读取 VERSION 文件）
