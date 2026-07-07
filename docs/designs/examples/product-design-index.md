# 产品级设计索引入口示例：ecommerce-platform

> **版本**: 1.2.0
> **创建时间**: 2026-04-15
> **更新时间**: 2026-05-04
> **总功能点数**: 54

---

## 一、项目概述

电商平台，包含用户管理、商品管理、订单管理、支付集成等核心功能。前后端项目，前端基于 Vue 3，后端基于 Node.js + Express。

---

## 二、功能设计模块导航

| 功能模块 | 文件 | 功能点数 | 最后更新 | 活跃变更 |
|--------|------|----------|---------|---------|
| 认证 | [functional-designs/auth.md](functional-designs/auth.md) | 8 | 2026-05-04 | — |
| 商品 | [functional-designs/product.md](functional-designs/product.md) | 12 | 2026-05-01 | product-search-upgrade |
| 订单 | [functional-designs/order.md](functional-designs/order.md) | 15 | 2026-05-04 | — |
| 支付 | [functional-designs/payment.md](functional-designs/payment.md) | 10 | 2026-05-03 | fix-payment-callback |
| 用户 | [functional-designs/user.md](functional-designs/user.md) | 6 | 2026-04-28 | — |
| 通知 | [functional-designs/notification.md](functional-designs/notification.md) | 3 | 2026-04-20 | — |

---

## 三、技术设计文档

| 文档 | 说明 | 最后更新 |
|------|------|---------|
| [technical-designs/architecture.md](technical-designs/architecture.md) | 系统架构全景 | 2026-05-04 |
| [technical-designs/data-model.md](technical-designs/data-model.md) | 全景数据模型 | 2026-05-03 |
| [technical-designs/api-catalog.md](technical-designs/api-catalog.md) | API 目录 | 2026-05-04 |
| [technical-designs/nfr-baseline.md](technical-designs/nfr-baseline.md) | NFR 基线 | 2026-04-30 |

---

## 四、变更日志

| 日期 | 变更 | 功能模块 | 类型 |
|------|------|--------|------|
| 2026-05-04 | ecommerce-platform-init 归档 | auth, order, payment | 新增 |
| 2026-05-01 | product-search-upgrade | product | 更新 |
| 2026-04-30 | add-2fa 归档 | auth | 新增 |
| 2026-04-28 | user-profile 归档 | user | 新增 |
| 2026-04-20 | notification-system 归档 | notification | 新增 |

> 完整变更日志见 [changelog.md](changelog.md)

---

## 五、活跃变更

| 变更名称 | 功能模块 | 当前阶段 | 预计影响 |
|----------|--------|---------|---------|
| product-search-upgrade | product | 编码 | technical-designs/data-model.md, technical-designs/api-catalog.md |
| fix-payment-callback | payment | 缺陷修复 | functional-designs/payment.md |

---

## 六、NFR 基线摘要

| 类别 | 目标 | 当前值 |
|------|------|--------|
| API P95 延迟 | < 500ms | 320ms |
| 页面首次加载 | < 2s | 1.8s |
| 服务可用率 | 99.9% | 99.95% |
| 代码覆盖率 | ≥ 80% | 85% |
