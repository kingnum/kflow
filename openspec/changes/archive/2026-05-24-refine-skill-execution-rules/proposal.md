## Why

KFlow Skills 体系在测试执行、原型设计流程、版本迁移、一致性保障、容错降级等维度存在实践缺口，导致：1）测试前服务启动未显式绑定 service-guide.md，依赖 agent 推断；2）E2E 测试中子代理将 playwright-cli 交互误用为脚本编写；3）原型设计阶段可能在 explore→design 路径中被悄悄跳过；4）re-init 时未对未归档变更做阶段对齐检查；5）前端实现与原型设计之间缺乏轻量级对账机制（截图对比太耗 token）；6）子代理在模型 API 报错时自行改用 Bash 执行 Playwright，绕过 /playwright-cli 约束。

## What Changes

- **测试前服务启动显式绑定**：WAIT_SYNC 步骤必须读取 service-guide.md 中的启动命令和环境配置来启动服务，不依赖 agent 自行推断
- **generated-test.spec.ts 改为可选收集**：仅当本轮测试通过率 ≥80% 时收集为回归资产；子代理禁止在 playwright-cli 交互前主动编写任何测试脚本
- **强制原型设计询问**：explore 完成后对前后端项目插入 AskUserQuestion，使用 prototype_decision 标记控制幂等，guide RESUME 路由不重复触发
- **re-init 变更对齐检查**：扫描未归档变更的阶段列表，对比当前 skill 体系阶段定义，输出对齐报告但不自动修改
- **原型→代码一致性保障**：从实际原型 HTML 文件自动提取 design-tokens.css + element-spec.md + nav-tree.md，code 阶段注入约束，code-review 阶段 Grep 对账替代截图对比
- **子代理工具切换禁令**：禁止子代理因模型 API 报错自行改用 Bash 或更换测试工具，改为阻塞+上报；如确需换工具必须 AskUserQuestion 确认

## Capabilities

### New Capabilities

- `prototype-decision-gate`: 原型设计决策门控——explore 完成后对前后端项目强制询问是否进入原型设计，prototype_decision 标记控制幂等
- `prototype-to-code-consistency`: 原型到代码一致性保障——从原型 HTML 自动提取设计令牌/元素清单/导航树，编码阶段注入约束，审查阶段 Grep 对账

### Modified Capabilities

- `centralized-service-management`: WAIT_SYNC 步骤显式绑定 service-guide.md 中的启动命令和环境配置
- `playwright-cli-e2e-workflow`: generated-test.spec.ts 从必须改为可选收集（通过率≥80%时），新增禁止主动编写测试脚本硬约束，新增子代理工具切换禁令
- `devflow-init`: 新增 re-init 变更对齐检查步骤，扫描未归档变更阶段列表与当前 skill 体系对比

## Impact

- **修改的 Skill 设计文档**：`kflow-e2e-test.md`、`kflow-api-test.md`、`kflow-explore.md`、`kflow-init.md`、`kflow-code.md`、`kflow-code-review.md`、`kflow-prototype-design.md`
- **修改的核心机制**：`core-mechanisms.md`（服务管理职责归属、阶段对齐检查机制）
- **修改的现有规格**：`centralized-service-management/spec.md`、`playwright-cli-e2e-workflow/spec.md`、`devflow-init/spec.md`
- **新建的规格**：`prototype-decision-gate/spec.md`、`prototype-to-code-consistency/spec.md`
- **无破坏性变更**：所有变更为新增约束或补充机制，不影响已有变更的正常流转
