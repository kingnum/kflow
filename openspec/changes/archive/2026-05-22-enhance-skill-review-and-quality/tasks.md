## 1. Plan Mode 绕过（问题 1）

- [x] 1.1 修改 `CLAUDE.md`：在强制规则区新增强制规则——用户输入匹配「继续/恢复/resume + 变更名」时，禁止进入 Plan Mode，直接进入 Skill 路由链
- [x] 1.2 修改 `.claude/skills/kflow-guide/SKILL.md`：description frontmatter 增加 RESUME 路由优先级说明和 Plan Mode 绕过提示；PARSE 步骤增加「正则匹配 RESUME 模式时禁止 Plan Mode」的优先级说明

## 2. 原型审查产物路径统一（问题 2）

- [x] 2.1 修改 `.claude/skills/kflow-prototype-design/SKILL.md`：VERIFY 步骤 6.1（CDN 扫描）产物路径改为 `self-reviews/prototype/cdn-crossref-check/report.md`，6.2（交叉引用）合并到同一报告
- [x] 2.2 修改 `.claude/skills/kflow-prototype-design/SKILL.md`：VERIFY 步骤 6.3（导航验证）报告路径从 `prototype/nav-check-round-{N}.md` 改为 `self-reviews/prototype/nav-check/round-{N}.md`
- [x] 2.3 修改 `.claude/skills/kflow-prototype-design/SKILL.md`：VERIFY 步骤 6.4（Playwright 验证）报告路径从 `prototype/playwright-check-round-{N}.md` 改为 `self-reviews/prototype/playwright-check/round-{N}.md`
- [x] 2.4 修改 `docs/designs/core-mechanisms.md`：更新 self-reviews/ 目录结构示例，增加 prototype/nav-check/、prototype/playwright-check/、prototype/cdn-crossref-check/ 子目录说明

## 3. 子代理隔离规则（问题 3）

- [x] 3.1 修改 `docs/designs/core-mechanisms.md`：新增「子代理隔离规则」章节——子代理意外停止/报错/要求重做时，主代理 MUST 重新创建子代理，SHALL NOT 接管执行；列出适用阶段清单
- [x] 3.2 修改 `.claude/skills/kflow-explore/SKILL.md`：SELFREV 步骤增加对 core-mechanisms.md 子代理隔离规则的引用
- [x] 3.3 修改 `.claude/skills/kflow-prototype-design/SKILL.md`：DESIGN/VERIFY/SELFREV 步骤增加对 core-mechanisms.md 子代理隔离规则的引用
- [x] 3.4 修改 `.claude/skills/kflow-design/SKILL.md`：SELFREV 和四视角审查步骤增加对 core-mechanisms.md 子代理隔离规则的引用
- [x] 3.5 修改 `.claude/skills/kflow-plan/SKILL.md`：Agent 迭代执行和 SELFREV 步骤增加对 core-mechanisms.md 子代理隔离规则的引用

## 4. 详细设计复杂度评估（问题 4.1）

- [x] 4.1 修改 `.claude/skills/kflow-design/SKILL.md`：步骤 4（DESIGN）每个设计域完成后增加复杂度评估——对每个 FP 评估低/中/高，生成复杂度分布表
- [x] 4.2 修改 `.claude/skills/kflow-design/SKILL.md`：步骤 4 之后、步骤 5（NFR）之前增加「高复杂度 FP 逐项确认」步骤——对每个高复杂度 FP 发起 AskUserQuestion，用户确认后方可继续
- [x] 4.3 修改 `.claude/skills/kflow-design/references/self-review.md`：可行性维度增加复杂度相关检查项（高复杂度 FP 是否已用户确认、中复杂度 FP 是否标注关键决策点）
- [x] 4.4 修改 `.claude/skills/kflow-design/SKILL.md`：输出产物表增加复杂度分布表（在 detailed-design.md 或 detailed-design/index.md 中）
- [x] 4.5 修改 `.claude/skills/kflow-design/SKILL.md`：核心提醒区增加「高复杂度 FP 必须逐项经用户确认后方可进入子变更划分」

## 5. detailed-design.md 拆分（问题 4.2）

- [x] 5.1 修改 `.claude/skills/kflow-design/SKILL.md`：输出产物表更新——FP > 20 时 `detailed-design.md` 变为 `detailed-design/` 目录（6 文件结构），FP ≤ 20 保持单文件
- [x] 5.2 修改 `.claude/skills/kflow-design/SKILL.md`：新增「详细设计文档拆分规则」章节——触发条件（FP > 20）、目录结构（index.md + architecture.md + domains/*.md + nfr.md + config-and-errors.md + subchange-division.md）、设计域文件命名规范、index.md 索引模板
- [x] 5.3 修改 `.claude/skills/kflow-design/SKILL.md`：步骤 3-4（DOMAIN + DESIGN）增加拆分模式下的输出逻辑——每个设计域独立文件写入 `detailed-design/domains/{domain-name}.md`
- [x] 5.4 修改 `.claude/skills/kflow-design/SKILL.md`：步骤 5（NFR）/5.5（CONFIG）/5.6（ERROR）在拆分模式下输出到独立文件（nfr.md、config-and-errors.md）
- [x] 5.5 修改 `.claude/skills/kflow-design/SKILL.md`：步骤 8（DIVIDE）在拆分模式下输出到 `subchange-division.md`
- [x] 5.6 修改 `.claude/skills/kflow-plan/SKILL.md`：门控检查适配——"detailed-design.md 存在"改为"detailed-design/index.md 或 detailed-design.md 存在"；READ 步骤适配目录结构

## 6. kflow-plan SELFREV（问题 5）

- [x] 6.1 修改 `.claude/skills/kflow-plan/SKILL.md`：执行流程图步骤 8（VERIFY）之后、步骤 9（COMPLETE）之前插入 SELFREV 步骤（步骤 8.5）
- [x] 6.2 修改 `.claude/skills/kflow-plan/SKILL.md`：新增「SELFREV — 10 轮自审（子代理串行 + 重复制）」步骤详情——定制 4 维度（任务覆盖完整性/DoD 验收标准正确性/HITL 标注准确性/任务粒度合理性）、每维度检查规则、子代理执行流程、报告路径（self-reviews/plan/{YYYYMMDD}-{HHMMSS}.md）、边审边修规则、强制执行规则
- [x] 6.3 修改 `.claude/skills/kflow-plan/SKILL.md`：输出产物表增加自审报告条目（self-reviews/plan/ 目录）
- [x] 6.4 修改 `.claude/skills/kflow-plan/SKILL.md`：allowed-tools 增加 Agent（子代理启动需要）
- [x] 6.5 修改 `.claude/skills/kflow-plan/SKILL.md`：核心提醒区增加「10 轮子代理自审强制执行，定制 4 维度，不可提前终止」

## 7. 设计文档同步

- [x] 7.1 修改 `docs/designs/skills/kflow-design.md`：同步复杂度评估、文档拆分、子代理隔离规则相关变更
- [x] 7.2 修改 `docs/designs/skills/kflow-plan.md`：同步 SELFREV 新增、子代理隔离规则相关变更
