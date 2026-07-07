# Tasks: 阶段钩子与服务生命周期管理

## 1. 设计文档 — 核心机制

- [x] 1.1 新增 `docs/designs/core-mechanisms/09-phase-hooks.md`：阶段 PRE_HOOK/POST_HOOK 设计规范，含钩子配置表（12 阶段）、各阶段服务生命周期规则、RELOAD 清单定义、服务停止超时链
- [x] 1.2 修改 `docs/designs/core-mechanisms/05-execution-services.md` §7：补充 with_server.py 持久化模式说明、`.service-state.json` 格式定义、端口冲突检测机制
- [x] 1.3 修改 `docs/designs/core-mechanisms/05-execution-services.md` §8：拆分"服务刷新同步点"为"编译验证同步点"（编码阶段）+"测试服务刷新同步点"（测试阶段），明确每轮测试后 STOP 服务
- [x] 1.4 更新 `docs/designs/core-mechanisms/index.md`：新增 09-phase-hooks.md 入口

## 2. 设计文档 — Skill 规格

- [x] 2.1 修改 `docs/designs/skills/kflow-code.md`：移除"自动化服务循环"（START→COMPILE→RESTART），替换为"编译验证"（统一编译→验证退出码）；更新执行流程图
- [x] 2.2 修改 `docs/designs/skills/kflow-prototype-design.md`：VERIFY 步骤后增加浏览器进程清理步骤（playwright-cli kill-all）
- [x] 2.3 修改 `docs/designs/skills/kflow-api-test.md`：增加 PRE_HOOK/POST_HOOK 引用，每轮前 STOP→编译→迁移→START→健康检查，每轮后 STOP
- [x] 2.4 修改 `docs/designs/skills/kflow-e2e-test.md`：增加 PRE_HOOK/POST_HOOK 引用，每轮前 STOP→编译→迁移→START→健康检查，每轮后 STOP+浏览器清理
- [x] 2.5 修改 `docs/designs/skills/kflow-integration-test.md`：增加 PRE_HOOK/POST_HOOK 引用，每轮前 STOP→编译→迁移→START→健康检查，每轮后 STOP+浏览器清理
- [x] 2.6 修改 `docs/designs/skills/kflow-code-review.md`：确认不需要服务（纯静态分析），增加 RELOAD 清单（service-guide.md, CONTEXT.md, detailed-design.md, .status.md）
- [x] 2.7 修改 `docs/designs/skills/kflow-bug-fix.md`：增加 PRE_HOOK/POST_HOOK 引用（同触发阶段的钩子配置）
- [x] 2.8 修改 `docs/designs/skills/kflow-design.md`：接口设计表新增"关联配置项"列和"配置影响说明"列
- [x] 2.9 修改 `docs/designs/skills/kflow-explore.md`：functional-designs/part-NN.md 内容要求新增"关联配置项"章节；functional-designs/index.md 新增"配置项影响矩阵"章节
- [x] 2.10 修改 `docs/designs/skills/kflow-plan.md`：增加 PRE_HOOK/POST_HOOK 引用，RELOAD 清单（detailed-design.md, .status.md）
- [x] 2.11 修改 `docs/designs/skills/kflow-archive.md`：增加 PRE_HOOK/POST_HOOK 引用，RELOAD 清单（全量产物, .status.md）
- [x] 2.12 修改 `docs/designs/skills/kflow-audit.md`：增加 PRE_HOOK/POST_HOOK 引用，RELOAD 清单（全量产物, cross-reviews/, test-reports/, .status.md）

## 3. 模板文件

- [x] 3.1 修改 `docs/designs/templates/changes/{change}/functional-designs/part-NN.md`：新增"关联配置项"章节模板（配置项名称、关联功能点ID、关联类型、配置值变化→功能行为变化描述）
- [x] 3.2 修改 `docs/designs/templates/changes/{change}/functional-designs/index.md`：新增"配置项影响矩阵"章节模板
- [x] 3.3 修改 `docs/designs/templates/changes/{change}/detailed-design.md`：接口设计表新增"关联配置项"和"配置影响说明"列
- [x] 3.4 修改 `docs/designs/templates/changes/{change}/e2e-tests/part-NN.md`：新增"页面数据来源表"和"配置项变更影响矩阵"章节模板
- [x] 3.5 新增 `docs/designs/templates/skills/SKILL-template.md`：阶段 Skill 的 SKILL.md 通用模板，含 PRE_HOOK/POST_HOOK 引用占位和执行流程骨架
- [x] 3.6 更新 `docs/designs/templates/index.md`：新增 SKILL-template.md 条目

