## ADDED Requirements

### Requirement: 归档阶段禁止自动流转

系统 SHALL 确保归档阶段不因前置阶段完成而自动触发，MUST 用户显式确认后方可进入。

#### Scenario: 审计通过后不自动调度归档

- **WHEN** kflow-audit 阶段完成且审计通过
- **THEN** 系统 SHALL NOT 自动调用 kflow-archive
- **AND** 系统 SHALL 通过 AskUserQuestion 获取用户显式确认
- **AND** Archive 是 KFlow 体系中唯一禁止自动流转的阶段

#### Scenario: 归档确认后正常流转

- **WHEN** 用户显式确认进入归档
- **THEN** 系统 SHALL 正常进入 kflow-archive 阶段
- **AND** 按现有归档流程执行

### Requirement: 前端子变更依赖 API 契约规则

系统 SHALL 定义前端子变更的特殊依赖规则：依赖 API 契约（design 阶段已定义）而非后端子变更编码完成。

#### Scenario: 前端子变更的启动依赖判定

- **WHEN** 系统检查前端子变更的启动依赖
- **THEN** 依赖条件 SHALL 判定为：detailed-design.md 中对应 API 契约章节存在且状态为 ✅ 完成
- **AND** SHALL NOT 要求后端子变更编码状态为 ✅ 完成
- **AND** 前端子变更可与后端子变更并行启动

#### Scenario: 前端子变更使用 mock 数据开发

- **WHEN** 前端子变更进入编码阶段
- **AND** 后端子变更编码尚未完成
- **THEN** 前端子变更 SHALL 基于 API 契约使用 mock 数据进行开发
- **AND** 后端编码完成后执行集成对接（替换 mock 为真实 API）
