# Spec Delta

## ADDED Requirements

### Requirement: 轻量档单 Agent 收敛驱动代码审查

变更档位为 `轻量` 时，系统 SHALL 使用单个 Agent 串行覆盖安全+规范与质量+性能两视角的全部检查项，SHALL NOT 启动并行审查 Agent。代码审查轮数 SHALL 由收敛实际发生在第几轮决定，SHALL NOT 预置或受限于任何档位轮数上限，SHALL NOT 因变更档位为 `轻量` 而将审查限制为单轮。检查项 SHALL NOT 因合并为单 Agent 而裁剪。

#### Scenario: 轻量档单 Agent 执行

- **WHEN** 变更档位为 `轻量` 且代码审查启动
- **THEN** 系统 SHALL 启动单个审查 Agent
- **AND** 该 Agent SHALL 串行覆盖安全+规范视角与质量+性能视角的全部检查项

#### Scenario: 轻量档轮数由收敛决定

- **WHEN** 变更档位为 `轻量` 且代码审查执行
- **THEN** 代码审查轮数 SHALL 由收敛实际发生在第几轮决定
- **AND** SHALL NOT 预置轮数上限，SHALL NOT 因变更档位为 `轻量` 而将审查限制为单轮或禁止多轮迭代

#### Scenario: 轻量档检查项不得缩减

- **WHEN** 轻量档单 Agent 审查执行
- **THEN** 该 Agent 检查范围 SHALL 包含 SQL 注入、XSS/CSRF、敏感信息泄露、编码规范、依赖安全漏洞、N+1 查询、内存泄漏、错误处理完整性、代码复杂度
- **AND** SHALL NOT 因合并为单 Agent 而裁剪任一检查项

## MODIFIED Requirements

### Requirement: 两视角并行审查

变更档位为 `标准` 或 `完整` 时，系统 SHALL 使用两个并行 Agent 执行代码审查。

#### Scenario: 档位适用范围

- **WHEN** 变更档位为 `轻量`
- **THEN** 本节两视角并行审查 SHALL NOT 适用，改由「轻量档单 Agent 收敛驱动代码审查」承担

#### Scenario: 安全+规范视角审查

- **WHEN** 代码审查启动 且 变更档位为 `标准` 或 `完整`
- **THEN** Agent 1 检查以下内容：
  - SQL 注入风险（参数化查询）
  - XSS/CSRF 防护
  - 敏感信息泄露（密钥、token、密码明文）
  - 编码规范符合性
  - 依赖安全漏洞
- **AND** 输出安全+规范审查结果

#### Scenario: 质量+性能视角审查

- **WHEN** 代码审查启动 且 变更档位为 `标准` 或 `完整`
- **THEN** Agent 2 检查以下内容：
  - N+1 查询问题
  - 内存泄漏风险
  - 错误处理完整性
  - 代码复杂度（圈复杂度、函数长度）
- **AND** 输出质量+性能审查结果

## REMOVED Requirements

### Requirement: 轻量档单 Agent 代码审查

**Reason**: 该需求将轻量档代码审查约束为「单轮执行、轮次上限为 1 轮、SHALL NOT 启动多轮重复制迭代」。本变更删除全部档位轮次上限，审查轮数由收敛实际发生在第几轮决定，轻量档不再受限于单轮规则。

**Migration**: 迁移至本能力新增的「轻量档单 Agent 收敛驱动代码审查」——保留单 Agent 串行覆盖安全+规范与质量+性能两视角的审查形态与「检查项不得缩减」，轮数改由收敛决定。收敛终止模型、见证轮判据的权威定义见 `convergence-driven-repetition` 能力。
