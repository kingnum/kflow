# 集成测试用例：ecommerce-platform-init

> 本示例展示 v1.4.0 中新增的变更级集成测试用例格式，验证跨子变更接口契约。

---

## 测试信息
- **所属变更**: ecommerce-platform-init
- **测试类型**: 变更级集成测试
- **涉及子变更**: user-auth, order-management, payment-integration
- **跨子变更接口契约数**: 5

---

## 跨子变更接口契约清单

| 契约ID | 契约描述 | 提供方 | 消费方 | 验证方式 |
|--------|---------|--------|--------|---------|
| C-001 | JWT Token 格式和验证 | user-auth | order-management, payment-integration | 接口调用 |
| C-002 | 用户身份验证中间件 | user-auth | 所有子变更 | 接口调用 |
| C-003 | 用户信息查询接口 | user-auth | order-management | 接口调用 |
| C-004 | 订单数据查询接口 | order-management | payment-integration | 接口调用 |
| C-005 | 订单状态回调接口 | payment-integration | order-management | 接口调用 |

---

## 测试用例

### TC-INT-001: 认证 → 下单 → 支付 全流程

| 项目 | 详情 |
|------|------|
| **测试目标** | 验证从用户注册到支付完成的完整跨子变更流程 |
| **涉及契约** | C-001, C-002, C-003, C-004, C-005 |
| **涉及子变更** | user-auth, order-management, payment-integration |

#### 测试步骤

| 步骤 | 操作 | 涉及子变更 | 预期结果 |
|------|------|-----------|---------|
| 1 | 调用 POST /api/auth/register 注册用户 | user-auth | 返回 JWT token 和用户信息 |
| 2 | 使用 JWT token 调用 POST /api/orders 创建订单 | order-management (消费 C-001, C-002) | 订单创建成功，状态为 pending |
| 3 | 调用 GET /api/users/{id} 验证用户信息 | user-auth → order-management (契约 C-003) | 返回用户信息 |
| 4 | 调用 POST /api/orders/{id}/pay 发起支付 | payment-integration (消费 C-001, C-002, C-004) | 支付处理中 |
| 5 | 模拟支付回调 POST /api/payment/callback | payment-integration → order-management (契约 C-005) | 订单状态更新为 paid |

#### 验收标准

| 维度 | 标准 |
|------|------|
| Happy Path | 全流程 5 步全部成功，订单最终状态为 paid |
| Error Path | 步骤 2 使用无效 JWT → 返回 401 |
| Error Path | 步骤 4 使用其他用户 Token 访问他人订单 → 返回 403 |
| Edge Case | 步骤 2 使用过期 Token → 返回 401 + 提示刷新 |
| Quality | 全流程端到端响应时间 < 3s |

---

### TC-INT-002: 并发下单 - 库存一致性

| 项目 | 详情 |
|------|------|
| **测试目标** | 验证高并发场景下跨子变更的数据一致性 |
| **涉及契约** | C-002 |
| **涉及子变更** | user-auth, order-management |

#### 测试步骤

| 步骤 | 操作 | 预期结果 |
|------|------|---------|
| 1 | 准备 2 个已注册用户 | 各自持有有效 JWT token |
| 2 | 库存设为 1，两用户同时调用 POST /api/orders 购买同一商品 | 仅 1 个订单创建成功，另 1 个返回库存不足 |
| 3 | 检查数据库订单数和库存数 | 订单数 = 1，库存 = 0，数据一致 |

#### 验收标准

| 维度 | 标准 |
|------|------|
| Happy Path | 并发控制正确，无超卖 |
| Error Path | 库存不足时返回清晰的错误提示 |
| Quality | 无数据不一致或死锁 |

---

### TC-INT-003: JWT Token 跨子变更传播

| 项目 | 详情 |
|------|------|
| **测试目标** | 验证 JWT token 在所有子变更的 API 中正确传播和验证 |
| **涉及契约** | C-001, C-002 |
| **涉及子变更** | user-auth, order-management, payment-integration |

#### 测试步骤

| 步骤 | 操作 | 涉及接口 | 预期结果 |
|------|------|---------|---------|
| 1 | 获取有效 JWT token | POST /api/auth/login | 200, 返回 token |
| 2 | 使用 token 访问订单 API | GET /api/orders | 200, 返回订单列表 |
| 3 | 使用 token 访问支付 API | GET /api/payment/methods | 200, 返回支付方式 |
| 4 | 使用 token 访问用户 API | GET /api/users/me | 200, 返回当前用户信息 |
| 5 | 修改 token 中 userId → 访问订单 | GET /api/orders | 401, token 无效 |

#### 验收标准

| 维度 | 标准 |
|------|------|
| Happy Path | 所有子变更 API 正确识别有效 JWT token |
| Error Path | 被篡改的 token 被所有 API 拒绝 |
| Error Path | 过期 token 被所有 API 拒绝并提示刷新 |

---

## 测试执行记录

| 轮次 | 执行时间 | 用例数 | 通过 | 失败 | 通过率 | 报告 |
|------|---------|--------|------|------|--------|------|
| 1 | 2026-05-05 10:00 | 8 | 6 | 2 | 75% | round-1.md |
| 2 | 2026-05-05 14:00 | 8 | 8 | 0 | 100% | round-2.md |

## 总结

集成测试通过率 100%（第 2 轮），所有跨子变更接口契约验证通过。

| 契约ID | 验证轮次 | 最终结果 |
|--------|---------|---------|
| C-001 | Round 1 | ✅ 通过 |
| C-002 | Round 1 | ✅ 通过 |
| C-003 | Round 2 | ✅ 通过（第 1 轮失败，已修复） |
| C-004 | Round 1 | ✅ 通过 |
| C-005 | Round 2 | ✅ 通过（第 1 轮失败，已修复） |
