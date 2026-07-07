## Why

当前系统中，原型设计（prototype-design）阶段产出的 HTML 原型与其后的 E2E 测试用例（e2e-tests/）之间缺乏系统化的元素级追溯链。设计阶段编写 E2E 测试用例时依赖人工经验判断"应该测什么"，容易遗漏原型中已定义但未显式覆盖的交互元素、浮窗、表单状态和页面跳转链路。同时，prototype/element-spec.md 和 prototype/nav-tree.md 两个文件的职责分散，在编解码约束和 E2E 覆盖两个方向上的信息冗余且不完整。

## What Changes

- **新增** `element-coverage-tree.md` 统一产物文件，以树状图形式记录页面导航结构、交互元素、操作状态、浮窗/弹窗链路、及 TC-ID 映射，替代 prototype/element-spec.md 和 prototype/nav-tree.md
- **新增** design 阶段的 EXPLORE 子步骤：有原型时解析 prototype HTML 生成树，无原型时通过 playwright-cli 逐页探索实际前端页面生成树
- **增强** E2E 测试用例设计门控：树中每个元素+状态必须挂载至少一个 TC-ID，覆盖率达到 100% 后方可进入下一阶段
- **增强** E2E 测试执行阶段（kflow-e2e-test）：每轮加载树并统计元素实际触达率，未触达元素作为回归信号上报
- **修改** prototype-design COMPLETE 步骤：不再生成 element-spec.md，改为生成 prototype/element-coverage-tree.md（无 TC-ID 的初始版本）
- **BREAKING**: 废弃 `prototype/element-spec.md` 产物，其编码约束和对账功能由 element-coverage-tree.md 承接

## Capabilities

### New Capabilities
- `e2e-element-coverage-tree`: 统一元素覆盖树——系统 SHALL 在变更级维护一份树状结构的元素覆盖文件，合并页面导航（原 nav-tree.md）、交互元素清单（原 element-spec.md 超集）、操作驱动的动态链路（浮窗/弹窗/跳转）、及 E2E 测试场景 ID 映射。有原型时落点在 `prototype/element-coverage-tree.md`，无原型时落点在 `e2e-tests/element-coverage-tree.md`

### Modified Capabilities
- `prototype-to-code-consistency`: 移除 element-spec.md 相关 requirement，将元素覆盖对账和路由覆盖对账的数据源切换为 element-coverage-tree.md；移除 nav-tree.md 相关 requirement，导航结构信息合并到 element-coverage-tree.md
- `playwright-cli-e2e-workflow`: 新增每轮测试 RELOAD 步骤加载 element-coverage-tree.md 并统计元素实际触达率，未触达元素标记为回归信号；新增 element-coverage-tree.md 的探索生成模式（无原型时使用 playwright-cli 逐页探索实际页面）
- `e2e-data-tracing`: 元素覆盖树的元素节点 SHALL 支持标注数据来源类型（后端API/前端静态/配置控制/浏览器存储），与现有页面数据来源表保持一致

## Impact

- **设计文档**: `docs/designs/skills/kflow-design.md`（§7 E2ETESTS 增强）、`docs/designs/skills/kflow-e2e-test.md`（执行流程增强）、`docs/designs/skills/kflow-prototype-design.md`（COMPLETE 步骤修改）
- **运行时 Skill**: `.claude/skills/kflow-design/SKILL.md`、`.claude/skills/kflow-e2e-test/SKILL.md`、`.claude/skills/kflow-prototype-design/SKILL.md`
- **模板**: `docs/designs/templates/changes/{change}/e2e-tests/index.md`（新增元素覆盖树章节）、`docs/designs/templates/changes/{change}/e2e-tests/part-NN.md`（新增覆盖元素字段）、新增 `element-coverage-tree.md` 产物格式规范
- **Specs**: 新增 1 个 spec（e2e-element-coverage-tree），修改 3 个 spec（prototype-to-code-consistency、playwright-cli-e2e-workflow、e2e-data-tracing）
