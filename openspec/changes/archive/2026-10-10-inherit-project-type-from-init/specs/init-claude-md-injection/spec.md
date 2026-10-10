# Spec Delta

## MODIFIED Requirements

### Requirement: 项目画像 section 注入

kflow-init SHALL 向 CLAUDE.md 注入「项目画像」section，包含项目特定上下文信息。注入使用 `## 项目画像` 作为唯一 marker，支持幂等更新。首次注入或信息变更时替换整个 section。CLAUDE.md 不存在时跳过注入。

该 section 的「项目类型」字段 SHALL 作为项目类型项目级记录的唯一真源，供变更创建链路（kflow-guide、kflow-explore）读取；其读取优先级高于 `docs/toolchain.md` 头部的同名字段。项目类型的检测、确认、继承与消费规则由 `project-type-detection` 能力定义，本能力 SHALL NOT 重复定义。

#### Scenario: 首次注入项目画像

- **WHEN** CLAUDE.md 存在且不包含 `## 项目画像` marker
- **THEN** 系统在 CLAUDE.md 末尾追加项目画像 section
- **AND** section 包含：项目类型、语言、框架、数据库、构建工具、关键目录、入口文件、产品文档状态
- **AND** 标注生成来源和时间戳（`> 来源: kflow-init | 扫描时间: {YYYY-MM-DD HH:MM}`）

#### Scenario: 重复执行 init 时幂等更新项目画像

- **WHEN** CLAUDE.md 已包含 `## 项目画像` marker
- **THEN** 系统重新扫描项目并替换 `## 项目画像` 到下一个 `## ` 之间的内容
- **AND** 更新扫描时间戳
- **AND** 不修改 CLAUDE.md 中其他 section 的内容

#### Scenario: re-init 记录一致时静默沿用项目类型

- **WHEN** CLAUDE.md 已包含「## 项目画像」marker 且项目类型行已有值
- **AND** 重新扫描结果与该值一致
- **THEN** 系统静默沿用该值
- **AND** SHALL NOT 使用 AskUserQuestion 询问项目类型

#### Scenario: re-init 记录冲突时请求裁决项目类型

- **WHEN** CLAUDE.md 已包含「## 项目画像」marker 且项目类型行已有值
- **AND** 重新扫描结果与该值冲突
- **THEN** 系统使用 AskUserQuestion 请求用户裁决
- **AND** 按裁决结果更新项目类型行

#### Scenario: 项目画像字段 — 新项目

- **WHEN** 项目无前端依赖且无源码目录
- **THEN** 技术栈字段标注为"待确定"
- **AND** 关键目录和入口文件标注为"待确定"
- **AND** 产品文档状态全部标注为 ❌ 不存在

#### Scenario: 项目画像字段 — 老项目

- **WHEN** 项目有完整的源码和配置文件
- **THEN** 系统从 package.json 提取语言、框架、构建工具
- **AND** 从目录结构推断关键目录和入口文件
- **AND** 从数据库配置提取数据库类型
- **AND** 检测产品文档存在性并标注状态
