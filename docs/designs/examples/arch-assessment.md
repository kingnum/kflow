# 架构评估报告：支付回调接口跨子变更契约矛盾

> **触发条件**: 测试用例 ITC-007「支付回调更新订单状态」连续 3 轮集成测试失败
> **生成时间**: 2026-05-03 16:00
> **变更**: ecommerce-platform-init

---

## 一、问题概述

| 项目 | 详情 |
|------|------|
| 触发用例 ID | ITC-007「支付回调更新订单状态」 |
| 连续失败轮次 | Round 1 / Round 2 / Round 3 |
| 涉及子变更 | order-management（订单管理）、payment-integration（支付集成） |
| 涉及设计域 | 业务域 - 订单支付流程 |
| 关联接口契约 | POST /api/orders/{id}/payment-callback |

---

## 二、证据收集

### 2.1 失败用例详情

| 轮次 | 预期结果 | 实际结果 | 错误信息 |
|------|---------|---------|---------|
| Round 1 | HTTP 200 + 订单状态=PAID | HTTP 400 | "payment provider not configured for this order" |
| Round 2 | HTTP 200 + 订单状态=PAID | HTTP 400 | 同上（修复后仍失败） |
| Round 3 | HTTP 200 + 订单状态=PAID | HTTP 500 | 内部错误：订单状态转换不合法（PENDING → PROCESSING） |

### 2.2 关联接口契约

从 [detailed-design.md](../designs/skills/../../examples/design-level-restructure.md) 提取：

| 设计域 | 接口 | 当前定义 | 问题 |
|--------|------|---------|------|
| order-management | POST /api/orders/{id}/payment-callback | 接收 `{provider, transactionId}` | 缺少 payment-integration 期望的 `{signature, amount}` |
| payment-integration | 回调发送方 | 发送 `{provider, transactionId, signature, amount, currency}` | 5 字段，order-management 只接受 2 字段 |

### 2.3 受影响子变更依赖关系

```
user-auth (✅ 已完成，不受影响)
    │
order-management (❌ 受影响)
    │
payment-integration (❌ 受影响，依赖 order-management)
```

### 2.4 已尝试的修复方案

| 轮次 | 修复类型 | 修复内容 | 结果 |
|------|---------|---------|------|
| Round 1→2 | 接口实现修复 | order-management 增加 payment-provider 默认配置 | 仍失败，问题不在实现 |
| Round 2→3 | 接口契约修复 | 增加 provider 字段校验 | 再次失败，暴露出更深层的契约矛盾 |

---

## 三、根因深挖

### 3.1 问题分类：架构设计错误 - 接口契约矛盾

**核心矛盾**：order-management 子变更设计时，将支付回调视为"简单的状态更新接口"，仅接收 provider 和 transactionId。而 payment-integration 子变更设计时，将回调定义为"支付平台标准通知接口"，需携带签名验证和金额校验。

**设计阶段遗漏**：
- detailed-design.md 中两个子变更的接口定义分别编写，未做跨子变更接口一致性校验
- 支付回调流程在变更级设计中缺少端到端数据流定义
- 订单状态机缺少 PROCESSING 中间状态，导致回调到达时订单处于不可转换状态

### 3.2 影响范围

| 影响维度 | 详情 |
|---------|------|
| 受影响子变更 | order-management（接口扩展）、payment-integration（字段适配） |
| 受影响设计域 | 业务域 - 订单支付流程 |
| 受影响文档 | detailed-design.md §3.2 支付回调接口、§4.1 订单状态机 |
| 连锁影响 | 接口单元测试、E2E测试用例需同步更新 |

---

## 四、多方案输出

### 方案 A（推荐方案）：统一支付回调接口 + 完整状态机

**改动内容**：
1. detailed-design.md 修订：支付回调接口統一为 5 字段标准（provider, transactionId, signature, amount, currency）
2. order-management 接口扩展：接收 5 字段 → 验证签名 → 校验金额 → 更新订单状态
3. payment-integration 适配：按统一接口标准调整字段序列化逻辑
4. 订单状态机扩展：增加 PROCESSING 中间状态（PENDING → PROCESSING → PAID/FAILED）

**改动量估算**：
| 子变更 | 新增字段 | 修改文件 | 预计工时 |
|--------|---------|---------|---------|
| order-management | +3 接口字段 | 3 文件 | 4h |
| payment-integration | 字段序列化调整 | 1 文件 | 1h |
| detailed-design.md | §3.2 + §4.1 修订 | 1 文档 | 0.5h |

**风险评估**：低风险。改动集中在支付流程，不影响已完成的 user-auth 子变更。

### 方案 B（最小改动方案）：order-management 单侧适配

**改动内容**：
1. order-management 增加字段容错，仅解析 provider + transactionId，忽略多余字段
2. payment-integration 保持现有标准，发送完整 5 字段
3. 不修改订单状态机，PENDING 直接跳转到 PAID

**局限性**：
- 缺少签名验证，存在安全风险（伪造回调）
- 缺少金额校验，无法检测支付金额与订单金额不一致
- 缺少 PROCESSING 状态，大额支付场景下可能出现状态不同步
- 长期维护成本高：后续子变更可能再次遇到此契约不一致

---

## 五、用户决策

| 选项 | 说明 | 建议 |
|------|------|------|
| 方案 A（推荐） | 统一接口 + 完整状态机 | ✅ 推荐：一次性根本解决 |
| 方案 B（最小改动） | 单侧适配 | ⚠️ 短期可行，长期有隐患 |
| 自定义 | 用户提供替代方案 | — |
| 拒绝改造 | 绕过此用例，后续处理 | 记录技术债务 |

> **用户选择**: 方案 A（示例中假定选择推荐方案）

---

## 六、执行记录

| 时间 | 操作 | 结果 |
|------|------|------|
| 2026-05-03 15:00 | Round 1 测试 ITC-007 失败 | 接口实现错误分类，尝试修复 |
| 2026-05-03 15:20 | Round 2 测试 ITC-007 失败（连续2次） | 怀疑接口契约问题 |
| 2026-05-03 15:40 | Round 3 测试 ITC-007 失败（连续3次） | ⚠️ 触发架构评估自动机制 |
| 2026-05-03 16:00 | 架构评估完成 | 输出多方案，等待用户决策 |
| 2026-05-03 16:30 | 用户选择方案 A | 开始执行：修订 detailed-design.md |
