# Proposal: 阶段钩子与服务生命周期管理

## Why

当前系统存在五个结构性问题：
1. 各阶段启动的服务没有显式关闭机制，导致进程残留堆积
2. 阶段执行前不重读基础配置文件，依赖旧的内存缓存，可靠性差
3. 功能设计文档缺少配置项关联，配置变更的影响范围不可追溯
4. 详细设计中的接口定义与功能-配置关联脱节，缺乏推导依据
5. E2E 测试用例不标注页面数据来源和配置影响，回归测试范围不明确

此外，编码阶段的"编译验证"与测试阶段的"服务刷新"概念混淆——前者仅需验证可编译，后者才需要启动持久服务，当前设计将两者混为一谈。

## What Changes

### 基础设施层

- **服务生命周期管理**：为每个阶段定义明确的服务启动/停止规则。原型设计阶段用后停止浏览器；编码阶段仅编译验证（不启动持久服务）；API/E2E/集成测试阶段每轮前停止旧服务→启动新服务→每轮后停止服务
- **阶段前置/后置钩子标准化**：定义 PRE_HOOK（RELOAD 文件 + 端口检查 + 服务启动）和 POST_HOOK（服务停止 + 浏览器清理 + 状态更新），各阶段 Skill 通过共享引用文件执行
- **阶段前强制重读文件**：各阶段在 PRE_HOOK 中必须重读 `docs/service-guide.md`、`docs/toolchain.md`、`CONTEXT.md` 等基础信息文件
- **`with_server.py` 双模式改造**：新增 `--daemon` 持久化模式（含 `--state-file`、`--status`、`--health`、`--stop-all` 子命令），保留现有一次性模式的向前兼容
- **运行时服务状态文件**：新增 `.service-state.json` 追踪 PID、端口、启动时间、健康检查状态
- **端口冲突检测**：启动前检查目标端口占用状态，被占用时阻塞并提示
- **服务停止超时机制**：SIGTERM 30s → SIGKILL 10s → 报错 的强制终止链

### 设计层

- **功能-配置关联**：`functional-designs/part-NN.md` 新增"关联配置项"章节，定义每个功能点依赖的配置项及配置值变化对功能行为的影响
- **配置-接口推导链**：`detailed-design.md` 接口设计表新增"关联配置项"和"配置影响说明"列，建立从功能-配置关系到接口定义的推导依据

### 测试层

- **E2E 数据来源追溯**：`e2e-tests/part-NN.md` 新增"页面数据来源表"和"配置项变更影响矩阵"，标注每个页面元素的数据来源（后端 API / 前端静态 / 配置控制）及配置变更后的影响

### 基础设施安装

- **共享钩子文件**：`.claude/skills/kflow-shared/` 目录新增 `phase-hooks.md`、`service-lifecycle.md`，作为所有阶段 Skill 的共享引用
- **SKILL.md 通用模板**：`docs/designs/templates/skills/SKILL-template.md`（新增），含钩子引用占位，创建/更新 Skill 时参考
- **CLAUDE.md 规则注入**：新增钩子合规规则和模板引用规则，通过 CLAUDE.md 强制执行（不修改 skill-creator 和 kflow-skills-auditor 代码）

## Capabilities

### New Capabilities
- `phase-hooks`: 阶段前置/后置钩子标准化——PRE_HOOK（RELOAD+端口检查+服务启动）和 POST_HOOK（服务停止+浏览器清理+状态更新），各阶段通过共享引用文件执行
- `phase-file-reload`: 阶段执行前强制重读基础信息文件——各阶段在 PRE_HOOK 中按 RELOAD 清单重读 `docs/service-guide.md`、`CONTEXT.md` 等文件
- `feature-config-mapping`: 功能设计文档中的功能-配置关联——每个功能点标注关联配置项及配置值变化对功能行为的影响
- `e2e-data-tracing`: E2E 测试用例中的数据来源追溯——标注页面元素的数据来源（后端 API/前端静态/配置控制）和配置项变更影响矩阵
- `port-conflict-detection`: 服务启动前端口冲突检测——检查 `service-guide.md` 定义的端口是否被占用，被占用时阻塞并提示

### Modified Capabilities
- `centralized-service-management`: with_server.py 新增 `--daemon` 持久化模式；新增 `.service-state.json` 运行时状态追踪；服务停止增加超时强制终止链
- `per-round-service-refresh`: 编译验证与测试服务刷新分离——编码阶段末尾仅编译验证（不启动服务），测试阶段每轮前执行完整服务刷新（STOP→编译→迁移→START→健康检查）；**BREAKING**: 每轮测试完成后必须 STOP 服务
- `functional-design-content`: part-NN.md 新增"关联配置项"章节，定义配置项与功能点的关联关系及配置变更影响
- `phase-boundary-enforcement`: 各阶段门控检查新增 RELOAD 步骤——阶段执行前必须重读基础信息文件

## Impact

- **核心机制文档**: `docs/designs/core-mechanisms/` 新增 `09-phase-hooks.md`，修改 `05-execution-services.md`（§7-§8）
- **运行时 Skill**: 新增 `.claude/skills/kflow-shared/`（phase-hooks.md, service-lifecycle.md），修改 12 个阶段 Skill（kflow-explore, kflow-prototype-design, kflow-design, kflow-plan, kflow-code, kflow-code-review, kflow-api-test, kflow-e2e-test, kflow-integration-test, kflow-audit, kflow-bug-fix, kflow-archive）
- **脚本工具**: `scripts/with_server.py` 新增 `--daemon` 等持久化模式参数
- **模板文件**: 修改 `functional-designs/part-NN.md`、`detailed-design.md`、`e2e-tests/part-NN.md` 模板，新增 `templates/skills/SKILL-template.md`
- **CLAUDE.md**: 新增钩子合规规则和模板引用规则
