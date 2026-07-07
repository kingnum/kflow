## Why

`skills/kflow-shared/` 作为跨 Skill 共享运行时文件库，在 `npx skills add` 安装时不会被部署到消费方项目的 `.claude/skills/` 下，导致所有 KFlow Skill 在消费方项目中存在无法解析的外部依赖。同时，当前 SKILL.md 没有版本字段，消费方无法判断已安装的 KFlow Skills 版本是否需要升级。

## What Changes

- **移除 `skills/kflow-shared/`**：将 9 个共享文件内容按引用关系分发到各 skill 的 `references/` 子目录，实现每个 skill 完全自包含
- **SKILL.md 瘦身**：辅助规则（钩子细节、重复制模型、门控规则、状态值定义、服务生命周期等）从 SKILL.md 下沉到 `references/` 对应文件，SKILL.md 仅保留核心流程与关键决策点
- **新增 `version` 字段**：每个 SKILL.md 的 front matter 新增 `version` 字段，值来源于根目录 `VERSION` 文件
- **新增 `scripts/sync-version.sh`**：批量同步版本号到所有 SKILL.md 的脚本，修改 VERSION 后手动调用
- **新增 `scripts/sync-references.sh`**：构建时确保 references/ 文件与变更同步的校验脚本
- **`scripts/package-skills.sh` 更新**：增加版本一致性校验步骤
- **路径引用更新**：所有 SKILL.md 中对 `kflow-shared/xxx.md` 的引用替换为 `.claude/skills/<skill-name>/references/xxx.md`（消费方），开发仓库中使用 `skills/<skill-name>/references/xxx.md`，由打包脚本处理路径适配
- **BREAKING**：消费方项目不再存在 `kflow-shared/` 目录，所有引用改为各 skill 的 `references/` 子目录

## Capabilities

### New Capabilities
- `skill-self-contained`: 每个 Skill 目录下包含 `references/` 子目录，存储该 Skill 所需的共享规则（钩子、门控、重复制、状态值、服务生命周期等），Skill 安装后零外部依赖
- `version-tracking`: SKILL.md 的 front matter 中包含 `version` 字段，与根 `VERSION` 文件保持同步，消费方可通过 `grep '^version:'` 查看已安装版本

### Modified Capabilities
- `layered-context-loading`: 上下文分层加载源从 `kflow-shared/` 改为各 skill 自身的 `references/` 目录，加载路径和文件结构相应调整
- `phase-hooks`: 钩子执行步骤从集中式 `kflow-shared/phase-hooks.md` 拆分为各 skill 的 `references/hooks.md`，每个 skill 仅包含自身阶段相关的钩子配置
- `execution-repetition-mode`: 重复制执行模型从 `kflow-shared/repetition-model.md` 拆分为各执行类 skill 的 `references/repetition.md`
- `phase-self-review`: 自审规范从 `kflow-shared/self-review.md` 拆分为各设计类 skill 的 `references/self-review.md`

## Impact

- 影响所有 17 个 KFlow Skills 的 SKILL.md（新增 front matter `version` 字段 + 引用路径更新 + 内容瘦身）
- 各 skill 目录新增 `references/` 子目录（按需 1-5 个文件）
- 删除 `skills/kflow-shared/` 整个目录及 `scripts/with_server.py`
- 新增 `scripts/sync-version.sh`、`scripts/sync-references.sh`
- 更新 `scripts/package-skills.sh`（增加版本校验 + 路径适配）
- 更新 `CLAUDE.md`（移除 kflow-shared 相关描述）
- 更新 `docs/designs/` 中涉及 kflow-shared 的引用
