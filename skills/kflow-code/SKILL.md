---
name: kflow-code
version: 0.16.0
description: Use when user needs coding implementation/编码实现、TDD、功能实现, or subchange task plan is ready for execution. 子变更级TDD编码——编译验证、数据库迁移管理、多Agent并行编码、跨变更冲突检测。必须阶段。含 PRE_HOOK/POST_HOOK 阶段钩子。
license: MIT
triggers:
  - 编码实现
  - TDD
  - 功能实现
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Agent
---

# 角色

编码执行器（子变更级）。按 TDD 垂直切片流程实现功能点，管理编译验证和数据库迁移，协调多 Agent 并行编码，执行变更级同步收敛。代码审查由独立 Skill `kflow-code-review` 执行。

> ⚠ **子代理强制规则**（参见 skills/kflow-code/references/repetition.md §12）:
> 1. 本阶段主工作 MUST 通过 Agent 子代理执行，主 Agent 仅负责调度和验收
> 2. 主 Agent SHALL NOT 直接执行本阶段主工作，无例外
> 3. 子代理 SHOULD 前台运行（推荐 `run_in_background=false`），后台模式仅在权限已预配置时使用
> 4. 适用场景：直接触发 + triage 路由 + 其他 Skill 调用
> 5. 后台子代理权限失败时 SHALL 创建新的前台子代理重新执行，主 Agent SHALL NOT 直接接管（参见 §12.7）

# 任务

门控检查（含跨变更冲突检测）→ 检查/生成/补充 `service-guide.md` → PRE_HOOK 前置钩子 → TDD 任务循环（Red→Green→Refactor→Commit）→ 数据库迁移管理 → 多 Agent 并行编码 → 编译验证 → 变更级同步收敛 → 触发代码审查 → POST_HOOK 后置钩子 → 更新状态。

# 门控检查

进入编码阶段前检查：

| 检查项 | 要求 |
|--------|------|
| `.status.md` | 存在 |
| 计划状态 | = ✅ 完成 |
| 所有子变更 `tasks.md` | 文件存在 |
| 依赖子变更 | 已完成编码和接口单元测试（如有依赖） |
| NFR 章节完整性 | `detailed-design.md` 中 NFR 章节含性能+安全需求 |
| 跨变更冲突检测 | 检查活跃变更文件重叠（见 §跨变更冲突检测） |
| `docs/service-guide.md` | 存在（init 可预生成草稿）或自动生成（见 §服务指引） |

不满足则 ❌ 阻塞，提示先完成前置条件。

# 输入要求

| 产物 | 文件 | 图例 | 适用SC类型 | 说明 |
|------|------|------|-----------|------|
| 功能设计文档 | `functional-designs/` | ✅ 必须 | 后端SC | 功能点清单、业务规则、业务流程 |
| 覆盖追溯矩阵 | `traceability.md` | ✅ 必须 | 后端SC | FP 清单（设计列+计划列已完成） |
| 变更级详细设计 | `detailed-design.md`（或 `detailed-design/index.md`） | ✅ 必须 | 全部 | 统一详细设计（读取属于当前子变更的章节） |
| 接口测试用例 | `api-tests/` | ✅ 必须 | 全部 | 接口测试用例 |
| 领域词汇表 | `CONTEXT.md` | ✅ 必须 | 全部 | 项目级领域词汇表，用于代码命名对齐 |
| 子变更任务清单 | `tasks.md` | ✅ 必须 | 全部 | 子变更任务清单（含 DoD） |
| 原型产物清单 | `prototype/index.md` | ✅ 必须 | 前端SC | 原型产物清单（Prototype Manifest），前端子变更编码的核心输入 |
| E2E测试用例 | `e2e-tests/` | 🔶 条件 | 前端SC（前后端项目） | E2E 测试用例，前后端项目需要 |

> **前端SC 输入限定**：前端子变更的输入 SHALL 限定为 `prototype/index.md` 中声明的角色为 entry/page/tokens/coverage/shared 的原型产物。SHALL NOT 将 prototype/design-prompt.md 或 design-system/MASTER.md 列为输入源（过程产物，非编码所需）。

# 输出产物

| 产物 | 文件 | 图例 | 验收标准 |
|------|------|------|---------|
| 测试代码 + 实现代码 | （代码文件） | ✅ 必须 | 编译通过，所有单元测试通过 |
| 服务指引 | `docs/service-guide.md` | ✅ 必须 | 含 dev/test/staging/prod 四环境配置 |
| 迁移脚本 | `docs/changes/{change}/migrations/{序号}_{子变更}_{描述}.sql` | 🔶 条件 | 涉及数据模型变更时 |
| 回滚脚本 | `docs/changes/{change}/migrations/{序号}_{子变更}_{描述}_rollback.sql` | 🔶 条件 | 涉及数据模型变更时 |
| 迁移记录 | `docs/changes/{change}/migrations/migration-log.md` | 🔶 条件 | 涉及数据模型变更时 |

