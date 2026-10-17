## Purpose

Define the requirements and behaviors for the Large Doc Splitting capability in the KFlow Skills system.
## Requirements
### Requirement: 按数量拆分触发条件

系统 SHALL 对 4 组文档引入按数量拆分机制，每个分册不超过 30 个条目。

#### Scenario: 条目数不超过 30
- **WHEN** functional-designs、api-tests、e2e-tests、integration-tests 中任一组文档的条目数 ≤ 30
- **THEN** 该组仅包含 index.md + 一个 part-01.md
- **AND** part-01.md 包含全部条目

#### Scenario: 条目数超过 30
- **WHEN** 上述任一组文档的条目数 > 30
- **THEN** 系统拆分为 index.md + 多个 part-NN.md 分册
- **AND** 每个分册条目数 ≤ 30
- **AND** 最后一个分册条目数可能少于 30

### Requirement: 拆分适用文档范围

拆分机制 SHALL 适用于以下 5 组文档。

#### Scenario: 适用拆分的文档组
- **WHEN** 以下文档的条目数超过阈值
- **THEN** functional-designs 按功能点数拆分（> 30 触发）
- **AND** api-tests 按接口数拆分（> 30 触发）
- **AND** e2e-tests 按场景数拆分（> 30 触发）
- **AND** integration-tests 按场景数拆分（> 30 触发）
- **AND** detailed-design 按功能点数拆分（> 20 触发，拆分为 6 文件目录结构而非 part-NN.md 分册）

