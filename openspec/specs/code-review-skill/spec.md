# code-review-skill Specification

## Purpose
定义 kflow-code-review 代码审查能力：在子变更编码阶段完成后自动触发，以安全规范与质量性能两个并行视角审查代码，按严重度门控判定通过或阻塞，并对修复结果执行分级重审闭环与标准报告输出。
## Requirements
### Requirement: 代码审查独立 Skill

系统 SHALL 提供 `kflow-code-review` 作为独立的代码审查 Skill，在编码阶段完成后执行。

#### Scenario: Skill 触发
- **WHEN** 子变更 TDD 编码循环全部完成（所有功能点 Green + 已提交）
- **THEN** 系统自动进入 `kflow-code-review` 阶段
- **AND** 不需要用户手动调用

#### Scenario: 前置门控检查
- **WHEN** Skill 启动
- **THEN** 系统检查子变更编码状态 = ✅ 完成
- **AND** 检查子变更 tasks.md 中所有实现任务已完成
- **AND** 不满足则提示先完成编码

### Requirement: 轻量档单 Agent 代码审查

变更档位为 `轻量` 时，系统 SHALL 使用单个 Agent 执行代码审查，串行覆盖安全+规范与质量+性能两视角的全部检查项，单轮执行，不启动并行审查 Agent。

#### Scenario: 轻量档单 Agent 执行
- **WHEN** 变更档位为 `轻量` 且代码审查启动
- **THEN** 系统 SHALL 启动单个审查 Agent
- **AND** 该 Agent SHALL 串行覆盖安全+规范视角与质量+性能视角的全部检查项

#### Scenario: 轻量档单轮执行
- **WHEN** 变更档位为 `轻量`
- **THEN** 代码审查目标轮次 SHALL 为 1 轮
- **AND** SHALL NOT 启动多轮重复制迭代

#### Scenario: 轻量档检查项不得缩减
- **WHEN** 轻量档单 Agent 审查执行
- **THEN** 该 Agent 检查范围 SHALL 包含 SQL 注入、XSS/CSRF、敏感信息泄露、编码规范、依赖安全漏洞、N+1 查询、内存泄漏、错误处理完整性、代码复杂度
- **AND** SHALL NOT 因合并为单 Agent 而裁剪任一检查项

### Requirement: 两视角并行审查

变更档位为 `标准` 或 `完整` 时，系统 SHALL 使用两个并行 Agent 执行代码审查。

#### Scenario: 档位适用范围
- **WHEN** 变更档位为 `轻量`
- **THEN** 本节两视角并行审查 SHALL NOT 适用，改由「轻量档单 Agent 代码审查」承担

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

### Requirement: 审查门控规则

系统 SHALL 按门控规则判定审查是否通过，判定条件按变更档位分支。

#### Scenario: 审查通过
- **WHEN** 变更档位为 `标准` 或 `完整`
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
- **WHEN** 变更档位为 `标准` 或 `完整` 且存在高严重度问题
- **THEN** 修复后由原视角 + 安全视角交叉检查
- **AND** 两个视角均确认修复后才算关闭

#### Scenario: 中严重度问题验证
- **WHEN** 变更档位为 `标准` 或 `完整` 且存在中严重度问题
- **THEN** 修复后由原视角重新审查

#### Scenario: 低严重度问题验证
- **WHEN** 变更档位为 `标准` 或 `完整` 且存在低严重度问题
- **THEN** 随机抽取 30% 由 Agent 验证
- **AND** 剩余 70% 由开发者自查确认

### Requirement: 代码审查报告输出

系统 SHALL 按标准格式输出代码审查报告。

#### Scenario: 报告内容
- **WHEN** 代码审查完成
- **THEN** 报告包含审查时间、子变更名、审查文件数
- **AND** 问题清单含编号、所属 Agent、严重度、文件位置、问题描述、修复状态
- **AND** 包含门控结论（通过或阻塞原因）
- **AND** 输出到 `subchanges/{subchange}/test-reports/review/code-review.md`