# 执行流程

```
编码阶段流程:

┌─────────────────────────────────────────────────────────────────────────┐
│                         CODE WORKFLOW                                    │
├─────────────────────────────────────────────────────────────────────────┤
│  1. PRE_HOOK  → CHECK_STATE → RELOAD → 引用                        │
│  │              skills/kflow-code/references/hooks.md code 阶段 PRE_HOOK        │
│  2. CHECK     → 门控检查 + 跨变更冲突检测                                │
│  3. SERVICE   → 检查/生成 docs/service-guide.md                          │
│  │   ├── 存在且非草稿 → 直接读取使用                                      │
│  │   ├── 存在且为草稿（含 init 逆向标记）                                  │
│  │   │   └── 进入补充流程：保留 dev 配置，补充 test/staging/prod           │
│  │   └── 不存在 → 自动分析项目结构 → AskUserQuestion 确认 → 生成          │
│  4. CONSTRAINT → 约束前置检查（共享文件+域隔离+FP 类型）                    │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                    任务循环 (TDD 垂直切片)                         │    │
│  │  RED(写测试) → VERIFY(确认失败) → GREEN(最小实现) →                │    │
│  │  VERIFY(确认通过) → REFACTOR(重构深化) → COMMIT(提交)              │    │
│  │  涉及数据模型变更 → 编写迁移脚本 + 回滚脚本                         │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                 多 Agent 并行编码策略                              │    │
│  │  无依赖子变更并行 + 有依赖子变更顺序                              │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                    编译验证                                        │    │
│  │  COMPILE_BE(编译后端，验证退出码) + COMPILE_FE(编译前端，验证退出码) │   │
│  │  仅编译验证，不启动服务                                            │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│       │                                                                  │
│       ▼                                                                  │
│  ┌─────────────────┐                                                    │
│  │ 变更级同步收敛    │ ← 等待全部完成 → 冲突检查 → 编译 → 迁移合并        │
│  └─────────────────┘                                                    │
│       │                                                                  │
│       ▼                                                                  │
│  ┌─────────────────┐                                                    │
│  │ kflow-code-    │ ← 代码审查由独立 Skill 执行（两视角并行审查）         │
│  │ review          │                                                     │
│  └─────────────────┘                                                    │
│       │                                                                  │
│       ▼                                                                  │
│  ┌─────────────────┐                                                    │
│  │ 下一子变更       │ ← 选择下一个子变更（检查依赖）                       │
│  └─────────────────┘                                                    │
│       │                                                                  │
│       ▼                                                                  │
│  ┌─────────────────┐                                                    │
│  │ POST_HOOK       │ → 引用 skills/kflow-code/references/hooks.md code         │
│  │                 │   阶段 POST_HOOK → UPDATE_STATE                     │
│  └─────────────────┘                                                    │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 步骤 1：PRE_HOOK — 阶段前置钩子

编码阶段开始时执行标准化前置钩子流程：

```
1. CHECK_STATE → 检查阶段状态文件是否完整，确认前置阶段已完成
2. RELOAD     → 重载变更上下文（子变更任务清单、设计文档、依赖关系）
3. HOOK_EXEC  → 引用 `skills/kflow-code/references/hooks.md` code 阶段 PRE_HOOK
```

> **原则**：不在此处内联复制钩子执行步骤。具体的钩子逻辑定义在 `skills/kflow-code/references/hooks.md` 中。本 Skill 仅声明引用关系。

---

## 步骤 2：CHECK — 门控检查 + 跨变更冲突检测

### 门控验证

验证计划完成、tasks.md 存在、依赖满足、NFR 完整。

### 跨变更冲突检测

编码启动前检测活跃变更之间的文件修改重叠：

```
1. 读取 docs/changes/index.md 获取所有活跃变更
2. 对比各活跃变更的"影响文件"字段
3. 存在文件重叠 → AskUserQuestion 通知用户确认
4. 无重叠 → 允许继续编码
```

---

## 步骤 3：SERVICE — 服务指引管理

### service-guide.md 处理流程

```
检查 docs/service-guide.md 状态:

├── 存在且非草稿（无「由 AI 逆向分析生成」标记）
│   └── 直接读取使用，跳过生成流程
│
├── 存在且为草稿（含 init 逆向标记）
│   ├── 保留已有 dev 环境配置
│   ├── 补充 test/staging/prod 环境配置
│   └── 移除草稿标记，替换为正式内容
│
└── 不存在
    ├── 自动分析项目结构（识别启动命令、端口、数据库连接）
    ├── 扫描配置文件识别外部服务依赖（见 §外部服务依赖识别）
    ├── AskUserQuestion 确认/补充配置信息（含外部服务连接信息）
    ├── 生成 docs/service-guide.md（含 dev/test/staging/prod 四环境配置 + 服务依赖章节）
    └── 写入配置状态标记（见 §配置状态标记写入）
