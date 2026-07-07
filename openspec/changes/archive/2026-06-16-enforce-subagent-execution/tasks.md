## 1. 共享文档强化

- [x] 1.1 强化 `kflow-shared/repetition-model.md` §12：新增 §12.1 主 Agent 职责边界硬线声明（调度+验收，SHALL NOT 执行阶段主工作，无例外）
- [x] 1.2 强化 `kflow-shared/repetition-model.md` §12：细化 §12.2 重试粒度为轮次级（某轮子代理崩溃 → 新建 Agent 重跑该轮，≤3 次重试，全部失败标记 ⚠️ 阻塞）
- [x] 1.3 强化 `kflow-shared/repetition-model.md` §12：更新 §12.3 适用阶段清单，补全全部 7 个执行类阶段并区分「隔离规则」和「子代理强制规则」适用范围

## 2. 运行时 SKILL.md 更新（7 个执行类阶段）

- [x] 2.1 `kflow-plan/SKILL.md`：在重复制执行流程章节前新增「⚠ 子代理强制规则」引用框（3 条规则 + 引用 repetition-model.md §12）
- [x] 2.2 `kflow-code/SKILL.md`：在重复制执行流程章节前新增「⚠ 子代理强制规则」引用框
- [x] 2.3 `kflow-code-review/SKILL.md`：在重复制执行流程章节前新增「⚠ 子代理强制规则」引用框
- [x] 2.4 `kflow-api-test/SKILL.md`：在重复制执行流程章节前新增「⚠ 子代理强制规则」引用框
- [x] 2.5 `kflow-e2e-test/SKILL.md`：在重复制执行流程章节前新增「⚠ 子代理强制规则」引用框
- [x] 2.6 `kflow-integration-test/SKILL.md`：在重复制执行流程章节前新增「⚠ 子代理强制规则」引用框
- [x] 2.7 `kflow-bug-fix/SKILL.md`：在重复制执行流程章节前新增「⚠ 子代理强制规则」引用框

## 3. 设计文档同步

- [x] 3.1 更新 `docs/designs/skills/kflow-plan.md`：同步子代理强制规则变更
- [x] 3.2 更新 `docs/designs/skills/kflow-code.md`：同步子代理强制规则变更
- [x] 3.3 更新 `docs/designs/skills/kflow-code-review.md`：同步子代理强制规则变更
- [x] 3.4 更新 `docs/designs/skills/kflow-api-test.md`：同步子代理强制规则变更
- [x] 3.5 更新 `docs/designs/skills/kflow-e2e-test.md`：同步子代理强制规则变更
- [x] 3.6 更新 `docs/designs/skills/kflow-integration-test.md`：同步子代理强制规则变更
- [x] 3.7 更新 `docs/designs/skills/kflow-bug-fix.md`：同步子代理强制规则变更
- [x] 3.8 更新 `docs/designs/core-mechanisms/07-agent-model.md`：同步 §12 变更描述

## 4. Openspec Specs 更新

- [x] 4.1 更新 `openspec/specs/subagent-isolation-rule/spec.md`：新增主 Agent 职责边界硬线要求 + 轮次级重试机制要求 + SKILL.md 内联规则框要求；修改现有适用范围要求
- [x] 4.2 更新 `openspec/specs/shared-repetition-model/spec.md`：修改共享文件定义要求，包含 §12 强化内容

## 5. SKILL.md 同步验证

- [x] 5.1 使用 `/kflow-skills-auditor` 审查更新后的 7 个运行时 SKILL.md，确认规则框格式和内容一致性
- [x] 5.2 使用 `/skill-creator` 根据变更后的设计文档更新对应的运行时 Skill（设计文档 → SKILL.md 同步）
