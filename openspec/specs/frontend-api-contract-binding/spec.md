# frontend-api-contract-binding Specification

## Purpose
定义前端子变更如何通过 detailed-design.md「子变更划分」章节中的「依赖API契约」声明获取接口信息，以及该信息如何传递到 plan 和 code 阶段。

## ADDED Requirements

### Requirement: 前端子变更依赖 API 契约声明
系统 SHALL 在 detailed-design.md「子变更划分」章节中，为每个前端子变更显式声明「依赖API契约」列表。

#### Scenario: 依赖 API 契约声明格式
- **WHEN** kflow-design 划分子变更且存在前端子变更
- **THEN** 前端子变更的划分条目 SHALL 包含「依赖API契约」列表
- **AND** 列表每项 SHALL 包含：HTTP 方法 + 路径 + 指向 detailed-design.md 中接口设计章节的引用
- **AND** 格式为：`METHOD /path → detailed-design.md §章节号`

#### Scenario: 无 API 契约依赖时跳过
- **WHEN** 前端子变更仅涉及纯前端展示页面（无后端 API 调用）
- **THEN** 「依赖API契约」SHALL 标注为「无」
- **AND** 编码时跳过 API 对接步骤

### Requirement: Plan 阶段传递 API 契约到 tasks.md
系统 SHALL 在 plan 阶段为前端子变更生成 tasks.md 时，将 API 契约信息写入「输入源」区。

#### Scenario: 前端 tasks.md 输入源含 API 契约
- **WHEN** kflow-plan 为前端子变更生成 tasks.md
- **THEN** 每个前端 FP 的「输入源」区 SHALL 包含 API 契约列表
- **AND** API 契约列表 SHALL 引用 detailed-design.md 中的接口设计章节
- **AND** 格式为：`API 契约: detailed-design.md §{章节号}（{METHOD} {路径}）`

#### Scenario: 多个 API 契约按功能点分组
- **WHEN** 一个前端 FP 依赖多个 API 契约
- **THEN** 该 FP 的输入源 SHALL 列出所有依赖的 API 契约
- **AND** 按页面或功能区域分组排列

### Requirement: Code 阶段按 API 契约实现
系统 SHALL 在 code 阶段为前端子变更按 API 契约实现 API 对接。

#### Scenario: 基于 API 契约使用 mock 数据
- **WHEN** 前端子变更 code 阶段执行 API 对接
- **AND** 后端子变更编码尚未完成
- **THEN** 系统 SHALL 基于 detailed-design.md §接口设计中的入参/出参定义生成 mock 数据
- **AND** mock 数据 SHALL 覆盖接口定义的 Happy Path 和 Error Path

#### Scenario: 后端完成后替换 mock
- **WHEN** 后端子变更编码完成且服务可用
- **THEN** 系统 SHALL 将前端 mock 替换为真实 API 调用
- **AND** 验证 API 调用返回值与契约定义一致

### Requirement: API 契约的接口设计章节引用
系统 SHALL 确保前端子变更的 API 契约引用指向 detailed-design.md 中的精确章节。

#### Scenario: 接口设计章节作为引用目标
- **WHEN** 前端子变更声明依赖 API 契约
- **THEN** 引用目标 SHALL 为 detailed-design.md「二、设计域章节」中的「接口设计」子章节
- **AND** SHALL NOT 引用 functional-designs/ 中的功能点（功能点不定义接口细节）

#### Scenario: 引用格式规范
- **WHEN** detailed-design.md 为单文件形态
- **THEN** 引用格式为：`detailed-design.md §2.1 接口设计（POST /auth/login）`
- **AND** 当 detailed-design.md 为目录形态时，引用格式为：`detailed-design/domains/{domain}.md §接口设计`
