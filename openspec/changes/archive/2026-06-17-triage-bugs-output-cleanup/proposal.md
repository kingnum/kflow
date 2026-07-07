# Proposal: triage-bugs-output-cleanup

## Why

kflow-bug-triage 实际运行时 bugs/ 目录产出严重偏离设计定义：分页文件命名随意（`bug-001-005.md` 而非 `bug-001-020.md`）、每次登记都新建文件而非追加到现有分页、BUG-ID 前缀 B-/W-/S- 与序号 BUG-001 混用、fix-report 文件散落在 bugs/ 目录（实际应属于子变更目录或 bug 详情的一部分），问题详情的节结构不遵循模板。这些混乱导致无法快速定位问题的完整生命周期，降低了 bugs/ 目录作为追踪载体的价值。

## What Changes

**修复记录归属重构（A/B 双路径）**：
- **A 路径（用户反馈 → triage → L4 → bug-fix）**：bug-fix 修复完成后，将修复记录（根因分类、修复文件、验证结果、Post-mortem）回写到 `bugs/bug-NNN-NNN.md` 对应 BUG 的「修复记录」节；bugs/ 目录中不再产出独立 fix-report 文件
- **B 路径（测试阶段自动发现 → bug-fix）**：fix-report 继续输出到 `subchanges/{subchange}/test-reports/fix-reports/`（保持现有设计）；若该测试发现的 bug 同时已在 bugs/ 中登记，则同步回写 bugs/ 详情

**分页文件规则强化**：
- 明确「追加优先、满额新建」原则：登记新 BUG 时追加到当前分页文件，仅当该文件满 20 条时才创建新分页
- 文件名固定为 `bug-{start}-{end}.md`（第一个文件固定 `bug-001-020.md`）

**BUG-ID 编号规范化（BREAKING）**：
- BUG-ID 改为纯序号 `BUG-{NNN}`，消除 `B-`/`W-`/`S-` 前缀
- 严重度（🔴阻塞/🟡警告/🔵建议）作为独立字段，不编码到 ID 中
- 设计文档、模板、spec 中严重度分级表去掉「编号前缀」列

**问题详情模板精简与硬约束**：
- 去掉无实际意义的 frontmatter（`stage`、`skill`、`template_for`）
- 在 SKILL.md 的 REGISTER 步骤明确列出必填节清单（基本信息、问题描述、诊断结果、解决方案、处理状态、修复记录占位、关联），使用 `SHALL 按以下节的顺序输出，SHALL NOT 省略任何节` 格式
- bug-fix 的 SKILL.md 增加回写约束：修复完成后 SHALL 回写 bugs/ 对应 BUG 的修复记录节、更新 bugs/index.md 状态

## Capabilities

### New Capabilities
- `bug-fix-writeback`: 定义 bug-fix 对 bugs/ 目录的回写职责——A 路径修复记录回写（追加到 bug 详情修复记录节）、index.md 状态更新、B 路径同步回写规则

### Modified Capabilities
- `bug-registration`: 分页文件命名和创建策略强化（追加优先、满额新建）；BUG-ID 改为纯序号，消除前缀混用；问题详情模板精简（去掉 frontmatter，增加修复记录节占位）
- `bug-triage-skill`: 严重度分级去掉编号前缀；输出产物描述增加修复记录占位节

## Impact

- **设计文档**：`docs/designs/skills/kflow-bug-triage.md`（严重度表去掉前缀、输出产物增加修复记录节描述）、`docs/designs/skills/kflow-bug-fix.md`（增加回写 bugs/ 职责）
- **模板文件**：`docs/designs/templates/changes/{change}/bugs/bugs-index.md`（去掉前缀）、`bugs-detail.md`（精简 frontmatter、增加修复记录节）
- **运行时 Skill**：`.claude/skills/kflow-bug-triage/SKILL.md`（REGISTER 步骤硬约束）、`.claude/skills/kflow-bug-fix/SKILL.md`（增加回写步骤）
- **Specs**：`bug-registration`（分页/命名/ID）、`bug-triage-skill`（严重度前缀）、新增 `bug-fix-writeback`
- **已有 bugs/ 目录**（测试项目）：已存在的 fix-report 和 bug 详情文件在下次 triage 时按需迁移，不在本次变更中强制迁移
