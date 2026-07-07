# phase-boundary-enforcement Delta Spec

## MODIFIED Requirements

### Requirement: 阶段门控包含 RELOAD 步骤

每个阶段的门控检查 SHALL 在检查文件存在性之后、进入核心执行流程之前，增加 RELOAD 步骤，强制执行基础信息文件的重读。门控检查 SHALL 按子变更类型区分适用性。

#### Scenario: 门控检查增强

- **WHEN** 任何阶段 Skill 进入执行流程
- **THEN** 门控检查 SHALL 在原有的文件存在性检查之后，增加 RELOAD 步骤
- **AND** RELOAD 步骤 SHALL 按照钩子配置表中该阶段定义的 RELOAD 清单，重新读取所有基础信息文件的最新内容
- **AND** RELOAD 步骤 SHALL 在阶段核心逻辑执行之前完成

#### Scenario: RELOAD 步骤阻塞

- **WHEN** RELOAD 步骤中某文件不存在或无法读取
- **THEN** SHALL 标记当前阶段为 ❌ 阻塞
- **AND** SHALL 提示缺失的文件路径
- **AND** SHALL NOT 使用过时的缓存内容继续执行

#### Scenario: RELOAD 与存在性检查的关系

- **WHEN** 现有门控检查已验证文件存在
- **THEN** RELOAD 步骤 SHALL 在存在性检查之后执行
- **AND** RELOAD 专注于读取最新内容（非检查存在性）
- **AND** 若文件在检查后被删除（极端情况），RELOAD 失败 SHALL 触发阻塞

## ADDED Requirements

### Requirement: Plan 阶段入口门控增强

系统 SHALL 在 plan 阶段入口门控中增加以下检查项。

#### Scenario: CONTEXT.md 存在性检查
- **WHEN** 进入 plan 阶段 [全部]
- **THEN** 门控 SHALL 检查 CONTEXT.md 文件存在
- **AND** 不存在时 SHALL 提示「缺少项目级领域词汇表，请先完成设计探索阶段」

#### Scenario: functional-designs/ 存在性检查
- **WHEN** 进入 plan 阶段 [全部]
- **THEN** 门控 SHALL 检查 functional-designs/index.md 存在
- **AND** 不存在时 SHALL 提示「缺少功能设计文档，请先完成设计探索阶段」

#### Scenario: api-tests/ 存在性检查
- **WHEN** 进入 plan 阶段 [全部]
- **THEN** 门控 SHALL 检查 api-tests/index.md 存在
- **AND** 不存在时 SHALL 提示「缺少接口测试用例，请先完成详细设计阶段」

#### Scenario: e2e-tests/ 条件存在性检查
- **WHEN** 进入 plan 阶段 [前端SC + 前后端项目]
- **THEN** 门控 SHALL 检查 e2e-tests/index.md 存在
- **AND** 不存在时 SHALL 提示「缺少 E2E 测试用例，请先完成详细设计阶段」
- **AND** [后端子变更] SHALL 跳过此检查

### Requirement: Code 阶段入口门控增强

系统 SHALL 在 code 阶段入口门控中增加子变更类型判断和前端输入源检查。

#### Scenario: 子变更类型判断分支
- **WHEN** 进入 code 阶段
- **THEN** 系统 SHALL 读取 detailed-design.md 中子变更划分章节确定当前子变更类型
- **AND** SHALL 根据子变更类型选择对应的门控检查项

#### Scenario: 前端子变更 prototype/* 强制检查
- **WHEN** 进入 code 阶段 [前端SC]
- **THEN** 门控 SHALL 检查 prototype/index.html 存在
- **AND** SHALL 检查 prototype/design-tokens.css 存在
- **AND** SHALL 检查 prototype/element-coverage-tree.md 存在
- **AND** 任一文件缺失 SHALL 阻塞编码，提示「前端子变更缺少原型核心产物」

#### Scenario: CONTEXT.md 存在性检查
- **WHEN** 进入 code 阶段 [全部]
- **THEN** 门控 SHALL 检查 CONTEXT.md 存在
- **AND** 不存在时 SHALL 提示「缺少项目级领域词汇表，代码命名无法对齐」

### Requirement: E2E 测试阶段入口门控增强

系统 SHALL 在 e2e-test 阶段入口门控中增加 element-coverage-tree.md 检查。

#### Scenario: element-coverage-tree.md 存在性检查
- **WHEN** 进入 e2e-test 阶段 [前端项目]
- **THEN** 门控 SHALL 检查 element-coverage-tree.md 存在（prototype/ 或 e2e-tests/ 目录下）
- **AND** 不存在时 SHALL 提示「缺少元素覆盖树，请重新执行详细设计阶段生成」
- **AND** [纯后端项目] SHALL 跳过此检查

### Requirement: 集成测试入口设计产物回溯验证

系统 SHALL 在 integration-test 阶段入口门控中增加设计阶段产物完整性快速检查。

#### Scenario: 设计产物回溯验证
- **WHEN** 进入 integration-test 阶段 [全部]
- **THEN** 门控 SHALL 快速检查 functional-designs/index.md 和 detailed-design.md 存在且非空
- **AND** [前后端项目 + 原型未跳过] SHALL 检查 prototype/index.html 存在
- **AND** 缺失时 SHALL 提示「设计阶段产物不完整，请先执行 kflow-verify 诊断」

### Requirement: 门控规则显式标注 SC 类型适用性

系统 SHALL 对所有门控规则显式标注适用子变更类型。

#### Scenario: 门控规则标注格式
- **WHEN** 门控规则被定义或修改
- **THEN** 每条规则 SHALL 标注适用性：`[全部]` / `[后端子变更]` / `[前端子变更]` / `[前端项目]` / `[纯后端项目]`
- **AND** 标注 SHALL 用于门控执行时判断是否应用该规则
