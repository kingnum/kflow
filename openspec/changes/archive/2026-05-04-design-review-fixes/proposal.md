# 设计评审修正：Skills 体系设计 v1.5.0 → v1.6.0

## Why

v1.5.0 设计评审发现了 18 个问题：文件名引用不一致会导致实现出错、集成测试和接口单元测试缺少独立 Skill 入口、kflow-code 职责过载导致边界模糊、kflow-bug-fix 两级路由存在上下文检测歧义、checkpoint 无过期清理、阶段数量描述与实际不符等。这些问题必须在进入大规模 Skill 实现前修正，否则技术债务会快速累积。

## What Changes

- 统一文件命名：`functional-design.md`（功能设计）/ `detailed-design.md`（详细设计），全局修复 `design.md` 和 `functional-detailed-design.md` 笔误
- 新增 `kflow-integration-test` Skill（变更级），集成测试执行 + 四分法缺陷修复内聚一体
- 拆分 `kflow-code`：提取 `kflow-code-review` 为独立 Skill（两视角并行代码审查），TDD 编码保留在 `kflow-code`
- `kflow-bug-fix` 简化为仅子变更级（三分法），变更级修复内聚到 `kflow-integration-test`
- 变更级服务刷新同步点：所有子变更编码完成后、测试开始前，由上层 Agent 统一执行编译-迁移-重启-健康检查
- 连续 3 轮同一用例失败自动触发架构评估：自动分析 + 多方案输出 + 用户决策
- checkpoint 两级化：变更级操作（design/integration-test/archive）留在变更级，子变更级操作（plan/code/review/test）迁移到 `subchanges/{subchange}/checkpoints/`
- 阶段数量修正：前后端 9 阶段 / 纯后端 7 阶段（从 7/5 修正）
- 意图识别增加优先级规则
- 版本号同步、DoD 基准可配置标注、设计合并冲突裁决标准、回退后重审范围、并行编码共享文件冲突预防

## Capabilities

### New Capabilities

- `integration-test-skill`: 独立的集成测试 Skill，执行变更级集成测试，内聚四分法缺陷修复循环，含架构评估自动触发
- `code-review-skill`: 独立的代码审查 Skill，两视角并行审查（安全+规范、质量+性能），含审查闭环验证
- `service-refresh-gate`: 变更级服务编译刷新同步点，所有子变更编码完成后统一编译、迁移执行、服务重启、健康检查
- `two-level-checkpoint`: checkpoint 两级存储结构，变更级操作和子变更级操作分开保存，恢复时按归属查找
- `architecture-auto-assessment`: 连续 3 轮同一用例失败自动触发架构评估，输出多方案分析报告供用户决策
- `intent-priority-rules`: 关键词意图识别优先级规则，解决多关键词同时命中时的歧义

### Modified Capabilities

- `code-review-phase`: 由 kflow-code 子阶段提升为独立 `kflow-code-review` Skill，门控规则从编码内子门控变为独立阶段门控
- `defect-root-cause`: `kflow-bug-fix` 移除变更级四分法（合并到 `kflow-integration-test`），仅保留子变更级三分法，上下文检测不再需要
- `integration-testing`: 从无 Skill 的阶段描述变为有独立 Skill 的正式阶段，产物和流程标准化
- `devflow-guide`: 阶段数量从 7+1/5+1 修正为 9/7，意图识别增加优先级映射
- `devflow-archive`: 归档前门控增加变更级服务刷新标记检查

## Impact

- 设计文档目录：`docs/designs/index.md`, `docs/designs/overview.md`, `docs/designs/core-mechanisms.md`
- Skill 设计文档：新增 `skills/kflow-integration-test.md`, `skills/kflow-code-review.md`；修改 `skills/kflow-code.md`, `skills/kflow-bug-fix.md`, `skills/kflow-guide.md`, `skills/kflow-plan.md`, `skills/kflow-e2e-qa.md`, `skills/kflow-design.md`, `skills/kflow-archive.md`, `skills/kflow-audit.md`, `skills/kflow-prototype-design.md`, `skills/index.md`
- 示例文档：`examples/change-status.md`, `examples/rollback-status.md`
- 后续实现阶段需重写 `.claude/skills/` 下的 `kflow-code.md`, `kflow-bug-fix.md`，并新建 `kflow-code-review.md`, `kflow-integration-test.md`
