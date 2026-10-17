# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

本项目用于对 KFlow（Kingnum Development Flow）这套软件开发 Skills 进行**设计、实现、构建与发布**。

### 核心内容

- [docs/designs/](docs/designs/) — 设计文档，定义 KFlow Skills 的详细规格、核心机制与运行流程
- [skills/](skills/) — 基于设计文档实现的可运行 KFlow Skills（各阶段 Skill 定义）
- [references-src/](references-src/) — 共享 references 的权威源与切片清单；各 skill 的 `references/` 由脚本生成，不手工编辑
- [.claude/skills/](.claude/skills/) — Claude Code 运行时注册的 Skill（openspec-* 工具链、skill-creator 等）
- [VERSION](VERSION) — 版本号文件
- [scripts/](scripts/) — 构建与打包脚本（`sync-references.sh` 从权威源生成切片副本并校验、`gen-slice-manifest.py` 生成切片清单、`sync-version.sh` 版本同步、`package-skills.sh` 打包、`validate-frontmatter.py` front matter 校验）

### 工作流程

```
设计（docs/designs/）→ 实现（skills/）→ references 切片生成 → 审查 → 构建打包 → 发布
```

## 设计变更流程

> **强制规则**：Skills 的设计变更须使用 openspec 进行（`openspec-propose` → `openspec-explore` → `openspec-apply-change` → `openspec-archive-change`），确保设计到交付的全流程可追溯、可验证。
>
> **强制规则**：用户输入匹配「继续/恢复/resume + 变更名」模式时，SHALL NOT 进入 Plan Mode，直接进入 Skill 路由链。此规则优先级高于 Plan Mode 自动触发。

## 提案创建要求

> **强制规则**：创建提案（`openspec-propose`）时，提案任务清单中须包含同步更新 `.claude/skills/` 中对应 SKILL.md 的任务（标注"设计文档 → SKILL.md 同步"）。
>
> **强制规则**：tasks.md 中 SHALL NOT 包含归档（openspec-archive-change）、Git commit、版本自增、打包等元工作流任务。这些由 CLAUDE.md 的归档后规则和流程自动驱动，不属于变更的实际交付工作。

## 项目结构

```
├── docs/designs/           # 设计文档
│   ├── index.md            # 设计文档入口
│   ├── overview.md         # 设计概述
│   ├── skills/             # 各 Skill 详细设计规格
│   ├── core-mechanisms/    # 核心运行机制
│   └── templates/          # 模板
├── skills/                 # 已实现的 KFlow Skills（各含 references/ 自包含辅助规则）
├── references-src/         # 共享 references 权威源 + 切片清单（生成 skills/*/references/）
├── .claude/
│   ├── skills/             # 运行时技能（openspec-*、skill-creator）
│   └── commands/opsx/      # openspec 命令
├── scripts/                # 构建与打包脚本
├── VERSION                 # 版本号文件
├── references/             # 参考资料
├── hooks/                  # 钩子脚本
├── README.md
└── LICENSE
```

## Skill 开发规范

Skill 开发采用**设计-开发-审查分离**模式：

```
docs/designs/skills/（设计规格）→ skill-creator（开发迭代）→ 发布
```

- **设计阶段**：在 `docs/designs/skills/` 编写 Skill 详细设计规格，使用 openspec 流程管理变更
- **开发阶段**：使用 `/skill-creator` 将设计规格实现为可运行的 `skills/` 条目

编写 Skill 时遵循以下强制性规范：

- **name**: 仅字母/数字/连字符，中文团队专用 `kflow-` 前缀
- **version**: 每个 SKILL.md front matter 须包含 `version` 字段，与根 `VERSION` 文件一致，通过 `scripts/sync-version.sh` 批量同步
- **description**: 中英混合格式（英文主描述 + `/中文触发词`），无中文触发词不发布
- **内容语言**: 英文（模板示例除外）
- **格式**: YAML Front Matter + Markdown
- **Token 效率**: 消除重复冗余，同一规则不出现两次
- **自包含**: 每个 skill 的辅助规则（钩子、门控、重复制等）存放在自身 `references/` 子目录中，skill 安装后零外部依赖
- **references 生成**: 共享 references 文件（`gates.md` / `repetition.md` / `state-values.md` / `self-review.md` / `phase-transition.md` / `service-lifecycle.md` / `hooks.md`）的权威源位于 `references-src/`，各 skill 的 `references/` 副本由 `scripts/sync-references.sh` 按阶段切片生成，SHALL NOT 手工编辑。修改权威源后先运行 `python scripts/gen-slice-manifest.py` 刷新切片清单的行号，再运行 `bash scripts/sync-references.sh` 生成并校验

