# KFlow Skills 核心运行机制

> **版本**: 参见仓库根目录 `VERSION` 文件
> **创建时间**: 2026-04-29
> **更新时间**: 2026-05-28

本文档定义 KFlow Skills 体系的核心运行机制，原 `core-mechanisms.md`（2235 行）已拆分为以下 9 个文件：

## 文档导航

| 文件 | 章节 | 说明 |
|------|------|------|
| [01-project-types.md](01-project-types.md) | 一、项目类型区分机制 | 前后端/纯后端项目检测规则、阶段差异 |
| [02-directory-structure.md](02-directory-structure.md) | 二、目录结构规范 | 变更管理目录、命名规范、文档拆分策略 |
| [03-status-and-tasks.md](03-status-and-tasks.md) | 三~四、状态文件 + 任务清单 | 状态文件格式、门控规则、任务清单模板 |
| [04-gates-and-transitions.md](04-gates-and-transitions.md) | 五~六、条件产物引用 + 阶段流转 | 产物引用图例、正向/回退流转、归档条件、设计合并 |
| [05-execution-services.md](05-execution-services.md) | 七~八、执行服务 | 服务管理（含持久化模式）、编译验证与测试服务刷新分离、批量推进、脚本原则、文档禁止、审查合并、覆盖追溯 |
| [09-phase-hooks.md](09-phase-hooks.md) | 阶段钩子与服务生命周期 | PRE_HOOK/POST_HOOK 规范、12 阶段钩子配置表、RELOAD 清单、服务停止超时链、端口冲突检测、浏览器进程管理 |
| [06-recovery.md](06-recovery.md) | 十二、中断恢复机制 | checkpoint 两级存储、恢复优先级链、kflow-resume 流程 |
| [07-agent-model.md](07-agent-model.md) | 十五~十六、子代理执行模型 + 自审机制 | 重复制、复杂度评估、子代理隔离规则、10 轮自审、VERIFY 子代理验证 |
| [08-governance.md](08-governance.md) | 十七~十八、阶段边界 + Git 管理 | 文档白名单、越界禁止、git commit 节点 |
