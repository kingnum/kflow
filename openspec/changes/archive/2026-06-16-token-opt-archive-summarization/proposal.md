## Why

当一个产品经历 5+ 次变更后，`functional-designs/` 目录持续膨胀（每次归档合并都追加功能设计内容）。后续变更的 RELOAD 清单要求加载 `functional-designs/index.md` 和相关 part-NN.md 文件，总量随变更次数线性增长。到第 5+ 个变更时，单次 RELOAD 可能加载 20+ 个功能模块文档，显著增加上下文压力。

## What Changes

- 归档阶段新增「产品级摘要生成」步骤：每次归档合并后，为每个功能模块生成 2-3 行摘要（模块名 + 核心功能 + FP-ID 范围）
- 摘要存储位置：`docs/designs/functional-designs/module-summary.md`
- 后续变更的 RELOAD 优先加载 `module-summary.md` 而非全部功能模块文档
- 仅当子变更直接涉及某模块时才加载该模块全文
- 修改 kflow-archive 设计文档和 SKILL.md，新增摘要生成步骤
- 修改 phase-hooks.md RELOAD 清单，explore/design/plan 等阶段新增 `module-summary.md` 为可选加载项

## Capabilities

### New Capabilities
- `archive-product-summary`: 归档后产品级功能摘要生成——定义摘要格式、生成规则、存储位置、RELOAD 引用策略

### Modified Capabilities
- `devflow-archive`: 归档阶段新增摘要生成步骤
- `phase-file-reload`: RELOAD 清单新增 module-summary.md 可选加载项

## Impact

- **kflow-archive SKILL.md**: 新增摘要生成步骤
- **kflow-archive 设计文档**: 同步更新
- **kflow-shared/phase-hooks.md**: RELOAD 清单更新
- **核心机制文档 09-phase-hooks.md**: 设计文档同步
- 预估收益：第 5+ 次变更时 RELOAD 上下文量级降低 50%+
