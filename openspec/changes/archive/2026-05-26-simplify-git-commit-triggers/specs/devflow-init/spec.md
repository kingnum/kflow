## MODIFIED Requirements

### Requirement: 变更流程强制规则 section 扩展

kflow-init SHALL 在「变更流程强制规则」section 中包含 git 相关规则和 Skill 改进建议自动捕获规则。使用现有 marker `## 变更流程强制规则` 和新增 marker `## Skill 改进建议自动捕获` 幂等更新。

#### Scenario: 注入扩展的流程规则

- **WHEN** 执行 kflow-init
- **THEN** 系统在「变更流程强制规则」section 中包含以下 git 规则：
  - 首次 init 时，若目录非 git 仓库，询问是否执行 git init
  - 归档完成后，询问是否将当前变更及相关文件提交 git

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

- **WHEN** CLAUDE.md 已有「变更流程强制规则」section 但 git 规则内容过时
- **THEN** 系统替换为包含最新 git 规则（2 条询问式）的版本
- **AND** 保留原有非 git 规则的内容结构

#### Scenario: 自动捕获规则已存在的幂等更新

- **WHEN** CLAUDE.md 已包含 `## Skill 改进建议自动捕获` marker
- **THEN** 系统 SHALL 不重复追加该 section
- **AND** 可选择更新 section 内容以反映最新的触发模式定义

## REMOVED Requirements

### Requirement: 首次 init 后自动 git commit

**Reason**: git commit 触发点简化——init 阶段改为询问是否执行 `git init`（创建仓库），不再涉及 git commit 操作。

**Migration**: 首次 init 时，系统检测目录是否为 git 仓库。若不是，AskUserQuestion 询问是否执行 `git init`。若是，跳过。
