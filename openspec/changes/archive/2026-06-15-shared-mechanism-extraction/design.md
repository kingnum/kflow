## Context

KFlow Skills 体系的核心机制文档（`docs/designs/core-mechanisms/`，9 个文件共 3,111 行）定义了阶段门控、状态管理、执行模型、恢复机制等通用规范。审查发现这些通用机制在 Skill 设计文档中被大量复制：

- 重复制执行模式（07-agent-model.md §15，170 行）→ 被 5 个执行类 Skill 设计文档各复制 ~70 行
- 10 轮自审（07-agent-model.md §16，210 行）→ 被 explore/design/prototype 设计文档复制
- 门控规则（03-status-and-tasks.md §3.4，200 行）→ 与 04-gates-and-transitions.md §6.5 重复
- 归档条件（04-gates-and-transitions.md §6.3，120 行）→ 与 kflow-archive.md 几乎逐字重复
- 恢复流程（06-recovery.md §12.2-12.3，60 行）→ 与 kflow-resume.md 几乎逐字重复
- 服务管理（05-execution-services.md §7.7-8.2，90 行）→ 与 09-phase-hooks.md + service-lifecycle.md 重复

总计约 700 行跨层冗余，修改时容易遗漏同步。

## Goals / Non-Goals

**Goals:**
- 建立 `kflow-shared/` 作为通用机制的"单一事实源"
- 核心机制文档保留索引和上下文说明，具体规范引用 `kflow-shared/`
- Skill 设计文档引用 `kflow-shared/`，仅保留阶段特定参数
- 消除核心机制文档间的重复段落
- 为后续 Token 分层加载优化奠定文件结构基础

**Non-Goals:**
- 不修改运行时 SKILL.md（后续 skill-align-* 变更处理）
- 不改变任何机制的语义或行为（纯结构重构）
- 不合并或重组核心机制文件的章节编号
- 不新增任何机制规则

## Decisions

### D1: 共享文件存放位置

**决策**: 共享定义文件放在 `.claude/skills/kflow-shared/` 目录下（与已有的 `phase-hooks.md`、`service-lifecycle.md` 同级）。

**理由**: kflow-shared 已被 CLAUDE.md 和核心机制文档引用为"运行时共享文件"目录。将设计层的共享定义也放在此处，形成统一的引用入口。子代理只需加载 `kflow-shared/` 即可获得所有共享规范，无需再加载核心机制文档中的重复内容。

**新增文件清单**:

| 文件 | 来源 | 内容 |
|------|------|------|
| `repetition-model.md` | 07-agent-model.md §15 | 复杂度公式、10轮规则、验收标准、prompt规范、子代理隔离规则 |
| `self-review.md` | 07-agent-model.md §16 | 自审流程、三阶段维度表、记录存储、报告规范、VERIFY子代理验证 |
| `gate-rules.md` | 03-status-and-tasks.md §3.4 | 9个门控规则、回退门控、HITL阻塞plan入口规则 |
| `state-values.md` | 03-status-and-tasks.md §3.3 | 13种状态值定义（✅/🔄/⏳/❌/⚠️/⏸️等） |
| `recovery-protocol.md` | 06-recovery.md §12.2-12.3 | checkpoint两级存储、5级恢复优先级链、调度映射表 |
| `archive-rules.md` | 04-gates-and-transitions.md §6.3-6.3.1 | 归档条件检查清单、设计合并7步工作流、归档后禁止操作 |

### D2: 核心机制文档的改造方式

**决策**: 核心机制文档保留原有章节结构，在具体规范段落处替换为引用指令。

**改造模式**:
```markdown
## 十五、子代理执行模型

> 完整规范参见 `kflow-shared/repetition-model.md`

### 15.1 概述
（保留简短概述，1-2句）

### 15.2 阶段分类
（保留分类表，但标注"详细规范参见 kflow-shared/repetition-model.md §X"）
```

**原则**:
- 保留章节编号和标题（维持导航结构）
- 删除重复的详细规范段落（>10行的完整规则定义）
- 保留简短概述和分类表（<10行的索引性内容）
- 每个被改造的章节开头添加引用指令

### D3: Skill 设计文档的改造方式

**决策**: 各 Skill 设计文档中的通用机制段落替换为单行引用 + 阶段特定参数。

**改造模式**:
```markdown
## 重复制执行

> 通用规范参见 `kflow-shared/repetition-model.md`

### 阶段特定参数
- 复杂度权重: 功能点数 × 1 + 接口数 × 1.5 + 场景数 × 2（编码阶段）
- 工作项定义: 全部功能点的 TDD 循环
- 产物要求: traceability.md 编码列覆盖率 100%
```

### D4: 核心机制文档间重复的消除

| 重复内容 | 保留位置 | 删除位置 |
|---------|---------|---------|
| 端口冲突检测（3场景） | `09-phase-hooks.md` §八 | `05-execution-services.md` §7.7 |
| 服务停止超时链 | `09-phase-hooks.md` §七 | `05-execution-services.md` §7.8 |
| 服务刷新流程 | `09-phase-hooks.md` §三 | `05-execution-services.md` §8.2（保留概述，删除详细步骤） |
| 回退触发来源 + 门控 | `04-gates-and-transitions.md` §6.5 | `03-status-and-tasks.md` §3.4 的回退部分 |
| 编码阶段上游问题决策流程 §6.9 | 保留 §6.6 | 删除 §6.9 |

### D5: 引用格式规范

**决策**: 统一使用 Markdown 引用格式：
```markdown
> 完整规范参见 `kflow-shared/{filename}.md` {§section}
```

不使用链接格式（`[text](path)`），因为 `kflow-shared/` 文件是 Skill 加载路径，不是文档导航路径。引用格式明确指示 AI 在运行时加载对应文件。

## Risks / Trade-offs

| 风险 | 影响 | 缓解措施 |
|------|------|---------|
| 引用链过长：子代理需要理解"参见 X 文件"并加载 | 可能增加子代理的解析开销 | 子代理 prompt 中直接列出需要加载的 kflow-shared 文件路径 |
| 结构重构后核心机制文档的可读性下降（大量"参见"指令） | 人类阅读时需要跳转多个文件 | 保留概述和分类表，确保核心机制文档仍可作为索引快速浏览 |
| 共享文件内容过于庞大 | kflow-shared/ 文件总行数可能超过 1000 行 | 每个共享文件聚焦单一机制，最大文件预估 < 300 行 |
| 改造过程中遗漏某处引用 | 导致冗余未完全消除 | 改造完成后执行全文搜索验证，确保核心机制中的被迁移内容不再有第二处完整定义 |
