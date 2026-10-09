# Proposal

## Why

审计是归档门控，当前标准/完整档由 4 个并行子代理分担七维度评分，每个子代理冷启动都要重复 RELOAD 全量产物（`.status.md`、`functional-designs/`、`detailed-design.md`、`cross-reviews/`、`test-reports/`），Token 与耗时开销与维度数不成比例。

七维度的切分点也落在证据源与判定性质的**内部**而非之间：

- 「流程合规性」与「产物完整性」读同一份 `.status.md` 与同一棵目录树，只是同一批证据的两个视角
- 「审查质量」与「缺陷管理」查同一条「问题 → 修复 → 闭环」链，仅证据源不同
- 「效率指标」与「Post-mortem 汇总」从不产出阻塞/严重级问题——审计判定完全由问题分级决定，加权总分不参与门控，因此这两个维度的门控价值为零

同时执行者模型有两套：轻量档由主 Agent 自检，标准/完整档由子代理评估。轻量档下主 Agent 既执行审计又判定审计，缺少独立视角。

## What Changes

- **执行者统一为单个子代理**：审计（含轻量档）SHALL 由**一个子代理**执行，替换标准/完整档的 4 个并行子代理与轻量档的主 Agent 轻量自检
- **维度瘦身（BREAKING）**：标准/完整档由七维度合并为**四维度**，权重直接相加以保留总分的历史可比性
  - 流程与产物合规性 **45%**（原 流程合规性 22% + 产物完整性 23%）
  - 审查与缺陷闭环 **30%**（原 审查质量 20% + 缺陷管理 10%）
  - 测试充分性 **15%**（保留）
  - 效率与改进 **10%**（原 效率指标 5% + Post-mortem 汇总 5%）
- **保留加权总分**（0-100）：继续只作变更健康度参考，不参与门控判定；判定链路（阻塞/严重/建议分级 → 阻断或记录）不变
- **新增单子代理的证据隔离约束**：子代理 SHALL 先完成全部维度的事实采集并逐维度呈现证据，再统一评分，用以替代原先 4 个子代理互相看不到对方结论的天然隔离，抑制光环效应
- **轻量档产物形态不变**：仍为 3 项检查项的简化审计记录、不计算评分、不输出评分表；仅执行者由主 Agent 改为子代理
- **修正既存不一致**：`devflow-audit` 的 Purpose 写「六维度评估」而需求与实现均为七维度，一并改为与新结构一致

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `devflow-audit`: 新增「审计由单一子代理执行」要求；「审计六维度评估」改写为四维度评估（维度合并与权重重分配，并修正既存的六/七维度不一致）；「轻量档审计降级为轻量自检」改写为轻量档同样由子代理执行；「审计报告输出」明确总分的健康度参考定位与不参与门控
- `subagent-isolation-rule`: 「隔离规则适用范围」清单补入 `kflow-audit`（含轻量档轻量自检），使审计子代理明确受同一条「异常时禁止主代理接管 + 轮次级重试」规则约束

## Impact

**实现**

- `skills/kflow-audit/SKILL.md`（主改）：front matter `description` 的权重串、审计路径分流表、任务描述、执行流程图 EVALUATE 步、审计维度表、按档位给分规则表、审计报告格式、核心提醒
- `skills/kflow-archive/SKILL.md`：门控项的「七维度评估通过」措辞（2 处）

**设计文档**

- `docs/designs/skills/kflow-audit.md`（镜像同步）
- `docs/designs/core-mechanisms/04-gates-and-transitions.md`：流程图节点与档位分支说明
- `docs/designs/index.md`、`overview.md`、`skills/index.md`、`skills/kflow-guide.md`：维度描述行
- `docs/designs/templates/changes/{change}/audit-report.md`：形态 B 结构重写
- `docs/designs/examples/audit-report.md`：示例同步

**规范**

- `openspec/specs/devflow-audit/spec.md`
- `openspec/specs/subagent-isolation-rule/spec.md`

**文档**

- `README.md`：档位对照表、维度权重串、版本更新说明条目

**兼容性**

已归档变更的既有审计报告为七维度结构，新报告为四维度；加权总分仍为 0-100 量纲，总分层面的历史可比性保留，维度层面的可比性不保留。审计报告为流程产物而非对外接口，无外部依赖受影响。
