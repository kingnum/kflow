## ADDED Requirements

### Requirement: 功能设计文件命名

系统 SHALL 将设计探索阶段的输出文件命名为 functional-design.md。

#### Scenario: 设计探索阶段输出
- **WHEN** kflow-explore 阶段完成
- **THEN** 输出文件为 functional-design.md（不再使用 design-explore.md）
- **AND** 文件内容不变（功能点清单、需求澄清、项目类型）

### Requirement: 详细设计文件命名

系统 SHALL 将详细设计阶段的输出文件命名为 detailed-design.md。

#### Scenario: 详细设计阶段输出
- **WHEN** kflow-design 阶段完成
- **THEN** 输出文件为 detailed-design.md（不再使用 design.md）
- **AND** 文件内容不变（架构、数据模型、接口、NFR、子变更划分）

### Requirement: 旧命名兼容期

系统 SHALL 在过渡期兼容读取旧命名格式的文件。

#### Scenario: 发现旧命名文件
- **WHEN** Skill 读取变更目录时发现 design-explore.md 而非 functional-design.md
- **THEN** 系统正常读取旧文件
- **AND** 提示用户文件命名已更新，建议迁移

#### Scenario: 新旧文件同时存在
- **WHEN** 变更目录同时存在 design-explore.md 和 functional-design.md
- **THEN** 系统优先读取新命名文件（functional-design.md）
- **AND** 提示用户清理旧的 design-explore.md

### Requirement: 门控检查使用新文件名

系统 SHALL 在阶段门控检查中使用新文件命名。

#### Scenario: 详细设计门控检查
- **WHEN** 进入 kflow-design 阶段
- **THEN** 门控检查 functional-design.md 是否存在（而非 design-explore.md）

#### Scenario: 计划阶段门控检查
- **WHEN** 进入 kflow-plan 阶段
- **THEN** 门控检查 detailed-design.md 是否存在（而非 design.md）
