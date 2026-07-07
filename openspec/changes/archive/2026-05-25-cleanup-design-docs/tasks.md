## 1. CLAUDE.md 修复

- [x] 1.1 修复 CLAUDE.md 行 77-78 的阶段数：`7 阶段` → `11 阶段`，`5 阶段` → `9 阶段`
- [x] 1.2 修复 CLAUDE.md 行 72-73 工作流链：补全 kflow-code-review、kflow-api-test、kflow-integration-test、kflow-audit
- [x] 1.3 验证修改后 CLAUDE.md 阶段数与 docs/designs/skills/index.md 一致

## 2. core-mechanisms.md 拆分（7 文件，每个 ≤ 500 行）

- [x] 2.1 创建 `docs/designs/core-mechanisms/` 目录
- [x] 2.2 提取章节一 → `01-project-types.md`（~35 行）
- [x] 2.3 提取章节二（含 2.3~2.5）→ `02-directory-structure.md`（~320 行）
- [x] 2.4 提取章节三+四 → `03-status-and-tasks.md`（~495 行）
- [x] 2.5 提取章节五+六 → `04-gates-and-transitions.md`（~290 行）
- [x] 2.6 提取章节七~十一、十三~十四 → `05-execution-services.md`（~550 行，精简模板后 ≤ 500）
- [x] 2.7 提取章节十二 → `06-recovery.md`（~165 行）
- [x] 2.8 提取章节十五 → `07-agent-model.md`（~385 行）
- [x] 2.9 提取章节十七~十八 → `08-governance.md`（~150 行）
- [x] 2.10 创建 `core-mechanisms/index.md` 导航页（八文件链接 + 一句话描述）
- [x] 2.11 删除原 `core-mechanisms.md`（2235 行）
- [x] 2.12 验证每个拆分文件行数 ≤ 500

## 3. 锚点引用批量更新（按 design.md 锚点映射表）

- [x] 3.1 Grep 定位所有对 `core-mechanisms.md` 的引用（设计文档 + 模板 + 运行时 Skill）
- [x] 3.2 按锚点映射表批量更新引用路径（原 `#xxx` → 目标文件 `#xxx`）
- [x] 3.3 更新设计文档中的锚点引用
- [x] 3.4 更新模板文档中的锚点引用
- [x] 3.5 验证：拆分后每个目标文件存在且包含对应锚点（无死链）

## 4. 运行时 Skill 内联规则（方案 B：运行时自包含）

- [x] 4.1 内联 `.claude/skills/kflow-prototype-design/SKILL.md`（3 处）：DESIGN/VERIFY/SELFREV 步骤的 §15.11 引用改为内联规则摘要
- [x] 4.2 内联 `.claude/skills/kflow-explore/SKILL.md`（1 处）：SELFREV 步骤
- [x] 4.3 内联 `.claude/skills/kflow-design/SKILL.md`（2 处）：SELFREV/REVIEW 步骤
- [x] 4.4 内联 `.claude/skills/kflow-plan/SKILL.md`（2 处）：SELFREV/重复制步骤
- [x] 4.5 删除 `.claude/skills/kflow-resume/SKILL.md`（1 处）：GATE 步骤的 `core-mechanisms.md` 归属说明
- [x] 4.6 运行 Grep 验证运行时 Skill 中无 `core-mechanisms` 外链残留

## 5. 设计文档版本号同步

- [x] 5.1 更新 `docs/designs/skills/kflow-explore.md` 版本号 2.1.0 → 2.3.0
- [x] 5.2 更新 `docs/designs/skills/kflow-design.md` 版本号 2.0.0 → 2.1.0
- [x] 5.3 更新 `docs/designs/skills/kflow-code.md` 版本号 2.0.0 → 2.1.0
- [x] 5.4 检查 explore/design/code 三处设计文档与运行时 SKILL.md 的内容差异，补充缺失机制

## 6. 清理历史参考目录

- [x] 6.1 删除 `references/` 目录（全部 15 个子目录，~100MB）
- [x] 6.2 删除 `evals-workspace/` 目录（~248K）
- [x] 6.3 删除 `mattpocock-skills-main/` 目录（~300K）
- [x] 6.4 清理 `.claude/worktrees/`：`git worktree prune` + 删除残留目录（~1.1GB）
- [x] 6.5 更新 CLAUDE.md：删除 `references/` 项目结构描述（第 39-47 行）
- [x] 6.6 更新 CLAUDE.md：删除"当前运营中的 Skills（旧体系）"段落（第 52-63 行）
- [x] 6.7 验证 Grep：确认无文档引用 `references/` 路径