#### Scenario: detailed-design 拆分规则（新增）
- **WHEN** 变更功能点总数 > 20
- **THEN** detailed-design.md SHALL 拆分为 `detailed-design/` 目录
- **AND** 目录包含 index.md + architecture.md + domains/*.md + nfr.md + config-and-errors.md + subchange-division.md
- **AND** 拆分规则详见 design-doc-directory spec
- **AND** FP ≤ 20 时保持单文件 detailed-design.md

### Requirement: 分册文件命名规范

分册文件 SHALL 统一使用 `part-NN.md` 格式命名。

#### Scenario: 分册命名
- **WHEN** 创建分册文件
- **THEN** 文件名格式为 `part-01.md`、`part-02.md` ... 使用两位数字序号
- **AND** 每组文档的索引入口统一命名为 `index.md`

### Requirement: 分册模板格式

每个分册 SHALL 使用独立模板，包含本册条目的完整覆盖信息。

#### Scenario: 分册 frontmatter 字段
- **WHEN** 分册文件被创建
- **THEN** frontmatter 包含 part（分册号）、range（条目范围）、count（条目数）、covered_fp（覆盖的功能点范围）

#### Scenario: 分册正文结构
- **WHEN** 分册正文被渲染
- **THEN** 开头包含"本册覆盖范围"摘要
- **AND** 随后为条目的详细定义（与不分拆时的格式一致）
- **AND** 末尾包含本册修订记录

### Requirement: 索引文件规范

索引文件 SHALL 统一命名为 index.md，SHALL 具备逐条可读性。

#### Scenario: 索引文件结构
- **WHEN** 索引文件被创建
- **THEN** 包含分册总览表（分册号、文件链接、条目范围、条目数、内容简述）
- **AND** 包含逐条清单（每个条目的 ID、名称、简述、关键属性）

#### Scenario: e2e-tests 索引逐条清单
- **WHEN** e2e-tests/index.md 被创建
- **THEN** 逐条清单包含：功能点ID、功能点简述、覆盖场景（场景ID列表）、验证类型、所在分册

#### Scenario: api-tests 索引逐条清单
- **WHEN** api-tests/index.md 被创建
- **THEN** 逐条清单包含：接口ID、方法、路径、简述、用例数、所在分册

#### Scenario: functional-designs 索引逐条清单
- **WHEN** functional-designs/index.md 被创建
- **THEN** 逐条清单包含：功能点ID、名称、简述、优先级、依赖功能点、所在分册

#### Scenario: integration-tests 索引逐条清单
- **WHEN** integration-tests/index.md 被创建
- **THEN** 逐条清单包含：功能点ID、功能点简述、所属子变更、子变更级测试状态、集成场景（场景ID列表）、集成验证要点、所在分册

### Requirement: 门控检查适配拆分

阶段门控检查 SHALL 适配目录化结构，检查 index.md 存在即可。

#### Scenario: 功能设计门控检查
- **WHEN** 门控检查 functional-design.md 是否存在
- **THEN** 改为检查 functional-designs/index.md 是否存在
- **AND** index.md 存在即视为功能设计阶段产物已输出

#### Scenario: 测试用例门控检查
- **WHEN** 门控检查 api-tests.md / e2e-tests.md / integration-tests.md
- **THEN** 改为检查对应目录的 index.md 是否存在


### Requirement: 已拆分文档的按需分片读取

对已按数量拆分的文档组（functional-designs / api-tests / e2e-tests / integration-tests 的 `part-NN.md` 分册，以及 detailed-design 的目录化结构），读取侧 SHALL 经索引定位后读取目标分册或行区间，SHALL NOT 将全部分册整体读取。

#### Scenario: 按索引定位后读取单个分册

- **WHEN** 某阶段需要 functional-designs 中特定功能点的定义
- **THEN** 读取 SHALL 先取 `functional-designs/index.md` 定位该功能点所在分册
- **AND** 随后仅读取该分册（或该分册中的目标行区间）
- **AND** SHALL NOT 读取其余分册

#### Scenario: 目录化详细设计的按域读取

- **WHEN** 某阶段需要 detailed-design 中某一设计域的章节
- **THEN** 读取 SHALL 先取 `detailed-design/index.md` 定位该域所在文件
- **AND** 随后仅读取该域文件的所需章节
- **AND** SHALL NOT 读取 `architecture.md` / `nfr.md` / `config-and-errors.md` / `subchange-division.md` 中与本次任务无关的文件

#### Scenario: 未拆分文档的片段读取

- **WHEN** 某文档未触发拆分阈值但仍超过单次读取的合理体量
- **THEN** 读取侧 SHALL 按章节行区间读取所需片段
- **AND** SHALL NOT 以整体读取的方式载入全文

#### Scenario: 索引文件作为唯一整体读取对象

- **WHEN** 某阶段需要了解拆分文档组的全貌
- **THEN** 整体读取的对象 SHALL 限于该文档组的 `index.md`
- **AND** `index.md` 的体量 SHALL 保持在可整体读取的范围内

### Requirement: 片段注入优先于读取指令

主 Agent 构造子代理 prompt 时，对子代理所需的大文档输入 SHALL 直接选取并注入所需片段，SHALL NOT 仅以「请读取某文件」的形式转嫁读取动作。

#### Scenario: 主 Agent 选取片段内联

- **WHEN** 子代理的任务涉及详细设计的特定章节
- **THEN** 主 Agent SHALL 选取该章节内容并内联进子代理 prompt
- **AND** SHALL NOT 仅给出文件路径并交由子代理自行全文读取

#### Scenario: 片段选取的范围以子代理职责为界

- **WHEN** 主 Agent 为子代理选取片段
- **THEN** 选取范围 SHALL 与该子代理承担的功能点或任务项对应
- **AND** SHALL NOT 注入与该子代理职责无关的章节

#### Scenario: 子代理保留按需自行读取的权利

- **WHEN** 子代理在执行中发现内联片段不足以完成其任务
- **THEN** 子代理 SHALL 有权按章节行区间自行读取所需内容
- **AND** 该自主读取 SHALL 遵循按需分片读取规则

### Requirement: 产品级文档的章节索引与分片

拆分机制的适用范围 SHALL 扩展到产品级文档（`CONTEXT.md`、`docs/designs/**`、`docs/open/**`）。产品级文档 SHALL 按体积触发两档处理：超过索引阈值者 SHALL 提供章节索引，超过分片阈值者 SHALL 拆分为目录化结构。

#### Scenario: 超过索引阈值时提供章节索引

- **WHEN** 某产品级文档的单文件体积超过 30 KB
- **THEN** 该文档 SHALL 提供章节索引（文件头部的章节导航，或同级 `index.md`）
- **AND** 索引 SHALL 列出各章节的标题与其行号区间或所在文件
- **AND** 读取侧 SHALL 能够据此按章节定位

#### Scenario: 超过分片阈值时拆分

- **WHEN** 某产品级文档的单文件体积超过 80 KB
- **THEN** 该文档 SHALL 拆分为目录化结构 `<name>/index.md + <name>/<section>.md`
- **AND** `index.md` SHALL 承载章节导航与分册清单
- **AND** 原单文件路径 SHALL NOT 继续存在

#### Scenario: 拆分后的引用同步

- **WHEN** 一个产品级文档被拆分或改变文件边界
- **THEN** 全部引用该文档的项目文档、Skill 规则与脚本 SHALL 被同步更新
- **AND** 引用更新 SHALL 在拆分动作内完成，SHALL NOT 留待后续

#### Scenario: 术语类文档的例外

- **WHEN** 某产品级文档为术语表（如 `CONTEXT.md`），且其读取模式为「按术语名随机查询」
- **THEN** 该文档 MAY 保持单文件
- **AND** 此时 SHALL 提供按模块或按首字母的术语索引
- **AND** 读取侧 SHALL 按索引定位到目标术语所在区间
