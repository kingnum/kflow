# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

本项目用于对 KFlow（Kingnum Development Flow）这套软件开发 Skills 进行**设计、实现、构建与发布**。

### 核心内容

- [docs/designs/](docs/designs/) — 设计文档，定义 KFlow Skills 的详细规格、核心机制与运行流程
- [skills/](skills/) — 基于设计文档实现的可运行 KFlow Skills（各阶段 Skill 定义）
- [.claude/skills/](.claude/skills/) — Claude Code 运行时注册的 Skill（openspec-* 工具链、skill-creator 等）
- [VERSION](VERSION) — 版本号文件
- [scripts/](scripts/) — 构建与打包脚本（含 `sync-version.sh` 版本同步、`sync-references.sh` 一致性校验）

### 工作流程

```
设计（docs/designs/）→ 实现（skills/）→ 审查 → 构建打包 → 发布
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

## 工作流规则

- **并行执行**：尽可能使用子代理并行执行任务
- **规划先行**：开展任务前必须先规划、编写任务文档
- **验证闭环**：任务完成后需验证、调整至满足要求
- **障碍自解**：遇到可解决障碍（服务未启动、依赖未安装等）必须先解决再继续，禁止因障碍停止
- **文档禁止占位符**：正式文档中禁止 TODO/TBD/{待填写}/...等占位符

## 语言约定

- AI 对话、文档编写、代码注释默认使用**中文**
- 技术术语可保留英文（如 prompt, context, token）
- 代码命名使用英文

## 版本管理

版本统一由 `VERSION` 文件管理（纯文本，首行为版本号）。手动编辑该文件更新版本：

- 补丁更新: `0.16.0` → `0.16.1`
- 次要更新: `0.16.0` → `0.17.0`
- 主要更新: `0.16.0` → `1.0.0`