```

### 外部服务依赖识别

在自动分析项目结构时，SHALL 扫描项目配置文件识别外部服务依赖：

```
1. 扫描以下配置文件:
   ├── Java: application.yml, application.properties, pom.xml
   ├── Node.js: package.json, .env.example
   ├── Go: go.mod, config.yaml
   └── Python: requirements.txt, pyproject.toml, settings.py

2. 识别以下类型的外部服务依赖:
   ├── 数据库: MySQL/PostgreSQL/MongoDB/Oracle/SQL Server
   ├── 缓存: Redis/Memcached
   ├── 消息队列: RabbitMQ/Kafka/RocketMQ/Pulsar
   └── 对象存储: MinIO/S3/OSS/COS

3. 在 service-guide.md 中生成「服务依赖」章节表格:
   | 服务名称 | 类型 | dev 环境地址 | 端口 | 说明 |
   |---------|------|-------------|------|------|
   | {服务名} | {数据库/缓存/MQ/对象存储} | {主机地址} | {端口} | {说明} |

4. 对非 localhost/127.0.0.1 且非环境变量占位符（${...}）的地址标记为「需确认的外部服务」
```

### 外部服务连接信息询问

识别到至少一个外部服务依赖时，SHALL 通过 AskUserQuestion 收集连接信息：

```
AskUserQuestion:
  Question: "检测到以下外部服务依赖，请提供 dev 环境连接信息:"
  逐项询问:
    ├── 数据库: 类型 / 主机地址 / 端口 / 数据库名
    ├── 缓存 (Redis): 主机地址 / 端口
    ├── 消息队列: 类型 / 主机地址 / 端口
    └── 对象存储: 类型 / 端点地址 / 端口
  Options:
    - "确认以上配置" → 写入 service-guide.md
    - "稍后配置" → 标记 ⏳ 待配置，后续测试阶段 PRE_HOOK 补全
```

若无外部服务依赖（纯静态前端或单进程应用），在「服务依赖」章节标注「无外部服务依赖」，不触发询问。

### 配置状态标记写入

service-guide.md 生成完成后，SHALL 在文件头部写入配置状态标记：

```markdown
> **配置状态**: ✅ 已就绪 ({生成/确认日期})
> **生成来源**: kflow-code 编码阶段自动分析
```

| 场景 | 标记内容 |
|------|---------|
| 用户确认全部配置 | `> **配置状态**: ✅ 已就绪 (YYYY-MM-DD 确认)` |
| 用户部分跳过 | `> **配置状态**: ⏳ 待配置`（标注跳过的配置项） |

生成来源标记（`kflow-code 编码阶段自动分析`）区别于 kflow-init 的草稿标记（`由 AI 逆向分析生成`）。

### service-guide.md 格式

详见 [references/service-guide-template.md](references/service-guide-template.md) — 完整格式模板（项目类型、四环境配置、测试账号、健康检查）。

---

## 步骤 8：编译验证

编码完成后执行编译验证，确认代码可编译通过，但不启动服务：

```
编译验证:

COMPILE_BE(编译后端，验证退出码) + COMPILE_FE(编译前端，验证退出码)
```

| 验证项 | 说明 |
|--------|------|
| COMPILE_BE | 编译后端代码，检查退出码为 0 |
| COMPILE_FE | 编译前端代码，检查退出码为 0（仅前后端项目） |
| 不启动服务 | 仅编译验证，不执行服务启动、迁移或健康检查 |

> **原则**：编译验证仅校验代码编译是否通过，不替代服务生命周期管理。服务的启动、停止、重启由变更级 agent 独占管理。

---

## 步骤 3.5：CONSTRAINT — 约束前置检查

进入 TDD 任务循环前，SHALL 验证共享文件冲突预防规则和前后端文件隔离约束：

```
约束前置检查:

