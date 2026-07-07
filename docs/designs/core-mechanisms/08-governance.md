# KFlow Skills 核心运行机制

> **版本**: 参见仓库根目录 `VERSION` 文件
> **创建时间**: 2026-04-29
> **更新时间**: 2026-05-17

> **加载层级**: 基础层
> **适用阶段**: 全部

本文档定义 KFlow Skills 体系的核心运行机制，包括目录结构、状态文件、任务清单、阶段流转规则、回退机制和条件产物引用规范。

---


## 十七、阶段边界强制

> **版本**: 1.10.0 新增

### 17.1 概述

每个阶段采用文档白名单模式，只允许创建其输出产物表中列出的文件。信息不足时记录到 `docs/skill-suggestion.md`，禁止自创新文档填补信息空缺。无论用户输入来源（口述/文件/URL），各阶段必须生成完整的标准输出产物。

### 17.2 文档创建白名单模式

每个阶段仅允许创建其"输出产物"表中列出的文件：

| 阶段 | 允许创建的文件（白名单） |
|------|------------------------|
| explore | functional-designs/index.md, functional-designs/part-NN.md, CONTEXT.md, .status.md |
| prototype | prototype/index.md, prototype/verify-report.md, .status.md（用户评审记录） |
| design | detailed-design.md, traceability.md, api-tests/*, e2e-tests/*, integration-tests/*, self-reviews/design/*.md, cross-reviews/*, .status.md, docs/adr/*（条件） |
| plan | subchanges/{subchange}/tasks.md, subchanges/{subchange}/.status.md |
| code | 代码文件, migrations/*, docs/service-guide.md, subchanges/{subchange}/.status.md |
| code-review | subchanges/{subchange}/test-reports/review/code-review.md, subchanges/{subchange}/.status.md |
| e2e-test | subchanges/{subchange}/test-reports/e2e/*, subchanges/{subchange}/test-reports/api/*, subchanges/{subchange}/.status.md |
| bug-fix | subchanges/{subchange}/test-reports/fix-reports/*, subchanges/{subchange}/.status.md |
| integration-test | test-reports/integration/*, .status.md |
| archive | docs/archive/*, docs/designs/index.md, docs/changes/index.md, .status.md |

**白名单违规处理**：
- 尝试创建白名单外文件 → 禁止创建
- 如内容确有必要 → 记录到 `docs/skill-suggestion.md`
- 如确需扩展文档结构 → 通过 skill-suggestion 提议流程改进

### 17.3 标准产物强制生成

无论用户输入来源是什么，各阶段 MUST 生成完整的标准输出产物：

| 输入来源 | 处理方式 | 禁止行为 |
|---------|---------|---------|
| 用户口述需求 | 基于对话内容生成完整标准产物 | 不可因"用户描述不够详细"而跳过产物生成 |
| 用户以文件提供需求 | 读取文件后仍需生成完整的标准产物 | 不可直接引用用户文件替代标准产物 |
| 用户以 URL 提供需求 | 读取 URL 内容后仍需生成完整的标准产物 | 不可仅保存 URL 引用作为替代 |

**产物质量标准**：标准产物质量与输入来源无关，所有输入来源产出的产物质量一致。

### 17.4 信息不足溢出路径

当当前阶段文档内容无法满足需求时：

```
信息不足处理流程:

发现信息不足
    │
    ├── 步骤 1: 在当前阶段文档中标记"待补充"
    │         └── 说明具体缺少什么信息
    │
    ├── 步骤 2: 记录到 docs/skill-suggestion.md
    │         └── 作为流程改进建议
    │
    └── 步骤 3: 禁止自创新文档来填补信息空缺
              └── 如需扩展文档结构，通过 skill-suggestion 提议
```

### 17.5 阶段内容禁止越界

每个阶段仅输出其职责范围内的内容，禁止输出后续阶段的职责内容：

| 阶段 | 域内（允许） | 域外（禁止） |
|------|------------|------------|
| explore | 用户视角：页面结构/菜单层级/可执行操作/表单项定义/业务规则 | 技术架构选型、数据模型设计、接口定义 |
| prototype | UI原型/交互流程/视觉风格 | 功能决策变更、业务规则修改、技术实现决策 |
| design | 系统架构/数据模型/接口设计/NFR/子变更划分/测试用例 | functional-designs/ 修改、prototype/ 修改 |

**数据流向规则**：
- explore 输出 → prototype 输入（只读）
- explore + prototype 输出 → design 输入（只读）
- 下游不可修改上游产物

### 17.6 越界处理

当下游阶段发现上游产物存在问题时：

```
发现上游问题:
    │
    ├── 步骤 1: 记录到 docs/skill-suggestion.md
    │
    ├── 步骤 2: 提示用户是否需要阶段回退
    │
    └── 步骤 3: 禁止直接修改上游产物来"修复"问题
```

**阶段回退提醒**：

| 场景 | 记录方式 | 建议动作 |
|------|---------|---------|
| design 发现功能设计不完整 | skill-suggestion.md | 提示回退到 explore 阶段补充 |
| prototype 发现功能点定义不清晰 | skill-suggestion.md | 在当前能力范围内完成原型 + 提示需回退 explore |
| prototype 发现功能设计不完整 | skill-suggestion.md | 提示回退 explore 补充功能点描述 |
| code 发现原型交互/视觉/状态问题 | skill-suggestion.md | 通过 AskUserQuestion 确认后回退到 prototype-design（REVISION 模式） |
| code 发现功能点/业务规则需调整 | skill-suggestion.md | 通过 AskUserQuestion 确认后回退到 explore（功能性）或 design（技术性） |

### 17.7 前端子变更阶段边界约束

前端子变更与后端子变更之间存在共享文件冲突风险，SHALL 遵循以下边界约束：

| 约束 | 说明 |
|------|------|
| 文件隔离 | 前端子变更操作前端代码（组件/路由/样式/状态管理），后端子变更操作后端代码（API/服务/数据模型），禁止跨域修改 |
| 依赖方向 | 前端子变更依赖 API 契约（design 阶段已定义），不依赖后端子变更编码完成 |
| 并行策略 | 前端子变更可与后端子变更并行启动（使用 mock 数据），后端编码完成后执行集成对接 |
| 共享文件处理 | 公共配置文件（如 package.json、路由注册入口）由前端子变更负责，后端子变更不修改；如确需修改，由变更级 agent 统一处理 |
| 前端 FP > 10 时 | 拆分为「骨架子变更」（脚手架/路由/布局/组件库/设计令牌）+ 串行「页面组子变更」，骨架先行建立共享基础设施 |

---

## 十八、Git 版本管理机制

> **版本**: 2.0.0 新增

### 18.1 概述

本机制在 KFlow Skills 体系的关键节点使用 git 版本管理，确保变更边界的可追溯性：

| 节点 | 触发时机 | 执行者 | 提交信息格式 |
|------|---------|--------|-------------|
| 归档后 | kflow-archive 归档流程完成，询问用户确认 | kflow-archive | `归档变更 {name}: {一行摘要}` |

此外，kflow-init 在首次初始化时检测目录是否为 git 仓库，若非仓库则询问用户是否执行 `git init`（不自动 commit）。

### 18.2 提交信息格式规范

统一采用简洁的一行中文摘要格式（仅归档后提交使用）：

| 场景 | 格式 | 示例 |
|------|------|------|
| 归档已完成 | `归档变更 {name}: {摘要}` | `归档变更 add-2fa: 新增双因素认证，更新认证域文档` |
| 归档未完成 | `归档变更 {name}(未完成): {归档原因}` | `归档变更 refactor-user(未完成): 中途归档` |

### 18.3 提交失败处理

所有 git commit 操作失败时，不阻塞主流程：

| 失败原因 | 处理方式 |
|---------|---------|
| 无变更内容 | 提示"无内容需要提交"，正常继续 |
| git 配置问题 | 提示失败原因和修复建议，建议用户手动提交 |
| 用户选择跳过 | 输出提醒"归档内容尚未提交"，不阻塞归档流程 |

### 18.4 不自动 push

所有 git commit 操作不自动 push 到远程仓库。push 操作由用户自行决定时机。

### 18.5 强制规则注入

kflow-init 在向 CLAUDE.md 注入「变更流程强制规则」时，包含以下 git 规则：

1. **首次 init 时，若目录非 git 仓库，询问是否执行 git init**
2. **归档完成后，询问是否将当前变更及相关文件提交 git**（若确认，则在 commit 前执行版本自增和打包）
