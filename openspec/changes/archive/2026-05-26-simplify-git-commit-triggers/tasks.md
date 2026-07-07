## 1. 纠正 kflow-archive：移除 VERSION+PACKAGE + COMMIT 改为询问

- [x] 1.1 更新 `docs/designs/skills/kflow-archive.md`：移除步骤 9 VERSION 和步骤 10 PACKAGE（含整个「归档后版本自增、打包与 git commit」section），COMMIT 从强制改为 AskUserQuestion 询问，删除 `git add VERSION targets/`
- [x] 1.2 更新 `.claude/skills/kflow-archive/SKILL.md`：同步设计文档变更（description 移除打包/版本描述、角色移除打包/版本描述、任务链移除 VERSION+PACKAGE、workflow 图修复、COMMIT 改为询问），使用 `/skill-creator` 根据变更后的设计文档更新运行时 Skill（kflow-archive 的 SKILL.md），标注"设计文档 → SKILL.md 同步"

## 2. 删除 kflow-guide PRECOMMIT 步骤

- [x] 2.1 更新 `docs/designs/skills/kflow-guide.md`：删除「新变更前 git commit 检查」整段（含触发条件、检查流程 5 步、提交信息格式规范表格），workflow 图中移除步骤 2 PRECOMMIT，步骤序号重排
- [x] 2.2 更新 `.claude/skills/kflow-guide/SKILL.md`：同步设计文档变更（workflow 图移除 PRECOMMIT、删除新变更前检查流程、步骤序号重排），使用 `/skill-creator` 根据变更后的设计文档更新运行时 Skill（kflow-guide 的 SKILL.md），标注"设计文档 → SKILL.md 同步"

## 3. 删除 kflow-plan 每功能点 commit 步骤

- [x] 3.1 更新 `docs/designs/skills/kflow-plan.md`：tasks.md 模板从 8 步改为 7 步（删除 Step 8 提交变更），TDD 循环描述改为 Step 1-7，VERIFY 步骤删除「提交记录」检查项，自审维度「任务粒度合理性」删除「提交粒度」检查项
- [x] 3.2 更新 `.claude/skills/kflow-plan/SKILL.md`：同步设计文档变更（模板、VERIFY、自审维度），使用 `/skill-creator` 根据变更后的设计文档更新运行时 Skill（kflow-plan 的 SKILL.md），标注"设计文档 → SKILL.md 同步"

## 4. 修正 kflow-init git 规则

- [x] 4.1 更新 `docs/designs/skills/kflow-init.md`：删除规则 #9（新变更前必须检查 git）、规则 #10 从「首次 init 后必须 git commit」改为「首次 init 时若目录非 git 仓库询问是否执行 git init」、步骤 12 COMMIT 改为 GIT INIT（检测仓库→询问 git init），更新 CLAUDE.md 注入模板中的规则条款从 3 条（#7/#8/#9/#10）改为 2 条
- [x] 4.2 更新 `.claude/skills/kflow-init/SKILL.md`：同步设计文档变更（规则条款、步骤 12、CLAUDE.md 注入模板），使用 `/skill-creator` 根据变更后的设计文档更新运行时 Skill（kflow-init 的 SKILL.md），标注"设计文档 → SKILL.md 同步"

## 5. 更新项目级 CLAUDE.md 和核心机制文档

- [x] 5.1 更新 `CLAUDE.md`：归档后 git commit 从「必须执行」改为「询问是否执行」，版本自增+打包规则保留但措辞调整——将 git commit 前强制打包改为归档完成后先询问是否提交（若确认则在 commit 前执行版本自增+打包），保持 version bump + packaging 流程完整性
- [x] 5.2 更新 `docs/designs/core-mechanisms/08-governance.md`：18.5 强制规则注入从 3 条改为 2 条、18.1 提交信息格式删除不再需要的 `{动词}: {摘要}` 和 `init: {摘要}` 格式行、18.3 提交失败处理中「用户选择跳过」统一为所有场景适用

## 6. OpenSpec specs 归档

- [x] 6.1 确认所有 delta spec 文件内容与 proposal/design 一致，无遗漏
