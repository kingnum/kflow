## Purpose

定义变更目录中文件的命名规范，包括功能设计目录化命名、测试用例目录化命名、详细设计文件命名、旧命名兼容规则、门控检查使用新命名格式，以及 self-reviews/ 和 cross-reviews/ 目录命名和时间戳格式。
## Requirements
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

### Requirement: 详细设计文件命名

系统 SHALL 将详细设计阶段的输出文件命名为 detailed-design.md。

#### Scenario: 详细设计阶段输出
- **WHEN** kflow-design 阶段完成
- **THEN** 输出文件为 detailed-design.md（不再使用 design.md）
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

### Requirement: 产品级功能设计文档目录化

系统 SHALL 将产品级功能设计文档组织为 `docs/designs/functional-designs/` 目录结构，前后端项目按一级菜单划分子目录，纯后端项目按设计域创建简化文件。

#### Scenario: 产品级 functional-designs 目录（前后端项目）
- **WHEN** 产品级功能设计文档首次创建且项目为前后端
- **THEN** 输出目录为 `docs/designs/functional-designs/`
- **AND** 目录内按一级菜单组织：`{一级菜单}/index.md` + `{一级菜单}/part-NN.md`
- **AND** 一级菜单名使用 kebab-case 格式

#### Scenario: 产品级 functional-designs 目录（纯后端项目）
- **WHEN** 产品级功能设计文档首次创建且项目为纯后端
- **THEN** 输出目录为 `docs/designs/functional-designs/`
- **AND** 目录内按设计域组织：`{domain}.md` 平铺文件
- **AND** 使用 backend-domain-template 简化模板

#### Scenario: 功能模块命名（前后端项目）
- **WHEN** 归档时需要确定功能模块归属
- **THEN** 目录名 SHALL 使用对应的一级菜单项 kebab-case 名称
- **AND** 如菜单项为中文，转换为 kebab-case 拼音或英文翻译（如"系统管理"→`system-admin`）

#### Scenario: 功能模块命名（纯后端项目）
- **WHEN** 归档时需要确定功能模块归属
- **THEN** 文件名 SHALL 使用设计域的 kebab-case 名称
- **AND** 避免使用抽象的 domain 名称

### Requirement: 产品级技术设计文档目录化

系统 SHALL 将产品级技术设计文档组织为 `docs/designs/technical-designs/` 目录结构，包含 6 个文件。

#### Scenario: 产品级 technical-designs 目录
- **WHEN** 产品级技术设计文档首次创建
- **THEN** 创建 `docs/designs/technical-designs/` 目录
- **AND** 包含 architecture.md、data-model.md、api-catalog.md、nfr-baseline.md、config-items.md、error-handling.md

### Requirement: 门控检查使用新命名

系统 SHALL 在阶段门控检查中使用新的审查目录路径和新的命名格式。

#### Scenario: design 阶段自审完成检查
- **WHEN** 门控检查 design 阶段自审是否完成
- **THEN** 检查 `self-reviews/design/` 是否存在且包含 10 个时间戳命名的 .md 文件

#### Scenario: 四视角审查完成检查
- **WHEN** 门控检查 design 阶段四视角审查是否完成
- **THEN** 检查 `cross-reviews/` 是否存在且至少有一个批次目录
- **AND** 最新批次的 synthesis.md 标记为 ✅ 关闭

### Requirement: self-reviews 目录命名规范

系统 SHALL 使用 `self-reviews/` 作为自循环审查记录的根目录。

#### Scenario: self-reviews 目录创建
- **WHEN** 变更目录首次执行设计阶段自审
- **THEN** 创建 `self-reviews/` 根目录
- **AND** 按阶段创建子目录 explore/、prototype/、design/

#### Scenario: self-reviews 子目录结构
- **WHEN** explore 阶段执行自审
- **THEN** 自审报告保存到 `self-reviews/explore/`
- **AND** prototype 阶段保存到 `self-reviews/prototype/`
- **AND** design 阶段保存到 `self-reviews/design/`

### Requirement: cross-reviews 目录命名规范

系统 SHALL 使用 `cross-reviews/` 作为四视角交叉审查记录的根目录。

#### Scenario: cross-reviews 目录创建
- **WHEN** kflow-design 首次执行四视角审查
- **THEN** 创建 `cross-reviews/` 根目录
- **AND** 每次审查（含重审）创建独立的 `{YYYYMMDD}-{HHMMSS}/` 子目录

#### Scenario: cross-reviews 取代 review-reports
- **WHEN** kflow-design 执行四视角审查
- **THEN** 审查报告保存到 `cross-reviews/{timestamp}/`
- **AND** 不再使用 `review-reports/` 目录
- **AND** 旧变更目录中的 `review-reports/` 保持兼容读取

### Requirement: 时间戳命名格式统一

系统 SHALL 对所有审查记录文件/目录使用统一的 `{YYYYMMDD}-{HHMMSS}` 时间戳命名。

#### Scenario: 单文件时间戳命名
- **WHEN** 自审报告为单文件
- **THEN** 文件名为 `{YYYYMMDD}-{HHMMSS}.md`
- **AND** 时间戳为审查开始的本地时间

#### Scenario: 多文件时间戳命名
- **WHEN** 四视角审查涉及多个文件
- **THEN** 目录名为 `{YYYYMMDD}-{HHMMSS}/`
- **AND** 时间戳为审查开始的本地时间
- **AND** 目录内文件保持原有命名（business-review.md 等）

#### Scenario: 自然排序即时间序
- **WHEN** 读取 self-reviews/{phase}/ 或 cross-reviews/
- **THEN** 条目按名称自然排序即为执行时间序
- **AND** 无需额外的排序逻辑或元数据

