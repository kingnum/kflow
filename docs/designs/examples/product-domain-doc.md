# 认证域

> **设计域**: auth
> **最后更新**: 2026-05-04
> **来源变更**: ecommerce-platform-init（2026-05-04）、add-2fa（2026-04-30）

---

## 一、功能设计

### 1.1 功能概述

认证域负责用户身份验证和会话管理，包括注册、登录、密码重置、双因素认证等功能。

### 1.2 功能点清单

| 功能点 | 描述 | 来源变更 | 归档时间 |
|--------|------|---------|---------|
| 用户注册 | 邮箱+密码注册，发送验证邮件 | ecommerce-platform-init | 2026-05-04 |
| 用户登录 | 邮箱+密码登录，返回 JWT token | ecommerce-platform-init | 2026-05-04 |
| 密码重置 | 通过邮箱验证码重置密码 | ecommerce-platform-init | 2026-05-04 |
| 双因素认证 | TOTP 二次验证 | add-2fa | 2026-04-30 |

---

## 二、技术设计

### 2.1 技术选型

| 组件 | 技术 | 版本 |
|------|------|------|
| 认证协议 | JWT + Refresh Token | — |
| 密码加密 | bcrypt | 2.4.3 |
| 双因素认证 | speakeasy (TOTP) | 2.0.0 |
| Token 存储 | Redis | 7.x |

### 2.2 数据模型

#### User 实体
```
User:
  - id: UUID (PK)
  - email: string (unique, indexed)
  - passwordHash: string
  - isVerified: boolean
  - twoFactorEnabled: boolean
  - twoFactorSecret: string (encrypted)
  - createdAt: datetime
  - updatedAt: datetime
```

#### RefreshToken 实体
```
RefreshToken:
  - id: UUID (PK)
  - userId: UUID (FK → User)
  - token: string (indexed)
  - expiresAt: datetime
  - createdAt: datetime
```

### 2.3 接口设计

| 接口 | 方法 | 路径 | 认证 |
|------|------|------|------|
| 注册 | POST | /api/auth/register | 无 |
| 登录 | POST | /api/auth/login | 无 |
| 刷新 Token | POST | /api/auth/refresh | Refresh Token |
| 登出 | POST | /api/auth/logout | JWT |
| 密码重置请求 | POST | /api/auth/reset-password | 无 |
| 密码重置确认 | PUT | /api/auth/reset-password | 验证码 |
| 双因素设置 | POST | /api/auth/2fa/setup | JWT |
| 双因素验证 | POST | /api/auth/2fa/verify | JWT + TOTP |

### 2.4 安全设计

- 密码: bcrypt 12 rounds 哈希
- JWT: RS256 签名，access token 15min 过期，refresh token 7d 过期
- 双因素: TOTP 30s 窗口，2 个窗口容差
- 限流: 登录接口 5次/分钟/IP，密码重置 1次/分钟/邮箱
- 敏感字段: twoFactorSecret AES-256-GCM 加密存储

> 来源变更: add-2fa | 归档时间: 2026-04-30
> 原始文件: docs/archive/2026-04-30-add-2fa/

### 2.5 跨域接口契约

| 接口 | 提供者 | 消费者 | 契约 |
|------|--------|--------|------|
| 用户身份验证 | auth | order, payment | GET /api/auth/verify → { userId, roles } |
| 用户信息查询 | auth | order, payment | GET /api/users/{id} → { id, email } |

> 来源变更: ecommerce-platform-init | 归档时间: 2026-05-04
> 原始文件: docs/archive/2026-05-04-ecommerce-platform-init/
