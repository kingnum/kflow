## Context

当前 `skills/kflow-shared/` 包含 9 个共享文件（总计 1946 行），被 17 个 KFlow Skill 通过跨文件引用使用。这些引用假设消费方项目根目录下存在 `kflow-shared/` 目录，但实际上：

- `npx skills add` 仅安装 `.claude/skills/<skill-name>/SKILL.md`，不会在项目根创建 `kflow-shared/`
- 开发仓库 `skills/` 下的 `kflow-shared/` 不会被打包脚本分发
- 这意味着所有 KFlow Skill 在消费方项目中存在无法解析的外部依赖

同时，当前 SKILL.md 的 front matter 缺少 `version` 字段，消费方无法判断已安装的 KFlow Skills 版本。

## Goals / Non-Goals

**Goals:**
- 移除 `skills/kflow-shared/`，将共享内容分发到各 skill 的 `references/` 子目录
- 每个 skill 完全自包含，通过 `npx skills add` 安装后零外部依赖
- SKILL.md 瘦身：核心流程保留在主文件，辅助规则下沉到 `references/`
- 新增 `version` front matter 字段 + 同步脚本，实现版本追踪
- 打包脚本增加路径适配和版本一致性校验

**Non-Goals:**
- 不改变现有阶段流程和门控逻辑的语义
- 不改变 `npx skills add` 的安装机制
- 不同步维护两份 `references/` 内容（无中央 kflow-shared 源）

## Decisions

### 决策 1：references/ 文件分发映射

基于引用热度分析确定每个 skill 的 references/ 内容：

```
文件                     行数    分配目标 (skills)
─────────────────────────────────────────────────────
phase-hooks.md           283    code, api-test, e2e-test, integration-test,
                                plan, code-review, audit, archive, bug-triage,
                                bug-fix, design, prototype-design
                                共 12 个 skill，每 skill 仅含自身阶段的钩子章节
repetition-model.md      455    code, api-test, e2e-test, integration-test,
                                plan, code-review, bug-triage, bug-fix
                                共 8 个执行类 skill
gate-rules.md            262    code, api-test, e2e-test, integration-test,
                                plan, code-review, design, explore,
                                prototype-design, bug-fix
                                共 10 个 skill，每 skill 仅含当前阶段门控
state-values.md           37    code, api-test, e2e-test, integration-test,
                                plan, code-review, design, explore,
                                prototype-design
                                共 9 个 skill
service-lifecycle.md     332    code, api-test, e2e-test, integration-test
                                共 4 个需要服务管理的 skill
self-review.md           211    explore, prototype-design, design
                                共 3 个设计类 skill
permission-model.md      121    init (唯一引用方)
recovery-protocol.md     144    resume (唯一引用方)
archive-rules.md         101    archive (唯一引用方)
```

此外，`kflow-shared/scripts/with_server.py` 移至 `skills/kflow-code/scripts/with_server.py`（主要使用者为 code 阶段）。

**Rationale**: 每个 skill 仅携带自己需要的规则，避免冗余。单引用文件归入对应 skill 无需特别处理。

### 决策 2：SKILL.md 瘦身策略

**保留在 SKILL.md 的内容：**
- Front matter (name, version, description, triggers, allowed-tools)
- 核心执行流程图 (ASCII 流程图 + 步骤摘要)
- 本阶段特有的规则（不在任何共享文件中的规则）
- `references/` 文件的加载指令（告知子代理何时读取哪些文件）

**下沉到 references/ 的内容：**
- PRE_HOOK / POST_HOOK 详细步骤序列 → `references/hooks.md`
- 重复制执行模型完整规则 → `references/repetition.md`
- 门控条件详细定义 → `references/gates.md`
- 状态值枚举和说明 → `references/state-values.md`
- 服务启动/停止/健康检查操作 → `references/service-lifecycle.md`
- 10 轮自审流程详情 → `references/self-review.md`
- 权限声明模型 → `references/permission-model.md` (init)
- 恢复优先级链 → `references/recovery-protocol.md` (resume)
- 归档规则 → `references/archive-rules.md` (archive)

