## MODIFIED Requirements

### Requirement: 变更流程强制规则 section 扩展

kflow-init SHALL 在「变更流程强制规则」section 中新增 git commit 相关规则和 Skill 改进建议自动捕获规则。使用现有 marker `## 变更流程强制规则` 和新增 marker `## Skill 改进建议自动捕获` 幂等更新。

#### Scenario: 注入扩展的流程规则

- **WHEN** 执行 kflow-init
- **THEN** 系统在「变更流程强制规则」section 中包含以下 git 规则：
  - 每个变更归档后必须执行 git commit（提交信息包含变更名称和归档日期）
  - 开始新变更前必须检查 git 状态，有未提交变更时分析-总结-确认-提交
  - 首次 init 完成后若生成了产品文档则必须 git commit

#### Scenario: 注入 Skill 改进建议自动捕获规则

- **WHEN** 执行 kflow-init
- **AND** CLAUDE.md 不存在 `## Skill 改进建议自动捕获` marker
- **THEN** 系统在 CLAUDE.md 末尾追加 `## Skill 改进建议自动捕获` section
- **AND** section 内容 SHALL 定义三种触发模式和处理规则：
  - 「因...无法...」→ 记录阻塞原因和失败的执行路径
  - 「因...导致...」→ 记录因果链和受影响的阶段
  - 用户纠正后 AI 回复中的「你说得对」等附和 → 记录用户的纠正内容
- **AND** 标注来源为 kflow-init 和注入时间戳

#### Scenario: 已有流程规则的增量更新

- **WHEN** CLAUDE.md 已有「变更流程强制规则」section 但不含 git 规则
- **THEN** 系统替换为包含 git 规则的最新版本
- **AND** 保留原有非 git 规则的内容结构

#### Scenario: 自动捕获规则已存在的幂等更新

- **WHEN** CLAUDE.md 已包含 `## Skill 改进建议自动捕获` marker
- **THEN** 系统 SHALL 不重复追加该 section
- **AND** 可选择更新 section 内容以反映最新的触发模式定义
