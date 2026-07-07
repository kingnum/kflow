# 子变更任务清单：user-auth

## 子变更信息
- **所属变更**: ecommerce-platform-init
- **功能点数**: 10（≤10）
- **优先级**: 高
- **依赖子变更**: 无
- **当前阶段**: 编码

## 功能点清单

| 序号 | 功能点 | 关联功能点 | 状态 |
|------|--------|-----------|------|
| 1 | 用户注册 | #2 | ✅ 完成 |
| 2 | 用户登录 | #1, #3 | 🔄 进行中 |
| 3 | 密码重置 | #2 | ⏳ 待开始 |
| 4 | 用户信息修改 | #1 | ⏳ 待开始 |
| 5 | 用户头像上传 | #4 | ⏳ 待开始 |
| 6 | 用户注销 | #2 | ⏳ 待开始 |
| 7 | 用户禁用（管理员） | #1 | ⏳ 待开始 |
| 8 | 用户列表查询（管理员） | 无 | ⏳ 待开始 |
| 9 | 登录日志记录 | #2 | ⏳ 待开始 |
| 10 | 登出 | #2 | ⏳ 待开始 |

---

### 功能点 1: 用户注册

#### DoD 验收标准

| 维度 | 验收标准 | 状态 |
|------|---------|------|
| Happy Path | WHEN 用户输入有效邮箱和密码 THEN 系统创建用户并返回 JWT token | ✅ 通过 |
| Error Path | WHEN 用户输入已注册邮箱 THEN 系统返回 409 Conflict 且提示"邮箱已注册" | ✅ 通过 |
| Error Path | WHEN 用户密码长度 < 8 位 THEN 系统返回 400 Bad Request 且提示"密码长度至少8位" | ✅ 通过 |
| Edge Case | WHEN 用户邮箱长度 = 255 字符 THEN 系统正常处理（边界值测试） | ✅ 通过 |
| Quality | WHEN 并发 100 个注册请求 THEN 无数据损坏且 P95 < 500ms | ✅ 通过 |

#### 实现任务

- [x] **Step 1: 编写测试用例代码**
  ```java
  @Test
  void shouldRegisterUserSuccessfully() {
      UserRegistrationRequest request = new UserRegistrationRequest(
          "testuser@example.com",
          "password123",
          "Test User"
      );
      User user = userService.register(request);
      assertNotNull(user.getId());
      assertEquals("testuser@example.com", user.getEmail());
  }
  ```

- [x] **Step 2: 运行测试，确认失败（Red）**
  命令: `mvn test -Dtest=UserRegistrationTest`
  预期: FAIL

- [x] **Step 3: 实现最小代码**
  实现用户注册接口

- [x] **Step 4: 运行测试，确认通过（Green）**
  命令: `mvn test -Dtest=UserRegistrationTest`
  结果: PASS

- [x] **Step 5: 检查代码质量**
  检查是否符合编码规范，无安全漏洞

- [x] **Step 6: 执行必要重构（可选）**
  无需重构，代码结构清晰

- [x] **Step 7: 确认重构后测试仍通过**
  跳过（无重构）

- [x] **Step 8: 提交变更**
  commit: "feat(user-auth): implement user registration"

---

### 功能点 2: 用户登录

#### DoD 验收标准

| 维度 | 验收标准 | 状态 |
|------|---------|------|
| Happy Path | WHEN 用户输入正确的邮箱和密码 THEN 系统返回 JWT token 且有效期 15min | ⏳ |
| Error Path | WHEN 用户输入错误密码 THEN 系统返回 401 Unauthorized 且提示"邮箱或密码不正确" | ⏳ |
| Error Path | WHEN 用户连续 5 次输入错误密码 THEN 账号锁定 30 分钟 | ⏳ |
| Edge Case | WHEN 用户账号状态为 disabled THEN 系统返回 403 Forbidden 且提示"账号已被禁用" | ⏳ |
| Quality | WHEN 1000 并发登录请求 THEN 登录成功率 ≥ 99.9% 且无数据泄露 | ⏳ |

#### 实现任务

- [x] **Step 1: 编写测试用例代码**
  ```java
  @Test
  void shouldLoginUserSuccessfully() {
      UserLoginRequest request = new UserLoginRequest(
          "testuser@example.com",
          "password123"
      );
      LoginResponse response = userService.login(request);
      assertNotNull(response.getToken());
      assertEquals("testuser@example.com", response.getUser().getEmail());
  }
  ```

- [x] **Step 2: 运行测试，确认失败（Red）**
  命令: `mvn test -Dtest=UserLoginTest`
  预期: FAIL

- [ ] **Step 3: 实现最小代码**
  实现用户登录接口

- [ ] **Step 4: 运行测试，确认通过（Green）**
  命令: `mvn test -Dtest=UserLoginTest`
  预期: PASS

- [ ] **Step 5: 检查代码质量**
- [ ] **Step 6: 执行必要重构（可选）**
- [ ] **Step 7: 确认重构后测试仍通过**
- [ ] **Step 8: 提交变更**

---

### 功能点 3: 密码重置

#### DoD 验收标准

| 维度 | 验收标准 | 状态 |
|------|---------|------|
| Happy Path | WHEN 用户输入已注册邮箱 THEN 系统发送密码重置链接到该邮箱 | ⏳ |
| Error Path | WHEN 用户输入未注册邮箱 THEN 系统返回 200 OK 但提示"如邮箱已注册，将收到重置链接" | ⏳ |
| Error Path | WHEN 重置链接已过期（>30min） THEN 系统提示"链接已过期，请重新申请" | ⏳ |
| Edge Case | WHEN 用户连续请求重置密码超过 5 次/小时 THEN 系统限流 | ⏳ |
| Quality | WHEN 重置密码完成 THEN 所有该用户的活跃 Token 立即失效 | ⏳ |

#### 实现任务

- [ ] **Step 1: 编写测试用例代码**
- [ ] **Step 2: 运行测试，确认失败（Red）**
- [ ] **Step 3: 实现最小代码**
- [ ] **Step 4: 运行测试，确认通过（Green）**
- [ ] **Step 5: 提交变更**

---

### 功能点 4-10: 其他功能点

（每个功能点按上述格式展开，包含 DoD 验收标准区块和 TDD 任务列表）

---

## 数据库迁移任务

- [ ] 编写迁移脚本: `001_user-auth_create_users.sql`
- [ ] 编写回滚脚本: `001_user-auth_create_users_rollback.sql`
- [ ] 执行迁移并记录到迁移日志

---

## 代码审查任务

- [ ] Agent 1 (安全+规范): SQL注入/XSS/CSRF 检查
- [ ] Agent 2 (质量+性能): N+1查询/内存泄漏/复杂度检查
- [ ] 输出代码审查报告

---

## 集成验证

- [ ] 运行子变更全部单元测试
- [ ] 执行 E2E 测试（参考 e2e-tests/）
- [ ] 确认所有测试通过和 DoD 验收全部满足
- [ ] 提交代码变更

---

## 代码重构

- [ ] 检查代码质量
- [ ] 执行必要的重构（Refactor）
- [ ] 确认重构后测试仍通过

---

## 任务执行记录

### 2026-04-30 10:30
- 开始编码阶段
- 功能点1（用户注册）开始实现

### 2026-04-30 10:45
- 功能点1（用户注册）实现完成
- DoD 验收全部通过
- 测试通过，提交变更

### 2026-04-30 11:00
- 功能点2（用户登录）开始实现
- 测试代码编写完成
- 测试执行失败（Red）- 符合预期
