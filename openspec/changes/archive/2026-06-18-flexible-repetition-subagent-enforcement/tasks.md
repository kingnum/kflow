## 1. 权限预配置

- [x] 1.1 创建/更新 `.claude/settings.json`，在 permissions.allow 中添加 kflow 所需权限（Bash 命令模式、Read/Write/Edit、Glob/Grep、Agent、WebFetch）
- [x] 1.2 验证权限配置正确性：执行简单测试确认子代理可无阻碍使用所需工具

## 2. 子代理强制规则框前置（7 个执行类阶段 SKILL.md）

- [x] 2.1 更新 `.claude/skills/kflow-plan/SKILL.md`：在角色声明后、任务声明前添加「⚠ 子代理强制规则」引用框（4 条规则 + 引用 §12）
- [x] 2.2 更新 `.claude/skills/kflow-code/SKILL.md`：添加同样的规则框
- [x] 2.3 更新 `.claude/skills/kflow-code-review/SKILL.md`：添加同样的规则框
- [x] 2.4 更新 `.claude/skills/kflow-api-test/SKILL.md`：添加同样的规则框
- [x] 2.5 更新 `.claude/skills/kflow-e2e-test/SKILL.md`：添加同样的规则框
- [x] 2.6 更新 `.claude/skills/kflow-integration-test/SKILL.md`：添加同样的规则框
- [x] 2.7 更新 `.claude/skills/kflow-bug-fix/SKILL.md`：添加同样的规则框，移除原有的"禁止后台运行"相关硬规则

## 3. kflow-shared/repetition-model.md 更新

- [x] 3.1 新增「弹性轮次决策」章节：定义首次执行 10 轮 + 回退重执行按影响范围分数决定轮次的规则
- [x] 3.2 新增「验证门控」章节：定义非严格重复制的验证标准（受影响项 100% + 全量 1 轮兜底 + 产物完整性）
- [x] 3.3 新增「阶段执行历史追踪」章节：定义 .status.md 中执行历史表和修订信息节的格式
- [x] 3.4 新增「影响范围分数读取」章节：定义执行阶段如何从 .status.md 读取并使用影响范围分数
- [x] 3.5 更新 §12 子代理隔离规则：移除"禁止后台运行"硬规则，改为推荐前台模式 + 允许后台模式（需权限预配置）
- [x] 3.6 更新 §4 重复制执行流程图：新增 CHECK_HISTORY 步骤（检查阶段执行历史）

## 4. kflow-bug-triage SKILL.md 和设计文档更新

- [x] 4.1 更新 `.claude/skills/kflow-bug-triage/SKILL.md`：在诊断流程中新增影响范围评估步骤（DIAGNOSE 后、REPORT 前）
- [x] 4.2 更新 `.claude/skills/kflow-bug-triage/SKILL.md`：在路由输出中新增执行模式声明（EXECUTION_MODE = SUBAGENT_REQUIRED）
- [x] 4.3 更新 `.claude/skills/kflow-bug-triage/SKILL.md`：更新输出产物表，新增影响范围评估节
- [x] 4.4 更新 `docs/designs/skills/kflow-bug-triage.md`：同步 SKILL.md 的变更，新增影响范围评估章节和执行模式声明章节

## 5. kflow-bug-fix SKILL.md 和设计文档更新

- [x] 5.1 更新 `.claude/skills/kflow-bug-fix/SKILL.md`：移除 10 轮强制迭代硬规则，改为引用 kflow-shared/repetition-model.md 的弹性轮次决策
- [x] 5.2 更新 `.claude/skills/kflow-bug-fix/SKILL.md`：重复制章节新增首次执行 vs 回退重执行的区分逻辑
- [x] 5.3 更新 `.claude/skills/kflow-bug-fix/SKILL.md`：验收标准更新为弹性验证门控（受影响项 100% + 全量 1 轮兜底）
- [x] 5.4 更新 `docs/designs/skills/kflow-bug-fix.md`：同步 SKILL.md 的变更

## 6. 其他执行类阶段 SKILL.md 更新

- [x] 6.1 更新 `.claude/skills/kflow-plan/SKILL.md`：重复制章节引用弹性轮次决策，更新验收标准
- [x] 6.2 更新 `.claude/skills/kflow-code/SKILL.md`：同上
- [x] 6.3 更新 `.claude/skills/kflow-code-review/SKILL.md`：同上
- [x] 6.4 更新 `.claude/skills/kflow-api-test/SKILL.md`：同上
- [x] 6.5 更新 `.claude/skills/kflow-e2e-test/SKILL.md`：同上
- [x] 6.6 更新 `.claude/skills/kflow-integration-test/SKILL.md`：同上

## 7. 设计文档同步更新

- [x] 7.1 更新 `docs/designs/core-mechanisms/07-agent-model.md`：§15 简要概述 + 引用 kflow-shared/repetition-model.md，新增弹性重复制概述
- [x] 7.2 更新 `docs/designs/skills/kflow-plan.md`：重复制章节引用共享文件
- [x] 7.3 更新 `docs/designs/skills/kflow-code.md`：同上
- [x] 7.4 更新 `docs/designs/skills/kflow-code-review.md`：同上
- [x] 7.5 更新 `docs/designs/skills/kflow-api-test.md`：同上
- [x] 7.6 更新 `docs/designs/skills/kflow-e2e-test.md`：同上
- [x] 7.7 更新 `docs/designs/skills/kflow-integration-test.md`：同上

## 8. 模板文件更新

- [x] 8.1 更新 `.status.md` 模板：新增「阶段执行历史」表（Phase/Execution Count/Last Type/Rounds/Score/Notes）
- [x] 8.2 更新 `.status.md` 模板：新增「最近修订信息」节（Trigger/Source/Timestamp/Summary/Affected Items/Score/Rounds）
- [x] 8.3 更新 `bugs/bug-NNN-NNN.md` 模板：新增「影响范围评估」节（Affected FPs/Interfaces/Data Model/Score）
- [x] 8.4 更新 `bugs/bug-NNN-NNN.md` 模板：在解决方案节新增「执行模式声明」字段

## 9. Spec 文件更新

- [x] 9.1 将 specs/triage-impact-assessment/spec.md 归档到 openspec/specs/triage-impact-assessment/spec.md
- [x] 9.2 将 specs/flexible-repetition-mode/spec.md 归档到 openspec/specs/flexible-repetition-mode/spec.md
- [x] 9.3 将 specs/subagent-enforcement-notice/spec.md 归档到 openspec/specs/subagent-enforcement-notice/spec.md
- [x] 9.4 合并 specs/shared-repetition-model/spec.md 到 openspec/specs/shared-repetition-model/spec.md
- [x] 9.5 合并 specs/subagent-isolation-rule/spec.md 到 openspec/specs/subagent-isolation-rule/spec.md
- [x] 9.6 合并 specs/bug-triage-skill/spec.md 到 openspec/specs/bug-triage-skill/spec.md
- [x] 9.7 合并 specs/execution-repetition-mode/spec.md 到 openspec/specs/execution-repetition-mode/spec.md

## 10. 验证测试

- [x] 10.1 场景1验证：触发 kflow-bug-fix，确认子代理强制规则框生效，主 Agent 使用子代理执行
- [x] 10.2 场景2验证：触发 kflow-bug-triage → L4 路由到 kflow-bug-fix，确认路由输出包含执行模式声明，bug-fix 使用子代理执行
- [x] 10.3 场景3验证：模拟设计修订回退，确认后续阶段按影响范围分数调整重复制轮次
- [x] 10.4 场景4验证：确认权限预配置生效，子代理执行过程中无权限请求中断

