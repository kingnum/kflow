## 1. 核心机制文档版本号清理

- [x] 1.1 修改 9 个核心机制文档头部版本号：替换独立版本号为"参见仓库根目录 `VERSION` 文件"
- [x] 1.2 删除 01/02/03/04/06/08 头部 v2.4.0 变更说明（仅 07-agent-model.md 保留）

## 2. Skill 设计文档版本号清理

- [x] 2.1 修改 18 个 Skill 设计文档头部版本号：替换为"参见仓库根目录 `VERSION` 文件"（已标注的 kflow-archive/kflow-init 跳过）

## 3. Skill 实现版本号清理

- [x] 3.1 移除 18 个 SKILL.md frontmatter 中的 `version:` 字段

## 4. 审计规则

- [x] 4.1 `kflow-skills-auditor` SKILL.md 新增检查项：SKILL.md frontmatter 不应包含 `version:` 字段

## 5. 验证

- [x] 5.1 全文搜索确认无残留的独立版本号定义（排除章节级历史标注"vX.X.X 新增"）
