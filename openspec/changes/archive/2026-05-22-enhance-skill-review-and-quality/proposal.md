## Why

KFlow Skills 体系在实际使用中暴露了 5 类问题：RESUME 路由被 Claude Code Plan Mode 拦截导致无法正常恢复流程；原型设计审查产物散落在 prototype/ 目录而非统一的 self-reviews/ 下；子代理意外停止后主代理可能接管工作破坏隔离性；详细设计阶段缺乏复杂度评估机制导致模糊设计进入编码阶段；kflow-plan 缺乏与 explore/design 对齐的子代理重复制自审。这些问题直接影响流程可靠性和设计质量，需要在编码阶段之前系统性修复。

## What Changes

- **CLAUDE.md** 新增强制规则：用户输入匹配「继续/恢复/resume + 变更名」时禁止进入 Plan Mode
- **kflow-guide SKILL.md** description 增加 Plan Mode 绕过提示，PARSE 步骤增加优先级说明
- **kflow-prototype-design SKILL.md** 审查产物路径统一到 `self-reviews/prototype/` 下按子目录分类（nav-check/、playwright-check/、cdn-crossref-check/）
- **core-mechanisms.md** 新增子代理隔离全局规则：子代理意外停止/报错/要求重做时 MUST 重新创建子代理，主代理 SHALL NOT 接管
- **kflow-design SKILL.md** 步骤 4 新增功能点复杂度评估（低/中/高），高复杂度 FP 逐项 AskUserQuestion 确认；FP > 20 时 detailed-design.md 强制拆分为 `detailed-design/` 目录（6 文件结构）
- **kflow-plan SKILL.md** 新增 SELFREV 步骤：10 轮子代理串行+重复制，定制 4 维度（任务覆盖完整性/DoD 验收标准正确性/HITL 标注准确性/任务粒度合理性）
- 涉及 Skill 的 references 子目录和设计文档同步更新

## Capabilities

### New Capabilities

- `resume-plan-mode-bypass`: RESUME 路由优先级保障——在 CLAUDE.md 和 kflow-guide 中强制要求「继续/恢复/resume + 变更名」模式跳过 Plan Mode，直接进入 Skill 路由链
- `subagent-isolation-rule`: 子代理隔离强制规则——所有使用子代理的阶段必须遵守：子代理异常停止时主代理 MUST 重新创建子代理，SHALL NOT 接管执行
- `design-complexity-gate`: 详细设计复杂度评估门控——对每个 FP 评估复杂度（低/中/高），高复杂度 FP 必须逐项 AskUserQuestion 与用户确认实现细节后方可继续
- `design-doc-directory`: detailed-design.md 目录化拆分——FP > 20 时强制拆分为 `detailed-design/` 目录（index.md + architecture.md + domains/*.md + nfr.md + config-and-errors.md + subchange-division.md）
- `plan-self-review`: 计划阶段子代理重复制自审——10 轮子代理串行执行，每轮全 4 维度（任务覆盖完整性/DoD 验收标准正确性/HITL 标注准确性/任务粒度合理性），边审边修，报告输出到 `self-reviews/plan/`
- `prototype-review-artifacts`: 原型设计审查产物路径统一——导航验证、Playwright 验证、CDN 扫描/交叉引用报告全部迁移到 `self-reviews/prototype/` 子目录

### Modified Capabilities

- `phase-self-review`: 自审覆盖面从 explore/design/prototype 扩展到 plan，所有执行类阶段统一使用子代理重复制自审
- `subagent-self-review`: 子代理自审规则增加隔离约束——子代理异常时主代理不得接管
- `prototype-navigation-verification`: 导航验证报告输出路径从 `prototype/nav-check-round-{N}.md` 变更为 `self-reviews/prototype/nav-check/round-{N}.md`
- `prototype-playwright-5round-verification`: Playwright 验证报告输出路径从 `prototype/playwright-check-round-{N}.md` 变更为 `self-reviews/prototype/playwright-check/round-{N}.md`
- `large-doc-splitting`: 大文档拆分规则扩展，新增 detailed-design.md 目录化拆分（FP > 20 阈值 + 6 文件结构模板）
- `design-level-restructure`: detailed-design.md 结构更新——支持单文件或目录两种形态，增加 index.md 索引模板

## Impact

- **Skills**: kflow-guide, kflow-explore, kflow-prototype-design, kflow-design, kflow-plan（5 个 SKILL.md + 1 个 references/self-review.md）
- **核心机制**: core-mechanisms.md（目录结构规范 + 子代理隔离规则）
- **设计文档**: docs/designs/skills/kflow-design.md, docs/designs/skills/kflow-plan.md（与 SKILL.md 同步）
- **项目配置**: CLAUDE.md（Plan Mode 禁止指令）
- **无破坏性变更**: 仅修改内部流程和产物路径，不影响已归档变更
