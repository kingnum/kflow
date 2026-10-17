# Spec Delta

## ADDED Requirements

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
