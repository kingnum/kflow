## Why

当前 KFlow Skills 体系缺少发布分发机制——17 个 Skills 各自维护独立版本号（1.0.0 ~ 3.0.0），没有打包输出，无法安装到目标项目。同时本仓库自身也缺少变更归档后的自动打包和版本管理流程。

## What Changes

- **BREAKING**: 16 个 kflow-* SKILL.md 移除独立 `version:` 字段，统一由仓库根目录 `VERSION` 文件管理
- 新增 `VERSION` 文件，初始版本 `0.0.1`，采用三段式语义化版本号
- 新增版本自增逻辑：Major 由用户手动决定，Minor（新 Skill/新阶段/核心机制变更），Patch（Bug修复/文档更新/重构）
- 新增 `targets/` 目录，每次 `/opsx:archive` 归档完成后自动打包运行时 Skills 为 `kflow-devflow-skills-x.x.x.zip`
- 打包范围：16 个 `kflow-*` Skills（排除 `kflow-skills-auditor`），包含 SKILL.md 及 references/ 全部文件
- 新增 CLAUDE.md 规则：`/opsx:archive` → 版本自增判定 → 打包 → git commit

## Capabilities

### New Capabilities

- `skill-packaging`: 归档后自动打包——扫描 16 个 kflow-* Skills（排除 kflow-skills-auditor），生成结构化 zip 包到 targets/ 目录，含 VERSION.txt
- `unified-version`: 统一版本号管理——VERSION 文件（三段式 x.x.x），版本自增判定逻辑（Major 手动 / Minor 新功能 / Patch 修复），各 SKILL.md 移除独立 version 字段

### Modified Capabilities

（本次无修改——git commit 相关规则调整已延后）

## Impact

- 受影响的文件: `VERSION`（新增）、`targets/`（新增）、16 个 `SKILL.md`（移除 version 字段）、`CLAUDE.md`（新增打包规则）
- 受影响的流程: `/opsx:archive` 完成后新增 PAK 步骤
- 依赖: 需要 zip 命令行工具（Windows: `Compress-Archive` 或 tar）