1. 共享文件识别 → 列出本变更涉及的共享文件清单
2. 域隔离确认 → 确认各子变更 Agent 的操作域边界
3. FP 类型校验 → 确认各 FP 类型与子变更类型匹配（见 §FP 类型二次校验）
4. 全部通过 → 进入任务循环
5. 任一不通过 → ❌ 阻塞，提示修复
```

| 检查项 | 说明 |
|--------|------|
| 共享文件保护 | 识别共享文件清单，Agent 禁止直接修改，wait-for-all 模式处理 |
| 域隔离边界 | 前端域/后端域目录范围已确认（见 §前后端子变更文件隔离规则） |
| FP 类型匹配 | 各 FP 类型与子变更类型一致（见 §FP 类型二次校验） |
| 跨变更文件重叠 | 活跃变更间无文件修改重叠（见 §跨变更冲突检测） |

---

## 步骤 4：TDD 任务循环

### FP 类型二次校验（编码前）

在进入 TDD 循环前，SHALL 对每个待实现 FP 进行类型二次校验：

```
1. 读取 functional-designs/index.md 中各 FP 的「类型」列
2. 比较:
   ├── FP 类型 = 子变更类型 → ✅ 进入 TDD 循环
   ├── 前端子变更 含「后端」FP → ⏭️ 跳过该后端 FP，记录到编码报告
   ├── 后端子变更 含「前端」FP → ⏭️ 跳过该前端 FP，记录到编码报告
   └── 类型列缺失 → 🟡 警告（旧版兼容），不跳过
3. 被跳过的 FP 在编码报告中标明「FP 类型与子变更类型不匹配」
```

按 `tasks.md` 中未被跳过的功能点顺序执行 TDD。每个 TDD 循环 SHALL 采用**垂直切片**方式。

```
TDD 循环:

┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐   ┌──────────┐   ┌────────┐
│  RED   │──▶│ VERIFY │──▶│ GREEN  │──▶│ VERIFY │──▶│ REFACTOR │──▶│ COMMIT │
│ 写测试  │   │ 确认失败│   │ 最小实现│   │ 确认通过│   │ 重构深化  │   │ 提交   │
└────────┘   └────────┘   └────────┘   └────────┘   └──────────┘   └────────┘
                    │
                    ├─ 涉及数据模型变更:
                    │   └─▶ 编写迁移脚本 + 回滚脚本
                    │
                    └─ 每周期完成后执行 TDD 检查清单
```

### TDD 核心原则

| 原则 | 说明 |
|------|------|
| 测试行为而非实现 | 测试 SHALL 描述系统做什么（行为），而非怎么做（实现） |
| 仅用公共接口 | 测试 SHALL 仅通过公共接口验证行为，禁止测试私有方法 |
| 内部重构不应破坏测试 | 如果改实现不变行为导致测试失败 → 测试与实现耦合 |
| Mock 仅用于外部边界 | Mock SHALL 仅用于数据库、外部服务等外部边界，禁止 mock 内部 collaborator |
| Vertical Slice（垂直切片） | 每次实现一个完整的端到端行为切片（schema → logic → API → test） |

### 好测试 vs 坏测试

| 好测试 | 坏测试 |
|--------|--------|
| 验证可观察行为 | 验证内部方法调用 |
| 通过公共接口 | 调用私有方法 |
| 重构不破坏 | 重构即破坏 |
| 可读性高（描述业务行为） | 可读性低（描述实现步骤） |
| 一次一个行为 | 一次测试多个行为 |

### Tracer Bullet 先行

第一个 RED→GREEN 循环 SHALL 是 **tracer bullet** — 证明端到端路径可用的最简实现：

| Tracer Bullet 要求 | 说明 |
|--------------------|------|
| 横切所有集成层 | 从接口到数据层全路径打通 |
| 最简实现 | 不包含完整业务逻辑，仅证明路径可用 |
| 可运行 | 必须能编译通过并产生可验证的输出 |
| 后续增量 | 每个后续 RED→GREEN 基于前一切片增量添加 |

### 水平切片反模式 — 警告

> **⚠️ 警告**：禁止先写所有测试再写所有代码的"水平切片"反模式。

```
❌ 错误: 水平切片
Layer 1: 写所有 Controller 测试 → 写所有 Controller 代码
Layer 2: 写所有 Service 测试 → 写所有 Service 代码
Layer 3: 写所有 Repository 测试 → 写所有 Repository 代码
问题: 测试假想行为 — 测试基于"我认为应该怎样"而非"实际怎样"编写
      重构不可靠 — 重构实现时这些测试大面积失败

