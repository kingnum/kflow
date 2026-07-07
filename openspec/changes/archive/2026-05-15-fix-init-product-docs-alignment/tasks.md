## 1. 设计文档更新

- [x] 1.1 core-mechanisms.md: 目录结构中 `domains/{domain}.md` → `functional-designs/{module}.md`，新增 `technical-designs/`，CONTEXT.md 确认 `docs/` 下路径，service-guide.md 产出 Skill 补充 kflow-init
- [x] 1.2 kflow-init.md: CONTEXT.md 路径修正（项目根目录 → docs/），产品文档检测 7→8 项，LEGACY 输出新增 service-guide.md 为第 7 类，文档路径 `domains/` → `functional-designs/`，新增 `technical-designs/`
- [x] 1.3 kflow-archive.md: MERGE 目标路径 `domains/{domain}.md` → `functional-designs/{module}.md`，新增 `technical-designs/` 合并逻辑，新增去草稿规则（首次合并替换标记）
- [x] 1.4 kflow-code.md: service-guide.md 职责说明补充（init 可预生成草稿，code 检测草稿时进入补充流程）
- [x] 1.5 overview.md: 如有目录结构引用，同步更新

## 2. 模板目录重组

- [x] 2.1 整体模板目录结构重组：`change/` → `changes/{change}/`，`product/` → `design-templates/functional-designs/` + `design-templates/technical-designs/`，`subchange/` → `subchanges/{subchange}/`，`integration/` → `changes/{change}/integration/`，`infra/` 拆分到对应目标路径
- [x] 2.2 product/domain-doc.md 重构为 `design-templates/functional-designs/module.md`，章节与变更级 part-NN.md 一致，新增来源标注字段（来源变更 + 归档时间）
- [x] 2.3 product/{architecture,data-model,api-catalog,nfr-baseline}.md → `design-templates/technical-designs/`
- [x] 2.4 change/service-guide.md → `templates/docs/service-guide.md`
- [x] 2.5 infra/toolchain.md → `templates/docs/toolchain.md`
- [x] 2.6 change/ 下其余模板保持路径映射到 `changes/{change}/`，subchange/ 下模板 → `subchanges/{subchange}/`
- [x] 2.7 templates/index.md 同步更新模板路径和编号

## 3. Skills 设计文档模板引用更新

模板路径变更后，所有 Skills 设计文档（`docs/designs/skills/{skill}.md`）中「输出产物」表格的模板列引用链接需同步修正：

- [x] 3.1 kflow-explore.md: 功能设计模板路径 `change/functional-designs/` → `changes/{change}/functional-designs/`，状态文件路径更新
- [x] 3.2 kflow-design.md: detailed-design、review-reports/*、api-tests/*、e2e-tests/*、integration-tests/*、traceability 模板路径更新
- [x] 3.3 kflow-plan.md: subchange-status、subchange-tasks 模板路径 `subchange/` → `subchanges/{subchange}/`
- [x] 3.4 kflow-code.md: service-guide 模板路径 `change/service-guide.md` → `docs/service-guide.md`，migration-log 路径更新
- [x] 3.5 kflow-audit.md: audit-report 模板路径更新
- [x] 3.6 kflow-code-review.md: code-review 模板路径更新
- [x] 3.7 kflow-e2e-test.md: e2e-round-report、api-round-report、api-summary、e2e-summary 模板路径更新
- [x] 3.8 kflow-bug-fix.md: fix-report、design-error-report 模板路径更新
- [x] 3.9 kflow-integration-test.md: integration-round-report、integration-summary、contract-error-report 模板路径更新

## 4. SKILL 实现逻辑更新（.claude/skills/）

以下 Skills 的 SKILL.md 需要更新**执行逻辑**，而不只是模板引用路径：

- [x] 4.1 kflow-init/SKILL.md: CONTEXT.md 路径修正（项目根目录 → docs/），产品文档检测 8 项路径更新，LEGACY 步骤新增 service-guide.md 生成逻辑，文档输出路径 `domains/` → `functional-designs/`
- [x] 4.2 kflow-archive/SKILL.md: MERGE 目标路径更新（`domains/{domain}.md` → `functional-designs/{module}.md`），新增 `technical-designs/` 分项更新逻辑，新增去草稿规则（首次合并检测+替换标记）
- [x] 4.3 kflow-code/SKILL.md: service-guide.md 生成前检测是否为 init 草稿（含「由 AI 逆向分析生成」标记），若是则进入补充流程（保留已有 dev 配置，补充多环境）
- [x] 4.4 skill-creator: 如 skill-creator 的模板初始化逻辑引用了旧模板目录结构，需同步更新

## 5. Spec 归档（apply 时执行）

- [x] 5.1 将 delta specs 合并到 openspec/specs/{devflow-init,archive-design-merge,stage-doc-templates,doc-naming-convention,domain-glossary,service-guide-generation,multi-environment-config,init-legacy-reverse-analysis}/
