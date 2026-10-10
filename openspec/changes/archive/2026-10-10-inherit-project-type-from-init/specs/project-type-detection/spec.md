# Spec Delta

## MODIFIED Requirements

### Requirement: 项目类型检测

系统 SHALL 优先读取项目级项目类型记录；仅在项目级记录缺失时，才执行项目根目录扫描检测。变更创建链路 SHALL NOT 在项目级记录可用时重新扫描判定项目类型。

#### Scenario: 项目级记录可用时直接采用

- **WHEN** 变更创建链路需要项目类型
- **AND** 项目级记录（CLAUDE.md「项目画像」表的项目类型行，或 `docs/toolchain.md` 头部的项目类型字段）存在
- **THEN** 系统直接采用该记录值
- **AND** SHALL NOT 重新扫描项目根目录判定项目类型
- **AND** 输出标注来源为项目级记录

#### Scenario: 项目级记录缺失时降级检测

- **WHEN** 变更创建链路需要项目类型
- **AND** 项目级记录不存在（项目从未执行 init）
- **THEN** 系统扫描项目根目录检测前端工程标识
- **AND** 使用 AskUserQuestion 向用户确认检测结果一次
- **AND** 将确认结果写入项目级记录（`docs/toolchain.md` 头部）

#### Scenario: 检测前端工程标识

- **WHEN** 系统执行项目根目录扫描检测
- **THEN** 系统扫描前端工程标识
- **AND** 标识包括：package.json 前端框架依赖、.vue/.tsx/.jsx 文件、vite.config/webpack.config 构建配置

#### Scenario: 判断为前后端项目

- **WHEN** 扫描检测到前端工程标识存在
- **THEN** 系统标记项目类型为"前后端项目"
- **AND** 流程包含原型设计和浏览器自动化测试阶段

#### Scenario: 判断为纯后端项目

- **WHEN** 未检测到前端工程标识
- **THEN** 系统标记项目类型为"纯后端项目"
- **AND** 流程跳过原型设计和浏览器自动化测试阶段

### Requirement: 项目类型记录

系统 SHALL 将项目类型记录到项目级真源，并继承到变更级快照。项目级真源包含 CLAUDE.md「项目画像」表的项目类型行与 `docs/toolchain.md` 头部的项目类型字段，两者由同一轮扫描写入、值保持一致。变更级快照包含 `functional-designs/index.md` 与变更级 `.status.md` 的项目类型字段。

#### Scenario: 记录项目类型

- **WHEN** 项目类型经扫描检测与用户确认确定（init 首次确认，或变更创建时的降级检测）
- **THEN** 系统将项目类型写入项目级真源：CLAUDE.md「项目画像」表的项目类型行，与 `docs/toolchain.md` 头部的项目类型字段
- **AND** 两者由同一轮扫描写入，值保持一致

#### Scenario: 继承到变更级快照

- **WHEN** 变更创建链路取得项目类型（读取项目级记录或降级检测）
- **THEN** 系统将项目类型写入 `functional-designs/index.md` 与变更级 `.status.md` 的项目类型字段
- **AND** 变更级快照标注来源（项目级记录继承 / 降级检测）

#### Scenario: 变更级快照在变更生命周期内冻结

- **WHEN** 变更进入执行阶段
- **THEN** 变更级 `.status.md` 的项目类型字段 SHALL NOT 随项目级记录变化而变更
- **AND** 该变更的所有阶段判定（含阶段适用性与阶段流转）以变更级快照为准

### Requirement: 项目类型确认

系统 SHALL 仅在以下两种情形使用 AskUserQuestion 确认项目类型：init 首次确定项目类型时；扫描结果与项目级记录冲突时。其余情形 SHALL 静默复用已记录的项目类型，SHALL NOT 发起确认。

#### Scenario: 用户确认项目类型

- **WHEN** 项目类型扫描完成，且项目级记录不存在（init 首次确定项目类型）
- **THEN** 系统使用 AskUserQuestion 展示检测结果
- **AND** 用户可确认或手动修正项目类型
- **AND** 确认结果写入项目级记录

#### Scenario: re-init 记录一致时静默复用

- **WHEN** kflow-init 重新执行（re-init）
- **AND** 项目级记录已存在
- **AND** 重新扫描结果与记录一致
- **THEN** 系统静默复用记录值
- **AND** SHALL NOT 使用 AskUserQuestion 询问项目类型

