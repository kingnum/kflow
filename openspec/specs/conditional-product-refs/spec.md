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

### Requirement: 评分维度按项目类型调整

系统 SHALL 在 E2E 测试报告中按项目类型调整健康评分维度。

#### Scenario: 前后端项目评分维度
- **WHEN** 项目类型为前后端项目
- **THEN** 健康评分包含功能完整性、控制台错误、视觉一致性（原型存在时）、性能响应、可访问性

#### Scenario: 纯后端项目评分维度
- **WHEN** 项目类型为纯后端项目（仅接口单元测试评分）
- **THEN** 评分维度为功能完整性、响应时间、错误处理、数据一致性
- **AND** 不包含控制台错误、视觉一致性、可访问性等前端维度

#### Scenario: 视觉一致性条件化
- **WHEN** 前后端项目但原型设计阶段标记为 ⏭️ 跳过
- **THEN** 视觉一致性评分项标记为 N/A
- **AND** 不依赖原型文件进行对比
