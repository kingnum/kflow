# 修复归档条件遗漏代码审查阶段

> **capability**: fix-archive-code-review
> **变更**: split-api-e2e-test-and-fix-archive

---

## 概述

修复 `kflow-archive.md` 中两处归档条件遗漏「代码审查」阶段的问题，确保与 `core-mechanisms.md` §6.3 一致。

## 需求

### REQ-1：门控检查章节修复

- **REQ-1.1**：`kflow-archive.md` 第 37 行「所有子变更各阶段完成检查」必须包含代码审查
- **REQ-1.2**：修正后内容为「（计划、编码、代码审查、接口单元测试、E2E测试）」

### REQ-2：归档条件章节修复

- **REQ-2.1**：`kflow-archive.md` 第 172 行归档条件 checklist 必须包含代码审查
- **REQ-2.2**：修正后内容为「所有子变更各阶段（计划、编码、代码审查、接口单元测试、E2E测试）完成」

### REQ-3：一致性验证

- **REQ-3.1**：修复后 `kflow-archive.md` 归档条件与 `core-mechanisms.md` §6.3 完全一致
