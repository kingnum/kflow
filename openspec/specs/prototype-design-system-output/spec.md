# prototype-design-system-output Specification

## Purpose

要求所有原型设计引擎在生成原型时必须输出 design-system/MASTER.md 设计系统文件，作为后续 code 与 code-review 阶段进行原型对账的必备输入。

## Requirements

### Requirement: design-system 作为原型设计通用必备产物

系统 SHALL 要求所有原型设计引擎在生成原型时输出 `docs/designs/prototypes/design-system/MASTER.md` 文件（产品级原型目录下），作为原型设计阶段的通用必备产物。该文件 SHALL NOT 作为下游阶段（plan、code、code-review、e2e-test）的输入；下游的设计令牌来源 SHALL 为产品级清单中角色为 tokens 的文件。

#### Scenario: 设计系统产物必检

- **WHEN** 原型设计阶段 DESIGN 步骤完成
- **THEN** 主 Agent SHALL 验证 `docs/designs/prototypes/design-system/MASTER.md` 存在
- **AND** 文件 SHALL 包含：色彩方案、字体系统、间距规格、组件规范、交互规则
- **AND** 如产物缺失 SHALL 标记为 ⚠️ 阻塞并提示用户

#### Scenario: 设计系统生成方式不限定

- **WHEN** 用户选定工具链方案
- **THEN** 无论选择哪个工具链，编排层 SHALL 在设计 prompt 中显式要求输出 design-system/MASTER.md
- **AND** 如果工具链包含 ui-ux-pro-max，SHALL 优先由其 `--design-system --persist` 生成
- **AND** 如果工具链不包含 ui-ux-pro-max，SHALL 由设计引擎按 prompt 模板生成
- **AND** 输出路径 SHALL 统一为产品级 `docs/designs/prototypes/design-system/MASTER.md`

#### Scenario: 设计系统不供下游阶段消费

- **WHEN** code 或 code-review 阶段启动
- **THEN** 系统 SHALL NOT 加载 `docs/designs/prototypes/design-system/MASTER.md` 作为输入（其在产品级清单中角色为 process）
- **AND** code-review 阶段在执行原型对账时 SHALL 以产品级清单中角色为 tokens 的文件（`docs/designs/prototypes/design-tokens.css`）为设计令牌来源
