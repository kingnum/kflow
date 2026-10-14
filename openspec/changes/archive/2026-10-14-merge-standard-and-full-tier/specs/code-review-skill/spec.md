# Spec Delta

## MODIFIED Requirements

### Requirement: 两视角并行审查

变更档位为 `标准` 时，系统 SHALL 使用两个并行 Agent 执行代码审查。

#### Scenario: 档位适用范围

- **WHEN** 变更档位为 `轻量`
- **THEN** 本节两视角并行审查 SHALL NOT 适用，改由「轻量档单 Agent 收敛驱动代码审查」承担

#### Scenario: 安全+规范视角审查

- **WHEN** 代码审查启动 且 变更档位为 `标准`
- **THEN** Agent 1 检查以下内容：
  - SQL 注入风险（参数化查询）
  - XSS/CSRF 防护
  - 敏感信息泄露（密钥、token、密码明文）
  - 编码规范符合性
  - 依赖安全漏洞
- **AND** 输出安全+规范审查结果

#### Scenario: 质量+性能视角审查

- **WHEN** 代码审查启动 且 变更档位为 `标准`
- **THEN** Agent 2 检查以下内容：
  - N+1 查询问题
  - 内存泄漏风险
  - 错误处理完整性
  - 代码复杂度（圈复杂度、函数长度）
- **AND** 输出质量+性能审查结果

### Requirement: 审查门控规则

系统 SHALL 按门控规则判定审查是否通过，判定条件按变更档位分支。档位字段缺失或读取到历史遗留的 `完整` 取值时，SHALL 按 `标准` 档的门控条件判定。

#### Scenario: 审查通过

- **WHEN** 变更档位为 `标准`
- **AND** Agent 1 高严重度 = 0 且 Agent 2 高严重度 = 0 且 Agent 2 中严重度 < 3
- **THEN** 系统输出 `test-reports/review/code-review.md`
- **AND** 标记子变更编码+审查阶段完成

#### Scenario: 轻量档审查通过

- **WHEN** 变更档位为 `轻量`
- **AND** 单 Agent 高严重度 = 0 且 中严重度 < 3
- **THEN** 系统输出 `test-reports/review/code-review.md`
- **AND** 标记子变更编码+审查阶段完成

#### Scenario: 审查不通过

- **WHEN** 高严重度 ≥ 1，或中严重度 ≥ 3
- **THEN** 系统标记子变更编码阶段为 ❌ 阻塞
- **AND** 输出完整问题清单及修复要求
- **AND** 修复完成后需重新触发代码审查

### Requirement: 审查闭环验证

系统 SHALL 在修复完成后执行分级重审。变更档位为 `轻量` 时，修复后 SHALL 仅执行单轮复检，SHALL NOT 执行分级重审闭环。

#### Scenario: 轻量档单轮复检

- **WHEN** 变更档位为 `轻量` 且存在问题标记为"已修复"
- **THEN** 系统 SHALL 执行单轮复检，由单 Agent 复核全部已修复问题
- **AND** SHALL NOT 执行按高/中/低严重度分级的差异化重审

#### Scenario: 高严重度问题验证

- **WHEN** 变更档位为 `标准` 且存在高严重度问题
- **THEN** 修复后由原视角 + 安全视角交叉检查
- **AND** 两个视角均确认修复后才算关闭

#### Scenario: 中严重度问题验证

- **WHEN** 变更档位为 `标准` 且存在中严重度问题
- **THEN** 修复后由原视角重新审查

#### Scenario: 低严重度问题验证

- **WHEN** 变更档位为 `标准` 且存在低严重度问题
- **THEN** 随机抽取 30% 由 Agent 验证
- **AND** 剩余 70% 由开发者自查确认
