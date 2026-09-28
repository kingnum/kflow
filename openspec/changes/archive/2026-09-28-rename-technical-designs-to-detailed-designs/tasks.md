# Tasks

## 1. 模板目录重命名

- [x] 1.1 用 `git mv` 将 `docs/designs/templates/design-templates/technical-designs/` 重命名为 `docs/designs/templates/design-templates/detailed-designs/`，验证 `git status` 显示 rename 且 6 个模板文件（architecture/data-model/api-catalog/nfr-baseline/config-items/error-handling.md）均在新路径存在

## 2. kflow-archive 运行时 Skill 同步（设计文档 → SKILL.md 同步）

- [x] 2.1 更新 `skills/kflow-archive/SKILL.md` 中 10 处 `technical-designs` → `detailed-designs`，及关联中文术语「技术设计」→「详细设计」（输入/输出产物表、执行流程图、设计合并流程各步骤），验证 Grep `technical-designs` 在该文件无命中
- [x] 2.2 在 `skills/kflow-archive/SKILL.md` 设计合并流程中补充旧目录 `docs/designs/technical-designs/` 的兼容读取与 `git mv` 迁移提示（对应 doc-naming-convention「旧命名兼容期」新增 Scenario），验证该文件包含兼容读取描述

## 3. kflow-init 运行时 Skill 同步（设计文档 → SKILL.md 同步）

- [x] 3.1 更新 `skills/kflow-init/SKILL.md` 中 6 处 `technical-designs` → `detailed-designs`，及关联中文术语（项目画像字段、产品文档状态表、LEGACY 逆向分析生成表），验证 Grep `technical-designs` 在该文件无命中
- [x] 3.2 在 `skills/kflow-init/SKILL.md` LEGACY 逆向分析中补充旧目录 `docs/designs/technical-designs/` 的兼容读取与迁移提示，验证该文件包含兼容读取描述

## 4. 设计文档同步

- [x] 4.1 更新 `docs/designs/core-mechanisms/02-directory-structure.md`、`docs/designs/index.md`、`docs/designs/overview.md` 中的 `technical-designs` 路径与「技术设计」术语，验证 Grep 在这些文件无 `technical-designs` 命中
- [x] 4.2 更新 `docs/designs/skills/kflow-archive.md`、`docs/designs/skills/kflow-init.md`、`docs/designs/examples/product-design-index.md`、`docs/designs/templates/index.md` 中的路径与术语，验证 Grep 在这些文件无 `technical-designs` 命中

## 5. 集成验证

- [x] 5.1 运行 `openspec validate --change rename-technical-designs-to-detailed-designs`，验证 delta 无 RENAMED/MODIFIED 标题不匹配或 Scenario 格式错误
- [x] 5.2 全库 Grep `technical-designs`，验证仅 `openspec/changes/archive/` 归档历史残留、所有现行文件（skills/、docs/designs/、openspec/specs/）均无命中
