## Why

当前各阶段产出门控检查存在缺口（8个已知缺口），子变更输入源未按类型（后端/前端）区分导致编码结果偏差，且执行阶段存在 HITL 决策点——设计阶段未完成的决策延后到编码阶段才触发。需要一个横切的产物验证能力和系统性的门控+输入源规范化，确保"设计阶段完成所有决策，执行阶段无决策点"。

## What Changes

### 第一层：门控规则补全（8个缺口）
- plan 入口：增加 CONTEXT.md、functional-designs/、api-tests/、e2e-tests/(条件) 存在性检查
- code 入口：增加子变更类型判断分支，前端子变更强制检查 prototype/index.html + design-tokens.css + element-coverage-tree.md
- code 入口：增加 CONTEXT.md 存在性检查
- e2e-test 入口：前端项目时强制检查 element-coverage-tree.md 存在
- integration-test 入口：增加设计阶段产物完整性回溯验证
- 门控规则显式标注「后端SC/前端SC」适用性

### 第二层：子变更类型与输入源规范化
- 明确子变更类型枚举：后端子变更 / 前端子变更，**禁止前后端混合子变更**
- 各阶段 Skill「输入要求」表增加「适用SC类型」列
- 前端子变更输入源仅包含原型核心产物（index.html, design-tokens.css, element-coverage-tree.md），排除过程产物（design-prompt.md, design-system/*）
- 前端子变更通过 detailed-design.md「子变更划分」章节声明「依赖API契约」列表获取接口信息
- plan/code 阶段前端子变更输入源补全

### 第三层：HITL 重新定义为设计阶段标记
- HITL = 设计不完整标记，**阻塞进入 plan 阶段**
- 所有进入 plan 的子变更 MUST 是 AFK
- HITL 决策点 MUST 在 design 或 prototype-design 阶段关闭
- **BREAKING**: 移除编码阶段 HITL 决策点 AskUserQuestion 机制

### 第四层：新增 kflow-verify 独立诊断 Skill
- 独立诊断 Skill（非流程阶段），可随时手动调用 + 归档前自动触发
- 7 维度诊断：产物存在性、内容完整性、输入源正确性、交叉引用一致性、设计决策完整性、门控合规性、审查闭环
- 3 级严重度：🔴阻塞 / 🟡警告 / 🔵建议
- 修复路由到对应阶段 REVISION 模式
- 输出诊断报告 verify-report.md

## Capabilities

### New Capabilities
- `phase-artifact-verification`: kflow-verify 独立诊断 Skill——7 维度全阶段产物诊断、严重度分级、修复路由到对应阶段 REVISION 模式，含诊断报告格式规范
- `subchange-input-source`: 子变更输入源规范——后端子变更与前端子变更的输入源定义、前端子变更原型核心产物限定（排除过程产物）、各阶段 Skill 输入表「适用SC类型」列
- `frontend-api-contract-binding`: 前端子变更 API 契约绑定机制——通过 detailed-design.md「子变更划分」章节的「依赖API契约」列表获取接口信息，plan 阶段写入 tasks.md「输入源」区

### Modified Capabilities
- `phase-boundary-enforcement`: 门控规则 §3.4 补全 8 个缺口（GAP-1~8），显式标注后端/前端子变更适用性
- `hitl-afk-classification`: HITL 从执行类型重新定义为设计阶段不完整标记，阻塞进入 plan；AFK 成为唯一合法执行类型；移除编码阶段 HITL 决策点机制
- `frontend-implementation-subchange`: 输入源明确化——限定为原型核心产物，排除过程产物；增加 detailed-design.md「依赖API契约」声明机制；禁止前后端混合子变更
- `phase-file-reload`: 各阶段 RELOAD 清单更新——plan 增加 functional-designs/ 和原型文件（条件），code 增加 CONTEXT.md，e2e-test 增加 element-coverage-tree.md
- `devflow-guide`: 新增 kflow-verify 路由入口，支持手动调用和归档前自动触发

## Impact

- 核心机制文档: `docs/designs/core-mechanisms/03-status-and-tasks.md`（门控规则 §3.4）、`docs/designs/core-mechanisms/04-gates-and-transitions.md`（HITL 定义）
- 设计文档: `docs/designs/skills/kflow-plan.md`、`kflow-code.md`、`kflow-design.md`、`kflow-e2e-test.md`、`kflow-integration-test.md`
- 新增设计文档: `docs/designs/skills/kflow-verify.md`
- 运行时 Skill: `.claude/skills/kflow-plan/SKILL.md`、`.claude/skills/kflow-code/SKILL.md`、`.claude/skills/kflow-guide/SKILL.md`
- 新增运行时 Skill: `.claude/skills/kflow-verify/`
- 模板文件: `docs/designs/templates/changes/{change}/change-status.md`
- 共享文件: `.claude/skills/kflow-shared/phase-hooks.md`
- OpenSpec specs: 5 个新建 + 5 个修改
