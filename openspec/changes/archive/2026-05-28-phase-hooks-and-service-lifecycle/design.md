# Design: 阶段钩子与服务生命周期管理

## Context

当前系统定义了 12 个阶段的 Skill 执行流程（explore → prototype → design → plan → code → code-review → api-test → e2e-test → integration-test → archive），每个阶段对服务生命周期的需求不同，但缺乏统一的服务启停规则和阶段前置/后置处理机制。

现有设计文档 `05-execution-services.md` §7-§8 已定义了"服务管理职责归属"和"服务刷新同步点"，但存在以下缺口：
- 编译验证与测试服务刷新概念混淆
- 服务启动后无显式关闭机制
- 阶段执行前不强制重读基础配置文件
- 缺少端口冲突检测和服务停止超时机制

变更的影响面：核心机制文档、7 个运行时 Skill、1 个脚本工具、3 个模板文件、CLAUDE.md。

## Goals / Non-Goals

**Goals:**
- 为 12 个阶段定义统一的服务生命周期管理规则
- 建立阶段 PRE_HOOK/POST_HOOK 标准化执行框架
- 将编译验证与测试服务刷新明确分离
- 通过共享引用文件消除钩子逻辑在 12 个 Skill 中的重复
- 通过 CLAUDE.md 规则注入实现钩子合规审计（不修改 skill-creator 和 kflow-skills-auditor 代码）

**Non-Goals:**
- 不修改 skill-creator 和 kflow-skills-auditor 的 `.claude/skills/` 代码
- 不改变 openspec 流程本身
- 不引入新的外部依赖

## Decisions

### D1: 钩子安装方式 — 共享引用 + CLAUDE.md 规则注入

**选择**: 在 `.claude/skills/kflow-shared/` 创建共享引用文件，各 SKILL.md 显式引用；在 CLAUDE.md 注入模板引用规则和审计规则。

**理由**:
- 方案 A（内联嵌入）：12 个 Skill 大量重复，更新遗漏风险高 → 不选
- 方案 B（路由注入）：直接调用 Skill 会绕过钩子，POST_HOOK 触发时机难控 → 不选
- 方案 D（共享引用 + 规则注入）：单一真相源，CLAUDE.md 规则保证合规，不修改 auditor/skill-creator → 选中

**替代方案**: 用 Claude Code settings.json hooks，但 hooks 是工具级事件，无法绑定到 Skill/阶段级别，且不具可移植性。

### D2: 编译验证与测试服务刷新的分离

**选择**: 编码阶段末尾仅执行"编译验证"（mvn compile/npm run build，验证退出码），不启动持久服务；测试阶段每轮执行"服务刷新"（STOP→COMPILE→MIGRATE→START→HEALTH）。

**理由**:
- 编码阶段的目标是证明代码可编译，不需要完整的启动+健康检查链路
- 代码审查阶段是纯静态分析，也不需要服务
- 测试阶段才需要持久运行的服务，且应该每轮前刷新、每轮后停止
- 当前 `kflow-code.md` 中的"自动化服务循环"与 `05-execution-services.md` §8 中的"所有子变更编码+审查完成后首次服务刷新"语义重叠且矛盾

### D3: with_server.py 双模式

**选择**: 保持现有一次性模式（向后兼容），新增 `--daemon` 持久化模式。

**理由**:
- 现有调用方无需改动
- 持久化模式使用 `--state-file` 输出 PID/端口/状态到 JSON 文件
- `--status`/`--health`/`--stop-all` 子命令实现服务状态的查询和管理
- 避免引入第二个脚本（单工具原则）

### D4: 服务状态文件格式

**选择**: 使用 `.service-state.json`（JSON 格式），存储在 `docs/changes/{change}/` 目录。

**理由**:
- JSON 易于脚本解析和 Claude 阅读
- 与 `.status.md` 放在同一变更目录下，上下文一致
- 记录 PID、端口、启动时间、最后健康检查时间和状态

### D5: 功能-配置关联的数据结构

**选择**: 在 `functional-designs/part-NN.md` 中新增"关联配置项"表格，包含：配置项名称、关联功能点ID、关联类型（控制可见性/控制数据范围/控制校验规则/控制流程分支/控制权限）、配置值变化→功能行为变化描述。

**理由**:
- 表格形式便于双向追溯
- "关联类型"枚举使得下游接口推导时能按类型生成对应的配置管理 API
- 配置值变化的影响描述直接为 E2E 测试用例的配置变更矩阵提供输入

## Risks / Trade-offs

- **共享文件被误改**: 所有阶段 Skill 依赖的共享文件被修改可能导致全局行为变更 → CLI 规则确保共享文件修改需经过 openspec 流程
- **服务停止失败**: 僵尸进程可能导致端口持续被占用 → 强制终止链（SIGTERM 30s → SIGKILL 10s）+ 端口释放验证
- **PRE_HOOK 执行耗时**: 重读文件 + 端口检查 + 服务启动增加阶段启动时间 → RELOAD 仅重读已变更的文件（通过文件 mtime 判断）；端口检查为轻量操作
- **DAEMON 模式脚本复杂度**: 双模式增加脚本维护成本 → 通过--help 输出和黑盒优先原则降低理解门槛
