## ADDED Requirements

### Requirement: 元素覆盖树节点支持数据来源标注

元素覆盖树中的元素节点 SHALL 支持标注其数据来源类型，与 e2e-tests/part-NN.md 中的页面数据来源表保持一致。

#### Scenario: 元素节点标注数据来源

- **WHEN** 生成或更新 element-coverage-tree.md
- **THEN** 每个元素节点 SHALL 可选标注 `data_source` 字段
- **AND** `data_source` 取值 SHALL 从以下枚举中选择：`后端API`、`前端静态`、`配置控制`、`浏览器存储`
- **AND** 若为 `后端API`，SHALL 标注具体的接口路径
- **AND** 若为 `配置控制`，SHALL 标注依赖的配置项名称

#### Scenario: 数据来源标注与测试用例保持一致

- **WHEN** e2e-tests/part-NN.md 中某测试场景的页面数据来源表已标注某元素的数据来源
- **AND** 该元素在 element-coverage-tree.md 中也有对应节点
- **THEN** 树中该元素的 data_source 标注 SHALL 与测试用例中的标注一致
- **AND** 系统 SHALL 在 design 阶段自审时验证一致性

#### Scenario: 纯静态元素可省略数据来源

- **WHEN** 元素为纯展示性元素（如静态文本、图标、分隔线）
- **THEN** data_source 字段 SHALL 可省略或标记为 `N/A`
- **AND** 不影响元素覆盖率的计算
