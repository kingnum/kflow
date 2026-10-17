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
| prototype | 产品级 docs/designs/prototypes/（index.html、manifest.md、design-tokens.css、design-system/MASTER.md、screens/*、components/*、assets/*）、变更级 prototype-changes.md, prototype-backup/*, prototype-plan/*, element-coverage-tree.md, self-reviews/prototype/*, .status.md（含审查方式记录） |
| design | detailed-design.md, traceability.md, api-tests/*, e2e-tests/*, integration-tests/*, self-reviews/design/*.md, cross-reviews/*, .status.md, docs/adr/*（条件） |
| plan | subchanges/{subchange}/tasks.md, subchanges/{subchange}/.status.md |
| code | 代码文件, migrations/*, docs/service-guide.md, subchanges/{subchange}/.status.md |
| code-review | subchanges/{subchange}/test-reports/review/code-review.md, subchanges/{subchange}/.status.md |
| e2e-test | subchanges/{subchange}/test-reports/e2e/*, subchanges/{subchange}/test-reports/api/*, subchanges/{subchange}/.status.md |
| bug-fix | subchanges/{subchange}/test-reports/fix-reports/*, subchanges/{subchange}/.status.md |
| integration-test | test-reports/integration/*, .status.md |
| archive | docs/changes/archive/*, docs/designs/index.md, docs/changes/index.md, .status.md |

**白名单违规处理**：
- 尝试创建白名单外文件 → 禁止创建
- 如内容确有必要 → 记录到 `docs/skill-suggestion.md`
- 如确需扩展文档结构 → 通过 skill-suggestion 提议流程改进

**白名单的档位适配**（轮次与审查形态均由变更级 `.status.md` 的 `变更档位` 字段驱动）：

| 产物目录 | 档位适配规则 |
|---------|-------------|
| `self-reviews/{phase}/` | 设计类与计划阶段的自审**固定单轮**（轮数恒为 1，无 0 轮豁免路径）；变更档位只决定审查形态与产出深度，SHALL NOT 决定轮数。全部档位均 SHALL 执行该单轮验证并创建该目录；仅 prototype 阶段选择「人工审查」时完全跳过自审，该目录 SHALL NOT 创建，且不构成白名单违规。**报告命名**：自审报告固定为 `report.md`（不按轮次编号）；prototype 的 VERIFY 合并报告固定为 `verify-report.md`（五分区，仅「子代理自动审查验证」路径产出）；两者均计入白名单 |
| `cross-reviews/` | 目录内视角报告数量按档位确定（轻量仅 `synthesis.md` / 标准两份视角报告 + `synthesis.md`）。历史遗留的四份视角报告存在时不构成白名单违规 |
| `.status.md` | 基本信息 SHALL 含 `变更档位` 字段；缺省或读取到历史遗留的 `完整` 取值时按 `标准` 档处理 |
| 裁剪阶段产物 | `轻量` 档下被判定为 `⏭️ 不适用` 的阶段不产出 `api-tests/`、`e2e-tests/`、`test-reports/integration/`，不构成白名单违规 |

> 白名单是「允许创建的集合」而非「必须创建的清单」——档位裁剪掉的产物不创建，不触发违规判定，审计亦不因此判为缺项。**自审报告在允许集合内**：`report.md` 固定一份（原型阶段另有 `verify-report.md`），不构成白名单违规，亦不判「轮次超标」。

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

### 17.8 阶段裁剪的治理口径

阶段裁剪是变更档位为 `轻量` 时的合法流程，其合法性由**声明依据**而非产物存在性判定。治理口径如下：

| 原则 | 说明 |
|------|------|
| 裁剪范围限定 | 仅 `轻量` 档的 `接口单元测试`、`E2E测试`、`集成测试` 三阶段可裁剪；`标准` 档 SHALL NOT 裁剪 |
| 合法性凭证 | 裁剪的合法前提是变更级 `.status.md` 的「阶段适用性声明」区中存在对应判定依据 |
| 无依据一律阻塞 | 无阶段适用性声明依据的 `⏭️`，在阶段门控、轻量自检、归档门控、产物诊断中 SHALL 一律判为阻塞，不因标记来源或标记者而豁免。本规则仅约束声称由**变更档位裁剪**产生的 `⏭️`；由**项目类型**产生的 `⏭️`（如纯后端项目的 E2E测试阶段与 E2E测试列）依据项目类型判定、与档位无关，SHALL NOT 要求适用性声明依据，且优先判定 |
| 声明与产物一致 | 声明 `⏭️ 不适用` 而产物存在时判为不一致并阻塞；声明 `✅ 适用` 而产物缺失时判为缺项并阻塞 |
| 白名单豁免 | 被裁剪阶段不创建其产物目录，SHALL NOT 构成 §17.2 白名单违规，审计亦 SHALL NOT 因此判为缺项 |
| 覆盖率分母排除 | `traceability.md` 中被裁剪的阶段整列填充 `⏭️` 并从覆盖率分母移除（`覆盖率 = 已填充格数 / (总格数 - 不适用格数)`）；该列 SHALL NOT 产生缺口追踪记录 |
| 保守回退 | 判定依据不可读（产物不存在、格式不符、字段缺失）时该阶段判为 `✅ 适用`——裁剪是优化而非正确性要求，失败方向 MUST 偏向执行 |
| 禁止降档 | 阶段适用性声明生成后，变更档位只允许升档；档位下调会使已生成的裁剪失去依据，故被禁止 |

> 裁剪的判定条件、声明写入位置与四态判定矩阵分别参见 `03-status-and-tasks.md` §3.1.2 与 `04-gates-and-transitions.md` §5.4。

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

### 18.5 强制规则注入的作用域边界

kflow-init 注入消费方 CLAUDE.md 的「变更流程强制规则」section SHALL NOT 包含 git 规则。本节所述两项 git 行为均在 skill 自身的执行流程中完成，写入消费方 CLAUDE.md 即构成双重定义：

| 事项 | 承载位置 |
|------|---------|
| 归档完成后询问是否执行 git commit | `kflow-archive` 的归档流程（§18.1 表中「归档后」节点） |
| 首次 init 时目录非 git 仓库，询问是否执行 git init | `kflow-init` 的步骤 GIT INIT（§18.1 末段） |

注入模板的模板版本标识取自 kflow-init 自身 front matter 的 `version` 字段，SHALL NOT 引用消费方项目中可能不存在的文件。

> kflow-init 注入的「变更流程强制规则」只承载跨 skill 的路由约束、用户接口约定与流程概览，其内容要求由 `init-claude-md-injection` 能力定义。本仓库自身归档后的版本自增与打包流程适用于 KFlow Skills 开发仓库，不属于消费方项目的注入规则——详见本仓库归档后规则（`CLAUDE.md`）。

---

## 十九、主 Agent 职责边界遵守核验

### 19.1 核验项

审计阶段 SHALL 核验执行类阶段主 Agent 的职责边界遵守情况，核验结论计入记账职责 (a) 门控校验的发现项。核验以两类可观测证据为依据：

| 证据 | 来源 | 用途 |
|------|------|------|
| 门控拒绝记录 | `.claude/kflow-gating.log`（门控脚本每次拒绝时追加） | 判定主 Agent 是否曾尝试执行阶段主工作，以及被拒后是否改为派发子代理 |
| 工具调用分布 | 主会话与子代理 transcript | 判定主 Agent 是否实际承担了阶段主工作（直接写入、运行测试等） |

### 19.2 判定口径

| 情形 | 判定 |
|------|------|
| 存在门控拒绝记录，且主 Agent 随后创建子代理完成该工作 | ✅ 合规——门控按设计生效，主 Agent 已改派 |
| 无门控拒绝记录，且工具调用分布中主 Agent 在非白名单路径的 `Edit`/`Write` 为 0、长输出命令为 0 | ✅ 合规 |
| 存在门控拒绝记录，但主 Agent 仍以其他方式（如绕过门控的路径写入、以子代理名义但内容由主 Agent 生成）完成阶段主工作 | ❌ 发现项——记录为「主 Agent 承担阶段主工作」 |
| 工具调用分布显示主 Agent 在执行类阶段直接写入非白名单文件或直接运行长输出测试命令（且无对应门控拒绝记录，说明门控未生效） | ❌ 发现项，同时记录「门控未生效」 |

### 19.3 记录与降级

- 门控拒绝记录 SHALL 仅在审计场景读取，SHALL NOT 参与常规阶段推进
- `.claude/kflow-gating.log` 不存在时，审计 SHALL 记为「无门控记录」，SHALL NOT 单独据此判为阻塞——门控可能尚未由 kflow-init 安装；此时以工具调用分布为主依据
- 发现项按严重度分级：主 Agent 实际完成阶段主工作且影响产物完整性 → 阻塞；仅有一次被门控拒绝后已改派 → 建议（记录改进观察，不阻塞）
- 核验结论 SHALL 写入审计报告的门控校验职责小节

> 权威定义见 `main-agent-execution-gating` 与 `subagent-isolation-rule` 能力。