✅ 正确: 垂直切片 / tracer bullet
Slice 1: Controller 测试 → Controller → Service → Repository → 全链路通过
Slice 2: Controller 测试 → Controller → Service → Repository → 全链路通过
每次只写一个测试 → 一个实现，每个切片完整可运行
```

### TDD 每周期检查清单

详见 [references/tdd-checklist.md](references/tdd-checklist.md) — RED/GREEN/REFACTOR 三阶段检查清单、深化模块 (Deepen Module) 检查项与示例。

---

## 步骤 4.2：命名对齐约束

编码阶段 SHALL 将代码命名对齐项目级 `CONTEXT.md` 领域词汇表：

| 约束 | 说明 |
|------|------|
| 模块命名 | 模块/包名 SHALL 使用 CONTEXT.md 中的领域术语 |
| 类命名 | 领域实体类名 SHALL 对齐 CONTEXT.md 中的实体名称 |
| 函数命名 | 业务函数/方法名 SHALL 使用 CONTEXT.md 术语描述行为 |
| 测试描述 | 测试用例描述 SHALL 使用 CONTEXT.md 术语 |

### 冲突处理

| 场景 | 处理方式 |
|------|---------|
| 代码命名与 CONTEXT.md 不一致 | SHALL 以 CONTEXT.md 为准修改代码 |
| CONTEXT.md 缺少需要的术语 | SHALL 回退到 kflow-explore 增补术语 |
| CONTEXT.md 术语定义不精确 | SHALL 记录建议到 skill-suggestion.md，待 explore 修订 |

---

## 步骤 4.3：前端子变更专属实现流程

> 当前端子变更类型为「前端子变更」时，执行前端实现子流程（非 TDD），原型产物作为执行输入而非提示性约束。

### 触发条件

| 条件 | 处理 |
|------|------|
| 子变更类型 = 前端子变更 | 进入前端实现子流程 |
| 子变更类型 = 后端子变更 | 跳过本节，继续 TDD 任务循环 |
| 原型设计阶段被跳过（⏭️） | 标记 ⚠️ 阻塞，提示原型缺失 |

### 前端实现子流程（四阶段）

```
Phase 1: 工程骨架搭建
  ├── 脚手架初始化（create-react-app / vite / next.js 等，按项目栈选择）
  ├── 路由框架（对齐 element-coverage-tree.md 📄 页面节点层）
  ├── 全局布局组件（Header/Sidebar/Footer，基于 prototype/index.md 中 entry 角色文件提取）
  ├── 公共组件库（Button/Input/Modal/Table 等，从 prototype/index.md 中 entry 角色文件提取）
  ├── 状态管理框架（Redux/Zustand/Context，按项目规模选择）
  └── 设计令牌注入（从 prototype/index.md 中 tokens 角色文件 → CSS 变量/theme 对象）
  
Phase 2: 逐页转译
  ├── 从 prototype/index.md 页面清单获取各页面对应的 HTML 文件路径 → 解析 DOM 结构
  ├── 转译为前端框架组件（React/Vue/Angular）
  ├── 逐页覆盖 element-coverage-tree.md 中该页面的所有 🔘 元素
  └── 逐页实现 element-coverage-tree.md 中该页面的所有 🎯 状态
  
Phase 3: API 对接
  ├── 基于 API 契约（detailed-design.md §接口设计）编写 mock 数据
  ├── 使用 mock 数据进行前端功能验证
  └── 后端编码完成后，替换 mock 为真实 API（集成对接步骤）
  
Phase 4: 状态覆盖
  ├── hover / active / focus / disabled / loading / empty / error
  └── 弹窗/抽屉的打开/关闭逻辑
```

### 原型产物获取方式（基于 prototype/index.md）

| 角色 | 获取方式 | 读取阶段 | 用途 |
|------|---------|---------|------|
| entry | 从 prototype/index.md 「产物组织方式」获取入口文件路径 | Phase 1, 2 | 页面结构、全局布局、交互元素 |
| page | 从 prototype/index.md 「页面清单」获取各页面对应 HTML 文件路径 | Phase 2 | 逐页转译 |
| tokens | 从 prototype/index.md 「原型文件清单」获取 tokens 角色文件路径 | Phase 1 | CSS 变量注入（颜色/间距/圆角/阴影） |
| coverage | 从 prototype/index.md 「原型文件清单」获取 coverage 角色文件路径 | Phase 1, 2, 4 | 📄 路由框架、🔘 元素清单、🎯 状态清单 |

### 缺失产物降级（基于清单角色）

| 缺失角色 | 处理 |
|---------|------|
| entry | ⚠️ 阻塞，核心输入不可缺失 |
| coverage | ⚠️ 降级：从 prototype/*.html 手动识别元素和状态 |
| tokens | ⚠️ 降级：从 prototype/*.html 内联样式中提取 |

### 前端编译验证

前端子变更所有页面实现完成后，执行编译验证：
- `tsc --noEmit`（TypeScript 项目）或 `npm run build`
- 编译失败 SHALL 阻塞前端子变更的完成

---

## 步骤 4.4：子代理工具切换禁令

> **来源**: refine-skill-execution-rules 变更。子代理因模型 API 报错时，SHALL NOT 自行切换工具（如改用 Bash 直接执行 Playwright 命令），应阻塞+上报，由用户决策。

```
子代理工具切换禁令:

