## 1. 新增模板

- [x] 1.1 创建 `templates/design-templates/functional-designs/index.md` — 菜单级索引模板（功能点清单、分册总览、修订记录）
- [x] 1.2 创建 `templates/design-templates/functional-designs/part-NN.md` — 产品级分册模板（与变更级 part-NN.md 同结构，额外增加来源标注字段）
- [x] 1.3 创建 `templates/design-templates/functional-designs/backend-domain.md` — 纯后端简化模板（设计域/接口参数定义/调用约束替代 UX 章节）
- [x] 1.4 创建 `templates/design-templates/technical-designs/config-items.md` — 配置项设计模板（对齐 detailed-design.md §五）
- [x] 1.5 创建 `templates/design-templates/technical-designs/error-handling.md` — 错误处理设计模板（对齐 detailed-design.md §六）

## 2. 修订现有模板

- [x] 2.1 修订 `templates/design-templates/technical-designs/architecture.md` — 增加配置项索引和错误处理索引区
- [x] 2.2 修订 `templates/design-templates/technical-designs/data-model.md` — 确认与 detailed-design.md §二数据部分的兼容性
- [x] 2.3 修订 `templates/design-templates/technical-designs/api-catalog.md` — 确认与 detailed-design.md §二接口部分的兼容性
- [x] 2.4 修订 `templates/design-templates/technical-designs/nfr-baseline.md` — 确认与 detailed-design.md §三 NFR 的兼容性

## 3. 废弃与迁移

- [x] 3.1 标记 `templates/design-templates/functional-designs/module.md` 为废弃（在其 frontmatter 添加 `deprecated: true`）
- [x] 3.2 更新 `templates/index.md` — 反映模板变更（+5 新增, -1 废弃, 4 修订）

## 4. 更新 kflow-init SKILL.md

- [x] 4.1 更新 LEGACY 步骤的 L2 描述 — 增加 L2.5 前端工程扫描（前后端项目条件执行）
- [x] 4.2 添加 L2.5 前端扫描详细流程：路由扫描 → 菜单扫描 → 页面组件扫描
- [x] 4.3 更新 7 类文档生成逻辑：functional-designs 从平铺文件改为目录结构或简化模板
- [x] 4.4 更新 8 项产品文档检测表 — #3 从文件计数改为目录数（前后端）/文件数（纯后端）
- [x] 4.5 增加 technical-designs 从 4 文件扩展为 6 文件的生成说明（新增 config-items.md、error-handling.md）

## 5. 更新 kflow-archive SKILL.md

- [x] 5.1 更新 MERGE 步骤：functional-designs 合并目标从平铺 `{module}.md` 改为目录结构 `{menu}/part-NN.md`
- [x] 5.2 更新 MERGE 步骤：technical-designs 合并从 4 文件扩展为 6 文件
- [x] 5.3 更新去草稿逻辑：适配目录结构下的草稿标记检测

## 6. 更新设计规格文档

- [x] 6.1 更新 `docs/designs/skills/kflow-init.md` — LEGACY 步骤新增 L2.5、前后端差异化、目录化输出
- [x] 6.2 更新 `docs/designs/skills/kflow-archive.md` — MERGE 步骤适配目录结构和 6 文件体系
- [x] 6.3 更新 `docs/designs/core-mechanisms.md` — 产品文档状态检测项描述、functional-designs 目录结构规范
- [x] 6.4 更新 `docs/designs/overview.md` — 模板数量和选项说明更新

## 7. 更新 CLAUDE.md 注入规则

- [x] 7.1 更新 kflow-init SKILL.md CLAUDE.md 注入模板 — 8 项检测表反映新的检测逻辑（#3 目录数/文件数，#4-#7 侧带检测 config-items.md、error-handling.md）

## 8. 验证与文档

- [x] 8.1 对照所有 10 个 spec 文件核对实现完整性
- [x] 8.2 确认变更级模板（changes/{change}/functional-designs/）无需变更
- [x] 8.3 确认 `.claude/skills/kflow-explore/SKILL.md` 和 `.claude/skills/kflow-design/SKILL.md` 不受影响
