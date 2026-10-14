# Spec Delta

## MODIFIED Requirements

### Requirement: 历史变更的档位缺省回退

缺少「变更档位」字段的历史变更 `.status.md`，系统 SHALL 按 `完整` 档处理。

#### Scenario: 无档位字段按完整档处理

- **WHEN** 变更级 `.status.md` 基本信息中不含「变更档位」字段
- **THEN** 系统 SHALL 按 `完整` 档确定审查形态与产出深度