1. 子代理执行过程中如遇模型 API 报错/工具不可用:
   ├── SHALL: 阻塞当前执行，输出错误信息和恢复建议
   ├── SHALL: 上报主 Agent，由主 Agent 通知用户
   ├── SHALL NOT: 自行切换工具（如 Agent 报错 → 改用 Bash）
   └── SHALL NOT: 降级到其他执行方式

2. 恢复建议输出:
   ├── 明确列出失败的工具和操作
   ├── 提供恢复指令（如安装缺失工具/确认工具可用性）
   └── 等待用户决策

3. 主 Agent 收到上报后:
   ├── 向用户展示阻塞信息
   ├── 不自行尝试修复（subagent-isolation-rule）
   └── 等待用户确认后再继续
```

---

## 步骤 5：数据库迁移管理

当编码涉及数据模型变更时，在变更级 `migrations/` 目录创建迁移脚本。

### 迁移脚本规范

| 文件 | 命名格式 | 说明 |
|------|---------|------|
| 迁移脚本 | `{序号}_{子变更}_{描述}.sql` | 正向迁移（DDL/DML） |
| 回滚脚本 | `{序号}_{子变更}_{描述}_rollback.sql` | 回滚操作 |

示例：
```
migrations/
├── 001_user-auth_create_users.sql
├── 001_user-auth_create_users_rollback.sql
├── 002_order-management_create_orders.sql
├── 002_order-management_create_orders_rollback.sql
└── migration-log.md
```

### 迁移执行记录 (migration-log.md)

```markdown
# 数据库迁移记录

| 序号 | 迁移文件 | 子变更 | 执行时间 | 执行人 | 状态 | 回滚状态 |
|------|---------|--------|---------|--------|------|---------|
| 001 | 001_user-auth_create_users.sql | user-auth | 2026-05-03 10:00 | Agent | ✅ 成功 | 未回滚 |
```

---

## 步骤 6：多 Agent 并行编码

### 策略概述

```
┌─ 无依赖 AFK 子变更并行编码 ────────────────────────┐
│  Agent 1: subchange-1 编码                          │
│  Agent 2: subchange-2 编码（无依赖）                 │
│  Agent 3: subchange-3 编码（无依赖）                 │
└─────────────────────────────────────────────────────┘
                        ↓
┌─ 有依赖子变更顺序编码 ──────────────────────────────┐
│  等待依赖完成 → 开始编码                             │
└─────────────────────────────────────────────────────┘
```

### Agent 分配原则

1. 检测子变更依赖关系图
2. 所有进入编码阶段的子变更均为 AFK 类型（HITL = 设计不完整标记，已在 plan 入口被拒绝）
3. 无依赖子变更 → 可并行启动
4. 有依赖的子变更等待其依赖项完成后再启动

### 子变更执行策略

| 依赖状态 | 并行策略 | 执行方式 |
|---------|---------|---------|
| 无依赖 | 可并行 | 同时启动多个 Agent |
| 有依赖 | 依赖完成后再启动 | 等待依赖子变更完成后启动 |

### 冲突预防规则

| 规则 | 说明 | 执行方式 |
|------|------|---------|
| 独立域约束 | 每个 Agent 仅修改分配的子变更目录 | 明确约束范围 |
| 禁止跨域修改 | 禁止修改其他子变更代码 | Prompt 中明确 "Do NOT change other code" |
| 共享文件锁定 | 共享配置文件需等待其他 Agent 完成 | 顺序处理共享文件 |
| 跨变更冲突预防 | 编码前检查活跃变更文件重叠 | 读取 index.md 对比影响文件 |
| 结果合并验证 | Agent 完成后检查文件冲突 | 验证无交叉修改 |

### 共享文件冲突预防

多 Agent 并行编码时存在共享文件（如 `.gitignore`、`package.json`、公共配置文件）的并发修改风险：

1. **识别共享文件**：编码启动前识别共享文件清单（`shared-types/`、`service-guide.md`、`package.json`、`tsconfig.json`、`.gitignore` 等跨子变更共享文件）
2. **Agent 禁止操作共享文件**：Agent 仅修改分配的子变更目录，禁止直接修改共享文件
3. **wait-for-all 模式**：需修改共享文件时，等待所有 Agent 完成后由上层 Agent（变更级 agent）统一修改
4. **冲突回滚**：冲突检测时发现非法跨域修改 → 回退该 Agent 的变更，重新执行

### 前后端子变更文件隔离规则

前端子变更与后端子变更的代码域天然隔离，但共享配置文件（如前端路由注册入口、公共类型定义）存在交叉风险：

| 规则 | 说明 |
|------|------|
| 前端域 | 前端子变更操作：`src/pages/`、`src/components/`、`src/router/`、`src/store/`、`src/styles/`、`src/layouts/` |
| 后端域 | 后端子变更操作：`src/api/`、`src/services/`、`src/models/`、`src/db/`、`src/middleware/` |
| 共享文件 | `package.json`、`tsconfig.json` 等由变更级 agent 统一管理，子变更 Agent 禁止修改 |
| 跨域变更 | 如需同时修改前后端共享文件，由变更级 agent 在「集成对接」步骤统一处理 |
| 违规处理 | 发现跨域修改 → 回退该 Agent 的变更，记录到 skill-suggestion.md |

**前端 FP > 10 时的文件隔离**：

```
前端 FP > 10:
  ├── 骨架子变更（先行）: 脚手架/路由/布局/组件库/设计令牌
  │   └── 统一创建共享基础设施（路由入口、全局布局、公共组件、状态管理框架）
  └── 页面组子变更（串行追加）: 各页面组件文件（独立文件，无共享冲突）
      └── 在骨架已建立的框架内增量添加页面，各自操作独立的页面组件文件
