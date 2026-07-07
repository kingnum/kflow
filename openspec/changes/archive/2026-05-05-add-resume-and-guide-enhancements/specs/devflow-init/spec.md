# devflow-init Delta Spec

## ADDED Requirements

### Requirement: CLAUDE.md 变更流程强制规则注入

kflow-init SHALL 在完成 toolchain.md 输出后向项目 CLAUDE.md 注入变更流程强制规则。

#### Scenario: 首次注入

- **WHEN** CLAUDE.md 中不存在 `## 变更流程强制规则` section
- **THEN** 系统在 CLAUDE.md 末尾追加变更流程强制规则 section
- **AND** 规则内容包含正确流程说明和禁止做法说明
- **AND** 规则标注来源（kflow-init 自动生成）、版本号和生成时间

#### Scenario: 重复注入（幂等）

- **WHEN** CLAUDE.md 中已存在 `## 变更流程强制规则` section
- **THEN** 系统替换已有 section 内容为最新版本
- **AND** 不修改 CLAUDE.md 其他 section

#### Scenario: 规则内容要求

- **WHEN** 注入变更流程强制规则
- **THEN** 规则 SHALL 包含：
  - 所有用户变更必须首先通过 `kflow-guide` 进行流程指引
  - 新变更由 guide 引导后进入 `kflow-explore`
  - 中断恢复时使用「继续 {change-name}」触发 `kflow-resume`
  - 禁止直接调用 `kflow-code`、`kflow-plan`、`kflow-explore` 跳过 guide 指引