## 4. 运行时共享文件

- [x] 4.1 新增 `.claude/skills/kflow-shared/phase-hooks.md`：PRE_HOOK/POST_HOOK 执行规范，含 12 阶段钩子配置表、RELOAD 清单、服务生命周期操作步骤
- [x] 4.2 新增 `.claude/skills/kflow-shared/service-lifecycle.md`：服务启动/停止/健康检查的具体操作指令，含端口冲突检测规则、服务停止超时链、with_server.py 调用规范

## 5. 脚本工具

- [x] 5.1 增强 `scripts/with_server.py`：新增 `--daemon` 持久化模式、`--state-file` 状态文件路径、`--status` 状态查询、`--health` 健康检查、`--stop-all` 停止所有服务、端口冲突检测逻辑
- [x] 5.2 更新 `scripts/with_server.py` 的 `--help` 输出，包含新增参数的说明和用法示例

## 6. 运行时 Skill 同步（设计文档 → SKILL.md）

> 使用 `/skill-creator` 根据变更后的设计文档更新对应的运行时 Skill

- [x] 6.1 更新 `kflow-code` 的 SKILL.md：移除自动化服务循环，替换为编译验证步骤，增加 PRE_HOOK/POST_HOOK 引用
- [x] 6.2 更新 `kflow-prototype-design` 的 SKILL.md：VERIFY 后增加浏览器清理步骤，增加 PRE_HOOK/POST_HOOK 引用
- [x] 6.3 更新 `kflow-api-test` 的 SKILL.md：增加 PRE_HOOK/POST_HOOK 引用
- [x] 6.4 更新 `kflow-e2e-test` 的 SKILL.md：增加 PRE_HOOK/POST_HOOK 引用
- [x] 6.5 更新 `kflow-integration-test` 的 SKILL.md：增加 PRE_HOOK/POST_HOOK 引用
- [x] 6.6 更新 `kflow-code-review` 的 SKILL.md：增加 RELOAD 步骤
- [x] 6.7 更新 `kflow-bug-fix` 的 SKILL.md：增加 PRE_HOOK/POST_HOOK 引用
- [x] 6.8 更新 `kflow-design` 的 SKILL.md：接口设计表新增"关联配置项"和"配置影响说明"列
- [x] 6.9 更新 `kflow-explore` 的 SKILL.md：functional-designs/ 输出要求新增"关联配置项"章节和"配置项影响矩阵"章节
- [x] 6.10 更新 `kflow-plan` 的 SKILL.md：增加 PRE_HOOK/POST_HOOK 引用
- [x] 6.11 更新 `kflow-archive` 的 SKILL.md：增加 PRE_HOOK/POST_HOOK 引用
- [x] 6.12 更新 `kflow-audit` 的 SKILL.md：增加 PRE_HOOK/POST_HOOK 引用

## 7. CLAUDE.md 规则注入

- [x] 7.1 在 CLAUDE.md 新增规则：创建或更新阶段 Skill 时 SHALL 参考 `docs/designs/templates/skills/SKILL-template.md` 通用模板（含钩子引用）
- [x] 7.2 在 CLAUDE.md 新增审计规则：阶段 Skill 的 SKILL.md 执行流程中 MUST 包含对 `kflow-shared/phase-hooks.md` 的 PRE_HOOK 和 POST_HOOK 引用

## 8. 验证

- [x] 8.1 验证 `scripts/with_server.py --help` 输出包含所有新增参数
- [x] 8.2 验证所有 12 个受影响的运行时 SKILL.md 包含 PRE_HOOK/POST_HOOK 引用（10 个需要钩子的均有引用，2 个设计类含配置/输出变更）
- [x] 8.3 验证 `kflow-code` SKILL.md 不再包含"自动化服务循环"（START→COMPILE→RESTART）
- [x] 8.4 验证 `phase-hooks.md` 钩子配置表与各阶段 Skill 的 RELOAD 清单一致
- [x] 8.5 验证 3 个模板文件（functional-designs/part-NN.md, detailed-design.md, e2e-tests/part-NN.md）包含新增章节