```

---

## 步骤 7：变更级同步收敛

多 Agent 并行编码完成后，由上层 Agent 统一执行变更级收敛：

```
变更级同步收敛流程:

1. WAIT_ALL   → 等待所有子变更编码 Agent 完成
2. COLLECT    → 收集所有子变更的代码变更和迁移脚本
3. VERIFY     → 验证无交叉修改（共享文件冲突检查）
4. COMPILE    → 统一编译项目
5. MIGRATE    → 按序号合并并排序所有迁移脚本
6. REVIEW     → 触发 kflow-code-review（每个子变更独立审查）
7. SYNC       → 全部通过后释放门控 → 进入下一阶段
```

| 收敛步骤 | 执行者 | 说明 |
|---------|--------|------|
| 等待完成 | 上层 Agent | 确认所有并行 Agent 完成编码和提交 |
| 冲突检查 | 上层 Agent | 对比各子变更修改文件列表，检测交叉修改 |
| 迁移合并 | 上层 Agent | 收集所有迁移脚本，按序号排序，冲突时提示用户裁定 |
| 代码审查 | `kflow-code-review` | 每个子变更独立触发代码审查 Skill |
| 门控释放 | 上层 Agent | 全部子变更编码+审查通过后释放 |

---

## 步骤 9：触发代码审查 + 完成

触发 `kflow-code-review` 对每个子变更执行独立的两视角并行审查。更新 `.status.md`。

---

# 重复制（执行类阶段）

编码阶段属于执行类阶段，在现有多 Agent 并行编码机制基础上采用重复制模式。目标轮次由弹性轮次决策规则确定（参见 `skills/kflow-code/references/repetition.md` §14）：首次执行 10 轮，回退重执行按影响范围分数缩减。

## 每轮工作内容

**遍历项**：**双层遍历**——外层遍历全部未完成编码的子变更，内层遍历每个子变更 tasks.md 中的全部功能点

> **来源**: skill-execution-reliability 变更。编码阶段「工作项」定义为「全部未完成编码的子变更」，每轮自动处理所有未完成子变更，而非逐个子变更询问用户。

**每轮流程**：
1. **外层遍历**：读取所有子变更的编码状态，筛选出未完成编码的子变更
2. **内层遍历**：对每个未完成编码的子变更，遍历其 tasks.md 中全部功能点，执行完整 TDD 垂直切片：
   - 评估状态（已通过/未通过/部分通过）
   - RED：写/补测试代码
   - GREEN：写/改实现代码
   - REFACTOR：深化模块（小接口+深实现）
   - 验证通过（运行测试确认）
3. 首轮每个 FP 的首个 RED→GREEN 循环 SHALL 是 Tracer Bullet（端到端最简路径），后续轮次检查 Tracer Bullet 路径是否仍然畅通
4. 已通过的 FP 执行深化检查（模块深度/边界/重构），未通过的 FP 继续推进
5. 涉及数据模型变更时编写迁移脚本和回滚脚本

**每轮产物**：traceability.md「编码实现」列更新

**轮次结束后**：更新 .status.md 执行轮次计数器

## 复杂度评估

复杂度评估仅信息展示，不驱动执行行为：

```
复杂度分 = 功能点数 × 1 + 接口数 × 1.5 + 场景数 × 2

低复杂度 (< 20 分) / 中复杂度 (20-50 分) / 高复杂度 (> 50 分)
```

分级阈值保留但仅用于信息分类，复杂度分写入 .status.md 备注列标注「仅供参考，不驱动执行行为」。无论复杂度高低，均须完成全部 10 轮迭代后方可返回。

## 执行流程

```
1. 复杂度评估 → 写入 .status.md 备注列（仅信息展示，不驱动执行行为）

1.5 INIT → 主 Agent 按弹性轮次决策确定目标轮次 N，写入 .status.md 执行轮次为 1 / N

