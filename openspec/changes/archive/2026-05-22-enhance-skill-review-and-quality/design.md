## Context

KFlow Skills 体系经过多个变更迭代，现有 15 个已实现 Skill + 17 个设计规格。在实际使用中暴露了 5 类问题，涉及流程路由、审查产物组织、子代理隔离、设计深度和审查覆盖面。当前状态：

- **RESUME 路由**：kflow-guide 正则解析正确，但 Claude Code Plan Mode 在 Skill 触发评估前拦截会话
- **原型审查产物**：导航验证和 Playwright 验证报告散落在 `prototype/` 目录，与 `core-mechanisms.md` 定义的 `self-reviews/` 结构不一致
- **子代理隔离**：explore/prototype-design/design 的 SELFREV 已使用子代理，但缺乏「主代理不得接管」的全局强制规则
- **设计深度**：kflow-design 当前无复杂度评估机制，所有 FP 统一处理，高复杂度 FP 的模糊设计可能直接进入编码
- **设计文档结构**：detailed-design.md 为单文件，大变更时文件过长
- **plan 审查**：kflow-plan 使用单 Agent 迭代执行模式，无独立的子代理重复制 SELFREV

## Goals / Non-Goals

**Goals:**
- 确保「继续/恢复/resume + 变更名」输入 100% 路由到 kflow-resume，不被 Plan Mode 拦截
- 所有原型设计审查产物统一在 `self-reviews/prototype/` 下按子目录分类管理
- 所有使用子代理的阶段强制遵守隔离规则：主代理绝不接管子代理工作
- 详细设计阶段对高复杂度 FP 前置用户确认，消除"模糊设计"
- FP > 20 时 detailed-design.md 自动拆分为目录结构
- kflow-plan 具备与 explore/design/prototype 对齐的子代理重复制自审

**Non-Goals:**
- 不修改 Claude Code 本身的 Plan Mode 行为（仅在配置层规避）
- 不改变 SELFREV 的轮次数量（保持 10 轮）
- 不修改 VERIFY 步骤的验证逻辑，仅调整产物输出路径
- 不改变子变更划分逻辑
- 不修改已归档变更的目录结构

## Decisions

### D1: Plan Mode 绕过策略

**选择**：CLAUDE.md 指令 + kflow-guide description 提示（双重防护）
**备选**：仅修改 CLAUDE.md 或仅修改 kflow-guide
**理由**：CLAUDE.md 是 Claude Code 加载的第一优先级配置，对 Plan Mode 有约束力；kflow-guide description 作为第二层确保 Skill 匹配引擎正确触发。单层防护不可靠——CLAUDE.md 可能被 Plan Mode 绕过，Skill description 可能因优先级不够而未触发。

### D2: 审查产物路径结构

**选择**：`self-reviews/prototype/` 下按子目录分类（nav-check/、playwright-check/、cdn-crossref-check/）
**备选**：全部平铺在 self-reviews/prototype/ 下
**理由**：子目录分类避免平铺时文件名混乱（自审报告与验证报告混合），且与 core-mechanisms.md 中已有的 explore/design 子目录结构一致。

### D3: detailed-design.md 拆分阈值

**选择**：FP > 20 强制拆分
**备选**：FP > 15 或总是拆分
**理由**：与 explore 阶段分册阈值（每分册 ≤30 FP）形成梯度。20 是实践中有意义的阈值——少于 20 个 FP 的变更，单文件足以管理；超过 20 个意味着至少 3 个设计域，目录结构更合理。总是拆分会给小变更增加不必要的文件碎片。

### D4: 设计域文件存储位置

**选择**：`detailed-design/domains/{domain-name}.md`
**备选**：`detailed-design/` 下平铺 domain-{name}.md
**理由**：子目录避免详细设计根目录文件过多，domain 数量通常 ≥3，子目录更清晰。

### D5: kflow-plan SELFREV 审查维度

**选择**：定制 4 维度（任务覆盖完整性/DoD 验收标准正确性/HITL 标注准确性/任务粒度合理性）
**备选**：复用 design 的 4 维度（一致性/完备性/可行性/可测性）
**理由**：plan 阶段的产物是 tasks.md（任务清单），与 design 阶段的 detailed-design.md（设计文档）性质不同。design 维度侧重"设计是否合理"，plan 维度侧重"任务是否可执行"。定制维度更精准。

### D6: 子代理隔离规则层级

**选择**：core-mechanisms.md 全局规则 + 各 Skill SKILL.md 步骤级标注
**备选**：仅在各 Skill 中标注
**理由**：全局规则确保新增 Skill 自动继承此约束；步骤级标注确保执行时不被遗漏。两层防护。

## Risks / Trade-offs

- **[Plan Mode 仍可能拦截]** → 双重防护（CLAUDE.md + description），如仍失败则需在 Claude Code 层面解决
- **[detailed-design/ 目录与现有 detailed-design.md 迁移成本]** → 存量变更不受影响（仅新变更生效），无需迁移
- **[子代理隔离增加 Token 成本]** → 重新创建子代理比主代理接管更安全，Token 成本换正确性，可接受
- **[复杂度评估主观性]** → 提供具体判定标准（系统集成/分布式事务/非平凡算法/性能敏感/安全敏感/规则模糊），减少主观偏差
- **[plan SELFREV 增加阶段耗时]** → 10 轮子代理串行与 design SELFREV 模式一致，总耗时可控
