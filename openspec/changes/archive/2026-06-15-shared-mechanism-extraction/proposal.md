## Why

核心机制文档（`docs/designs/core-mechanisms/`）中定义的通用机制（重复制执行模式、10轮自审、门控规则、状态值定义、恢复流程、归档条件等）被大量复制到 7+ 个 Skill 设计文档中，造成约 700 行冗余。核心机制文档之间也存在重复（端口冲突检测在 05/09 重复，回退规则在 03/04 重复，服务超时链在 05/09 重复）。冗余导致修改时容易遗漏同步，且子代理每次冷启动加载全量核心机制文档（~10K tokens）存在优化空间。

## What Changes

- 将 6 类通用机制从核心机制文档抽取到 `.claude/skills/kflow-shared/` 目录，建立"单一事实源"
- 核心机制文档改为引用 `kflow-shared/` 共享文件，删除重复段落
- 各 Skill 设计文档中的大段重复内容替换为引用
- 删除 `04-gates-and-transitions.md` 内部重复（§6.9 与 §6.6 重复）
- `05-execution-services.md` 中与 `service-lifecycle.md` 重复的服务管理细节删除

## Capabilities

### New Capabilities
- `shared-repetition-model`: 重复制执行规范统一共享文件（复杂度公式、10轮规则、验收标准、子代理prompt规范）
- `shared-self-review`: 10轮自审通用规范共享文件（流程、记录存储、报告规范）
- `shared-gate-rules`: 门控规则统一定义共享文件（9个门控规则 + 回退规则）
- `shared-state-values`: 状态值定义共享文件（13种状态的唯一规范）
- `shared-recovery-protocol`: 恢复优先级链与流程共享文件
- `shared-archive-rules`: 归档条件 + 设计合并流程共享文件

### Modified Capabilities
- `execution-repetition-mode`: 核心定义迁移到 kflow-shared/repetition-model.md，核心机制文档改为引用
- `phase-self-review`: 核心定义迁移到 kflow-shared/self-review.md，核心机制文档改为引用
- `phase-hooks`: 删除与 05-execution-services.md 重复的服务管理段落，改为引用 service-lifecycle.md
- `devflow-archive`: 归档条件定义迁移到 kflow-shared/archive-rules.md
- `two-level-checkpoint`: 恢复流程定义迁移到 kflow-shared/recovery-protocol.md
- `resume-five-question-summary`: 引用恢复流程改为指向 kflow-shared/recovery-protocol.md

## Impact

- **核心机制文档**: 03-status-and-tasks.md, 04-gates-and-transitions.md, 05-execution-services.md, 06-recovery.md, 07-agent-model.md, 09-phase-hooks.md — 删除重复段落，替换为引用
- **kflow-shared/**: 新增 6 个共享定义文件
- **Skill 设计文档**: kflow-code.md, kflow-code-review.md, kflow-api-test.md, kflow-e2e-test.md, kflow-integration-test.md, kflow-archive.md, kflow-resume.md — 重复段落替换为引用
- **运行时 SKILL.md**: 本变更不涉及，后续 skill-align-* 变更处理
