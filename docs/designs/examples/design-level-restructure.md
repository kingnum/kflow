# 统一详细设计示例：ecommerce-platform-init

> 本示例展示 v1.5.0 中变更级 detailed-design.md 的完整格式，包含 NFR 章节、多子变更设计、跨子变更接口契约。

---

> **版本**: 1.0.0
> **创建时间**: 2026-04-30
> **关联变更**: ecommerce-platform-init
> **项目类型**: 前后端项目

---

## 一、系统架构

### 技术选型

| 层级 | 技术 | 版本 | 说明 |
|------|------|------|------|
| 前端框架 | Vue.js | 3.4 | Composition API + TypeScript |
| 后端框架 | Spring Boot | 3.2 | Java 17 |
| 数据库 | MySQL | 8.0 | 主数据库 |
| 缓存 | Redis | 7.0 | 会话缓存 + 热点数据 |

### 模块划分

```
ecommerce-platform
├── 认证域 (auth)
│   ├── 用户注册/登录
│   ├── 密码管理
│   └── 权限控制
├── 业务域 (business)
│   ├── 订单管理
│   ├── 商品管理
│   └── 购物车
└── 基础设施域 (infra)
    ├── 日志服务
    ├── 文件存储
    └── 消息队列
```

---

## 二、设计域章节

### 2.1 认证域

#### 功能点设计

| 功能点ID | 功能点名称 | 数据模型 | 接口 | 核心流程 | 所属子变更 |
|----------|-----------|---------|------|---------|-----------|
| FP-001 | 用户注册 | User | POST /api/auth/register | 邮箱验证→创建用户→发送欢迎邮件 | user-auth |
| FP-002 | 用户登录 | User, Session | POST /api/auth/login | 验证凭据→生成JWT→创建会话 | user-auth |
| FP-003 | 密码重置 | User, ResetToken | POST /api/auth/reset-password | 验证邮箱→发送重置链接→更新密码 | user-auth |
| FP-004 | 用户信息修改 | UserProfile | PUT /api/users/{id} | 验证权限→更新字段→刷新缓存 | user-auth |
| FP-005 | 用户头像上传 | User, FileStorage | POST /api/users/{id}/avatar | 验证文件→上传MinIO→更新URL | user-auth |

#### 数据模型：User

```
User:
  - id: Long (PK, auto_increment)
  - email: VARCHAR(255) UNIQUE NOT NULL
  - password_hash: VARCHAR(255) NOT NULL
  - display_name: VARCHAR(100)
  - avatar_url: VARCHAR(500)
  - status: ENUM('active','disabled','pending')
  - role: ENUM('user','admin')
  - created_at: DATETIME
  - updated_at: DATETIME
```

索引: idx_email (email), idx_status (status)

#### 接口设计

| 接口 | 方法 | 路径 | 入参 | 出参 | 跨子变更契约 |
|------|------|------|------|------|------------|
| 用户注册 | POST | /api/auth/register | {email, password, name} | {id, email, token} | order-management 依赖用户认证 |
| 用户登录 | POST | /api/auth/login | {email, password} | {token, user} | 所有子变更共用 JWT token |
| 获取用户信息 | GET | /api/users/{id} | - | {user} | order-management 查询用户信息 |

#### 跨子变更接口契约

| 契约 | 提供方 | 消费方 | 约定 |
|------|--------|--------|------|
| JWT Token 格式 | user-auth | order-management, payment-integration | Header: Authorization: Bearer {jwt} |
| 用户身份验证中间件 | user-auth | 所有子变更 | 请求自动注入 currentUserId |
| 用户信息查询接口 | user-auth | order-management | GET /api/users/{id} 批量接口 P95 < 100ms |

### 2.2 业务域

#### 功能点设计

| 功能点ID | 功能点名称 | 数据模型 | 接口 | 核心流程 | 所属子变更 |
|----------|-----------|---------|------|---------|-----------|
| FP-006 | 创建订单 | Order, OrderItem | POST /api/orders | 验证库存→锁定商品→生成订单→扣减库存 | order-management |
| FP-007 | 订单列表查询 | Order | GET /api/orders | 分页查询→按状态过滤→按时间排序 | order-management |
| FP-008 | 订单详情查询 | Order, OrderItem | GET /api/orders/{id} | 查询订单→关联商品→查询物流 | order-management |
| FP-009 | 取消订单 | Order | PUT /api/orders/{id}/cancel | 验证状态→释放库存→更新状态 | order-management |
| FP-010 | 订单支付 | Order, Payment | POST /api/orders/{id}/pay | 调用支付→验证结果→更新订单状态 | payment-integration |

#### 数据模型：Order

