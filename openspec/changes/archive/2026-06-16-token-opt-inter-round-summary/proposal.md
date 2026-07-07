## Why

重复制模式下，每轮子代理完全独立启动，零上下文继承。第 1 轮和第 10 轮加载完全相同的上下文，执行完全相同的检查。后期轮次（7-10 轮）往往无新发现但仍须走完全部流程，造成大量无效 Token 消耗。如果后期轮次能接收到前轮摘要（已发现问题、已修复项、未解决项），可以跳过已确认无问题的区域，提高有效工作密度。

## What Changes

- 定义轮间摘要格式：每轮子代理返回后，主 Agent 提取摘要（已发现问题列表、已修复项列表、未解决项列表、覆盖率变化）
- 后续轮次子代理的 prompt 中嵌入前轮摘要
- 后期轮次可基于摘要跳过已确认无问题的区域（但保留全量遍历的兜底检查）
- 修改重复制执行规范（kflow-shared/repetition-model.md）添加轮间摘要传递规则

## Capabilities

### New Capabilities
- `inter-round-summary`: 重复制轮间摘要传递机制——定义摘要格式、提取规则、注入方式、跳过条件

### Modified Capabilities
- `execution-repetition-mode`: 重复制模型新增轮间摘要传递规则

## Impact

- **kflow-shared/repetition-model.md**: 新增轮间摘要规范
- **核心机制文档 07-agent-model.md**: 同步更新
- **7 个执行类阶段 SKILL.md**: 子代理 prompt 构建逻辑更新
- 预估收益：后期轮次效率提升 30%+，全变更省 ~200-300K tokens
