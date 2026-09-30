# Spec Delta

## MODIFIED Requirements

### Requirement: 统一版本号文件

项目 SHALL 在仓库根目录维护 `VERSION` 文件，内容为三段式语义化版本号（`major.minor.patch`），作为整个 KFlow Skills 体系的统一版本标识。版本标识的适用范围为 `skills/` 下的全部运行时 kflow-* Skills，数量随体系演进，不写死为固定值。

#### Scenario: VERSION 文件初始创建

- **WHEN** 执行变更实现
- **THEN** 系统在仓库根目录创建 `VERSION` 文件
- **AND** 文件内容为 `0.0.1`

#### Scenario: 读取当前版本号

- **WHEN** 需要获取当前 Skills 体系版本号
- **THEN** 系统读取 `VERSION` 文件内容
- **AND** 解析为 `major.minor.patch` 三段整数

#### Scenario: 版本标识覆盖全部运行时 Skills

- **WHEN** `skills/` 下的运行时 kflow-* Skills 数量发生变化
- **THEN** `VERSION` 文件仍为该体系的唯一版本标识
- **AND** 规格与文档中的版本标识表述 SHALL NOT 依赖固定的 Skills 数量

### Requirement: Single version source for all documents

版本管理 SHALL 采用三层载体，且 `VERSION` 文件为唯一事实来源：

- **仓库级**：仓库根目录 `VERSION` 文件，首行为三段式版本号，记录体系当前版本。
- **Skill 级**：`skills/kflow-*/SKILL.md` front matter 中的 `version:` 字段，承载 `VERSION` 的同步副本，供消费方直接查看。
- **文档级**：设计文档与核心机制文档头部 SHALL NOT 写具体版本号，版本行 SHALL 标注 "版本: 参见仓库根目录 `VERSION` 文件"。

任何载体 SHALL NOT 持有独立于 `VERSION` 文件的版本值，SHALL NOT 出现两个载体版本号不一致的状态。

#### Scenario: Core mechanism doc header

- **WHEN** any core mechanism doc header is read
- **THEN** version line SHALL read "版本: 参见仓库根目录 `VERSION` 文件"

#### Scenario: Skill design doc header

- **WHEN** any skill design doc header is read
- **THEN** version line SHALL read "版本: 参见仓库根目录 `VERSION` 文件"

#### Scenario: SKILL.md carries the synced version value

- **WHEN** `skills/kflow-code/SKILL.md` 的 front matter 被读取
- **THEN** 其中 SHALL 包含 `version:` 字段
- **AND** 该值 SHALL 等于 `VERSION` 文件首行的版本号

#### Scenario: v2.4.0 changelog note only in relevant file

- **WHEN** 01-project-types.md, 02-directory-structure.md, 03-status-and-tasks.md, 04-gates-and-transitions.md, 06-recovery.md, 08-governance.md headers are read
- **THEN** they SHALL NOT contain the v2.4.0 changelog note (only 07-agent-model.md retains it)

## ADDED Requirements

### Requirement: SKILL.md 版本字段同步

系统 SHALL 提供 `scripts/sync-version.sh`，读取仓库根 `VERSION` 文件并把版本值写入每个 `skills/kflow-*/SKILL.md` front matter 的 `version` 字段。所有 SKILL.md 的 `version` 字段值 SHALL 完全相同。

#### Scenario: VERSION 更新后批量同步

- **WHEN** 开发者修改 `VERSION` 并运行 `./scripts/sync-version.sh`
- **THEN** 每个 `skills/kflow-*/SKILL.md` 的 `version:` 字段 SHALL 更新为新值

#### Scenario: 已存在的版本字段被覆盖

- **WHEN** `sync-version.sh` 运行时某个 SKILL.md 已含 `version:` 字段
- **THEN** 该字段的既有值 SHALL 被替换为当前 `VERSION` 值

#### Scenario: 缺失的版本字段被补入

- **WHEN** `sync-version.sh` 运行时某个 SKILL.md 尚无 `version:` 字段
- **THEN** SHALL 在 front matter 的 `name` 字段之后插入 `version:` 行

#### Scenario: 所有 Skills 版本一致

- **WHEN** 任意两个 kflow-* Skill 的 front matter 被比较
- **THEN** 二者的 `version` 值 SHALL 相同
- **AND** 二者 SHALL 均等于 `VERSION` 文件首行值

### Requirement: 打包前版本一致性校验

`scripts/package-skills.sh` SHALL 在生成 zip 之前校验每个待打包 SKILL.md 的 `version` 字段等于仓库根 `VERSION` 文件的值。任一不一致时 SHALL 中止打包并以非零状态退出，同时列出不一致的文件。

#### Scenario: 版本不一致时中止打包

- **WHEN** `package-skills.sh` 运行且某个 SKILL.md 的版本与 `VERSION` 不同
- **THEN** 脚本 SHALL 输出列出该文件的错误信息
- **AND** 脚本 SHALL 以非零状态退出
- **AND** SHALL NOT 生成 zip 产物

