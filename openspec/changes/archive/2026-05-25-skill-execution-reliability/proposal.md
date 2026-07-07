## Why

KFlow Skills 在执行可靠性方面存在5个实际运行中发现的缺陷：编码阶段逐个子变更询问用户而非自动连续执行；新会话中进入原型设计调整时未走 `kflow-prototype-design` 编排层入口调用底层原型skill；"因...无法..."等阻塞关键词和用户纠正AI行为的内容未被自动捕获到 `skill-suggestion.md` 作为Skill改进参考；所有缺陷修复100%完成且测试通过后缺少用户访问确认环节；中断恢复（resume）时可能因仅依赖 `.status.md` 状态值而跳过未完成阶段或误判阶段已完成。这些问题影响执行效率和状态可靠性。

## What Changes

- **编码/代码审查阶段自动遍历全部子变更**：每轮重复制中遍历全部未完成子变更，每个子变更内遍历全部功能点，禁止仅处理单个子变更后等待用户确认
- **原型设计"修订模式"**：`kflow-prototype-design` 的 CHECK 步骤后增加现有原型检测，`prototype/index.html` 已存在时走修订模式分支（加载现有原型+设计约束+合并用户修订需求→委托调用底层原型skill）
- **CLAUDE.md 全局 skill-suggestion 捕获规则**：`kflow-init` 向 CLAUDE.md 注入全局规则，自动捕获三种触发模式并记录到 `docs/skill-suggestion.md`（阻塞原因/因果链/用户纠正内容）
- **集成测试通过后用户验收确认**：集成测试通过+审计通过后增加 `AskUserQuestion` 用户访问确认门控，确认通过→归档，确认不通过→回到 bug-fix 描述具体问题（非 skill-suggestion 记录）
- **中断恢复产物完整性验证**：`kflow-resume` GATE 步骤增加阶段产物强制校验（轮次计数器必须=10/10、traceability 覆盖率、产物文件存在性），不满足时拒绝认定阶段完成

## Capabilities

### New Capabilities
- `auto-subchange-traversal`: 编码/代码审查阶段自动遍历全部子变更机制
- `prototype-revision-mode`: 原型设计修订模式（加载现有原型+合并修订需求+委托调用）
- `user-acceptance-gate`: 集成测试通过后用户访问确认门控
- `resume-product-gate`: 中断恢复阶段产物完整性验证（轮次强制校验+产物文件校验）

### Modified Capabilities
- `skill-suggestion-logging`: 扩展记录触发模式，新增三种关键词/场景的自动捕获规则
- `devflow-init`: 扩展 CLAUDE.md 注入内容，新增全局 skill-suggestion 捕获规则 section

## Impact

- `docs/designs/skills/kflow-code.md` — 执行流程增加"遍历全部子变更"指令
- `docs/designs/skills/kflow-code-review.md` — 同步更新
- `docs/designs/skills/kflow-prototype-design.md` — CHECK 后增加修订模式分支
- `docs/designs/skills/kflow-init` — CLAUDE.md 注入新增 skill-suggestion 捕获规则
- `CLAUDE.md` — 新增全局规则 section
- `docs/designs/skills/kflow-integration-test.md` — 门控增加用户验收确认
- `docs/designs/skills/kflow-resume.md` — GATE 步骤增加产物完整性验证
- `docs/designs/core-mechanisms.md` — 门控规则新增产物验证条目
