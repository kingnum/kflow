# Skills 优化建议记录

> **更新时间**: 2026-10-09

---

## 记录清单

### 记录 1

- **发现时间**: 2026-10-08
- **发现阶段**: 设计探索（`kflow-explore`）/ 归档
- **触发场景**: 核验 `skill-self-contained` 的「Zero external dependency after installation」时，发现规格中仍有外部技能格式文件的引用
- **问题描述**: `openspec/specs/adr-records/spec.md` 规定「每个 ADR SHALL 遵循 `grill-with-docs` 的 ADR-FORMAT.md 格式」。该技能未安装，全仓无承载该格式的 KFlow 自属文件，规格因此在安装布局下不可解析。同一类问题的 `CONTEXT.md` 一侧（`domain-glossary`）已由变更 `explore-clarify-convergence` 修复——改为引用 KFlow 自有的 `skills/kflow-explore/references/context-template.md`
- **改进建议**: 将 ADR 文件格式的权威收归 KFlow 自有 references（如 `kflow-design/references/adr-template.md`），并把 `adr-records` 的格式 requirement 改为指向该文件，移除对外部技能格式文件的引用
- **责任阶段**: 详细设计（`kflow-design`）/ 归档——ADR 属该阶段产物
- **状态**: 待优化（**另立变更**，不在 `explore-clarify-convergence` 范围内）
- **优先级**: 高

---

## 统计

| 状态 | 数量 |
|------|------|
| 待优化 | 1 |
| 优化中 | 0 |
| 已优化 | 0 |

---

## 使用说明

此文件用于记录 KFlow Skills 的流程指引错误反馈与优化建议，以及各阶段发现的信息不足事项。

### 记录时机

- 用户指出指引方向错误
- 用户纠正意图识别结果
- Skill 执行结果与预期不符
- 阶段越界处理：explore 阶段发现信息不足以完成功能设计时，除在产物中标记 `待补充`（含降级理由与责任阶段）外，同步记录到本文件