#### Scenario: 版本一致时正常打包

- **WHEN** `package-skills.sh` 运行且所有 SKILL.md 版本与 `VERSION` 一致
- **THEN** 打包 SHALL 正常进行

#### Scenario: 校验对象不得为空集

- **WHEN** 打包扫描未匹配到任何 kflow-* Skill
- **THEN** 脚本 SHALL 判定为失败并以非零状态退出
- **AND** SHALL NOT 以「所有 SKILL.md version 与 VERSION 一致」的结论通过校验

### Requirement: 消费方查看已安装版本

消费方 SHALL 能通过读取任一 Skill 的 SKILL.md front matter 的 `version` 字段确定已安装的 KFlow Skills 版本。

#### Scenario: 消费方查看已安装版本

- **WHEN** 消费方运行 `grep '^version:' .claude/skills/kflow-guide/SKILL.md`
- **THEN** SHALL 输出已安装的 KFlow Skills 版本号（形如 `version: 0.18.0`）

### Requirement: 归档后版本流程顺序

`/opsx:archive` 归档完成后，版本相关处理 SHALL 按以下顺序执行：

1. 判定版本自增级别
2. 更新仓库根 `VERSION` 文件
3. 运行 `scripts/sync-version.sh` 同步全部 SKILL.md 的 `version` 字段
4. 更新 `README.md` 的版本行与版本更新说明条目
5. 运行 `scripts/package-skills.sh` 打包
6. 执行 git commit，提交步骤 2~4 产生的版本变更

zip 产物为本地构建产物，受仓库 `.gitignore` 的 `targets/` 规则排除，SHALL NOT 纳入 git commit。

任一步骤失败 SHALL NOT 阻塞归档本身，SHALL 提示失败原因与手工补救方式。

#### Scenario: 归档后按序执行

- **WHEN** `/opsx:archive` 完成变更归档（文件移动与索引更新均已完成）
- **THEN** 系统 SHALL 按上述 1→6 顺序执行版本相关处理
- **AND** 步骤 3 SHALL 在步骤 2 更新 `VERSION` 之后执行
- **AND** 步骤 5 SHALL 在步骤 3 完成 SKILL.md 同步之后执行

#### Scenario: zip 产物不纳入提交

- **WHEN** 步骤 6 执行 git commit
- **THEN** 提交内容 SHALL 包含 `VERSION`、SKILL.md 的 `version` 字段变更与 README 版本条目
- **AND** SHALL NOT 包含 `targets/` 下的 zip 产物

#### Scenario: 步骤失败不阻塞归档

- **WHEN** 顺序中任一步骤执行失败
- **THEN** 归档结果 SHALL 保持有效
- **AND** 系统 SHALL 输出失败原因与手工补救方式

#### Scenario: 规则载体

- **WHEN** 仓库根 `CLAUDE.md` 被读取
- **THEN** 其中 SHALL 包含陈述上述顺序与自增级别判定的「归档后规则」章节
- **AND** 该章节 SHALL NOT 依赖字面版本号，使版本递增无需编辑该章节

### Requirement: 版本管理规则唯一性

版本管理规则 SHALL 仅由本能力定义。其他能力 SHALL NOT 定义版本字段的存在性、版本值的来源或自增级别规则。引用了 `VERSION` 文件的能力 SHALL 以本能力为上位规则。

#### Scenario: 不重复定义版本规则

- **WHEN** 检查 `openspec/specs/` 下各能力对版本字段的表述
- **THEN** 关于 SKILL.md 是否含 `version:` 字段的规则 SHALL 仅出现在本能力中
- **AND** 其他能力 SHALL NOT 出现与该规则相反的表述

#### Scenario: 版本字段的存在性无歧义

- **WHEN** 读者依据规格判断 SKILL.md 是否应含 `version:` 字段
- **THEN** 从规格集合中 SHALL 得到唯一结论：应包含
- **AND** SHALL NOT 存在要求移除或禁止该字段的规格

## REMOVED Requirements

### Requirement: SKILL.md 版本字段移除

**Reason**: 该需求要求 16 个运行时 SKILL.md 移除 front matter 中的 `version:` 字段。该要求与现行实现相反——18 个 SKILL.md 均含 `version:` 字段，`scripts/sync-version.sh` 负责写入、`scripts/package-skills.sh` 负责校验、消费方通过 `grep '^version:'` 查看已安装版本。同一个 `version:` 字段不可能既被移除、又被同步与校验。此外该需求列举的 16 个 Skills 与当前体系数量不符，且其「kflow-skills-auditor 保留 version 字段」的例外条款指向本仓库中不存在的 Skill。

**Migration**: SKILL.md 保留 `version:` 字段，其规则改由本能力「Single version source for all documents」的 Skill 级载体条款与「SKILL.md 版本字段同步」需求定义。原需求中唯一仍有效的约束——设计文档头部不写具体版本号——由同一需求的文档级载体条款承接。
