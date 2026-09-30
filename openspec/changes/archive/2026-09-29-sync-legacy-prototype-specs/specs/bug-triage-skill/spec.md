## MODIFIED Requirements

### Requirement: 四层溯源诊断流程

系统 SHALL 提供独立的四层溯源诊断 Skill（kflow-bug-triage），接收用户反馈后从最上游逐层排查问题源头，确定源头阶段后路由到对应的修复流程。诊断完成后 SHALL 一并执行影响范围评估。

#### Scenario: 完整四层诊断
- **WHEN** 用户通过 kflow-bug-triage 反馈问题
- **THEN** 系统按以下顺序逐层诊断：
  - L1 需求定义：检查 functional-designs/ 是否覆盖用户期望的行为、是否存在歧义或遗漏
  - L2 原型设计：检查产品级 `docs/designs/prototypes/` 是否正确实现了 L1 确认的功能点（以变更级 `prototype-changes.md` 界定本变更涉及的页面范围）
  - L3 详细设计：检查 detailed-design.md 中的接口/数据模型/状态流转是否与上游一致
  - L4 实现执行：检查代码是否正确实现了 detailed-design.md 的定义
- **AND** 每层 SHALL 输出判断结论（✅ 通过 / ❌ 有缺陷）和证据
- **AND** 当某层判定为 ❌ 时 SHALL 停止向下排查，将该层确定为问题源头
- **AND** 诊断完成后 SHALL 执行影响范围评估

#### Scenario: 快速排除
- **WHEN** 某层有明确证据表明问题不在该层
- **THEN** 系统 SHALL 跳过该层的详细检查，直接进入下一层
- **AND** 在诊断报告中标注快速排除的理由

#### Scenario: 诊断证据来源
- **WHEN** 系统执行某层诊断
- **THEN** SHALL 使用以下证据来源：
  - L1：functional-designs/index.md + functional-designs/part-NN.md + CONTEXT.md
  - L2：`docs/designs/prototypes/index.html` + 变更级 `prototype-changes.md` + 变更级 `element-coverage-tree.md` + functional-designs/
  - L3：detailed-design.md + api-tests/index.md + functional-designs/
  - L4：代码实现 + detailed-design.md

#### Scenario: 影响范围评估作为诊断的一部分
- **WHEN** 四层诊断完成
- **THEN** 系统 SHALL 执行影响范围评估（参见 triage-impact-assessment capability）
- **AND** 评估结果 SHALL 写入问题详情文件的影响范围评估节
