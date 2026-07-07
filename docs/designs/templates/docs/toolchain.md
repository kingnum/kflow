---
stage: 环境初始化
skill: kflow-init
version: 1.0.0
created_at: 2026-05-05
template_for: docs/toolchain.md
---

# 工具链配置：{project-name}

> **创建时间**: {YYYY-MM-DD HH:MM}
> **项目类型**: {前后端项目|纯后端项目}
> **覆盖度**: {percentage}%

---

## 一、环境能力扫描

### Skills

| Skill | 状态 | 适用场景 |
|-------|------|---------|
| huashu-design | {✅ 已安装 / ❌ 未安装} | HTML 原型设计 |
| kflow-guide | {✅ 已安装 / ❌ 未安装} | 流程指引 |
| kflow-explore | {✅ 已安装 / ❌ 未安装} | 设计探索 |
| /playwright-cli | {✅ 已安装 / ❌ 未安装} | E2E 浏览器测试 |

### 权限配置状态

| 字段 | 值 |
|------|-----|
| 配置状态 | ✅ 齐全 / ⚠️ 部分缺失 / ❌ 未配置 |
| 已配置权限数量 | {N}/16 |
| 缺失权限列表 | {缺失的权限列表，无则标"—"} |
| 配置时间 | {YYYY-MM-DD HH:MM} |

---

## 二、阶段工具推荐

| 阶段 | 首选工具 | 备选工具 | 状态 |
|------|---------|---------|------|
| 设计探索 | Read, Glob, Grep | — | ✅ 可用 |
| 原型设计 | huashu-design Skill | — | {✅ 可用 / ⚠️ 需安装 / ⏭️ 不适用} |
| 详细设计 | Read, Write, Edit, Agent | — | ✅ 可用 |
| 计划 | Write, Edit | — | ✅ 可用 |
| 编码 | Bash, Read, Write, Edit, Agent | — | ✅ 可用 |
| 接口单元测试 | Bash, Read, Edit | — | ✅ 可用 |
| E2E 测试 | /playwright-cli skill | playwright MCP | {✅ 可用 / ⚠️ 需安装 / ⏭️ 不适用} |
| 集成测试 | Bash, Read, Agent | — | ✅ 可用 |
| 缺陷修复 | Bash, Read, Edit, Agent | — | ✅ 可用 |
| 归档 | Bash, Read, Write, Edit | — | ✅ 可用 |
| 审计 | Read, Agent | — | ✅ 可用 |

---

## 三、安装建议

| 工具 | 用途 | 安装方式 | 优先级 |
|------|------|---------|--------|
| {工具名} | {用途} | {安装方式} | {高/中/低} |

---

## 四、多方案对比

### 方案 A：推荐最佳组合 (覆盖度 100%)

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
