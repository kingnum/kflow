## MODIFIED Requirements

### Requirement: 拆分适用文档范围

拆分机制 SHALL 适用于以下 5 组文档。

#### Scenario: 适用拆分的文档组
- **WHEN** 以下文档的条目数超过阈值
- **THEN** functional-designs 按功能点数拆分（> 30 触发）
- **AND** api-tests 按接口数拆分（> 30 触发）
- **AND** e2e-tests 按场景数拆分（> 30 触发）
- **AND** integration-tests 按场景数拆分（> 30 触发）
- **AND** detailed-design 按功能点数拆分（> 20 触发，拆分为 6 文件目录结构而非 part-NN.md 分册）

#### Scenario: detailed-design 拆分规则（新增）
- **WHEN** 变更功能点总数 > 20
- **THEN** detailed-design.md SHALL 拆分为 `detailed-design/` 目录
- **AND** 目录包含 index.md + architecture.md + domains/*.md + nfr.md + config-and-errors.md + subchange-division.md
- **AND** 拆分规则详见 design-doc-directory spec
- **AND** FP ≤ 20 时保持单文件 detailed-design.md
