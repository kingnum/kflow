# Tasks

## 1. 档位公式计量口径

- [x] 1.1 修改 `skills/kflow-design/SKILL.md` 的 TIER_RECHECK：将接口数定义为新增/修改的接口契约数、数据模型变更数定义为 schema/migration 数，并声明受影响但未改契约的接口不计入；验证：TIER_RECHECK 节包含三项计量口径
- [x] 1.2 修改 `skills/kflow-explore/SKILL.md` 的 TIER 初判说明，明确初判仍按功能点数，完整公式复核使用设计面口径；验证：初判映射表与说明不引入接口/数据模型定义
- [x] 1.3 修改 `skills/kflow-design/SKILL.md` 的核心提醒，补充“设计面分数与影响面清单分离”；验证：核心提醒包含该条
- [x] 1.4 更新 `references-src/state-values.md` 的档位行为差异表与计量口径；验证：权威源包含设计面口径

## 2. 硬升档与软升档

- [x] 2.1 修改 `skills/kflow-design/SKILL.md` 步骤 9.5b：定义硬升档触发条件（数据迁移、破坏性契约变更、跨变更契约影响）与软升档触发条件；验证：9.5b 表包含硬/软两类
- [x] 2.2 实现升档必要性判定：仅当升档会新增下游测试阶段或属于硬升档时提示；验证：SKILL.md 包含“无必要升档时不提示”的分支
- [x] 2.3 实现软升档默认保持轻量与用户拒绝规则：拒绝后写入 `.status.md` 理由且不重复提示；验证：SKILL.md 包含拒绝后的状态写入说明
- [x] 2.4 更新 `references-src/gates.md` 中的升档门控描述；验证：权威源包含硬/软升档分支

## 3. 轻量档两个子变更

- [x] 3.1 修改 `skills/kflow-design/SKILL.md` 的 DIVIDE 轻量档分支：允许 1 或 2 个子变更，类型混合时产出后端子变更 + 前端子变更，不再升档；验证：DIVIDE 分支包含两种子变更数量
- [x] 3.2 实现最小划分表：子变更名称、类型、包含功能点、实现顺序、依赖说明，前端标注依赖 API 契约；验证：SKILL.md 包含最小划分表字段
- [x] 3.3 实现“超过两个子变更或单个子变更 FP > 10 时升档为标准”的边界；验证：SKILL.md 包含该边界条件
- [x] 3.4 修改 `skills/kflow-design/SKILL.md` 的 FP 类型混合升档段落，删除强制升档表述，改为拆分两个子变更；验证：SKILL.md 中不再存在“FP 类型混合 → 强制升档”的规则
- [x] 3.5 更新 `references-src/gates.md` 与 `references-src/phase-transition.md` 中的子变更数量约束；验证：权威源与 SKILL.md 一致

## 4. 设计文档与三档残留清理

- [x] 4.1 修正 `docs/designs/skills/kflow-design.md` 中 `4~15 → 标准 / >15 → 完整` 的残留，改为二档口径与设计面分数；验证：该文件不再包含三档阈值
- [x] 4.2 清理 `openspec/specs/change-tier-classification/spec.md` 中的三档残留场景（中分映射标准档、高分映射完整档），保留历史 `完整` 读取归并；验证：spec 中不再出现 `4~15` 或 `>15 → 完整`
- [x] 4.3 更新 `docs/designs/core-mechanisms/03-status-and-tasks.md` §3.1.1、`04-gates-and-transitions.md`、`07-agent-model.md` 的档位描述；验证：三份文档与二档口径一致
- [x] 4.4 更新 `docs/designs/index.md` 与 `docs/designs/overview.md` 的档位机制表；验证：两处均描述设计面口径与两子变更规则

## 5. 共享 references 与运行时同步

- [x] 5.1 运行 `python scripts/gen-slice-manifest.py` 刷新切片清单，再运行 `bash scripts/sync-references.sh` 生成并校验各 skill 副本；验证：脚本退出码为 0 且无漂移告警
- [x] 5.2 执行“设计文档 → SKILL.md 同步”：将 4.1~4.4 的设计规格同步到 `.claude/skills/` 中对应的 SKILL.md；验证：差异比对无遗漏章节
- [x] 5.3 运行 `python scripts/validate-frontmatter.py` 与 `openspec validate relax-defect-tier-upgrades --strict`；验证：两者均通过

## 6. 集成场景验证

- [x] 6.1 构造“1 个 FP + 3 个受影响接口 + 0 个契约变更”的缺陷变更，验证设计面分数为 1、维持轻量、不弹升档；定向验证覆盖 3 个接口
- [x] 6.2 构造“1 个 FP + 1 个契约变更”的缺陷变更，验证设计面分数为 2.5、维持轻量（未超过 3）
- [x] 6.3 构造“1 个 FP + 1 个契约变更 + 1 个 schema 变更”的缺陷变更，验证设计面分数为 4.5、触发硬升档且不可拒绝
- [x] 6.4 构造“后端 FP + 前端 FP”的轻量变更，验证产出 2 个子变更、不升档、最小划分表字段齐全
- [x] 6.5 构造“后端子变更 FP > 10”的轻量变更，验证升档为标准并执行完整划分
- [x] 6.6 构造“软升档”场景并选择保持轻量，验证 `.status.md` 记录理由且后续阶段不重复提示
