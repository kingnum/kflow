## Why

当前每个子代理冷启动时加载全部 9 个核心机制文档（~10K tokens），无论该子代理所在阶段是否需要这些内容。执行类阶段（plan/code/code-review/api-test/e2e-test/integration-test/bug-fix）的子代理不需要了解恢复机制、归档条件等创造性阶段的内容。每次调用 ~10K tokens 的固定开销在 ~80 次子代理调用中累计约 800K tokens，其中大部分内容对执行类阶段无实际作用。

## What Changes

- 定义核心机制文档的分层加载策略：基础层（所有阶段必须加载）+ 阶段特定层（按阶段类型选择性加载）
- 基础层：项目类型区分（01）、状态值定义（kflow-shared/state-values.md）摘要、门控规则（kflow-shared/gate-rules.md）摘要
- 执行层附加：重复制模型（kflow-shared/repetition-model.md）——仅执行类阶段
- 服务层附加：服务生命周期（kflow-shared/service-lifecycle.md）——仅测试阶段
- 创意层附加：自审模型（kflow-shared/self-review.md）——仅设计类阶段
- 子代理 prompt 构建规范更新：按阶段类型列出需要加载的 kflow-shared 文件清单

## Capabilities

### New Capabilities
- `layered-context-loading`: 核心机制文档分层加载策略——定义基础层/执行层/服务层/创意层的文档加载清单

### Modified Capabilities
- `execution-repetition-mode`: 子代理 prompt 构建时按分层策略加载，而非全量加载核心机制文档
- `phase-file-reload`: RELOAD 机制与分层加载策略对齐

## Impact

- **核心机制文档**: 各文件添加"加载层级"标注
- **kflow-shared 文件**: 各文件添加"加载层级"标注
- **Skill 设计文档/SKILL.md**: 子代理 prompt 构建规范更新（7 个执行类阶段 + 3 个设计类阶段）
- 预估收益：每次子代理调用省 ~3-5K tokens，全变更省 ~240-400K tokens
