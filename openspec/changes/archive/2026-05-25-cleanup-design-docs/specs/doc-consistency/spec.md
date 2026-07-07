## ADDED Requirements

### Requirement: CLAUDE.md 阶段数与设计文档一致
CLAUDE.md 中标注的前后端项目阶段数和纯后端项目阶段数 SHALL 与 `docs/designs/` 下的设计文档完全一致。当前正确值为：前后端 11 阶段，纯后端 9 阶段。

#### Scenario: 阶段数验证
- **WHEN** 读取 CLAUDE.md 和 `docs/designs/index.md`
- **THEN** 两者的前后端阶段数和纯后端阶段数完全相同

### Requirement: CLAUDE.md 工作流链完整
CLAUDE.md 中的 Skills 工作流链 MUST 包含所有必须阶段 Skill，不得省略中间环节。

#### Scenario: 工作流链完整性
- **WHEN** 读取 CLAUDE.md 的工作流链
- **THEN** 链中包含 kflow-code-review、kflow-api-test、kflow-integration-test、kflow-audit 四个阶段

### Requirement: 设计文档版本号与运行时 SKILL.md 同步
`docs/designs/skills/` 下每个设计文档的版本号 SHALL NOT 低于 `.claude/skills/` 下对应 SKILL.md 的版本号。

#### Scenario: 版本号验证
- **WHEN** 对比 `docs/designs/skills/{name}.md` 和 `.claude/skills/{name}/SKILL.md` 的版本字段
- **THEN** 设计文档版本号 ≥ 运行时 SKILL.md 版本号

### Requirement: core-mechanisms 拆分后锚点有效
`core-mechanisms.md` 拆分为多文件后，所有 Skill 文档中对该文件的锚点引用 MUST 指向正确的拆分后文件路径。

#### Scenario: 拆分后无死链
- **WHEN** 所有 Skill 文档和模板中引用 `core-mechanisms` 的路径
- **THEN** 每个引用路径指向的文件存在且包含对应锚点

### Requirement: references/ 目录已清理
`references/` 目录及其所有子目录 MUST 从项目中删除，`CLAUDE.md` 中对该目录的所有引用 MUST 同步清除。

#### Scenario: references 清理验证
- **WHEN** 检查项目根目录
- **THEN** `references/` 目录不存在
- **AND** `CLAUDE.md` 中不包含 `references/` 路径引用

### Requirement: 临时工作区已清理
`.claude/worktrees/`、`evals-workspace/`、`mattpocock-skills-main/` 等历史临时目录 MUST 从项目中删除。

#### Scenario: 临时工作区清理验证
- **WHEN** 检查项目根目录和 `.claude/` 目录
- **THEN** `.claude/worktrees/` 不存在
- **AND** `evals-workspace/` 不存在
- **AND** `mattpocock-skills-main/` 不存在
