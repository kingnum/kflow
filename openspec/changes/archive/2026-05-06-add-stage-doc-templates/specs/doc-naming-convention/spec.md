## ADDED Requirements

### Requirement: 功能设计文件目录化

系统 SHALL 将设计探索阶段的输出从单文件改为目录结构。

#### Scenario: 设计探索阶段输出
- **WHEN** kflow-explore 阶段完成
- **THEN** 输出目录为 functional-designs/（不再使用 functional-design.md 单文件）
- **AND** 目录内包含 index.md + 至少一个 part-01.md

#### Scenario: 功能设计目录结构
- **WHEN** functional-designs/ 目录被创建
- **THEN** index.md 为功能设计索引入口
- **AND** 按功能点数决定分册数（≤30 一个分册，>30 多个分册）
- **AND** 分册文件命名为 part-01.md, part-02.md ...

### Requirement: 测试用例文件目录化

系统 SHALL 将测试用例文档从单文件改为目录结构。

#### Scenario: 测试用例目录结构
- **WHEN** api-tests、e2e-tests、integration-tests 文档需要产出
- **THEN** 分别创建 api-tests/、e2e-tests/、integration-tests/ 目录
- **AND** 每个目录包含 index.md + 分册文件

## MODIFIED Requirements

### Requirement: 功能设计文件命名

系统 SHALL 将设计探索阶段的输出目录命名为 functional-designs/。

#### Scenario: 设计探索阶段输出
- **WHEN** kflow-explore 阶段完成
- **THEN** 输出目录为 functional-designs/（不再使用 functional-design.md 单文件）
- **AND** 目录内包含 index.md 索引入口和 part-NN.md 分册文件

### Requirement: 详细设计文件命名

系统 SHALL 将详细设计阶段的输出文件命名为 detailed-design.md。

#### Scenario: 详细设计阶段输出
- **WHEN** kflow-design 阶段完成
- **THEN** 输出文件为 detailed-design.md（不变）
- **AND** 文件内容不变（架构、数据模型、接口、NFR、子变更划分）

### Requirement: 旧命名兼容期

系统 SHALL 在过渡期兼容读取旧命名格式的文件。

#### Scenario: 发现旧命名文件（功能设计）
- **WHEN** Skill 读取变更目录时发现 functional-design.md 而非 functional-designs/ 目录
- **THEN** 系统正常读取旧的 functional-design.md 单文件
- **AND** 提示用户文件命名已更新为目录结构，建议迁移

#### Scenario: 发现旧命名文件（测试用例）
- **WHEN** Skill 读取变更目录时发现 api-tests.md / e2e-tests.md / integration-tests.md 单文件
- **THEN** 系统正常读取旧单文件
- **AND** 提示用户文件命名已更新为目录结构，建议迁移

#### Scenario: 新旧文件同时存在
- **WHEN** 变更目录同时存在单文件和新目录结构
- **THEN** 系统优先读取新目录结构
- **AND** 提示用户清理旧的单文件

### Requirement: 门控检查使用新命名

系统 SHALL 在阶段门控检查中使用新命名格式。

#### Scenario: 功能设计门控检查
- **WHEN** 进入功能设计之后的阶段
- **THEN** 门控检查 functional-designs/index.md 是否存在（而非 functional-design.md）

#### Scenario: 测试用例门控检查
- **WHEN** 进入测试相关阶段
- **THEN** 门控检查 api-tests/index.md、e2e-tests/index.md、integration-tests/index.md 是否存在
