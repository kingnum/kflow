# 数据库迁移记录：ecommerce-platform-init

> 本示例展示 v1.4.0 中新增的数据库迁移记录格式。

---

## 迁移信息
- **所属变更**: ecommerce-platform-init
- **数据库**: MySQL 8.0
- **迁移目录**: `docs/changes/ecommerce-platform-init/migrations/`

## 迁移文件清单

| 序号 | 迁移文件 | 回滚文件 | 子变更 | 描述 |
|------|---------|---------|--------|------|
| 001 | 001_user-auth_create_users.sql | 001_user-auth_create_users_rollback.sql | user-auth | 创建用户表和会话表 |
| 002 | 002_user-auth_add_indexes.sql | 002_user-auth_add_indexes_rollback.sql | user-auth | 用户表性能索引 |
| 003 | 003_order-management_create_orders.sql | 003_order-management_create_orders_rollback.sql | order-management | 创建订单表和订单项表 |
| 004 | 004_payment-integration_create_payments.sql | 004_payment-integration_create_payments_rollback.sql | payment-integration | 创建支付记录表 |

## 执行记录

| 序号 | 迁移文件 | 子变更 | 执行时间 | 执行环境 | 状态 | 回滚状态 |
|------|---------|--------|---------|---------|------|---------|
| 001 | 001_user-auth_create_users.sql | user-auth | 2026-04-30 10:35 | dev | ✅ 成功 | 未回滚 |
| 002 | 002_user-auth_add_indexes.sql | user-auth | 2026-04-30 11:30 | dev | ✅ 成功 | 未回滚 |
| 003 | 003_order-management_create_orders.sql | order-management | 2026-05-02 10:15 | dev | ✅ 成功 | 未回滚 |
| 004 | 004_payment-integration_create_payments.sql | payment-integration | 2026-05-03 09:00 | dev | ⏳ 待执行 | N/A |

---

## 迁移脚本示例

### 001_user-auth_create_users.sql

```sql
-- 迁移: 创建用户表和会话表
-- 子变更: user-auth
-- 创建时间: 2026-04-30

CREATE TABLE IF NOT EXISTS users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    display_name VARCHAR(100),
    avatar_url VARCHAR(500),
    status ENUM('active', 'disabled', 'pending') DEFAULT 'pending',
    role ENUM('user', 'admin') DEFAULT 'user',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS user_sessions (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    token_hash VARCHAR(64) NOT NULL,
    refresh_token_hash VARCHAR(64),
    expires_at DATETIME NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_token_hash (token_hash),
    INDEX idx_expires_at (expires_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### 001_user-auth_create_users_rollback.sql

```sql
-- 回滚: 删除用户表和会话表
-- 对应迁移: 001_user-auth_create_users.sql

DROP TABLE IF EXISTS user_sessions;
DROP TABLE IF EXISTS users;
```

---

## 迁移规则

| 规则 | 说明 |
|------|------|
| 命名规范 | `{序号}_{子变更}_{描述}.sql` |
| 回滚脚本 | 每个迁移必须有对应的回滚脚本，命名为 `{序号}_{子变更}_{描述}_rollback.sql` |
| 序号格式 | 三位数字，递增（001, 002, ...） |
| 执行顺序 | 按序号依次执行 |
| 记录要求 | 每次执行后更新本 migration-log.md |
| 环境标记 | 记录执行的环境（dev/test/staging/prod） |
