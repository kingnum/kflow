# Tasks

## 1. 核心机制与设计文档更新

- [x] 1.1 更新 `docs/designs/core-mechanisms/07-agent-model.md` §16 自审机制：将「强制执行 10 轮自循环审查」改为「首次创建固定 10 轮 / 非首次创建弹性轮次 + 评分底线 > 8」，并引用 design-review-tiering。验证：grep 该文件确认「10 轮」仅以「首次创建」语义出现，无「无条件 10 轮」残留。
- [x] 1.2 更新 `docs/designs/skills/kflow-explore.md` SELFREV 步骤与「10 轮自审」章节：加入首次/非首次分支、弹性轮次公式、评分底线。验证：文档与 spec 增量（design-review-tiering）需求一致。
- [x] 1.3 更新 `docs/designs/skills/kflow-prototype-design.md` SELFREV 步骤：同上分支与公式。验证：与 kflow-explore 更新口径一致。
- [x] 1.4 更新 `docs/designs/skills/kflow-design.md` SELFREV 步骤（步骤 10）与「10 轮自审」章节：同上分支与公式。验证：REVIEW 分级（简化/完整）描述保持不变，仅 SELFREV 部分改动。
- [x] 1.5 更新 `docs/designs/index.md` 中「10 轮自审机制」条目为「首次/非首次分级自审」。验证：该条目不再表述为「每阶段 10 轮自循环审查」。

## 2. Skill 实现同步（设计文档 → SKILL.md 同步）

- [x] 2.1 同步 `skills/kflow-explore/SKILL.md` SELFREV 步骤 + `references/self-review.md`：将「10 轮强制、不可提前终止」改为「首次 10 轮 / 非首次 N 轮弹性（影响范围分数）+ 各维度 > 8 评分底线」。验证：self-review.md 含判定信号、弹性公式、评分底线规则，SKILL.md 与设计文档一致。
- [x] 2.2 同步 `skills/kflow-prototype-design/SKILL.md` SELFREV 步骤 + `references/self-review.md`：同 2.1 口径。验证：三份 self-review.md 的弹性规则表述一致。
- [x] 2.3 同步 `skills/kflow-design/SKILL.md` SELFREV 步骤 + `references/self-review.md`：同 2.1 口径，且 REVIEW（四视角）分级描述保持不变。验证：grep 确认三设计 skill 中「必须完成全部 10 轮」无残留。

## 3. README 与一致性校验

- [x] 3.1 更新 `README.md` 中「10 轮自审机制」相关描述（含 FAQ、变更历史摘要）为首次/非首次分级自审。验证：README 不再出现「三阶段强制 10 轮自审」的无条件表述。
- [x] 3.2 运行 `scripts/sync-references.sh` 校验 references 一致性，修复其报告的偏差。验证：脚本通过、无新增不一致。
- [x] 3.3 核对 `skills/kflow-audit`「产物完整性」维度对弹性自审报告份数的判定：确认其不因「报告份数 < 10」误判缺项；如需补充说明则在本任务内完成。验证：审计维度表述与弹性自审兼容。
