## Context

KFlow Skills 体系当前无发布分发机制。17 个 `kflow-*` Skills 各自维护独立版本号（`1.0.0` ~ `3.0.0`），无打包输出，无法安装到目标项目。本仓库自身也缺少变更归档后的自动打包和版本管理流程。

目标项目安装场景：拿到 `kflow-devflow-skills-x.x.x.zip` → 解压到 `.claude/skills/` → 运行 `/kflow-init` 初始化。

## Goals / Non-Goals

**Goals:**
- 统一版本号管理：`VERSION` 文件（`x.x.x`），16 个 Skills 移除独立 `version:` 字段
- 归档时自动打包：`/opsx:archive` 完成后扫描 `kflow-*`（排除 `kflow-skills-auditor`），生成 `targets/kflow-devflow-skills-x.x.x.zip`
- 版本自增判定：Major 手动 / Minor 新功能 / Patch 修复
- 打包产物纳入 git commit

**Non-Goals:**
- 不在本次调整目标项目的 git commit 行为（kflow-archive 的 commit 逻辑不变）
- 不改变 kflow-skills-auditor 的独立地位（不纳入打包）
- 不建立远程 registry 或发布渠道
- 不修改 openspec-* 等外部 Skills

## Decisions

### 1. VERSION 文件格式

选择：仓库根目录纯文本文件，内容为三段式版本号（如 `0.0.1`）。

理由：简单、无依赖、易于脚本和 AI 读取。无需 JSON/YAML 格式，单一字符串足够。

### 2. 版本自增判定逻辑

```
判定流程:
1. 读取当前 VERSION → 解析 major.minor.patch
2. 读取归档变更的 proposal.md 和 design.md
3. 按规则判定:
   ├── 新增 Skill / 新增阶段 / 核心机制变更 → minor +1, patch 归零
   ├── Bug修复 / 文档更新 / 重构 / references 变更 → patch +1
   └── 不确定 → 默认 patch +1，提示用户复核
4. Major 版本变更 → 询问用户确认
5. 输出新版本号
```

后续可从 proposal.md 中提取变更类型关键词辅助判定归属，减少 AI 判断偏差。

### 3. SKILL.md 版本号处理

选择：直接移除各 SKILL.md 的 `version:` 字段。

理由：统一版本后独立版本号无意义，保留会造成混淆。Skill 的 frontmatter 中 `version` 字段全部删除，版本信息由 VERSION 文件统一表达。

备选：改为引用 `version: "see VERSION"` → 不采用，增加维护负担且无实际作用。

### 4. 打包结构

```
targets/kflow-devflow-skills-x.x.x.zip
└── kflow-devflow-skills-x.x.x/
    ├── VERSION.txt             ← 含版本号 + 构建时间 + 归档变更名
    ├── kflow-guide/SKILL.md
    ├── kflow-explore/SKILL.md + references/
    ├── kflow-init/SKILL.md + references/
    ├── kflow-design/SKILL.md + references/
    ├── kflow-code/SKILL.md + references/
    ├── kflow-bug-fix/SKILL.md + references/
    ├── kflow-prototype-design/SKILL.md
    ├── kflow-plan/SKILL.md
    ├── kflow-code-review/SKILL.md
    ├── kflow-api-test/SKILL.md
    ├── kflow-e2e-test/SKILL.md
    ├── kflow-integration-test/SKILL.md
    ├── kflow-audit/SKILL.md
    ├── kflow-archive/SKILL.md
    ├── kflow-status/SKILL.md
    └── kflow-resume/SKILL.md
```

排除名单：`kflow-skills-auditor`、所有 `openspec-*`、`skill-creator`、`huashu-design`、`frontend-design`、`ui-ux-pro-max`。

### 5. 打包触发时机

触发点：`/opsx:archive` 完成归档后，在 git commit 之前执行打包。

```
/opsx:archive 完成
    → 读取 VERSION，判定新版本号
    → 更新 VERSION 文件
    → 扫描 .claude/skills/kflow-*（排除 kflow-skills-auditor）
    → 生成 VERSION.txt
    → 打包为 targets/kflow-devflow-skills-x.x.x.zip
    → git add targets/ VERSION（连同归档产物一起）
    → git commit
```

### 6. 跨平台 zip 命令

- Windows: `Compress-Archive -Path ... -DestinationPath ...`（PowerShell）
- Linux/macOS: `zip -r ...` 或 `tar -czf ...`

优先使用 tar（更通用），zip 作为备选。在 Windows 上需检测 Git Bash 自带 tar 是否可用。

## Risks / Trade-offs

- **版本判定不准确**: AI 分析变更性质可能误判 Minor/Patch → 默认 patch，Major 必须用户确认，降低误判影响
- **zip 工具不可用**: Windows 环境可能缺少 Compress-Archive 权限或 tar → 检测可用工具，均不可用时提示手动安装
- **历史 zip 累积**: targets/ 目录随归档增多会累积多个版本包 → 保留所有版本便于回溯，必要时可手动清理旧版
