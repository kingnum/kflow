# Spec Delta

## MODIFIED Requirements

### Requirement: 变更流程强制规则 section 扩展

kflow-init SHALL 向 CLAUDE.md 的「变更流程强制规则」section 注入跨 skill 的路由约束、用户接口约定与流程概览。使用现有 marker `## 变更流程强制规则` 幂等更新。该 section SHALL NOT 包含由某个 skill 在自身执行流程中完成的步骤。

#### Scenario: 注入扩展的流程规则

- **WHEN** 执行 kflow-init
- **THEN** 系统在「变更流程强制规则」section 中包含以下规则：
  - 所有变更须先经 `kflow-guide` 流程指引
  - 新变更经 guide 引导后进入 `kflow-explore`
  - 中断恢复使用「继续 {change-name}」
  - 禁止直接调用阶段 Skill 绕过 guide
  - 流程阶段列表
  - 查看状态使用「状态」「进度」关键词
- **AND** 该 section SHALL NOT 包含归档后 git commit 询问、非 git 仓库时的 git init 询问等 skill 内部执行步骤
- **AND** SHALL NOT 包含仓库根 `VERSION` 文件、`scripts/` 下的技能仓库脚本、`targets/` 打包产物或 `README.md` 版本条目

#### Scenario: 已有流程规则的增量更新

- **WHEN** CLAUDE.md 已有「变更流程强制规则」section 但其内容与当前模板版本不一致（含旧版仍含归档后 git commit 询问、版本自增或打包规则的情形）
- **THEN** 系统用当前模板内容替换该 section
- **AND** 替换后的 section SHALL NOT 含上述 git 与版本自增规则
- **AND** 该 section 之外的内容 SHALL NOT 被修改

## ADDED Requirements

### Requirement: Marker 版本判据与替换兜底

kflow-init SHALL 以自身 SKILL.md front matter 的 `version` 字段作为所注入 marker section 的模板版本标识。版本来源 SHALL NOT 引用消费方项目中可能不存在的文件（如仓库根 `VERSION` 文件）。

#### Scenario: marker 版本与当前模板版本一致

- **WHEN** CLAUDE.md 中 marker 区块标注的版本等于 kflow-init 当前的 `version` 字段值
- **THEN** 系统 SHALL 仅更新该区块的时间戳
- **AND** SHALL NOT 替换区块内容

#### Scenario: marker 版本与当前模板版本不一致

- **WHEN** CLAUDE.md 中 marker 区块标注的版本不等于 kflow-init 当前的 `version` 字段值
- **THEN** 系统 SHALL 用当前模板内容全量替换该区块内容

#### Scenario: marker 版本缺失或无法解析

- **WHEN** CLAUDE.md 中 marker 区块未标注版本，或其版本值无法解析
- **THEN** 系统 SHALL 判定该区块与当前模板版本不同
- **AND** SHALL 用当前模板内容全量替换该区块内容

### Requirement: 项目自定义规则区块保护

kflow-init SHALL 为项目自行维护的规则提供独立 marker 区块 `## 项目自定义规则`。该区块 SHALL NOT 纳入 kflow-init 的模板替换范围。

#### Scenario: 首次注入创建项目自定义区块

- **WHEN** 执行 kflow-init 且 CLAUDE.md 不含 `## 项目自定义规则` marker
- **THEN** 系统 SHALL 在 CLAUDE.md 中创建该区块
- **AND** 区块内 SHALL 标注该区块由项目自行维护、kflow-init 不覆盖其内容

#### Scenario: re-init 不覆盖项目自定义规则

- **WHEN** 执行 kflow-init 且 CLAUDE.md 已含 `## 项目自定义规则` marker
- **THEN** 系统 SHALL NOT 修改该区块内容
- **AND** SHALL NOT 因模板版本变化而替换或删除该区块
- **AND** 用户在框架管理区块之外新增的内容 SHALL NOT 被删除

### Requirement: Skill 改进建议自动捕获 marker 注入

kflow-init SHALL 向 CLAUDE.md 注入 `## Skill 改进建议自动捕获` section，定义 AI 对话中的三种触发模式。使用 `## Skill 改进建议自动捕获` 作为唯一 marker 幂等更新。

#### Scenario: 注入自动捕获规则

- **WHEN** 执行 kflow-init
- **AND** CLAUDE.md 不存在 `## Skill 改进建议自动捕获` marker
- **THEN** 系统在 CLAUDE.md 中追加该 section
- **AND** section 内容 SHALL 定义三种触发模式和处理规则：
  - 「因...无法...」→ 记录阻塞原因和失败的执行路径
  - 「因...导致...」→ 记录因果链和受影响的阶段
  - 用户纠正后 AI 回复中的「你说得对」等附和 → 记录用户的纠正内容
- **AND** 标注来源为 kflow-init 和注入时间戳

#### Scenario: 自动捕获规则已存在的幂等更新

- **WHEN** CLAUDE.md 已包含 `## Skill 改进建议自动捕获` marker
- **THEN** 系统 SHALL NOT 重复追加该 section
- **AND** SHALL 按 marker 版本判据决定是否更新该 section 内容
