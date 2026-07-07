# 提案：拆分 kflow-e2e-test + 修复 kflow-archive 归档条件遗漏

> **变更名称**: split-api-e2e-test-and-fix-archive
> **创建时间**: 2026-05-20
> **类型**: 功能增强 + Bug 修复

---

## 问题陈述

### 问题 1：kflow-e2e-test 命名与职责不匹配

当前 `kflow-e2e-test` 承担了两项独立职责：
- **接口单元测试**（API 测试，curl/HTTP 方式，所有项目类型）
- **E2E 浏览器自动化测试**（Playwright 驱动，仅前后端项目）

这导致以下问题：
- **命名误导**：Skill 名称 "e2e-test" 暗示仅浏览器自动化测试，实际还包含接口测试
- **纯后端项目缺口**：`kflow-e2e-test` 声明纯后端项目 ⏭️ 跳过此阶段，但 `kflow-design` 已为纯后端项目生成了 `api-tests/` 测试用例，导致纯后端项目的接口单元测试无 Skill 执行
- **调度映射合并**：`core-mechanisms.md` §12.3 将「接口单元测试」和「E2E测试」两个阶段映射到同一 Skill，无法独立调度

### 问题 2：kflow-archive 归档条件遗漏代码审查阶段

`kflow-archive.md` 中两处归档条件清单（第 37 行门控检查、第 172 行归档条件）均遗漏了「代码审查」阶段，与 `core-mechanisms.md` §6.3（第 1049 行，已正确包含代码审查）不一致。

---

## 变更方案

### 方案 A：拆分为 kflow-api-test + kflow-e2e-test

| 维度 | kflow-api-test（新） | kflow-e2e-test（修改） |
|------|----------------------|------------------------|
| 阶段 | 接口单元测试 | E2E 浏览器自动化测试 |
| 归属层级 | 子变更级 | 子变更级 |
| 适用项目 | 所有项目 | 仅前后端项目 |
| 测试方式 | curl / HTTP 请求 | playwright-cli snapshot+ref |
| 前置阶段 | 代码审查 | 接口单元测试 |
| 输出产物 | api/round-{n}.md, api/summary.md | e2e/round-{n}.md, e2e/summary.md, generated-test.spec.ts |
| 执行模式 | Agent 迭代执行，强制 10 轮 | Agent 迭代执行，强制 10 轮 |

**关键收益**：纯后端项目的接口单元测试获得明确执行入口，消除当前设计漏洞。

### 方案 B：修复 kflow-archive 归档条件

在 `kflow-archive.md` 两处归档条件清单中补充「代码审查」阶段。

---

## 影响范围

### 需修改文件（14 个设计文档）

| 层级 | 文件 | 变更类型 |
|------|------|---------|
| 新建 | `docs/designs/skills/kflow-api-test.md` | 新增设计规格 |
| 核心机制 | `docs/designs/core-mechanisms.md` | 更新 7 处（阶段表、流程图、调度映射、归档条件等） |
| 索引 | `docs/designs/index.md` | Skills 清单新增 1 行 + 更新 1 行 |
| 索引 | `docs/designs/overview.md` | Skills 表、依赖图、实施顺序 |
| 索引 | `docs/designs/skills/index.md` | Skills 清单、触发时机、依赖图、流转图 |
| Skill 设计 | `docs/designs/skills/kflow-e2e-test.md` | 移除 API 测试职责 |
| Skill 设计 | `docs/designs/skills/kflow-archive.md` | 补充代码审查阶段（2 处） |
| Skill 设计 | `docs/designs/skills/kflow-guide.md` | 流程概览表、关键词映射 |
| Skill 设计 | `docs/designs/skills/kflow-resume.md` | 调度映射表拆分 |
| Skill 设计 | `docs/designs/skills/kflow-code.md` | 后续阶段链引用 |
| Skill 设计 | `docs/designs/skills/kflow-code-review.md` | 输出给引用 |
| Skill 设计 | `docs/designs/skills/kflow-bug-fix.md` | 输入来自引用 |
| Skill 设计 | `docs/designs/skills/kflow-integration-test.md` | 输入来自引用 |
| Skill 设计 | `docs/designs/skills/kflow-audit.md` | 回退路由引用 |
| Skill 设计 | `docs/designs/skills/kflow-init.md` | 工具推荐矩阵 |
| 模板 | `docs/designs/templates/index.md` | 模板产出 Skill 归属 |

### 需同步更新（实际 Skill 实现文件）

| 文件 | 变更类型 |
|------|---------|
| `.claude/skills/kflow-e2e-test/SKILL.md` | 移除 API 测试职责 |
| `.claude/skills/kflow-api-test/SKILL.md` | 新建 |

---

## 非目标

- 不新增 Skill 功能特性（仅拆分职责）
- 不改变现有测试流程逻辑
- 不修改模板文件内容（仅更正索引中的归属标注）
