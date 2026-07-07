## 1. Specs 合并

- [x] 1.1 将 specs/bug-registration/spec.md delta 合并到 openspec/specs/bug-registration/spec.md（MODIFIED Requirements：分页详情文件格式追加优先场景、BUG-ID 编号规范、问题与修复报告关联 A/B 路径场景）
- [x] 1.2 将 specs/bug-triage-skill/spec.md delta 合并到 openspec/specs/bug-triage-skill/spec.md（MODIFIED Requirements：严重度分级去掉前缀、Skill 输出产物增加修复记录占位节和必填节硬约束）
- [x] 1.3 将 specs/bug-fix-writeback/spec.md 内容复制到 openspec/specs/bug-fix-writeback/spec.md（新增 capability）

## 2. 模板更新

- [x] 2.1 更新 `docs/designs/templates/changes/{change}/bugs/bugs-index.md`：去掉严重度前缀（B-/W-/S-）列，BUG-ID 列改为 BUG-{NNN} 格式，严重度作为独立列使用 emoji+文字
- [x] 2.2 更新 `docs/designs/templates/changes/{change}/bugs/bugs-detail.md`：去掉 frontmatter 中 stage/skill/template_for 字段；基本信息表格去掉前缀，BUG-ID 改为 BUG-{NNN}；在「处理状态」节后新增「修复记录」节（含修复日期、根因分类、修复文件、验证结果、修复内容、Post-mortem）；「关联」节中「关联修复报告」字段改为引用修复记录节

## 3. 设计文档更新

- [x] 3.1 更新 `docs/designs/skills/kflow-bug-triage.md`：严重度分级表去掉「编号前缀」列；输出产物表增加「修复记录占位节」说明；分页规则增加「追加优先、满额新建」明确措辞；问题登记机制说明 BUG-ID 改为纯序号 BUG-{NNN}
- [x] 3.2 更新 `docs/designs/skills/kflow-bug-fix.md`：输出产物表增加 A 路径回写职责说明；执行流程增加 A 路径回写步骤（修复完成后 SHALL 回写 bugs/ 修复记录节、更新 index.md 状态）；与其他 Skill 关系增加「回写 bugs/ 目录」说明

## 4. 运行时 Skill 更新（设计文档 → SKILL.md 同步）

- [x] 4.1 更新 `.claude/skills/kflow-bug-triage/SKILL.md`：严重度分级表去掉前缀；REGISTER 步骤增加硬约束（SHALL 按以下顺序输出必填节：基本信息、问题描述、诊断结果、解决方案、处理状态、修复记录占位、关联；SHALL NOT 省略任何节；SHALL 追加到当前分页文件，SHALL NOT 每次登记创建新文件）；输出产物表增加修复记录占位节说明
- [x] 4.2 更新 `.claude/skills/kflow-bug-fix/SKILL.md`：执行流程增加 A 路径回写步骤（修复验证通过后 SHALL 回写 bugs/ 修复记录节、更新 index.md 状态为「已解决」）；输出产物表增加 A 路径回写说明（bugs/bug-NNN-NNN.md 修复记录节）；约束节增加「A 路径 SHALL NOT 在 bugs/ 创建独立 fix-report 文件」

## 5. 验证

- [x] 5.1 检查所有更新的 SKILL.md 通过 kflow-skills-auditor 规范审查（name/description 格式、中英混合触发、Token 效率）
