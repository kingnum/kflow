# Spec Delta

## MODIFIED Requirements

### Requirement: 模板覆盖范围

系统 SHALL 为所有独立文件产物提供模板，新增自审轮次报告模板。

#### Scenario: 需要模板的产物
- **WHEN** 阶段产出是一个独立的 Markdown 文件
- **THEN** 该产物必须有对应模板
- **AND** 以下产物除外：HTML 原型产物（`docs/designs/prototypes/` 下的 `screens/*.html`、`components/*`、`assets/*`、`design-tokens.css`、`design-system/MASTER.md`，无固定模板结构）、迁移 SQL 脚本（内容为 DDL/DML）、代码文件（无固定模板结构）
- **AND** 新增 config-items.md、error-handling.md、backend-domain.md 必须有对应模板

#### Scenario: 自审报告需要模板
- **WHEN** 阶段产出包含 self-reviews/{phase}/{timestamp}.md
- **THEN** 该产物必须有对应的自审报告模板
- **AND** 模板按阶段提供维度差异版本