2. 构建阶段专属提示词
   ├── kflow-shared 分层加载（基础层 + 执行层）:
   │   ├── skills/kflow-code/references/state-values.md（摘要）
   │   ├── skills/kflow-code/references/gates.md（当前阶段相关门控）
   │   ├── skills/kflow-code/references/repetition.md
   ├── 输入: detailed-design.md + api-tests/ + 所有子变更 tasks.md
   ├── TDD 流程要求 (Red → Green → Refactor)，双层遍历：外层遍历全部子变更 + 内层遍历全部 FP 执行 TDD 循环
   ├── traceability.md 待填充列: 编码实现(SC)
   ├── 重复制遍历指令:
   │   「每轮遍历全部未完成编码的子变更，每个子变更内遍历全部功能点独立执行完整 TDD 流程。
   │     更新 .status.md 中执行轮次计数器为当前轮次号。
   │     禁止按轮次分段分配工作重点——每轮均须对所有子变更的全部功能点执行完整检查。
   │     必须完成全部 10 轮迭代后才可返回验收报告，禁止在第 10 轮前返回。
   │     若当前轮次无新发现且无可执行工作，仍须递增计数器并继续。」
   ├── 轮间摘要注入（第 2 轮起）: 主 Agent 每轮子代理返回后提取摘要（已发现问题/未解决问题/覆盖率变化/本轮建议关注），注入下一轮子代理 prompt（参见 repetition-model.md §13）
   └── 完成承诺: COMPLETED

3. 启动 Agent 迭代子代理 (Agent(description, prompt, run_in_background))
   └── 子代理内维持现有多 Agent 并行编码策略

4. 主 Agent 验收
   ├── 轮次: .status.md 执行轮次 = N / N（N 为目标轮次，由弹性轮次决策确定）
   ├── 产物: 所有功能点代码已实现且通过测试
   ├── 覆盖率: traceability.md「编码实现」列覆盖率 = 100%
   ├── 迁移: 涉及数据模型变更时迁移脚本+回滚脚本齐全
   └── 无占位符: 无 TODO/TBD/{待填写}
```

## 验收结果处理

| 情况 | 处理方式 |
|------|---------|
| 通过 | 更新 .status.md + 填写 traceability.md 对应列 → 释放代码审查阶段门控 |
| 轮次不足（< 10） | 拒收，直接重新启动 Agent 子代理继续执行，不进入 AskUserQuestion |
| 轮次达标但产物不合格 | 记录 `docs/skill-suggestion.md` → AskUserQuestion 询问重跑 |

---

# 与其他 Skill 的关系

| 关系 | Skill / 阶段 | 说明 |
|------|-------------|------|
| 输入来自 | `kflow-plan` | 计划阶段（子变更级），提供 tasks.md 含 DoD |
| 输出给 | `kflow-code-review` | 代码审查阶段（子变更级），独立审查 |
| 前置阶段 | 计划 | 门控依赖 |
| 后续阶段 | 代码审查 → 接口单元测试 → E2E测试（前后端）/ 接口单元测试（纯后端） | 阶段链 |
| 关系说明 | 代码审查拆分为独立 Skill | 本 Skill 不再包含审查子阶段 |
| 执行模式 | 重复制（内嵌多 Agent 并行编码） | 弹性轮次决策（参见 repetition-model.md §14），复杂度评估仅信息展示，主 Agent 验收闭环 |

# 核心提醒

- 代码审查由独立 Skill `kflow-code-review` 执行，本 Skill 不包含审查
- 多 Agent 并行编码时每个 Agent 仅修改分配的子变更目录，禁止跨域修改
- 涉及数据模型变更时必须同时编写迁移脚本和回滚脚本
- 第一个 TDD 循环 SHALL 是 tracer bullet（端到端最简路径），禁止水平切片反模式
- RED 阶段禁止重构，REFACTOR 阶段每次重构后运行全部测试
- 编码命名 SHALL 对齐 CONTEXT.md 领域词汇表，冲突时以 CONTEXT.md 为准
- **双层遍历**：每轮遍历全部未完成编码的子变更，每个子变更内遍历全部功能点，禁止逐个子变更询问
- **原型一致性**：前端SC 编码 SHALL 对齐 prototype/index.md 中声明的产物文件，禁止引用 process artifacts（design-prompt.md / design-system/MASTER.md）
- **子代理工具切换禁令**：子代理遇 API 报错时 SHALL NOT 自行换工具，须阻塞+上报
- 敏感信息（密码、密钥）禁止明文写入，必须使用环境变量引用

# 反馈机制

如果在使用本 Skill 过程中发现问题或有优化建议，请记录到 `docs/skill-suggestion.md` 文件中。
