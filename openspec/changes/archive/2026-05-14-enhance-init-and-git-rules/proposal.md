## Why

当前 `kflow-init` 对 CLAUDE.md 的注入信息过于单薄（仅有一段流程规则），缺少项目特定的上下文信息（技术栈、目录结构、产品文档状态等）供后续会话使用；同时缺少对老项目的逆向分析支持和变更边界的 git 版本管理机制。

## What Changes

- **kflow-init 扩展 CLAUDE.md 注入内容**：新增「项目画像」section，包含项目类型、技术栈摘要、源码结构、关键入口文件、产品文档状态等可重新扫描更新的字段；现有「变更流程强制规则」section 新增 git commit 规则
- **kflow-init 新增老项目逆向分析流程**：检测产品文档缺失时，询问用户是否通过代码逆向扫描生成产品级文档草稿（CONTEXT.md、领域文档、全景文档），经用户审核确认后写入并 git commit
- **新增 pre-change commit 规则（议题4）**：`kflow-guide` 开始新变更前检查 git 状态，有未提交变更时分析变更性质，总结并提示用户确认后提交（一行摘要格式）
- **新增 post-archive commit 规则（议题3）**：`kflow-archive` 归档完成后分析归档内容，生成一行摘要，执行 git add + git commit
- **新增 post-init commit 规则**：首次 `kflow-init` 完成产品文档生成后立即 git commit（`init: 项目初始化，生成产品级文档基线`）
- **统一 commit 信息格式**：采用简洁的一行中文摘要格式，如 `归档变更 add-2fa: 新增双因素认证，更新认证域文档`

## Capabilities

### New Capabilities

- `init-claude-md-injection`: kflow-init 向 CLAUDE.md 注入「项目画像」和扩展「变更流程强制规则」的能力，含 marker 幂等更新、re-init 重新扫描，以及首次 init 后的自动 git commit
- `init-legacy-reverse-analysis`: kflow-init 检测到老项目产品文档缺失时，通过代码逆向扫描生成产品级文档草稿（CONTEXT.md、领域文档、全景文档），用户审核确认后写入
- `pre-change-git-commit`: kflow-guide 在新变更开始前检测未提交内容，分析变更性质，生成一行摘要并提示用户确认提交
- `post-archive-git-commit`: kflow-archive 在归档完成后分析归档内容，生成一行摘要，执行 git commit

### Modified Capabilities

- `devflow-init`: 新增项目画像 section 定义、产品文档状态字段、老项目逆向分析流程、re-entrant 更新策略、首次 init 后 commit
- `devflow-guide`: 新增 pre-change commit 检查步骤（git status 检测 → 分析变更性质 → 生成一行摘要 → 用户确认 → 提交）
- `devflow-archive`: 新增 post-archive commit 步骤（分析归档内容 → 生成一行摘要 → git add + commit）

## Impact

- 受影响的设计文档：`docs/designs/skills/kflow-init.md`、`docs/designs/skills/kflow-guide.md`、`docs/designs/skills/kflow-archive.md`
- 受影响的 Skill 实现：`kflow-init`、`kflow-guide`、`kflow-archive`
- 受影响的规范文档：`specs/devflow-init/`、`specs/devflow-guide/`、`specs/devflow-archive/`
- 受影响的项目文件：`CLAUDE.md`（由 init 自动写入）、`docs/designs/domains/`（老项目逆向分析生成）
