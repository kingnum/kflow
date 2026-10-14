# Proposal

## Why

KFlow 的缺陷修复路径中，L1/L2/L3 三层（需求/原型/设计缺陷）路由到对应阶段的 REVISION 模式，有明确的状态流转与门控。但 **L4 实现层缺陷没有独立的生命周期**：`kflow-bug-triage` 的 L4 路由只修改 `bugs/` 目录、**不变更 `.status.md`**，随后调用 `kflow-bug-fix`；而 `kflow-bug-fix` 的轮次计数、验收判据、验证门控、终止结果写入**全部依赖变更级 `.status.md`**，其流程出口是「返回测试阶段执行新一轮测试」。

这导致 L4 缺陷无法脱离变更主流程独立闭环：

```
现状:  L4 缺陷 → bug-fix → 返回测试阶段 → 必须走完整测试阶段门控 → 审计 → 归档
                          ↑ 设计是对的、代码写错了，却要重跑全量测试与全部阶段门控
```

对于「设计正确、仅实现有误」这类缺陷——按 system 既有估计约占缺陷总量的 80%——重跑设计阶段门控与全量测试是纯开销：设计文档没有变化，重跑只会产生「确认设计没变」的空转。这直接违背敏捷开发「快速修复、快速交付」的要求。

需要在 L1/L2/L3 既有 REVISION 路径**完全不变**的前提下，为 L4 建立独立的轻量闭环。

## What Changes

### 一、新增缺陷修复快车道 `bugfix-fast-lane`

- 定义 L4 实现层缺陷的独立生命周期：**用户反馈 → 分诊 → 修复 → 定向验证 → 快速收口**
- 快车道**不生成、不重跑** `functional-designs/`、`detailed-design/`、`api-tests/`、`e2e-tests/`——设计未被判定有误，重跑无意义
- 快车道**不进入**变更级 11 阶段门控矩阵，走独立的轻量状态与门控
- 快车道**仅适用于 L4**；L1/L2/L3 继续走既有 REVISION 路径，本次不改动这三条路径

### 二、新增缺陷级状态文件 `bugfix-status.md`

每个进入快车道的缺陷 SHALL 拥有独立的状态文件（位于 `bugs/fix/{BUG-ID}/bugfix-status.md`），记录：

- 分诊结论与影响范围评估（承接 triage 输出）
- 受影响项清单（受影响功能点 / 接口 / 测试用例）
- 修复阶段的状态、耗时与轮次
- 定向验证结果
- 收口结论

该文件**独立于**变更级 `.status.md`——这是快车道能脱离主流程闭环的关键。

### 三、定义定向验证机制

- 定向验证 SHALL **仅验证受影响项清单覆盖的测试用例**，SHALL NOT 重跑全量测试套件
- 受影响项清单由 `kflow-bug-triage` 的影响范围评估产出并写入状态文件
- 定向验证失败时按 `kflow-bug-fix` 既有的「子变更修复三次尝试上限」处理，SHALL NOT 引入新的轮次模型
- **命名区分**：本机制为「定向验证」，与仓库中已移除的 `recheck-round`（审查循环终止前的复核轮，因依赖已废除的轮数上限而被移除）**语义不同**——前者重跑失败用例，后者复核审查循环内的修复。规范中 SHALL 显式区分

### 四、定义快速收口机制

- 定向验证通过后，系统 SHALL 收口该缺陷：更新 `bugs/index.md` 状态、写入 `bugfix-status.md` 收口结论、标记缺陷为「已解决」
- 快速收口 SHALL 同步校验：受影响项清单 100% 覆盖且全部通过、定向验证报告存在、无占位符
- 快速收口 SHALL NOT 触发阶段回退、SHALL NOT 阻塞变更级阶段流转
- **术语边界**：本机制命名为「快速收口」而非「快速归档」，以与仓库的变更归档元工作流（`/opsx:archive`）明确区分

### 五、`kflow-bug-fix` 支持快车道模式

- `kflow-bug-fix` SHALL 支持在**无触发测试阶段上下文**时执行修复（当前其流程出口「返回测试阶段」与轮次验收均依赖测试阶段）
- 快车道模式下，`kflow-bug-fix` 写入缺陷级 `bugfix-status.md` 而非变更级 `.status.md`
- 测试阶段内发现的缺陷（B 路径）走既有逻辑不变

### 六、`kflow-bug-triage` L4 路由分流

- L4 诊断结论由「直接调用 `kflow-bug-fix`」改为「进入快车道」
- 路由输出 SHALL 声明快车道入口与受影响项清单
- L1/L2/L3 路由输出格式不变

## Capabilities

### New Capabilities

- `bugfix-fast-lane`: 缺陷修复快车道——定义 L4 实现层缺陷的独立生命周期（分诊 → 修复 → 定向验证 → 快速收口）、快车道入口条件、缺陷级状态文件结构、定向验证的受影响项覆盖判定、快速收口校验项，以及快车道与变更级阶段门控的隔离边界

### Modified Capabilities

- `bug-triage-skill`: L4 路由由「直接调用 kflow-bug-fix」改为「进入快车道」，路由输出新增快车道入口声明与受影响项清单；L1/L2/L3 路由不变
- `bug-fix-writeback`: 新增快车道模式的回写规则——写入缺陷级 `bugfix-status.md` 并同步 `bugs/index.md`；A 路径（用户反馈）与 B 路径（测试阶段发现）的既有回写规则保留
- `change-level-bug-fix`: 明确变更级缺陷修复与缺陷级快车道的边界——变更级二分法修复保持既有行为，快车道为 L4 缺陷的独立路径

## Impact

### 规范文档（`docs/designs/`）

- `skills/kflow-bug-triage.md`（L4 路由分流、快车道入口声明）
- `skills/kflow-bug-fix.md`（快车道模式、无测试阶段上下文时的执行）
- `core-mechanisms/03-status-and-tasks.md`（缺陷级状态文件与变更级状态文件的关系）
- 新增缺陷级状态文件模板

### 可运行 Skills（`skills/`）

- `kflow-bug-triage/SKILL.md`（L4 路由改为快车道入口）
- `kflow-bug-triage/references/`（路由与钩子引用同步）
- `kflow-bug-fix/SKILL.md`（快车道模式、出口从「返回测试阶段」扩展为「返回测试阶段 / 快车道收口」）
- `kflow-bug-fix/references/repetition.md`、`gates.md`、`hooks.md`（快车道模式的分支）

### 模板（`docs/designs/templates/`）

- 新增 `bugfix-status.md` 缺陷级状态文件模板
- 更新 `changes/{change}/bugs/` 相关问题详情模板（增加快车道入口标记）

### 依赖

- **本变更依赖 `streamline-design-flow` 已落地**：快车道的验证与收口复用该变更确立的「有界验证 + 报告完整 + 计数」口径，避免再次引入无界循环
- 快车道的定向验证 SHALL NOT 使用收敛驱动循环（该模型已由 `streamline-design-flow` 废除）

### 不在本次范围

- 代码审查「闭环重审」机制的调整
- L1/L2/L3 REVISION 路径的任何改动
- 变更级阶段门控矩阵本身的结构调整
