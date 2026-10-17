# Spec Delta

## Purpose

定义执行类阶段主 Agent 的工具级硬门控——由阶段状态驱动的工具调用拒绝机制，把「主 Agent 职责边界硬线」从声明性约束升级为不可绕过的执行约束，消除主 Agent 直接执行阶段主工作导致的上下文膨胀。

## ADDED Requirements

### Requirement: 执行类阶段主 Agent 工具禁用门控

系统 SHALL 提供阶段感知的工具调用门控：当变更级 `.status.md` 的当前阶段属于执行类阶段（plan / code / code-review / api-test / e2e-test / integration-test / bug-fix）时，主 Agent 对生产代码、测试代码与脚本的 `Edit` / `Write` 调用，以及长输出构建与测试命令的 `Bash` 调用，SHALL 被拒绝并返回可读的拒绝原因。

#### Scenario: 执行类阶段主 Agent 写生产代码被拒

- **WHEN** 当前阶段为 `code`，主 Agent 调用 `Edit` 或 `Write` 且目标路径不在白名单内
- **THEN** 该调用 SHALL 被拒绝
- **AND** 拒绝原因 SHALL 说明主 Agent 在执行类阶段仅承担调度与验收，阶段主工作须由子代理执行
- **AND** 拒绝原因为指导性内容，SHALL NOT 阻止主 Agent 转而创建子代理

#### Scenario: 执行类阶段主 Agent 运行长输出命令被拒

- **WHEN** 当前阶段为执行类阶段，主 Agent 调用 `Bash` 且命令匹配长输出构建与测试命令模式（`pytest` / `python -m pytest` / `tsc` / `npx tsc` / `eslint` / `vite build` / `npm run test|build` / `yarn *` / `pnpm *`）
- **THEN** 该调用 SHALL 被拒绝
- **AND** 拒绝原因 SHALL 说明长输出命令在主 Agent 上下文中产生的输出会被后续每一轮重读

#### Scenario: 设计类阶段不受门控约束

- **WHEN** 当前阶段为设计类阶段（`explore` / `prototype-design` / `design`）
- **THEN** 主 Agent 的 `Edit` / `Write` 调用 SHALL NOT 被本门控拒绝
- **AND** 主 Agent SHALL 保留这些阶段产物的写作职责

#### Scenario: 白名单路径放行

- **WHEN** 当前阶段为执行类阶段，主 Agent 调用 `Edit` 或 `Write` 且目标路径为以下之一：`.status.md`、`status-log.md`、`docs/skill-suggestion.md`、`docs/doc-optimize-report.md`、`docs/doc-optimize-references.md`
- **THEN** 该调用 SHALL 被放行
- **AND** 主 Agent SHALL 能够更新阶段状态与历史记录、记录 skill 改进建议、以及执行独立维护工具的报告写入

> 白名单包含 `status-log.md` 是为满足 `status-file-layering` 的状态双写要求；包含两项 `doc-optimize` 报告是为保证独立维护工具 `kflow-doc-optimize` 在执行类阶段下仍可写入其产出，二者均非阶段主工作。

#### Scenario: 子代理不受门控约束

- **WHEN** 门控判定一次工具调用来自子代理
- **THEN** 该调用 SHALL 被放行，SHALL NOT 因执行类阶段而拒绝
- **AND** 子代理识别 SHALL 以 stdin 中的 `agent_id` / `agent_type` 为主判据——实测 Claude Code 2.1.278 中，子代理的 `PreToolUse` 输入含该两字段、主 Agent 不含
- **AND** 字段缺失时 SHALL 按主 Agent 处理；`agent_id` / `agent_type` 为未文档化字段，上游版本变化时应重新探测并以 `KFLOW_GATING_DISABLE=1` 提供临时关闭手段

#### Scenario: 探针验证结论

- **WHEN** 在真实会话中执行三条探针
- **THEN** 探针 1（hook stdin 转储）SHALL 记录主 Agent 与子代理的原始输入差异：主 Agent 不含 `agent_id` / `agent_type`，子代理含 `agent_id` / `agent_type`；两者的 `transcript_path` 均为会话级路径，不含子代理目录标识
- **AND** 探针 3（`Task` / `Agent` 拦截点）未观测到 hook 触发，SHALL NOT 作为门控实现路径
- **AND** 实现 SHALL 采用路径 A（`agent_id` / `agent_type`），并记录该字段为未文档化依赖的风险

#### Scenario: 门控异常的降级

- **WHEN** 门控脚本在读取输入、判定阶段或识别调用来源时发生异常
- **THEN** 该调用 SHALL 被放行（fail-open）
- **AND** 异常 SHALL 记录到 `.claude/kflow-gating.log`，SHALL NOT 阻塞正常流程

#### Scenario: 只读查询能力保留

- **WHEN** 当前阶段为执行类阶段，主 Agent 调用 `Read` / `Grep` / `Glob`，或调用不匹配长输出命令模式的 `Bash`（如 `ls` / `git status` / `git diff --stat` / `curl` 健康检查）
- **THEN** 该调用 SHALL 被放行
- **AND** 主 Agent SHALL 保留为用户快速核查的执行能力

### Requirement: 门控判定来源为阶段状态字段

门控的当前阶段判定 SHALL 来源于变更级 `.status.md` 的阶段状态字段，SHALL NOT 依赖对话上下文中的阶段记忆。

#### Scenario: 阶段判定读取状态文件

- **WHEN** 门控需要对一次工具调用作出判定
- **THEN** 当前阶段 SHALL 从变更级 `.status.md` 的阶段状态字段读取
- **AND** 判定结果 SHALL 随该字段的更新而改变

#### Scenario: 无法判定当前阶段时的降级

- **WHEN** 当前不在任何变更上下文中，或 `.status.md` 不存在、无阶段状态字段、字段值无法解析为已知阶段
- **THEN** 门控 SHALL 放行该调用
- **AND** SHALL NOT 因无法判定而阻塞非变更场景的常规工作

### Requirement: 门控由 kflow-init 安装

kflow-init SHALL 在目标项目的 `.claude/settings.json` 中写入门控所需的 hook 配置，包含门控脚本的注册与阶段判定所需的状态文件路径约定。门控 SHALL 与项目既有的 PreToolUse hook 配置共存，SHALL NOT 覆盖项目自定义的 hook 条目。

#### Scenario: 首次初始化写入门控配置

- **WHEN** kflow-init 在项目中完成权限配置步骤
- **THEN** `.claude/settings.json` 的 `hooks.PreToolUse` SHALL 包含门控脚本的注册条目
- **AND** 门控脚本文件 SHALL 随安装产物落位且可执行

#### Scenario: 既有项目升级补写

- **WHEN** kflow-init 在一个已配置过权限的项目中再次执行
- **THEN** 门控配置 SHALL 被补写或更新至最新形态
- **AND** 项目自定义的 hook 条目 SHALL 保持不变

#### Scenario: 门控被绕过时的可观测性

- **WHEN** 门控拒绝了一次工具调用
- **THEN** 该拒绝 SHALL 在会话中留下可观测记录
- **AND** 拒绝记录 SHALL 供审计阶段核验主 Agent 的职责边界遵守情况
