## MODIFIED Requirements

### Requirement: Code 阶段入口门控增强

系统 SHALL 在 code 阶段入口门控中增加子变更类型判断和前端输入源检查。

#### Scenario: 子变更类型判断分支
- **WHEN** 进入 code 阶段
- **THEN** 系统 SHALL 读取 detailed-design.md 中子变更划分章节确定当前子变更类型
- **AND** SHALL 根据子变更类型选择对应的门控检查项

#### Scenario: 前端子变更原型核心产物强制检查
- **WHEN** 进入 code 阶段 [前端SC]
- **THEN** 门控 SHALL 检查 docs/designs/prototypes/manifest.md 存在且清单中包含 entry 角色文件
- **AND** SHALL 检查变更级 prototype-changes.md 存在
- **AND** 任一缺失 SHALL 阻塞编码，提示「前端子变更缺少原型核心产物」

#### Scenario: CONTEXT.md 存在性检查
- **WHEN** 进入 code 阶段 [全部]
- **THEN** 门控 SHALL 检查 CONTEXT.md 存在
- **AND** 不存在时 SHALL 提示「缺少项目级领域词汇表，代码命名无法对齐」

### Requirement: E2E 测试阶段入口门控增强

系统 SHALL 在 e2e-test 阶段入口门控中增加 element-coverage-tree.md 检查。

#### Scenario: element-coverage-tree.md 存在性检查
- **WHEN** 进入 e2e-test 阶段 [前端项目]
- **THEN** 门控 SHALL 检查 element-coverage-tree.md 存在（有原型时在变更根目录，无原型时在 e2e-tests/ 目录下）
- **AND** 不存在时 SHALL 提示「缺少元素覆盖树，请重新执行详细设计阶段生成」
- **AND** [纯后端项目] SHALL 跳过此检查

### Requirement: 集成测试入口设计产物回溯验证

系统 SHALL 在 integration-test 阶段入口门控中增加设计阶段产物完整性快速检查。

#### Scenario: 设计产物回溯验证
- **WHEN** 进入 integration-test 阶段 [全部]
- **THEN** 门控 SHALL 快速检查 functional-designs/index.md 和 detailed-design.md 存在且非空
- **AND** [前后端项目 + 原型未跳过] SHALL 检查 docs/designs/prototypes/manifest.md 与变更级 prototype-changes.md 存在
- **AND** 缺失时 SHALL 提示「设计阶段产物不完整，请先执行 kflow-verify 诊断」

### Requirement: 阶段内容禁止越界

系统 SHALL 确保每个阶段仅输出其职责范围内的内容，禁止输出后续阶段的职责内容。

#### Scenario: explore 禁止输出技术设计
- **WHEN** kflow-explore 生成 functional-designs/
- **THEN** 内容聚焦用户视角（页面/操作/表单/规则）
- **AND** 不包含技术架构选型、数据模型设计、接口定义

#### Scenario: prototype 禁止输出业务规则变更
- **WHEN** kflow-prototype-design 生成 HTML 原型产物（直写产品级 `docs/designs/prototypes/`）
- **THEN** 原型基于 functional-designs/ 的业务规则设计交互
- **AND** 不可以在原型设计过程中修改业务规则

#### Scenario: design 禁止输出功能设计
- **WHEN** kflow-design 生成 detailed-design.md
- **THEN** 内容聚焦技术视角（架构/数据模型/接口/NFR）
- **AND** 不修改 functional-designs/ 中的功能定义
