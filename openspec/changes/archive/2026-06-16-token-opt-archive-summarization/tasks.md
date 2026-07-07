## 1. 摘要生成规范

- [x] 1.1 定义 `module-summary.md` 格式——模块名 + 核心功能 + FP-ID 范围 + 文档位置表格
- [x] 1.2 定义摘要生成时机——归档设计合并完成后自动更新

## 2. kflow-archive 修改

- [x] 2.1 `.claude/skills/kflow-archive/SKILL.md` 执行流程中添加摘要生成步骤（设计合并后）
- [x] 2.2 `docs/designs/skills/kflow-archive.md` 设计文档同步

## 3. RELOAD 清单更新

- [x] 3.1 `kflow-shared/phase-hooks.md` RELOAD 清单——explore/design/plan 阶段新增 `module-summary.md` 为可选加载项
- [x] 3.2 `09-phase-hooks.md` 设计文档同步

## 4. 验证

- [x] 4.1 确认 kflow-archive SKILL.md 包含摘要生成步骤
- [x] 4.2 确认 phase-hooks.md RELOAD 清单包含 module-summary.md
