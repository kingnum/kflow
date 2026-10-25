# Spec Delta

## MODIFIED Requirements

### Requirement: 需求澄清收敛硬门

系统 SHALL 在 kflow-explore 的 CLARIFY 步骤维护「未决问题清单」，并在进入 SPLIT 步骤之前要求该清单为**空**。清单中的每一项必须被**消解**，或被**显式降级**为 `待补充` 并记录降级理由与责任阶段。存在未消解且未降级的清单项时，系统 SHALL NOT 进入 SPLIT。

#### Scenario: 清单为空时放行

- **WHEN** CLARIFY 完成且未决问题清单为空
- **THEN** 系统 SHALL 允许进入 SPLIT 步骤

#### Scenario: 清单非空时阻塞

- **WHEN** CLARIFY 完成且未决问题清单存在未消解、未降级的项
- **THEN** 系统 SHALL NOT 进入 SPLIT 步骤
- **AND** 系统 SHALL 逐项处理：消解，或降级为 `待补充`

#### Scenario: 显式降级放行

- **WHEN** 某项无法在本阶段消解
- **AND** 该项被显式标记为 `待补充` 并记录了降级理由与责任阶段
- **THEN** 该项 SHALL NOT 阻塞进入 SPLIT

#### Scenario: 降级项留痕

- **WHEN** 任一清单项被降级为 `待补充`
- **THEN** 系统 SHALL 在变更级 `.status.md` 记录该降级项及其理由
- **AND** 该记录 SHALL 可被后续阶段读取

#### Scenario: 清单候选来源覆盖澄清内容域

- **WHEN** 系统生成或更新未决问题清单
- **THEN** 候选 SHALL 由页面结构/菜单、可执行操作、表单项、业务规则、业务流程、非功能期望六个内容域逐域遍历产生
- **AND** SHALL NOT 以直接置空代替逐域遍历
- **AND** 清单为空时 SHALL 说明六个内容域均已遍历且未发现歧义

#### Scenario: 非功能期望歧义进入清单

- **WHEN** 用户表达的非功能期望存在歧义（如「要快」缺少感受口径）
- **THEN** 该歧义 SHALL 作为未决问题清单候选
- **AND** 经消歧路径收敛为单一确定答案后方可进入 SPLIT
