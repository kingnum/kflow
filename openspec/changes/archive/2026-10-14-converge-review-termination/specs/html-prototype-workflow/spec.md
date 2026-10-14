# Spec Delta

## MODIFIED Requirements

### Requirement: 原型验证轮次的统一引用

html-prototype-workflow 中的导航合理性验证（9.1 节）与 Playwright 全覆盖验证（9.2 节）的轮次规则 SHALL 引用对应的专门能力：导航验证引用 `prototype-navigation-verification` 能力的「导航合理性验证轮次（纯收敛驱动）」，Playwright 验证引用 `prototype-playwright-5round-verification` 能力的「Playwright 全覆盖验证轮次（纯收敛驱动）」。本能力 SHALL NOT 另行定义固定 5 轮或「不允许提前终止」的轮次规则。

#### Scenario: 轮次规则单一来源

- **WHEN** 需要确定导航合理性验证或 Playwright 验证的轮次
- **THEN** 规则 SHALL 取自对应的专门能力（下限 1 轮、轮数由收敛决定、见证轮收敛终止、SHALL NOT 预设轮数上限）
- **AND** 本能力 SHALL NOT 重复定义轮次数值与终止条件

#### Scenario: 验证方式为人工审查时跳过

- **WHEN** 该变更选择「人工审查」审查方式
- **THEN** 系统 SHALL 跳过导航合理性验证与 Playwright 全覆盖验证
- **AND** SHALL NOT 启动任何验证子代理
- **AND** 系统 SHALL 直接进入用户评审 REVIEW 步骤