**重构后的 SKILL.md 结构：**
```markdown
---
name: kflow-code
version: 0.16.0
description: ...
triggers: ...
allowed-tools: ...
---

# Skill 名称

## 概述（3-5 行）

## 核心执行流程（ASCII 图 + 10 个步骤标题）

## 步骤说明（每步骤 1-3 行摘要 + references/ 引用）

## 输入输出产物

## 阶段特有规则

## 子代理构建指令（references/ 加载清单）
```

### 决策 3：路径引用方案

Claude Code 的 Read 工具以项目根目录解析相对路径，因此 references/ 引用需使用从根出发的完整路径：

| 环境 | 路径格式 | 示例 |
|------|---------|------|
| 开发仓库 | `skills/<skill-name>/references/<file>.md` | `skills/kflow-code/references/hooks.md` |
| 消费方项目 | `.claude/skills/<skill-name>/references/<file>.md` | `.claude/skills/kflow-code/references/hooks.md` |

`scripts/package-skills.sh` 在打包时自动将 `skills/` 前缀替换为 `.claude/skills/`。

**Alternatives considered:**
- 相对路径 (`references/hooks.md`): Read 工具解析为 `<项目根>/references/hooks.md`，无法定位到 skill 目录内。已排除。
- `glob + Read` 两步法: 先在 SKILL.md 中指示子代理 "通过 Glob 查找本 Skill 所在目录下的 references/"，再 Read。增加工具调用次数，且对子代理的要求不够直接。作为备选但非首选。

### 决策 4：版本同步机制

```
VERSION (单点真理)
    │
    ▼ scripts/sync-version.sh (手动触发)
    ├── skills/kflow-code/SKILL.md → version: 0.16.0
    ├── skills/kflow-plan/SKILL.md → version: 0.16.0
    ├── ... (全部 17 个)
    └── 读取每个 SKILL.md front matter 中的 version 行并替换
```

- 修改 `VERSION` 后手动执行 `./scripts/sync-version.sh`
- `package-skills.sh` 打包时校验：每个 SKILL.md 的 version 与 VERSION 一致，不一致则报错中止

### 决策 5：同步维护策略

- **无中央 kflow-shared 源**：规则变更时直接编辑对应 skill 的 `references/` 文件
- **多 skill 共享的规则**（如 repetition-model）：需要人工同步到所有相关 skill
- **单 skill 独有的规则**（如 recovery-protocol）：仅更新对应 skill
- **scripts/sync-references.sh**：提供校验功能，检测同一 references 文件在多个 skill 间是否一致（不自动修复，仅报告差异）

**Rationale**: 保留中央源意味着仍需维护 kflow-shared/，违背"移除共享依赖"的核心目标。参考脚本提供差异可见性，但不强制自动化同步。

## Risks / Trade-offs

| 风险 | 缓解措施 |
|------|---------|
| 多 skill 共享规则（如 repetition-model）需人工同步 | `sync-references.sh` 提供跨 skill 差异报告 |
| SKILL.md 瘦身后子代理可能不主动读取 references/ | SKILL.md 中显式加入 "MUST Read" 指令 |
| `with_server.py` 原始在 kflow-shared/scripts/，移至 kflow-code 后其他需要服务管理的 skill 引用路径变更 | 更新引用路径至 `skills/kflow-code/scripts/with_server.py`，确认所有调用方兼容 |
| references/ 目录增加 npx skills add 安装体积 | 增量约 100-500 行/skill，可忽略 |

## Migration Plan

1. 本变更在开发仓库 `skills/` 下完成所有文件重构
2. `sync-version.sh` 批量写入 version 字段
3. `sync-references.sh` 校验 references/ 一致性
4. `package-skills.sh` 打包时完成路径替换和版本校验
5. 消费方更新：`npx skills add` 重新安装各 skill（旧版 kflow-shared/ 手动删除）
6. 消费方验证：`grep '^version:' .claude/skills/kflow-guide/SKILL.md` 确认版本

## Open Questions

- 消费方项目中已存在的 `kflow-shared/` 目录是否需要自动化清理？建议在 `kflow-guide` 或 README 中提示手动删除步骤。
