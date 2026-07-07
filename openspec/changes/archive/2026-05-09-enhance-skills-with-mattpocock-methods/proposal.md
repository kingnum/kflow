## Why

当前 KFlow Skills 体系在调试系统性、领域语言对齐、测试哲学深度和任务分类方面存在方法论空白。通过引入 mattpocock-skills 中成熟的设计理念（diagnose、grill-with-docs、tdd），可以填补这些差距，提升从需求澄清到缺陷修复的全流程质量。

## What Changes

- **kflow-bug-fix 增强**：引入 diagnose 的系统化调试方法论——feedback loop 构建（10 种方法优先级排序）、可证伪多假设生成、regression test at correct seam、post-mortem 检查点
- **新增 CONTEXT.md 领域词汇表**：项目级统一领域语言，kflow-init 检测存在性，kflow-explore 增补新术语，所有后续阶段引用对齐
- **新增 ADR 架构决策记录**：在 kflow-design 阶段按三条件过滤创建（难以逆转 + 缺上下文奇怪 + 真实权衡），带过期条件标注，每变更上限控制
- **kflow-code TDD 增强**：引入 vertical slice/tracer bullet 理念、水平切片反模式警告、测试行为而非实现哲学、每周期检查清单
- **HITL/AFK 子变更分类**：子变更划分时标注 AFK（可自动执行）或 HITL（需人工决策点），指导执行策略

## Capabilities

### New Capabilities

- `diagnose-feedback-loop`: 系统化调试反馈循环构建方法论，增强 kflow-bug-fix 的 DISCOVER 步骤，引入多假设可证伪检验和 regression test at correct seam
- `domain-glossary`: 项目级 CONTEXT.md 领域词汇表，构建和维护统一领域语言，所有 Skill 以此为词汇锚点
- `adr-records`: 架构决策记录机制，在 kflow-design 阶段按三条件过滤创建，含过期条件标注和每变更上限控制
- `tdd-philosophy`: TDD 测试哲学增强，引入 tracer bullet 理念、反模式警告、测试行为而非实现原则、每周期检查清单
- `hitl-afk-classification`: 子变更 HITL/AFK 分类机制，在 kflow-design 子变更划分时标注，指导 ralph-loop 自动执行或人工决策点暂停
- `post-mortem-checkpoint`: 缺陷修复后的复盘检查点，将架构改进建议传递给 kflow-audit

### Modified Capabilities

- `defect-root-cause`: 在现有三分法分类基础上，增加系统化 feedback loop 构建步骤和可证伪多假设生成流程

## Impact

- **受影响的 Skill 设计文档（docs/designs/skills/）**：kflow-bug-fix、kflow-explore、kflow-design、kflow-code、kflow-init、kflow-audit
- **新增项目级文件**：`CONTEXT.md`（领域词汇表）、`docs/adr/`（架构决策记录目录）
- **门控规则**：kflow-init 增加 CONTEXT.md 存在性检查；kflow-design 增加 ADR 创建规则
- **状态文件**：kflow-design 的 `.status.md` 增加 ADR 记录字段；子变更划分增加 HITL/AFK 标注
