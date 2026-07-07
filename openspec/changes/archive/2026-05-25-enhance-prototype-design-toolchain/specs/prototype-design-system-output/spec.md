## ADDED Requirements

### Requirement: design-system 作为原型设计通用必备产物

系统 SHALL 要求所有原型设计引擎在生成原型时输出 `design-system/MASTER.md` 文件，作为后续 code 和 code-review 阶段进行原型对账的必要输入。

#### Scenario: 设计系统产物必检

- **WHEN** 原型设计阶段 DESIGN 步骤完成
- **THEN** 主 Agent SHALL 验证 `design-system/MASTER.md` 存在
- **AND** 文件 SHALL 包含：色彩方案、字体系统、间距规格、组件规范、交互规则
- **AND** 如产物缺失 SHALL 标记为 ⚠️ 阻塞并提示用户

#### Scenario: 设计系统生成方式不限定

- **WHEN** 用户选定工具链方案
- **THEN** 无论选择哪个工具链，编排层 SHALL 在设计 prompt 中显式要求输出 design-system/MASTER.md
- **AND** 如果工具链包含 ui-ux-pro-max，SHALL 优先由其 `--design-system --persist` 生成
- **AND** 如果工具链不包含 ui-ux-pro-max，SHALL 由设计引擎按 prompt 模板生成
- **AND** 输出路径 SHALL 统一为 `design-system/MASTER.md`

#### Scenario: 设计系统供后续阶段使用

- **WHEN** code 或 code-review 阶段启动
- **THEN** 系统 SHALL 加载 `design-system/MASTER.md` 作为设计约束参考
- **AND** code-review 阶段 SHALL 在执行原型对账时对比代码中的 CSS 变量与 design-system 中定义的设计令牌
