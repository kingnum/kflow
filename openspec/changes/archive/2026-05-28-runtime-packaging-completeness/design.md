## Context

当前 Skills 打包机制 (`scripts/package-skills.sh` 第 50 行) 仅扫描 `.claude/skills/kflow-*/` 目录，收集 17 个 Skill 的 SKILL.md 及其 references/ 目录。`kflow-shared/` 作为运行时共享文件目录也在此扫描范围内（包含 `phase-hooks.md` 和 `service-lifecycle.md`），但该目录下的 `scripts/` 子目录目前不存在。

`scripts/with_server.py` 目前位于项目根目录 `scripts/`，是一个通用的服务生命周期管理工具（端口冲突检测、健康检查、进程超时停止链、One-shot/Daemon 双模式），被 `kflow-shared/service-lifecycle.md` 引用 16+ 处，被 `kflow-shared/phase-hooks.md` 引用 4 处。

此外 `service-lifecycle.md:317` 存在对 `scripts/migrate.py` 的悬空引用（文件不存在，且是项目特定的迁移示例，不应出现在通用 Skill 中）。

## Goals / Non-Goals

**Goals:**
- `with_server.py` 随 Skills 打包分发，其他项目安装后能直接使用服务生命周期管理功能
- 引用路径统一使用 Skill 目录相对路径模式（与 `kflow-shared/phase-hooks.md` 引用一致）
- 清理悬空引用，保持通用 Skill 文档的项目无关性

**Non-Goals:**
- 不改变 Skills 打包机制整体架构
- 不实现 `migrate.py`（项目特定的迁移工具）
- 不改变 `kflow-shared/` 目录命名

## Decisions

### 1. `with_server.py` 放置位置

**Decision:** 移入 `.claude/skills/kflow-shared/scripts/with_server.py`

**Rationale:**
- `kflow-shared/` 已是运行时共享文件目录，`phase-hooks.md` 和 `service-lifecycle.md` 都在此
- 引用路径 `kflow-shared/scripts/with_server.py` 与 `kflow-shared/phase-hooks.md` 是相同的引用模式（Skill 目录相对路径）
- 打包时 `package-skills.sh` 扫描 `kflow-*/` 已包含 `kflow-shared/` 下所有内容（含 `scripts/` 子目录），无需修改打包脚本

**Alternatives considered:**
- 放在 zip 包根 `scripts/`：需要修改打包脚本，且安装后路径不一致
- 保持项目根 `scripts/`：不在打包范围内，其他项目无法使用

### 2. 引用路径更新方式

**Decision:** `service-lifecycle.md` 和 `phase-hooks.md` 中所有 `scripts/with_server.py` 引用改为 `kflow-shared/scripts/with_server.py`

**Rationale:**
- 现有 SKILL.md 引用 `kflow-shared/phase-hooks.md` 的方式就是直接用 `kflow-shared/` 前缀
- 统一引用模式，不引入特殊例外

### 3. `migrate.py` 处理

**Decision:** 删除 `service-lifecycle.md` 第七节中的 `scripts/migrate.py` 引用行（317 行），保留 Flyway 示例

**Rationale:**
- `migrate.py` 文件不存在
- 该示例是项目特定的迁移工具写法，不应出现在通用 Skill 文档中
- Flyway 示例已经足够说明迁移执行格式
- 具体项目的迁移命令由 `service-guide.md` 定义，不在通用文档中硬编码

## Risks / Trade-offs

[Risk] → 其他项目安装后，`with_server.py` 路径为 `.claude/skills/kflow-shared/scripts/with_server.py`，如果用户直接在终端执行命令，路径较长
→ Mitigation: 文档中保持引用路径清晰，用户可通过配置 PATH 或使用别名简化

[Risk] → 如果未来有更多运行时脚本需要分发，都放进 `kflow-shared/scripts/` 可能导致目录膨胀
→ Mitigation: 当前仅有 `with_server.py`，后续可根据实际情况按功能分子目录
