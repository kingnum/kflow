# 缺陷修复状态示例：BUG-005

> **示例说明**: 本文件展示 `bugs/fix/{BUG-ID}/bugfix-status.md`（缺陷级状态文件）的完整填写形态。
>
> 格式模板见 [templates/changes/{change}/bugs/fix/{BUG-ID}/bugfix-status.md](../templates/changes/{change}/bugs/fix/{BUG-ID}/bugfix-status.md)；字段定义见 [core-mechanisms/03-status-and-tasks.md](../core-mechanisms/03-status-and-tasks.md#35-缺陷级状态文件格式-bugsfixbug-idbugfix-statusmd)；机制定义见 `bugfix-fast-lane` 能力。
>
> 样例背景：变更 `ecommerce-platform-init`（前后端项目，含 3 个子变更 `user-auth` / `order-management` / `payment-integration`）。用户在验收时反馈订单导出金额显示错误，经 `kflow-bug-triage` 四层溯源判定为 L4 实现层缺陷，进入缺陷修复快车道。

---

## 一、基本信息

| 字段 | 值 |
|------|---|
| 缺陷标识 | BUG-005 |
| 所属变更 | ecommerce-platform-init |
| 分诊时间 | 2026-10-13 10:20 |
| 问题源头层级 | L4 实现执行 |
| 当前阶段 | 已收口 |

---

## 二、分诊结论

| 字段 | 值 |
|------|---|
| 四层判断摘要 | L1 功能点「订单导出」已定义导出字段含金额（含币种与两位小数）；L2 原型的导出结果页展示了正确的金额格式；L3 `detailed-design.md` 的 `/api/orders/export` 接口定义明确 `amount` 为 `decimal(10,2)` 且响应中含 `currency`。三层均通过，问题归因于 L4 代码实现 |
| 影响范围评估 | 受影响功能点 1 个（FP-018 订单导出）、受影响接口 1 个（`/api/orders/export`）、无数据模型变更 |

**四层溯源摘要**：

| 层级 | 结论 | 判断依据 |
|------|------|---------|
| L1 需求定义 | ✅ 通过 | `functional-designs/index.md` 的 FP-018「订单导出」明确列出金额列的格式要求（币种 + 两位小数），无歧义、边界条件齐全 |
| L2 原型设计 | ✅ 通过 | `docs/designs/prototypes/screens/order-export.html` 的导出结果预览展示了 `¥1,299.00` 形式的金额 |
| L3 详细设计 | ✅ 通过 | `detailed-design.md` 接口章节定义 `/api/orders/export` 响应字段 `amount`（`decimal(10,2)`）与 `currency`，与功能点一致 |
| L4 实现执行 | ❌ 问题源头 | `OrderExportService.java:142` 将 `BigDecimal` 金额转为 `double` 后做除法换算折扣价，浮点运算丢失精度，与 L3 的 `decimal` 定义不符 |

**用户确认记录**：

| 字段 | 值 |
|------|---|
| 用户是否覆盖诊断结论 | 否 |
| 覆盖后指定的层级 | 无 |
| 覆盖原因 | （无） |

---

## 三、受影响项清单

| 类别 | 清单 |
|------|------|
| 受影响功能点 | FP-018 |
| 受影响接口 | /api/orders/export |
| 受影响测试用例 | API-ORD-014（订单导出接口 - 金额字段格式）、API-ORD-015（订单导出接口 - 折扣订单金额计算） |
| 数据模型变更 | none |
| 影响范围分数 | 1×1 + 1×1.5 + 0×2 = 2.5 |

---

## 四、修复记录

| 字段 | 值 |
|------|---|
| 修复阶段状态 | 已完成 |
| 起始时间 | 2026-10-13 10:35 |
| 结束时间 | 2026-10-13 14:10 |
| 耗时 | 3h35m |
| 轮次 | 3 |
| 根因分类 | 实现错误 |
| 修复文件 | src/main/java/com/example/order/OrderExportService.java, src/test/java/com/example/order/OrderExportServiceTest.java |
| Regression Test at Correct Seam | ✅ 正确 seam——`OrderExportServiceTest` 通过 service 入口复制完整的「查询订单 → 计算折扣价 → 序列化导出」调用链，能够锻炼真实 bug 模式；已先写回归测试确认失败（`amount` 应为 `1299.00` 实为 `1298.9999999999998`）→ 应用修复 → 确认通过 |

**修复内容**：

- 第 1 轮（直接修复）：将 `amount.doubleValue()` 改为全链路 `BigDecimal` 运算，除法使用 `divide(divisor, 2, RoundingMode.HALF_UP)`。定向验证仍失败——`API-ORD-015` 期望 `¥0.00` 场景下返回 `null`（设计定义：折扣后金额为 0 时不显示金额列）。
- 第 2 轮（替代方案）：改用 `DecimalFormat("#,##0.00")` 统一格式化并在序列化层截断，未解决 `null` 语义问题。定向验证仍失败。
- 第 3 轮（重新审视假设）：重新对照 `detailed-design.md` 的接口定义，确认「金额为 0 → 返回 `null`」是设计约定，前两轮均误将该场景当作格式化问题处理。改为在计算层判定 `compareTo(BigDecimal.ZERO) == 0` 后返回 `null`。定向验证通过。

**Post-mortem**：

- 「什么可以防止此缺陷发生？」——货币与金额一律使用 `BigDecimal` 且禁止隐式转 `double`，这是本项目既有的编码约定，但未在代码审查的检查项中显式列出。
- 根本原因为何未被早期阶段捕获？`api-tests/` 的 `API-ORD-014` 只断言字段存在与类型，未断言精度；建议在测试用例设计规范中补充「金额类字段 MUST 断言精确值与边界值（0、负数、大额）」。
- 架构改进识别：无正确 seam 问题；但金额计算逻辑分散在 `OrderExportService` 与 `OrderCalculator` 两处，建议抽为单一 `Money` 值对象——已作为架构改进建议传递给 `kflow-audit`。

---

## 五、定向验证

### 验证记录 1

| 字段 | 值 |
|------|---|
| 验证时间 | 2026-10-13 11:50 |
| 验证范围 | 受影响项清单覆盖的测试用例 |
| 用例清单与结果 | API-ORD-014 → ❌、API-ORD-015 → ❌ |
| 受影响项覆盖率 | 100% |
| 通过结果 | 未通过 |
| 失败用例 | API-ORD-014, API-ORD-015 |
| 失败原因 | API-ORD-014 仍返回 `1298.9999999999998`；API-ORD-015 在折扣后金额为 0 时返回 `¥0.00` 而非设计的 `null` |
| 报告路径 | — |

### 验证记录 2

| 字段 | 值 |
|------|---|
| 验证时间 | 2026-10-13 13:05 |
| 验证范围 | 受影响项清单覆盖的测试用例 |
| 用例清单与结果 | API-ORD-014 → ❌、API-ORD-015 → ❌ |
| 受影响项覆盖率 | 100% |
| 通过结果 | 未通过 |
| 失败用例 | API-ORD-014, API-ORD-015 |
| 失败原因 | API-ORD-015 的 `null` 语义问题仍未解决；API-ORD-014 因格式化层改为 `DecimalFormat` 后本地通过，但导出响应经序列化后仍丢失末位精度 |
| 报告路径 | — |

### 验证记录 3

| 字段 | 值 |
|------|---|
| 验证时间 | 2026-10-13 14:05 |
| 验证范围 | 受影响项清单覆盖的测试用例 |
| 用例清单与结果 | API-ORD-014 → ✅、API-ORD-015 → ✅ |
| 受影响项覆盖率 | 100% |
| 通过结果 | 通过 |
| 失败用例 | （无） |
| 失败原因 | （无） |
| 报告路径 | bugs/fix/BUG-005/verify-report.md |

> 三次定向验证对应三次修复尝试：第 1 次与第 2 次未通过、第 3 次通过，未触及「三次修复尝试上限」（第 4 次 = 上限 + 1 才升级用户）。全流程未重跑该变更的全量测试套件，未触发集成测试轮次。

---

## 六、收口结论

| 校验项 | 结论 |
|-------|------|
| 受影响项清单 100% 覆盖且全部通过 | ✅ 满足 |
| 定向验证报告存在 | ✅ 满足 |
| 本文件全部必填区已填写且无占位符 | ✅ 满足 |
| 收口时间 | 2026-10-13 14:20 |
| 缺陷最终状态 | 已解决 |

**收口动作执行记录**：

- `bugs/index.md` 中 BUG-005 对应行状态更新为「已解决」，修复通道列为「快车道」
- `bugs/bug-001-020.md` 中 BUG-005 的「修复记录」节已追加修复摘要（修复日期、根因分类、修复文件、验证结果、修复内容、Post-mortem）
- 问题详情中的「快车道入口与收口状态」节收口状态更新为「已收口」
- 变更级 `.status.md` 的阶段状态矩阵字段**未做任何修改**
