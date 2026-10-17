# Spec Delta

## ADDED Requirements

### Requirement: kflow-doc-optimize 路由入口

kflow-guide SHALL 支持 `kflow-doc-optimize` Skill 的路由识别和调用，且该路由 SHALL NOT 被视为变更流程的一环。

#### Scenario: 文档优化触发词识别

- **WHEN** 用户输入包含「文档优化 / 文档瘦身 / 拆分文档 / 清理修订记录 / 文档体积」等关键词
- **THEN** kflow-guide SHALL 识别为 `kflow-doc-optimize` 调用意图
- **AND** 路由到该 Skill

#### Scenario: 无活跃变更时仍可路由

- **WHEN** 用户表达文档优化意图且项目中没有活跃变更
- **THEN** kflow-guide SHALL 仍然路由到 `kflow-doc-optimize`
- **AND** SHALL NOT 因缺少活跃变更而中止或要求先创建变更

#### Scenario: 优化意图与流程意图的区分

- **WHEN** 用户输入同时含变更名与优化意图
- **THEN** kflow-guide SHALL 优先按变更名模式路由（「恢复/resume + 变更名」或「继续 + 变更名」）
- **AND** SHALL NOT 将优化意图误判为对应变更的阶段推进

### Requirement: kflow-doc-optimize 纳入流程概览

kflow-guide 的流程概览 SHALL 包含 `kflow-doc-optimize` 作为独立维护工具的说明。

#### Scenario: 流程概览显示文档优化

- **WHEN** 用户请求查看流程概览
- **THEN** 系统 SHALL 显示 `kflow-doc-optimize` 作为独立维护工具
- **AND** 标注为「独立维护（非流程阶段），可随时调用优化存量文档的修订记录与体积」
