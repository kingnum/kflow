## 1. 创建 kflow-shared 共享文件

- [x] 1.1 创建 `.claude/skills/kflow-shared/repetition-model.md`——从 `07-agent-model.md` §15 抽取重复制执行规范（复杂度公式、10轮规则、验收标准、子代理prompt规范、子代理隔离规则），保留完整内容
- [x] 1.2 创建 `.claude/skills/kflow-shared/self-review.md`——从 `07-agent-model.md` §16 抽取10轮自审规范（流程、三阶段维度表、记录存储、报告格式、VERIFY子代理验证机制），保留完整内容
- [x] 1.3 创建 `.claude/skills/kflow-shared/gate-rules.md`——从 `03-status-and-tasks.md` §3.4 抽取9个门控规则 + 回退门控规则 + HITL阻塞plan入口规则 + 编码阶段上游问题决策流程，保留完整内容
- [x] 1.4 创建 `.claude/skills/kflow-shared/state-values.md`——从 `03-status-and-tasks.md` §3.3 抽取13种状态值定义及转换规则，保留完整内容
- [x] 1.5 创建 `.claude/skills/kflow-shared/recovery-protocol.md`——从 `06-recovery.md` §12.2-12.3 抽取checkpoint两级存储、5级恢复优先级链、调度映射表、恢复流程，保留完整内容
- [x] 1.6 创建 `.claude/skills/kflow-shared/archive-rules.md`——从 `04-gates-and-transitions.md` §6.3-6.3.1, §6.4, §6.7 抽取归档条件检查清单、设计合并7步工作流、归档后禁止操作、归档禁止自动流转规则，保留完整内容

## 2. 改造核心机制文档（引用替换）

- [x] 2.1 改造 `07-agent-model.md`——§15 重复制执行模型替换为概述(≤5行) + `> 完整规范参见 kflow-shared/repetition-model.md`；§16 自审机制替换为概述(≤5行) + `> 完整规范参见 kflow-shared/self-review.md`
- [x] 2.2 改造 `03-status-and-tasks.md`——§3.3 状态值表替换为 `> 完整规范参见 kflow-shared/state-values.md`；§3.4 门控规则替换为 `> 完整规范参见 kflow-shared/gate-rules.md`；保留回退部分的简短描述，删除与 04 重复的回退触发来源列表
- [x] 2.3 改造 `04-gates-and-transitions.md`——§6.3/§6.3.1/§6.4/§6.7 归档相关内容替换为 `> 完整规范参见 kflow-shared/archive-rules.md`；§6.5 回退规则替换为引用 `kflow-shared/gate-rules.md`；删除 §6.9（与 §6.6 重复）
- [x] 2.4 改造 `05-execution-services.md`——删除 §7.7 端口冲突检测（已在 `09-phase-hooks.md` §八 和 `service-lifecycle.md` §二 定义）替换为引用；删除 §7.8 超时链替换为引用；§8.2 保留同步点表格，删除详细服务刷新步骤替换为引用 `service-lifecycle.md`
- [x] 2.5 改造 `06-recovery.md`——§12.2 checkpoint存储 + §12.3 恢复流程替换为 `> 完整规范参见 kflow-shared/recovery-protocol.md`，保留概述

## 3. 改造 Skill 设计文档（冗余替换）

- [x] 3.1 改造 `docs/designs/skills/kflow-code.md`——重复制段落(~70行)替换为引用 `kflow-shared/repetition-model.md` + 仅保留阶段特定参数（复杂度权重、工作项定义、产物要求）
- [x] 3.2 改造 `docs/designs/skills/kflow-code-review.md`——同上，重复制段落替换为引用 + 阶段特定参数
- [x] 3.3 改造 `docs/designs/skills/kflow-api-test.md`——同上 + 服务管理约束段落替换为引用 `kflow-shared/service-lifecycle.md`
- [x] 3.4 改造 `docs/designs/skills/kflow-e2e-test.md`——同上
- [x] 3.5 改造 `docs/designs/skills/kflow-integration-test.md`——同上
- [x] 3.6 改造 `docs/designs/skills/kflow-archive.md`——归档条件和设计合并流程替换为引用 `kflow-shared/archive-rules.md`
- [x] 3.7 改造 `docs/designs/skills/kflow-resume.md`——恢复流程和优先级链替换为引用 `kflow-shared/recovery-protocol.md`

## 4. 验证

- [x] 4.1 全文搜索验证：确认核心机制文档中被迁移的内容（重复制规则、自审流程、门控规则、状态值、恢复流程、归档条件）不再有第二处完整定义
- [x] 4.2 确认所有 kflow-shared/ 新增文件的内容完整性——与原核心机制文档中的内容逐段比对，确保无遗漏
- [x] 4.3 确认各 Skill 设计文档中的引用格式统一：`> 完整规范参见 kflow-shared/{filename}.md`
