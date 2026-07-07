# 项目服务指引

> **项目**: ecommerce-platform-init
> **生成时间**: 2026-04-30 09:00
> **生成阶段**: 编码阶段自动生成
> **版本**: 1.4.0（支持多环境配置）

---

## 项目类型

- **类型**: Java/Spring Boot + Vue.js
- **后端框架**: Spring Boot 3.2
- **前端框架**: Vue.js 3.x

### 项目类型检测依据

| 检测项 | 检测结果 | 说明 |
|--------|---------|------|
| pom.xml | ✅ 存在 | Java/Maven 项目 |
| package.json | ✅ 存在 | Node.js 前端项目 |
| Vue 框架依赖 | ✅ vue: 3.x | 前后端项目 |
| Spring Boot 依赖 | ✅ spring-boot-starter | 后端框架 |

---

## 多环境配置

### dev 环境

| 配置项 | 值 | 说明 |
|--------|---|------|
| 后端启动命令 | `mvn spring-boot:run -Dspring-boot.run.profiles=dev` | Spring Boot 开发模式 |
| 前端启动命令 | `npm run dev` | Vite HMR 开发模式 |
| 后端端口 | 8080 | Spring Boot 服务端口 |
| 前端端口 | 5173 | Vite 开发服务器端口 |
| 数据库 | localhost:3306/ecommerce_dev | 本地开发库 |
| Redis | localhost:6379 | 本地缓存 |
| 配置变量 | `SPRING_PROFILES_ACTIVE=dev` | |

### test 环境

| 配置项 | 值 | 说明 |
|--------|---|------|
| 后端启动命令 | `mvn spring-boot:run -Dspring-boot.run.profiles=test` | 测试环境 |
| 前端启动命令 | `npm run dev -- --mode test` | 测试模式 |
| 后端端口 | 8081 | 测试端口（避免与 dev 冲突） |
| 前端端口 | 5174 | |
| 数据库 | test-db.internal:3306/ecommerce_test | 测试专用库 |
| Redis | test-redis.internal:6379 | 测试缓存 |

### staging 环境

| 配置项 | 值 | 说明 |
|--------|---|------|
| 启动命令 | `java -jar target/app.jar --spring.profiles.active=staging` | 预发布 |
| 端口 | 8080 | |
| 数据库 | staging-db.internal:3306/ecommerce_staging | 预发布数据库 |
| Redis | staging-redis.internal:6379 | |

### prod 环境

| 配置项 | 值 | 说明 |
|--------|---|------|
| 启动命令 | `java -jar target/app.jar --spring.profiles.active=prod` | 生产环境 |
| 端口 | 8080 | |
| 数据库 | `${PROD_DB_HOST}:${PROD_DB_PORT}/${PROD_DB_NAME}` | 通过环境变量注入 |
| Redis | `${PROD_REDIS_HOST}:${PROD_REDIS_PORT}` | 通过环境变量注入 |

> **安全要求**: 密码、密钥等敏感信息必须通过环境变量引用（如 `${DB_PASSWORD}`、`${JWT_SECRET}`），禁止明文写入本文档。

---

## 测试账号

| 环境 | 账号类型 | 用户名 | 密码来源 |
|------|---------|--------|---------|
| dev | 管理员 | admin_test | `${DEV_ADMIN_PASSWORD}` |
| dev | 普通用户 | user_test | `${DEV_USER_PASSWORD}` |
| test | 管理员 | admin_test | `${TEST_ADMIN_PASSWORD}` |
| test | 普通用户 | test_user_1 | `${TEST_USER_PASSWORD}` |

---

## 健康检查

| 检查项 | 接口 | 说明 |
|--------|------|------|
| 服务健康 | GET /actuator/health | Spring Boot Actuator |
| 数据库连接 | GET /actuator/health/db | 数据库健康检查 |
| Redis 连接 | GET /actuator/health/redis | 缓存健康检查 |

---

## 服务依赖

| 服务 | dev | test | staging | prod |
|------|-----|------|---------|------|
| MySQL | localhost:3306 | test-db.internal:3306 | staging-db.internal:3306 | `${PROD_DB_HOST}` |
| Redis | localhost:6379 | test-redis.internal:6379 | staging-redis.internal:6379 | `${PROD_REDIS_HOST}` |
| MinIO | localhost:9000 | test-minio.internal:9000 | staging-minio.internal:9000 | `${PROD_MINIO_ENDPOINT}` |

---

## 编码阶段自动化循环参考

### 编译 → 重启 → 测试 流程

1. **编译代码**: `mvn compile`
2. **重启服务**: `mvn spring-boot:run`（或使用 IDE 重启）
3. **执行测试**: `mvn test -Dtest={TestClassName}`

### 前端开发流程

1. **启动前端**: `npm run dev`
2. **浏览器访问**: `http://localhost:5173`
3. **API 代理**: 请求自动代理到 `http://localhost:8080`

---

## 测试执行配置

### 接口单元测试

| 配置项 | 值 | 说明 |
|--------|---|------|
| 测试命令 | `mvn test` | 执行所有单元测试 |
| 单个测试 | `mvn test -Dtest={ClassName}` | 执行指定测试类 |
| 覆盖率报告 | `mvn jacoco:report` | 生成覆盖率报告 |
| 覆盖率目标 | ≥ 80% | 代码覆盖率要求 |

### E2E 测试（前后端项目）

| 配置项 | 值 | 说明 |
|--------|---|------|
| 测试工具 | Playwright | 浏览器自动化测试 |
| 测试命令 | `npx playwright test` | 执行 E2E 测试 |
| 测试报告 | `playwright-report/` | 测试报告目录 |
| 测试浏览器 | Chrome | 默认测试浏览器 |

---

## 环境变量

| 变量名 | dev | test | staging | prod 来源 |
|--------|-----|------|---------|----------|
| SPRING_PROFILES_ACTIVE | dev | test | staging | prod |
| DB_HOST | localhost | test-db.internal | staging-db.internal | `${PROD_DB_HOST}` |
| DB_PORT | 3306 | 3306 | 3306 | `${PROD_DB_PORT}` |
| DB_NAME | ecommerce_dev | ecommerce_test | ecommerce_staging | `${PROD_DB_NAME}` |
| DB_USERNAME | dev_user | test_user | staging_user | `${PROD_DB_USERNAME}` |
| DB_PASSWORD | `****` | `****` | `****` | `${PROD_DB_PASSWORD}` |
| JWT_SECRET | `****` | `****` | `****` | `${JWT_SECRET}` |
| REDIS_HOST | localhost | test-redis.internal | staging-redis.internal | `${PROD_REDIS_HOST}` |
| REDIS_PORT | 6379 | 6379 | 6379 | `${PROD_REDIS_PORT}` |

---

## 注意事项

1. **启动顺序**: 先启动后端服务，再启动前端服务
2. **数据库准备**: 确保对应环境的 MySQL 服务运行且数据库已创建
3. **迁移执行**: 编码阶段涉及数据模型变更时，按迁移序号执行迁移脚本
4. **测试数据**: 测试账号仅供测试使用，不要用于生产环境
5. **端口冲突**: 多环境并行时，注意端口分配
6. **敏感信息**: 严禁在本文档中明文记录密码、密钥等敏感信息，必须通过环境变量引用
