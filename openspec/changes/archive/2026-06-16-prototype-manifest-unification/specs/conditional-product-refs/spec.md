## MODIFIED Requirements

### Requirement: 条件产物引用规范化

系统 SHALL 在所有 Skill 文档中使用标准化图例标注输入/输出产物的必须性，并将前端SC 的原型产物入口统一为 `prototype/index.md`。

#### Scenario: 产物表格使用标准图例
- **WHEN** Skill 文档定义输入要求或输出产物
- **THEN** 使用标准化图例：✅ 必须、🔶 条件、⏭️ 不适用
- **AND** 每个产物按项目类型（前后端/纯后端）分别标注
- **AND** 前端SC 的原型产物 SHALL 以 `prototype/index.md`（✅ 必须，前端SC）为统一入口
- **AND** SHALL NOT 在输入表中单独列出 `prototype/index.html`、`prototype/design-tokens.css`、`prototype/element-coverage-tree.md`

#### Scenario: 门控检查中显式处理跳过
- **WHEN** 门控检查涉及可选阶段的产物（如 prototype）
- **THEN** 检查逻辑区分三种情况：跳过（通过）、完成有文件（通过）、待开始（阻塞）
- **AND** 不因产物不存在而误报阻塞
