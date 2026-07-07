## Why

当前 `package-skills.sh` 仅扫描 `.claude/skills/kflow-*/` 目录，遗漏了 `scripts/with_server.py` 等运行时脚本。`kflow-shared/service-lifecycle.md` 和 `phase-hooks.md` 中有 20+ 处引用 `scripts/with_server.py`，但解压到其他项目后该文件缺失，导致服务生命周期管理功能不可用。同时 `service-lifecycle.md` 中存在对不存在的 `scripts/migrate.py` 的悬空引用。

## What Changes

- 将 `scripts/with_server.py` 移入 `.claude/skills/kflow-shared/scripts/with_server.py`，与 `kflow-shared/phase-hooks.md` 处于同一引用模式
- 更新 `service-lifecycle.md` 和 `phase-hooks.md` 中所有 `scripts/with_server.py` 引用为 `kflow-shared/scripts/with_server.py`
- 删除 `service-lifecycle.md` 中对不存在的 `scripts/migrate.py` 的悬空引用

> 注：打包脚本 `package-skills.sh` 无需修改，其 `for skill_dir in .claude/skills/kflow-*/` 已覆盖 `kflow-shared/` 下所有内容（含新增 `scripts/` 子目录）。

## Capabilities

### New Capabilities

无新增能力。

### Modified Capabilities

- `skill-packaging`: 扩展打包范围，将 `kflow-shared/scripts/` 目录纳入 zip 包，确保运行时脚本随 Skills 一起分发

## Impact

- `scripts/with_server.py` — 从项目根 scripts/ 移至 `.claude/skills/kflow-shared/scripts/`
- `.claude/skills/kflow-shared/service-lifecycle.md` — 更新 16 处引用路径，删除 migrate.py 引用
- `.claude/skills/kflow-shared/phase-hooks.md` — 更新 4 处引用路径（共 20+ 处引用更新）
- `scripts/package-skills.sh` — 无需修改（已扫描 `kflow-*/` 包含 `kflow-shared/` 下所有内容）
- 目标项目安装步骤不变，仍为解压到 `.claude/skills/` 目录
