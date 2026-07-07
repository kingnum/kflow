# 工具链配置示例：ecommerce-platform

> **创建时间**: 2026-05-04 10:00
> **项目类型**: 前后端项目
> **覆盖度**: 95%

---

## 一、环境能力扫描

### Skills

| Skill | 状态 | 适用场景 |
|-------|------|---------|
| huashu-design | ✅ 已安装 | HTML 原型设计 |
| kflow-guide | ✅ 已安装 | 流程指引 |
| kflow-explore | ✅ 已安装 | 设计探索 |
| kflow-prototype-design | ✅ 已安装 | 原型设计 |
| kflow-design | ✅ 已安装 | 详细设计 |
| kflow-plan | ✅ 已安装 | 计划 |
| kflow-code | ✅ 已安装 | 编码 |
| kflow-e2e-test | ✅ 已安装 | E2E 测试 |
| kflow-bug-fix | ✅ 已安装 | 缺陷修复 |
| kflow-status | ✅ 已安装 | 状态总结 |
| kflow-archive | ✅ 已安装 | 归档 |
| kflow-audit | ✅ 已安装 | 使用评估 |
| kflow-init | ✅ 已安装 | 环境初始化 |
| /playwright-cli | ❌ 未安装 | E2E 浏览器测试 |

---

## 二、阶段工具推荐

| 阶段 | 首选工具 | 备选工具 | 状态 |
|------|---------|---------|------|
| 设计探索 | Read, Glob, Grep | — | ✅ 可用 |
| 原型设计 | huashu-design Skill | — | ✅ 可用 |
| 详细设计 | Read, Write, Edit, Agent | — | ✅ 可用 |
| 计划 | Write, Edit | — | ✅ 可用 |
| 编码 | Bash, Read, Write, Edit, Agent | — | ✅ 可用 |
| 接口单元测试 | Bash, Read, Edit | — | ✅ 可用 |
| E2E 测试 | /playwright-cli skill | playwright MCP | ⚠️ 需安装 |
| 集成测试 | Bash, Read, Agent | — | ✅ 可用 |
| 缺陷修复 | Bash, Read, Edit, Agent | — | ✅ 可用 |
| 归档 | Bash, Read, Write, Edit | — | ✅ 可用 |
| 审计 | Read, Agent | — | ✅ 可用 |

---

## 三、安装建议

| 工具 | 用途 | 安装方式 | 优先级 |
|------|------|---------|--------|
| /playwright-cli | E2E 浏览器自动化测试 | 安装 skill | 高 |
| playwright MCP | E2E 备选方案 | 配置 MCP server | 低 |

---

## 四、多方案对比

### 方案 A：推荐最佳组合 (覆盖度 95%)

| 阶段 | 工具 | 风险 |
|------|------|------|
| 原型设计 | huashu-design Skill | 低 |
| E2E 测试 | /playwright-cli skill | 低 |

### 方案 B：降级方案 (覆盖度 90%)

| 阶段 | 工具 | 风险 |
|------|------|------|
| 原型设计 | huashu-design Skill | 低 |
| E2E 测试 | playwright MCP | 中（封装度较低） |

### 方案 C：最小必须方案 (覆盖度 70%)

| 阶段 | 工具 | 风险 |
|------|------|------|
| 原型设计 | ⏭️ 跳过 | 中（无原型验证） |
| E2E 测试 | ⏭️ 跳过 | 高（无浏览器自动化） |

---

## 五、变更级覆盖

如需为特定变更使用不同的工具链，在 `docs/changes/{change}/toolchain.md` 创建覆盖配置。变更级配置优先级高于项目级。