## 工作流规则

- **并行执行**：尽可能使用子代理并行执行任务
- **规划先行**：开展任务前必须先规划、编写任务文档
- **验证闭环**：任务完成后需验证、调整至满足要求
- **障碍自解**：遇到可解决障碍（服务未启动、依赖未安装等）必须先解决再继续，禁止因障碍停止
- **文档禁止占位符**：正式文档中禁止 TODO/TBD/{待填写}/...等占位符

## 文档与状态治理

以下约定由本次 `optimize-context-budget` 变更引入，后续变更须遵循：

- **状态分层**: 变更级状态分为 `.status.md`（仅当前有效状态，≤100 行）与 `status-log.md`（历史记录，仅在中断恢复与审计场景读取）。阶段完成/回退时 SHALL 双写：向 `status-log.md` 追加事件、刷新 `.status.md` 当前字段
- **修订记录留存**: 文档头部仅保留最近 **3 条**修订记录；超出部分移入 `docs/changes/{change}/revision-history.md`（变更级，按产物文件分组）或 `docs/designs/changelog.md`（产品级）。历史承载位置不参与常规读取
- **产品级文档体积**: > 30 KB 提供章节索引；> 80 KB 拆分为目录化结构；`CONTEXT.md` 术语表例外（保持单文件 + 术语索引）
- **读取纪律**: 已拆分文档经 `index.md` 定位后读取目标分册或行区间；同阶段内不重复全文读取；主 Agent 构造子代理 prompt 时优先注入片段
- **存量文档优化**: 独立维护 Skill `kflow-doc-optimize`（非流程阶段，可无活跃变更调用）负责存量文档的修订记录裁剪、拆分与引用校验；设计规格见 [docs/designs/skills/kflow-doc-optimize.md](docs/designs/skills/kflow-doc-optimize.md)
- **自动机制**: 归档的设计合并步骤自动执行产品级文档的修订记录裁剪、章节索引维护与拆分触发，无需用户操作；消费方项目的配置（`autoCompactWindow`、门控 hook）由 `kflow-init` 在目标项目执行时写入

## 语言约定

- AI 对话、文档编写、代码注释默认使用**中文**
- 技术术语可保留英文（如 prompt, context, token）
- 代码命名使用英文

## 版本管理

版本统一由 `VERSION` 文件管理（纯文本，首行为版本号）。手动编辑该文件更新版本：

- 补丁更新: patch 位 +1
- 次要更新: minor 位 +1，patch 位归零
- 主要更新: major 位 +1，其余位归零

## 归档后规则

`/opsx:archive` 完成变更归档后，版本相关处理按以下顺序执行：

1. 判定版本自增级别（新增 Skill、新增阶段、核心运行机制变更 → minor 位 +1 且 patch 归零；Bug 修复、文档更新、重构、`references/` 变更 → patch 位 +1；无法判定时默认 patch 并提示用户复核；major 位仅由用户手动决定）
2. 更新仓库根 `VERSION` 文件
3. 运行 `scripts/sync-version.sh`，把版本值同步到全部 `skills/kflow-*/SKILL.md` 的 `version` 字段
4. 更新 `README.md` 的版本行与版本更新说明条目
5. 运行 `scripts/package-skills.sh` 打包
6. 执行 git commit，提交步骤 2~4 产生的版本变更（`VERSION`、SKILL.md 的 `version` 字段、README 版本条目）

zip 产物位于 `targets/`，受 `.gitignore` 排除，不纳入 git commit。打包脚本优先产出真正的 zip（`zip` 命令或 Python `zipfile`），无可用工具时降级为同内容的 `.tar.gz` 并在输出中提示。任一步骤失败不阻塞归档本身，须提示失败原因与手工补救方式。


