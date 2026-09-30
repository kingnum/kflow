# prototype-change-tracking Specification

## Purpose

定义变更级原型改动追踪机制。变更直写产品级原型目录 `docs/designs/prototypes/`，通过 `prototype-changes.md` 改动清单、`prototype-backup/` 改动前快照与并发写入哈希检测，使改动可追溯、可检测跨变更冲突、可回滚。

## Requirements


### Requirement: 变更级改动清单

系统 SHALL 在变更目录下维护 `prototype-changes.md`，记录本变更对产品级原型目录 `docs/designs/prototypes/` 的全部改动。变更 SHALL NOT 维护自己的原型副本目录，SHALL 直接写产品级原型目录。

#### Scenario: 清单生成时机

- **WHEN** 系统向产品级原型目录 `docs/designs/prototypes/` 写入文件后
- **THEN** 系统 SHALL 立即更新变更级 `prototype-changes.md`
- **AND** 新增条目 SHALL 记录该文件的产品级相对路径、改动类型、改动前哈希与改动说明

#### Scenario: 条目格式

- **WHEN** 系统写入 `prototype-changes.md` 条目
- **THEN** 条目 SHALL 采用表格行格式 `| 文件路径 | 类型(新增/修改/删除) | 改动前哈希 | 说明 |`
- **AND** 类型为"新增"的条目，改动前哈希 SHALL 记录为 `-`，表示不存在改动前版本

#### Scenario: 清单作为修订模式检测对象

- **WHEN** 原型设计阶段入口 CHECK 判定是否进入修订模式
- **THEN** 系统 SHALL 以变更级 `prototype-changes.md` 是否存在且非空作为检测对象
- **AND** SHALL NOT 以变更级 `prototype/index.html` 是否存在作为检测对象

### Requirement: 改动前快照

系统 SHALL 在修改或删除产品级原型目录中已存在的文件之前，将改动前版本保存到变更级 `prototype-backup/`，且 SHALL 按产品级相对路径镜像存放。

#### Scenario: 修改前保存快照

- **WHEN** 系统准备修改 `docs/designs/prototypes/` 下的一个已存在文件
- **THEN** 系统 SHALL 先把该文件的当前版本复制到 `prototype-backup/` 下对应的产品级相对路径
- **AND** 快照 SHALL 在该文件被写入之前完成

#### Scenario: 删除前保存快照

- **WHEN** 系统准备删除 `docs/designs/prototypes/` 下的一个已存在文件
- **THEN** 系统 SHALL 先把该文件复制到 `prototype-backup/` 下对应的产品级相对路径
- **AND** 快照 SHALL 在该文件被删除之前完成

#### Scenario: 新增文件不生成快照

- **WHEN** 系统写入的文件在产品级原型目录中原本不存在
- **THEN** 系统 SHALL NOT 为该文件生成 `prototype-backup/` 快照
- **AND** 系统 SHALL 在 `prototype-changes.md` 中将其类型记录为"新增"

### Requirement: 并发写入检测

系统 SHALL 在向产品级原型目录写入文件前，比对 `prototype-changes.md` 记录的改动前哈希与磁盘当前文件哈希；不一致时 SHALL 提示"该文件已被其他变更修改"并交用户裁决。

#### Scenario: 哈希一致时正常写入

- **WHEN** 系统准备修改 `docs/designs/prototypes/` 下的文件且改动前哈希与磁盘当前哈希一致
- **THEN** 系统 SHALL 直接写入
- **AND** 系统 SHALL 在 `prototype-changes.md` 中把该文件的改动前哈希更新为本次写入前的版本哈希

#### Scenario: 哈希不一致时提示用户

- **WHEN** 改动前哈希与磁盘当前文件哈希不一致
- **THEN** 系统 SHALL 提示"该文件已被其他变更修改"
- **AND** 系统 SHALL 通过 AskUserQuestion 交用户裁决
- **AND** SHALL NOT 在用户裁决前覆盖该文件

#### Scenario: 用户裁决的三个选项

- **WHEN** 系统就哈希冲突征求用户裁决
- **THEN** 系统 SHALL 提供三个选项：基于新版本改、覆盖、人工合并
- **AND** 用户选择"基于新版本改"时，系统 SHALL 以磁盘当前版本为基线重新应用本变更的改动意图
- **AND** 用户选择"覆盖"时，系统 SHALL 以本变更版本覆盖磁盘文件，并将磁盘版本存入 `prototype-backup/`
- **AND** 用户选择"人工合并"时，系统 SHALL 停止自动写入并等待用户提供合并结果

### Requirement: 回滚支持

系统 SHALL 支持依据 `prototype-changes.md` 与 `prototype-backup/` 将产品级原型目录恢复到本变更介入之前的状态。

#### Scenario: 变更废弃时回滚

- **WHEN** 变更被废弃或用户要求回滚原型改动
- **THEN** 系统 SHALL 读取 `prototype-changes.md` 并逐条处理
- **AND** 类型为"修改"或"删除"的条目 SHALL 用 `prototype-backup/` 中对应产品级相对路径的快照恢复
- **AND** 类型为"新增"的条目 SHALL 删除产品级原型目录中的对应文件

#### Scenario: 回滚前确认

- **WHEN** 系统执行原型回滚
- **THEN** 系统 SHALL 先向用户展示受影响的文件清单并取得确认
- **AND** 回滚完成后 SHALL 在 `prototype-changes.md` 中标记条目已回滚
