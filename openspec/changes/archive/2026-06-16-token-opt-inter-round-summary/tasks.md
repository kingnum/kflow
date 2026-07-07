## 1. 轮间摘要规范

- [x] 1.1 定义轮间摘要格式——写入 `kflow-shared/repetition-model.md` 新增章节（已发现问题/未解决问题/覆盖率变化/本轮建议关注）
- [x] 1.2 定义摘要提取规则——主 Agent 在每轮子代理返回后从自审报告/产物差异中提取

## 2. 子代理 prompt 更新

- [x] 2.1 更新 7 个执行类阶段 SKILL.md 的子代理 prompt 构建——添加轮间摘要注入位置和摘要使用说明
- [x] 2.2 定义跳过条件：已修复项快速回归、未解决项重点分析、未涉及项全量检查（兜底）

## 3. 核心机制文档同步

- [x] 3.1 更新 `07-agent-model.md`（或 `kflow-shared/repetition-model.md`）——添加轮间摘要传递规则

## 4. 验证

- [x] 4.1 确认 repetition-model.md 包含轮间摘要规范
- [x] 4.2 确认执行类阶段 SKILL.md 子代理 prompt 章节包含摘要注入说明
