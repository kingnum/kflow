# Tasks: add-kflow-bug-triage

## 1. 模板文件

- [x] 1.1 创建 `docs/designs/templates/changes/{change}/bugs/bugs-index.md` 索引模板文件（含统计节、问题列表表格、分页表格）
- [x] 1.2 创建 `docs/designs/templates/changes/{change}/bugs/bugs-detail.md` 问题详情模板文件（含基本信息、问题描述、诊断结果、解决方案、处理状态、关联节）

## 2. 核心机制文档更新

- [x] 2.1 更新 `docs/designs/core-mechanisms/02-directory-structure.md`：在变更目录结构中新增 `bugs/` 子目录说明，含 index.md 和分页文件规则

## 3. kflow-bug-triage 设计规格（新 Skill）

- [x] 3.1 创建 `docs/designs/skills/kflow-bug-triage.md` 设计规格文档（四层溯源诊断流程、诊断判断标准、路由决策机制、执行流程、门控检查、输入输出、与其他 Skill 的关系、严重度分级）
- [x] 3.2 使用 `/skill-creator` 根据设计规格创建 `.claude/skills/kflow-bug-triage/SKILL.md` 运行时 Skill（设计文档 → SKILL.md 同步）

## 4. kflow-bug-fix 修改（三分法 → 二分法）

- [x] 4.1 修改 `docs/designs/skills/kflow-bug-fix.md`：门控检查去掉"用户描述的缺陷信息"入口；三分法改为二分法（删除设计错误分类和决策树分支）；删除"设计错误回退路由"节；三次尝试升级选项改为引导用户通过 triage 诊断；更新输出产物表（删除 design-error-report 条件产物）；更新与其他 Skill 的关系说明
- [x] 4.2 使用 `/skill-creator` 根据修改后的设计文档同步更新 `.claude/skills/kflow-bug-fix/SKILL.md`（设计文档 → SKILL.md 同步）

## 5. kflow-guide 修改（路由表更新）

- [x] 5.1 修改 `docs/designs/skills/kflow-guide.md`：INTENT 关键词表新增 triage 路由行（反馈/报告问题/报bug/提bug/问题 → kflow-bug-triage，优先级 1）；修改"修复/Bug/缺陷"关键词路由为上下文判断逻辑（有活跃 bug-fix → bug-fix，否则 → triage）；更新优先级排序表
- [x] 5.2 使用 `/skill-creator` 根据修改后的设计文档同步更新 `.claude/skills/kflow-guide/SKILL.md`（设计文档 → SKILL.md 同步）

## 6. Spec 合并

- [x] 6.1 将 `specs/bug-triage-skill/spec.md` 的新增要求合并到 `openspec/specs/` 目录（创建新 spec 目录 `openspec/specs/bug-triage-skill/`）
- [x] 6.2 将 `specs/bug-registration/spec.md` 的新增要求合并到 `openspec/specs/` 目录（创建新 spec 目录 `openspec/specs/bug-registration/`）
- [x] 6.3 将 `specs/defect-root-cause/spec.md` 的 MODIFIED/REMOVED 内容合并到 `openspec/specs/defect-root-cause/spec.md`
- [x] 6.4 将 `specs/intent-priority-rules/spec.md` 的 MODIFIED 内容合并到 `openspec/specs/intent-priority-rules/spec.md`
- [x] 6.5 将 `specs/change-rollback/spec.md` 的 MODIFIED 内容合并到 `openspec/specs/change-rollback/spec.md`

## 7. 文档索引更新

- [x] 7.1 更新 `docs/designs/skills/` 目录的相关索引文件（如有），新增 kflow-bug-triage 条目
- [x] 7.2 更新 `docs/designs/index.md` 或 `docs/designs/overview.md`（如涉及 Skill 清单）

## 8. 验证与审查

- [x] 8.1 使用 `kflow-skills-auditor` 审查新建的 `.claude/skills/kflow-bug-triage/SKILL.md`
- [x] 8.2 使用 `kflow-skills-auditor` 审查修改后的 `.claude/skills/kflow-bug-fix/SKILL.md`
- [x] 8.3 使用 `kflow-skills-auditor` 审查修改后的 `.claude/skills/kflow-guide/SKILL.md`
- [x] 8.4 检查所有修改文件之间的交叉引用一致性（triage 与 bug-fix 的协作描述、guide 与 triage 的路由描述）
