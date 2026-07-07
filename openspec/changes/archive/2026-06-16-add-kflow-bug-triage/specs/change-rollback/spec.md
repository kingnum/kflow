## MODIFIED Requirements

### Requirement: 阶段回退门控

系统 SHALL 定义阶段回退时的门控规则，支持七种回退触发来源，回退目标包含 explore、design、prototype-design 三种阶段。

> **变更说明**：新增第七种回退触发来源——kflow-bug-triage 诊断路由。triage 的四层诊断结果可直接触发回退到 explore（L1 需求问题）、prototype-design（L2 原型问题）或 design（L3 设计问题），路由逻辑与现有六种来源使用相同的回退门控规则。

#### Scenario: 回退触发来源
- **WHEN** 需要触发阶段回退
- **THEN** 系统判断回退触发来源为以下七种之一：缺陷修复根因（设计错误，仅三次尝试升级后用户选择）、代码审查发现问题、用户需求变更、kflow-audit 审计发现、编码发现原型交互/视觉/状态问题、编码发现功能点/业务规则问题、kflow-bug-triage 诊断路由
- **AND** 不同来源使用相同的回退门控规则

#### Scenario: triage 诊断触发回退到 explore
- **WHEN** kflow-bug-triage 诊断确定问题源头为 L1 需求定义
- **THEN** explore 阶段状态: ✅ → ⚠️ 需修订
- **AND** prototype-design、design、plan、code、test 等后续阶段状态: 重置为 ⏳ 待开始
- **AND** 受影响产物标记为"待修订"（不删除，保留参考）
- **AND** 回退后 SHALL 进入 explore 的 REVISION 模式

#### Scenario: triage 诊断触发回退到 prototype-design
- **WHEN** kflow-bug-triage 诊断确定问题源头为 L2 原型设计
- **THEN** prototype-design 阶段状态: ✅ → ⚠️ 需修订
- **AND** design、plan、code、test 等后续阶段状态: 重置为 ⏳ 待开始
- **AND** 受影响产物标记为"待修订"（不删除，保留参考）
- **AND** 回退后 SHALL 进入 prototype-design 的 REVISION 模式

#### Scenario: triage 诊断触发回退到 design
- **WHEN** kflow-bug-triage 诊断确定问题源头为 L3 详细设计
- **THEN** design 阶段状态: ✅ → ⚠️ 需修订
- **AND** plan、code、test 等后续阶段状态: 重置为 ⏳ 待开始
- **AND** 受影响产物标记为"待修订"（不删除，保留参考）
- **AND** 回退后 SHALL 进入 design 的 REVISION 模式

#### Scenario: 仅当前子变更回退
- **WHEN** 回退仅影响单个子变更
- **THEN** 其他子变更不受影响
- **AND** 仅该子变更的阶段状态被重置

#### Scenario: 接口契约变更导致多子变更联动回退
- **WHEN** 回退涉及接口契约变更
- **THEN** 依赖该接口的所有子变更联动回退
- **AND** 评估影响范围后用户确认修订方案
