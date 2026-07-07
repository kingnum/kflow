## 1. CONTEXT.md 领域词汇表基础设施

- [x] 1.1 修改 `docs/designs/skills/kflow-init.md`：增加 CONTEXT.md 存在性检测步骤，存在时加载词汇表，不存在时标记"待构建"
- [x] 1.2 修改 `docs/designs/skills/kflow-explore.md`：在 CLARIFY 步骤增加 CONTEXT.md 首次构建和增补流程，含术语提炼、对齐检查、修订记录
- [x] 1.3 修改 `docs/designs/skills/kflow-design.md`：在四视角审查内容中增加"术语一致性"检查项（设计文档实体名称是否对齐 CONTEXT.md）
- [x] 1.4 修改 `docs/designs/skills/kflow-code.md`：在编码规范中增加"命名对齐 CONTEXT.md 词汇"约束
- [x] 1.5 修改 `docs/designs/skills/kflow-code-review.md`：在审查检查项中增加"代码命名是否与 CONTEXT.md 冲突"
- [x] 1.6 修改 `docs/designs/core-mechanisms.md`：在项目级文件清单中增加 CONTEXT.md 定义

## 2. ADR 架构决策记录机制

- [x] 2.1 修改 `docs/designs/skills/kflow-design.md`：在详细设计流程中增加 ADR 创建步骤（位于 ARCH 步骤后），含三条件过滤、每变更上限、过期条件
- [x] 2.2 修改 `docs/designs/skills/kflow-design.md`：在输出产物中增加 ADR 文件（条件输出），注明 ADR 格式规范
- [x] 2.3 修改 `docs/designs/core-mechanisms.md`：在门控规则中增加 ADR 相关规则（三条件触发、上限控制、过期条件、序号管理）
- [x] 2.4 修改 `docs/designs/skills/kflow-archive.md`：在归档步骤中增加 ADR 索引更新检查（如有新增 ADR）

## 3. kflow-bug-fix 增强（diagnose 方法论）

- [x] 3.1 修改 `docs/designs/skills/kflow-bug-fix.md`：重构 DISCOVER 步骤，增加三个子步骤——BUILD LOOP（10 种方法优先级排序，自动化优先）、REPRODUCE（确认失败模式一致、多轮复现）、HYPOTHESISE（3-5 个可证伪假设，展示给用户）
- [x] 3.2 修改 `docs/designs/skills/kflow-bug-fix.md`：增加非确定性缺陷复现率提升策略
- [x] 3.3 修改 `docs/designs/skills/kflow-bug-fix.md`：增加 regression test at correct seam 评估步骤（seam 正确性评估、无正确 seam 时标记为发现）
- [x] 3.4 修改 `docs/designs/skills/kflow-bug-fix.md`：在 REPORT 步骤后增加 post-mortem 检查点（"什么可以防止此缺陷"、架构改进建议传递到 audit、调试日志清理确认、正确假设记录）
- [x] 3.5 修改 `docs/designs/skills/kflow-bug-fix.md`：在 ralph-loop 执行模式中整合新增步骤

## 4. kflow-code TDD 哲学增强

- [x] 4.1 修改 `docs/designs/skills/kflow-code.md`：在 TDD 循环章节前增加核心原则说明（测试行为而非实现、好测试 vs 坏测试定义）
- [x] 4.2 修改 `docs/designs/skills/kflow-code.md`：增加水平切片反模式警告（禁止一次写所有测试），增加 vertical slice / tracer bullet 正确模式说明
- [x] 4.3 修改 `docs/designs/skills/kflow-code.md`：增加 TDD 每周期检查清单（RED 阶段 3 项、GREEN 阶段 3 项、REFACTOR 阶段 4 项）
- [x] 4.4 修改 `docs/designs/skills/kflow-code.md`：REFACTOR 步骤增加"深化模块"说明（小接口 + 深实现 = 高 leverage）

## 5. HITL/AFK 子变更分类

- [x] 5.1 修改 `docs/designs/skills/kflow-design.md`：在子变更划分结果表格中增加"执行类型"列（AFK/HITL）
- [x] 5.2 修改 `docs/designs/skills/kflow-design.md`：在子变更划分规则中增加 HITL/AFK 判定标准和决策点说明要求
- [x] 5.3 修改 `docs/designs/skills/kflow-code.md`：在多 Agent 并行编码策略中增加 AFK 并行 / HITL 顺序执行规则
- [x] 5.4 修改 `docs/designs/skills/kflow-plan.md`：在任务清单中增加 HITL 子变更的决策点标注

## 6. kflow-audit 增强

- [x] 6.1 修改 `docs/designs/skills/kflow-audit.md`：在评估维度中增加 post-mortem 汇总评估（读取所有子变更 fix-report 的关联建议，汇总架构改进机会）
