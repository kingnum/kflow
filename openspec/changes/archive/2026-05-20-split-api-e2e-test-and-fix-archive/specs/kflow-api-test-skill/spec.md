# kflow-api-test Skill 规格

> **capability**: kflow-api-test-skill
> **变更**: split-api-e2e-test-and-fix-archive

---

## 概述

`kflow-api-test` 是一个新的执行类 Skill，负责对所有子变更执行接口单元测试。它从当前的 `kflow-e2e-test` 中拆分出来，独立承担 API 测试职责。

## 需求

### REQ-1：项目类型适配

- **REQ-1.1**：前后端项目必须执行接口单元测试
- **REQ-1.2**：纯后端项目必须执行接口单元测试
- **REQ-1.3**：接口单元测试在代码审查通过后、E2E 测试前执行

### REQ-2：门控检查

- **REQ-2.1**：进入前检查编码状态 = ✅ 完成
- **REQ-2.2**：进入前检查代码审查状态 = ✅ 完成
- **REQ-2.3**：进入前检查 test-reports/review/code-review.md 存在
- **REQ-2.4**：进入前检查 api-tests/ 测试用例文档存在

### REQ-3：测试执行

- **REQ-3.1**：使用 curl 或 HTTP 客户端对 api-tests/ 中定义的接口逐条测试
- **REQ-3.2**：每轮测试后产出 round-{n}.md 报告
- **REQ-3.3**：全部 10 轮完成后产出 summary.md

### REQ-4：执行模式

- **REQ-4.1**：采用 Agent 迭代执行模式
- **REQ-4.2**：强制 10 轮迭代下限
- **REQ-4.3**：复杂度评估提供节奏指引
- **REQ-4.4**：覆盖率目标：traceability.md「接口测试(ID)」列 = 100%

### REQ-5：健康评分

- **REQ-5.1**：功能完整性评分（通过数/总数 × 100）
- **REQ-5.2**：响应时间评分（< 200ms 满分）
- **REQ-5.3**：HTTP 状态码评分
- **REQ-5.4**：错误处理评分
- **REQ-5.5**：契约一致性评分
