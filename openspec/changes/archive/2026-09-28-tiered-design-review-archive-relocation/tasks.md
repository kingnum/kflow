# Tasks

## 1. 设计审查分级 — 设计文档

- [x] 1.1 更新 `docs/designs/core-mechanisms/04-gates-and-transitions.md`：正向流程图与「详细设计阶段 Skill 对应」中标注设计审查按变更类型分级（功能缺陷级→简化单视角；功能需求/产品需求级→完整四视角），并说明进入计划门控按模式分支。验证：grep 该文件出现「简化模式」与「变更类型」判定描述。
- [x] 1.2 更新 `docs/designs/skills/kflow-design.md`：REVIEW 步骤新增「简化/完整」分支，产物形态区分（简化=synthesis.md 单文件；完整=四份视角报告 + synthesis.md）。验证：grep 该文件出现「简化模式」与「单视角综合审查」。
- [x] 1.3 更新 `docs/designs/core-mechanisms/05-execution-services.md` 中四视角审查相关描述，标注分级执行。验证：grep 该文件审查段落含变更类型判定。

## 2. 设计审查分级 — SKILL.md 同步（设计文档 → SKILL.md 同步）

- [x] 2.1 同步 `skills/kflow-design/SKILL.md`：REVIEW 步骤按变更类型分支为简化（单 Agent 综合审查）与完整（四视角并行），输出产物表区分两种模式。验证：grep 该文件出现「简化模式」与「单视角」。
- [x] 2.2 同步 `skills/kflow-design/references/review-content.md`：标注四视角检查清单在简化模式下由单 Agent 串行覆盖、完整模式下由四 Agent 并行覆盖。验证：grep 该文件出现「简化模式」说明。
- [x] 2.3 同步进入计划门控（Gate 2）：将「所有审查视角状态 / cross-reviews/ 四份视角报告 / synthesis.md」的检查改为按变更类型分支（简化模式仅检查单一 synthesis.md）。更新所有自包含副本 `skills/*/references/gates.md`（共 10 份）。验证：`grep -L "简化" skills/*/references/gates.md` 返回空（全部已含分支）。
- [x] 2.4 同步 `skills/kflow-plan/SKILL.md` 中的进入计划门控描述，与 Gate 2 分支一致。验证：grep 该文件出现按变更类型分支的审查产物检查。
- [x] 2.5 同步 `skills/kflow-audit/SKILL.md`（或 references）：「审查 20%」维度按完整/简化模式分别给分，简化模式不因缺四份视角报告而判缺项。验证：grep 该文件出现审查模式分支给分规则。

## 3. 归档目录迁移 — 设计文档

- [x] 3.1 更新 `docs/designs/core-mechanisms/02-directory-structure.md`：归档目录树从 `docs/archive/` 改为 `docs/changes/archive/`，命名规范表同步。验证：grep 该文件不再含 `docs/archive`（除 `docs/changes/archive`）。
- [x] 3.2 更新 `docs/designs/core-mechanisms/08-governance.md`：archive 阶段白名单路径 `docs/archive/*` 改为 `docs/changes/archive/*`。验证：grep 该文件白名单行含 `docs/changes/archive/*`。
- [x] 3.3 更新设计文档 `docs/designs/skills/kflow-archive.md`、`kflow-status.md`、`kflow-resume.md`、`kflow-guide.md`、`kflow-init.md`、`kflow-e2e-test.md` 中的归档路径引用。验证：`grep -rn "docs/archive" docs/designs/skills/` 返回空。
- [x] 3.4 更新示例与模板 `docs/designs/examples/change-index.md`、`product-domain-doc.md`、`docs/designs/templates/changes/{change}/change-index.md`、`docs/designs/templates/design-templates/changelog.md` 中的归档路径。验证：`grep -rn "docs/archive" docs/designs/examples/ docs/designs/templates/` 返回空。

## 4. 归档目录迁移 — SKILL.md 同步（设计文档 → SKILL.md 同步）

- [x] 4.1 同步 `skills/kflow-archive/SKILL.md` 与 `references/archive-rules.md`：MOVE 步骤目标路径、输出产物表、归档索引记录改为 `docs/changes/archive/{YYYY-MM-DD}-{change}/`。验证：grep 两文件不再含 `docs/archive/`。
- [x] 4.2 同步 `skills/kflow-status/SKILL.md`：SCAN/FILTER 流程的归档检测与排除改为 `docs/changes/archive/`，消除「排除 archive/ 子目录」与 Glob 路径的错位。验证：grep 该文件 FILTER 步骤含 `docs/changes/archive/`。
- [x] 4.3 同步 `skills/kflow-resume/SKILL.md` 与 `references/recovery-protocol.md`：归档检测路径改为 `docs/changes/archive/*/{change}/` 与 `docs/changes/archive/*-{change}/`。验证：grep 两文件不再含 `docs/archive/`。
- [x] 4.4 同步 `skills/kflow-guide/SKILL.md`：活跃变更扫描排除 `docs/changes/archive/`。验证：grep 该文件排除逻辑含 `docs/changes/archive/`。
- [x] 4.5 同步 `skills/kflow-init/SKILL.md`：排除 `docs/changes/archive/` 下的变更。验证：grep 该文件排除逻辑含 `docs/changes/archive/`。
- [x] 4.6 同步 `skills/kflow-e2e-test/SKILL.md`：归档引用路径改为 `docs/changes/archive/`。验证：grep 该文件不再含 `docs/archive/`。

## 5. 验证与收尾

- [x] 5.1 全量扫描零残留：`grep -rn "docs/archive" skills/ docs/designs/` 仅命中 `docs/changes/archive`（允许归档变更示例或历史说明中出现）。验证：除 `docs/changes/archive` 外无裸 `docs/archive` 引用。
- [x] 5.2 `openspec validate tiered-design-review-archive-relocation --strict` 通过。验证：命令退出码 0，无缺失 Purpose/场景告警。
- [x] 5.3 交叉一致性检查：kflow-status 的 SCAN/FILTER 表述、kflow-resume 归档检测、kflow-archive MOVE 目标三处路径一致，均为 `docs/changes/archive/`。验证：三处 grep 结果路径前缀一致。
