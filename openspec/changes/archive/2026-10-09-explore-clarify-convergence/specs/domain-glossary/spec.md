# Spec Delta

## MODIFIED Requirements

### Requirement: CONTEXT.md 格式

`CONTEXT.md` SHALL 遵循 KFlow 自有的 `skills/kflow-explore/references/context-template.md`（开发布局）或 `.claude/skills/kflow-explore/references/context-template.md`（消费布局）所定义的格式。该格式权威 SHALL 在安装布局中可解析，且 SHALL 随 KFlow Skill 一同安装并自包含——系统 SHALL NOT 将 `CONTEXT.md` 的格式权威委托给任何外部技能的格式文件。

#### Scenario: CONTEXT.md 文件结构

- **WHEN** `CONTEXT.md` 被创建或读取
- **THEN** 文件 SHALL 包含以下结构：项目名标题、领域术语列表（每个含定义/别名/边界）、修订记录
- **AND** 禁止耦合实现细节，仅包含领域专家能理解的术语
