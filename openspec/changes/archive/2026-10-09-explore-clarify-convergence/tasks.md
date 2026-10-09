# Tasks

> 规格依据：`specs/requirement-clarification/spec.md`、`specs/domain-glossary/spec.md`。实现依据：`design.md`。

## 1. 收敛门规则文件（kflow-explore 自有 references）

- [x] 1.1 新增 `skills/kflow-explore/references/clarify-convergence.md`，承载四组规则：收敛硬门（清单 = ∅ 或显式降级）、消歧路径限定、需求内容非必要不增加、提问纪律（事实项/决策项分流）。验证：文件存在且四个小节标题齐全（`grep -c "^## " skills/kflow-explore/references/clarify-convergence.md` ≥ 4）
- [x] 1.2 在 1.1 中写明**候选清单生成规则**：由页面结构/菜单、可执行操作、表单项、业务规则、业务流程五个内容域逐域遍历产生候选；清单为空须说明五域均已遍历。验证：`grep -n "五个内容域\|逐域遍历" skills/kflow-explore/references/clarify-convergence.md` 命中
- [x] 1.3 在 1.1 中写明 **`待补充` 降级标记与 TODO/TBD 占位符的区别**（降级须含理由与责任阶段），避免与「文档禁止占位符」规则冲突。验证：`grep -n "待补充" skills/kflow-explore/references/clarify-convergence.md` 命中且含「理由」「责任阶段」

## 2. explore SKILL.md 同步（设计文档 → SKILL.md 同步）

- [x] 2.1 设计文档 → SKILL.md 同步：在 `skills/kflow-explore/SKILL.md` 步骤 6（CLARIFY）中加入收敛硬门——维护未决问题清单、五域遍历生成候选、消歧路径限定、非必要不增加。验证：`grep -n "未决问题清单\|消歧" skills/kflow-explore/SKILL.md` 命中
- [x] 2.2 设计文档 → SKILL.md 同步：在步骤 7（SPLIT）前置条件中引用该门（清单非空且未降级时不得进入 SPLIT）。验证：步骤 7 段落含对收敛门的引用（`grep -n "收敛门\|未决问题清单" skills/kflow-explore/SKILL.md` 在步骤 7 段落命中）
- [x] 2.3 设计文档 → SKILL.md 同步：对齐「越界处理」段落中「带待补充继续流转」的表述，明确其与 D5 降级标记为同一语义、须记录理由与责任阶段。验证：`grep -n "待补充" skills/kflow-explore/SKILL.md` 的命中行均含理由/责任阶段说明
- [x] 2.4 更新 `skills/kflow-explore/SKILL.md` 的 `references/` 加载清单，把 1.1 新增文件纳入对应加载层。验证：`grep -n "clarify-convergence.md" skills/kflow-explore/SKILL.md` 命中

## 3. CONTEXT.md 格式权威内部化

- [x] 3.1 确认并加固 `skills/kflow-explore/references/context-template.md` 为 CONTEXT.md 格式的**唯一权威**：文件自述其权威地位，并覆盖 project 名标题、术语列表（定义/别名/边界）、修订记录三要素。验证：`grep -n "定义\|别名\|边界\|修订记录" skills/kflow-explore/references/context-template.md` 命中三要素
- [x] 3.2 在 `skills/kflow-explore/SKILL.md` 步骤 6a 明确 CONTEXT.md 格式 SHALL 以 `references/context-template.md` 为准，SHALL NOT 引用任何外部格式文件。验证：`grep -n "context-template.md" skills/kflow-explore/SKILL.md` 命中且同段无外部技能名
- [ ] 3.3 核验 `domain-glossary` 规格与实现一致：`openspec show domain-glossary --type spec` 的「CONTEXT.md 格式」requirement 归档后须指向 `kflow-explore/references/context-template.md`。验证：归档后复查该 requirement 文本，无外部技能名

## 4. 设计文档同步（docs/designs）

- [x] 4.1 设计文档 → SKILL.md 同步：更新 `docs/designs/skills/kflow-explore.md` 的 CLARIFY 章节，反映收敛硬门、消歧路径、非必要不增加、提问纪律。验证：`grep -n "未决问题清单\|消歧" docs/designs/skills/kflow-explore.md` 命中
- [x] 4.2 更新 `docs/designs/skills/kflow-explore.md` 中 CONTEXT.md 格式的表述，指向 `references/context-template.md` 而非外部格式文件。验证：`grep -rn "CONTEXT-FORMAT\|grill-with-docs" docs/designs/` 无命中

## 5. 自包含核验

- [ ] 5.1 全仓核验零外部技能引用：`grep -rn "grill-with-docs\|grilling" skills/ openspec/specs/requirement-clarification/ openspec/specs/domain-glossary/` 无命中。验证：命令无输出
- [x] 5.2 核验所有 `Skill(...)` 调用与跨技能引用路径均指向 KFlow 自有资源且可解析。验证：`grep -rn "Skill(skill=" skills/` 命中的技能名均为 `kflow-*`；`docs/skill-suggestion.md` 记录 `adr-records` 一侧的外部依赖为待办（另立变更）

## 6. 集成验证

- [x] 6.1 运行 `openspec validate explore-clarify-convergence` 并确认输出 "is valid"（若 `--strict` 报模块解析错误，以普通校验结果为准并在提交说明中记录）
- [x] 6.2 走查样例一（有歧义需求）：构造一个含 2 项未决歧义的需求，确认 CLARIFY 阻塞在 SPLIT 之前，消解后放行。验证：走查结论记录到本变更的 review 记录
- [x] 6.3 走查样例二（无歧义需求）：构造一个无歧义的小需求，确认清单经五域遍历后为空、几乎零额外交互直接放行。验证：走查结论记录到本变更的 review 记录
- [x] 6.4 走查样例三（降级路径）：构造一项本阶段无法消解的歧义，确认其以 `待补充` + 理由 + 责任阶段降级后放行，且记录出现在 `.status.md`。验证：走查结论记录到本变更的 review 记录
