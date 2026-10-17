# context-budget-management Specification

## Purpose

定义 KFlow 的上下文预算维度的阈值、节流与度量口径——通过项目级压缩阈值配置与阶段边界的主动节流，抑制长会话上下文的单调累积，且不以任何形式增加用户的操作负担。

## Requirements

### Requirement: 项目级自动压缩阈值配置

kflow-init SHALL 在目标项目 `.claude/settings.json` 中写入自动压缩阈值配置 `autoCompactWindow: 300000`，使上下文在约 30 万 token 时触发自动压缩，而非等到接近上下文窗口上限。

#### Scenario: 首次初始化写入阈值

- **WHEN** kflow-init 在项目中完成环境配置
- **THEN** `.claude/settings.json` SHALL 包含 `autoCompactWindow` 字段且取值不超过 300000
- **AND** 该配置 SHALL 在所有 kflow 变更会话中生效

#### Scenario: 既有项目补写阈值

- **WHEN** kflow-init 在一个已初始化的项目中再次执行
- **THEN** 缺失的 `autoCompactWindow` 字段 SHALL 被补写
- **AND** 已存在且取值更小的 `autoCompactWindow` SHALL 保持不变

#### Scenario: 阈值与阶段边界节流协同

- **WHEN** 阈值配置已生效
- **THEN** 自动压缩 SHALL 作为兜底手段
- **AND** 阶段边界节流 SHALL 先于自动压缩发生

### Requirement: 阶段边界主动节流

阶段收尾时，主 Agent SHALL 将当前阶段的结论与下游所需输入落盘为交接摘要，使下一阶段能够以独立上下文承接；SHALL NOT 依赖对话上下文的延续来传递阶段信息。

#### Scenario: 阶段收尾落盘交接摘要

- **WHEN** 任一阶段完成其 COMPLETE 步骤
- **THEN** 主 Agent SHALL 将当前阶段结论写入变更级状态文件或阶段产物
- **AND** 交接摘要 SHALL 至少包含：阶段结论、产物路径、下游阶段必须读取的输入清单、未决事项
- **AND** 交接摘要 SHALL NOT 复制阶段产物的正文内容

#### Scenario: 下一阶段以独立上下文承接

- **WHEN** 阶段自动衔接到下一阶段
- **THEN** 下一阶段的主工作 SHALL 由子代理以独立上下文执行
- **AND** 子代理 SHALL 以交接摘要与产物文件为输入起点
- **AND** 子代理 SHALL NOT 依赖上一阶段对话上下文中的内容

#### Scenario: 节流不引入用户操作

- **WHEN** 阶段边界节流发生
- **THEN** 该过程 SHALL 全程由系统自动完成
- **AND** SHALL NOT 要求用户执行 `/clear`、`/compact` 或任何重置上下文的命令
- **AND** SHALL NOT 要求用户手动开启新会话

#### Scenario: 上下文超阈值的强制收尾

- **WHEN** 当前阶段的上下文消耗达到项目配置的阈值
- **THEN** 主 Agent SHALL 主动收尾当前阶段并落盘交接摘要
- **AND** SHALL NOT 继续在当前上下文中推进后续工作项

### Requirement: 上下文消耗的度量口径

系统 SHALL 定义上下文消耗的度量口径与基线对比方式，使 token 优化效果可被量化验证。

#### Scenario: 度量口径定义

- **WHEN** 对一次变更的 token 消耗作度量
- **THEN** 度量 SHALL 分别统计主会话与子代理的缓存读取量、输入量与输出量
- **AND** 度量 SHALL 记录上下文随轮次的增长曲线与自动压缩的发生点

#### Scenario: 改造前后对比

- **WHEN** 需要对一次优化作效果验证
- **THEN** 验证 SHALL 在同一项目上以真实变更执行前后对比
- **AND** 对比结果 SHALL 以基线变更的平均消耗为参照