#### Scenario: 变更创建时记录一致静默继承

- **WHEN** 变更创建链路读取到项目级记录
- **AND** 静默一致性校验结果与记录一致
- **THEN** 系统静默继承该值并输出「项目类型: {值}（继承项目级记录）」
- **AND** SHALL NOT 使用 AskUserQuestion 询问项目类型

#### Scenario: 变更创建时记录冲突触发复核

- **WHEN** 变更创建链路读取到项目级记录
- **AND** 静默一致性校验结果与记录冲突
- **THEN** 系统使用 AskUserQuestion 展示冲突项（扫描结果 vs 记录值）
- **AND** 用户可确认沿用记录值，或修正为扫描值
- **AND** 选择修正时更新项目级记录

## ADDED Requirements

### Requirement: 项目级项目类型记录真源与读取优先级

系统 SHALL 定义项目类型项目级记录的唯一真源与三级读取回落顺序：

1. CLAUDE.md「## 项目画像」表的项目类型行（会话自动加载，零读取成本）
2. `docs/toolchain.md` 头部的项目类型字段
3. 就地扫描检测（仅前两级均不可用时）

前两级均由 kflow-init 在同一轮扫描中写入，值一致；CLAUDE.md 项目画像为权威来源，`docs/toolchain.md` 头部为兜底来源。

#### Scenario: 读取第一优先级

- **WHEN** CLAUDE.md 存在且包含「## 项目画像」marker 与项目类型行
- **THEN** 系统从该行读取项目类型
- **AND** SHALL NOT 读取 `docs/toolchain.md`

#### Scenario: 第一优先级不可用时读取第二优先级

- **WHEN** CLAUDE.md 不存在，或不含「## 项目画像」marker，或项目类型行缺失
- **THEN** 系统读取 `docs/toolchain.md` 头部的项目类型字段

#### Scenario: 前两级均不可用时降级检测

- **WHEN** CLAUDE.md 与 `docs/toolchain.md` 均无项目类型记录
- **THEN** 系统执行就地扫描检测并向用户确认一次
- **AND** 确认结果写入 `docs/toolchain.md` 头部
- **AND** SHALL NOT 写入 CLAUDE.md「## 项目画像」区块（该区块为 kflow-init 整体扫描产物，残缺写入会与受管 marker 替换逻辑冲突）

### Requirement: 项目类型记录漂移检测

系统 SHALL 在变更创建时对项目类型执行一次静默一致性校验：扫描项目根目录的前端工程标识，并与项目级记录比对。校验 SHALL NOT 在结果一致时打扰用户。

#### Scenario: 校验结果一致

- **WHEN** 变更创建时执行静默一致性校验
- **AND** 扫描结果与项目级记录一致
- **THEN** 系统静默继承记录值并继续变更创建流程

#### Scenario: 校验发现漂移

- **WHEN** 变更创建时执行静默一致性校验
- **AND** 扫描结果与项目级记录冲突（如纯后端记录的项目新增了前端工程标识）
- **THEN** 系统使用 AskUserQuestion 展示冲突并请求用户裁决
- **AND** 用户确认变更项目类型时，更新项目级记录

#### Scenario: 漂移检测不作为阻塞项

- **WHEN** 静默一致性校验因项目根目录不可读等原因无法完成
- **THEN** 系统沿用项目级记录值继续流程
- **AND** SHALL NOT 因校验失败阻塞变更创建

### Requirement: 用户显式覆盖项目类型

系统 SHALL 接受用户在需求描述中显式声明的项目类型。显式声明优先于项目级记录与扫描结果，并触发项目级记录更新。本要求为初始误判提供纠正通道（此类误判中扫描信号与错误记录一致，一致性校验无法发现）。

#### Scenario: 用户显式声明项目类型

- **WHEN** 用户在需求描述中显式声明项目类型（如"这是前后端项目，前端在独立仓库"）
- **THEN** 系统采用该声明值，优先级高于项目级记录与扫描结果
- **AND** 更新项目级记录
- **AND** 本次变更的变更级快照写入声明值

#### Scenario: 用户指出既有记录有误

- **WHEN** 用户指出已记录的项目类型与实际情况不符
- **THEN** 系统按用户声明修正项目级记录
- **AND** 本次变更的变更级快照写入修正值
- **AND** SHALL NOT 要求用户重新执行 init
