# Proposal

## Why

设计四视角审查（kflow-design 的 REVIEW 步骤）是变更级最重的审查环节——4 个并行 Agent（业务/技术/安全/质量）+ 分级重审闭环。对功能缺陷级等小变更而言，这套完整审查成本过高，拖慢交付效率。同时，归档目录 `docs/archive/` 与活跃变更目录 `docs/changes/` 分离，导致 `kflow-status`/`kflow-resume` 的归档检测逻辑与文档表述（「扫描 docs/changes/ → 排除 archive/ 子目录」）存在错位。

## What Changes

- **设计审查分级（默认简化）**：设计四视角审查保持强制，但按变更类型分级——功能缺陷级走「简化模式」（单视角综合审查，单轮出报告）；功能需求级/产品需求级走「完整模式」（四视角并行 + 分级重审闭环，维持现状）。
- **归档目录迁移**：归档目录从 `docs/archive/{YYYY-MM-DD}-{change}/` 迁移到 `docs/changes/archive/{YYYY-MM-DD}-{change}/`，统一 `kflow-archive`/`kflow-status`/`kflow-resume`/`kflow-guide`/`kflow-init`/`kflow-e2e-test` 的归档路径引用与检测逻辑。

## Capabilities

### New Capabilities

- `design-review-tiering`: 设计审查分级——定义完整模式（四视角并行）与简化模式（单视角综合）的判定依据（变更类型）、产物形态与门控适配。
- `archive-directory-location`: 归档目录位置——钉死归档目录为 `docs/changes/archive/`，定义 status/resume/guide/init 的归档检测与排除规则。

### Modified Capabilities

（无。现有 `review-closed-loop` 与 `shared-archive-rules` 保持现状，仅被新能力引用。）

## Impact

- **kflow-design**：REVIEW 步骤新增「简化/完整」分支（按变更类型）。
- **kflow-archive**：归档 MOVE 步骤目标路径、输出产物表、归档检测路径。
- **kflow-status / kflow-resume / kflow-guide / kflow-init / kflow-e2e-test**：归档路径引用与排除逻辑。
- **kflow-audit**：「审查 20%」维度需按「完整/简化」分别给分，不因简化而误扣。
- **设计文档**：`02-directory-structure.md`、`08-governance.md`（归档白名单路径）、`04-gates-and-transitions.md`（进入计划门控的 cross-reviews 检查）。
- **无 API / 外部依赖变更**。
