## Why

PRE_HOOK 的 RELOAD 步骤要求重新读取清单中的文件以避免使用对话缓存中的旧版本。但当前机制仅通过 mtime 判断是否跳过——如果 mtime 未变且已在当前会话中读取过，可跳过。问题是：子代理是全新上下文，没有"已在当前会话中读取过"的概念，每次都必须完整重读所有 RELOAD 文件。对于大型变更（detailed-design.md 6 文件、functional-designs/ 多文件），RELOAD 的 Token 开销显著。

## What Changes

- 定义 RELOAD 增量检测机制：主 Agent 在每次子代理调用前，为已读取且未变化的文件生成"已验证标记"
- 子代理 prompt 中嵌入"已验证文件清单"——子代理收到标记后可跳过完整读取，仅读取文件路径和摘要信息
- 修改 phase-hooks.md RELOAD 执行规则，增加"已验证跳过"选项
- 修改 kflow-shared/phase-hooks.md RELOAD 清单详情，增加"轻量模式"（仅读取路径+摘要）

## Capabilities

### New Capabilities
- `incremental-reload`: RELOAD 增量检测与跳过机制——定义已验证标记格式、子代理轻量读取模式

### Modified Capabilities
- `phase-file-reload`: RELOAD 机制新增增量检测能力
- `phase-hooks`: PRE_HOOK RELOAD 步骤新增"已验证跳过"选项

## Impact

- **kflow-shared/phase-hooks.md**: RELOAD 执行规则更新
- **核心机制文档 09-phase-hooks.md**: 设计文档同步更新
- **所有阶段 SKILL.md**: PRE_HOOK 引用更新
- 预估收益：子代理 RELOAD 步骤 Token 减少 40-60%