```
Order:
  - id: Long (PK)
  - user_id: Long (FK → User.id)
  - status: ENUM('pending','paid','shipped','completed','cancelled')
  - total_amount: DECIMAL(10,2)
  - shipping_address: TEXT
  - created_at: DATETIME
  - updated_at: DATETIME

OrderItem:
  - id: Long (PK)
  - order_id: Long (FK → Order.id)
  - product_id: Long
  - quantity: INT
  - unit_price: DECIMAL(10,2)
```

---

## 三、非功能需求 (NFR)

### 3.1 性能需求

| 需求项 | 目标值 | 测量方式 | 适用场景 |
|--------|--------|---------|---------|
| API P95 响应时间 | < 500ms | 接口单元测试 | 所有查询接口 |
| API P99 响应时间 | < 1000ms | 接口单元测试 | 写操作 |
| 页面加载时间 | < 2s (首次) | E2E 测试 / Lighthouse | 前后端项目 |
| 数据库查询时间 | < 100ms | 单元测试 | 复杂联表查询 |
| 并发用户数 | ≥ 1000 | 压力测试 | 全站 |

### 3.2 安全需求

| 需求项 | 要求 | 验证方式 | 适用场景 |
|--------|------|---------|---------|
| 认证机制 | JWT + Refresh Token，Access Token 15min 过期 | 安全审查 | 所有接口 |
| 权限控制 | RBAC (user/admin)，管理接口仅 admin | 安全审查 | 管理接口 |
| 数据加密 | 密码 bcrypt(12)，敏感字段 AES-256 | 安全审查 + 代码审查 | 用户信息 |
| SQL注入防护 | 100% 参数化查询，禁止拼接 SQL | 代码审查 | 所有数据层 |
| XSS防护 | 输出编码，Content-Security-Policy 头 | 代码审查 | 前后端项目 |
| CSRF防护 | SameSite Cookie + CSRF Token | 代码审查 | 前后端项目 |

### 3.3 可用性需求

| 需求项 | 目标值 | 说明 |
|--------|--------|------|
| 服务可用率 | 99.9% | 非计划停机 < 8h/年 |
| 故障恢复时间 | < 30min | 自动故障转移 |
| 数据备份 | 每日全量 + binlog 增量 | 可恢复到任意时间点 |

### 3.4 可维护性需求

| 需求项 | 要求 | 说明 |
|--------|------|------|
| 日志规范 | 结构化日志 (JSON), traceId 贯穿 | 基于 SLF4J + Logback |
| 代码覆盖率 | ≥ 80% | 接口单元测试 |
| API 文档 | OpenAPI 3.0 (SpringDoc) | 所有接口 |
| 健康检查 | /health, /health/db, /health/redis | Actuator endpoint |

---

## 四、子变更划分

### 划分结果

| 子变更 | 功能点数 | 包含功能点ID | 依赖子变更 | 优先级 |
|--------|----------|-------------|-----------|--------|
| user-auth | 5 | FP-001~FP-005 | 无 | 高 |
| order-management | 4 | FP-006~FP-009 | user-auth | 高 |
| payment-integration | 1 | FP-010 | order-management | 中 |

### 依赖关系图

```
user-auth → order-management → payment-integration
```

### 实现顺序

1. user-auth（无依赖，基础模块，优先实现）
2. order-management（依赖 user-auth 提供用户认证）
3. payment-integration（依赖 order-management 提供订单数据）

---

## 五、配置项设计

| 配置项 | 类型 | 默认值 | 环境区分 | 说明 |
|--------|------|--------|---------|------|
| JWT_SECRET | String | - | dev/test/staging/prod | 通过环境变量 ${JWT_SECRET} 注入 |
| JWT_EXPIRATION_MINUTES | int | 15 | dev/test: 60 / staging/prod: 15 | Token 过期时间 |
| DB_MAX_POOL_SIZE | int | 20 | prod: 50 / 其他: 20 | 数据库连接池 |
| REDIS_HOST | String | localhost | 按环境配置 | Redis 缓存地址 |

## 六、错误处理设计

| 错误场景 | 错误码 | HTTP Status | 处理方式 | 用户提示 |
|----------|--------|------------|---------|---------|
| 邮箱已注册 | AUTH_001 | 409 | 返回冲突 | "该邮箱已注册，请直接登录" |
| 密码错误 | AUTH_002 | 401 | 记录尝试次数 | "邮箱或密码不正确" |
| Token 过期 | AUTH_003 | 401 | 返回刷新提示 | "登录已过期，请重新登录" |
| 库存不足 | ORDER_001 | 400 | 返回当前库存量 | "商品库存不足，当前库存: {n}" |
| 订单不可取消 | ORDER_002 | 422 | 返回当前状态 | "订单状态为'{status}'，不可取消" |
| 支付失败 | PAY_001 | 402 | 记录失败日志 | "支付失败，请重试" |
