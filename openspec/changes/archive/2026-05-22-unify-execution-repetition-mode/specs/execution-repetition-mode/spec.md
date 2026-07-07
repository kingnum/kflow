## ADDED Requirements

### Requirement: 执行类阶段统一采用重复制

7 个执行类阶段（plan/code/code-review/api-test/e2e-test/integration-test/bug-fix）的主执行工作 SHALL 统一采用重复制模式：子代理每轮遍历全部工作项独立执行完整流程，禁止按轮次分段分配工作重点，通过每轮全量遍历实现自然收敛。

#### Scenario: 编码阶段每轮遍历全部功能点

- **WHEN** 编码阶段子代理执行任意轮次迭代
- **THEN** 子代理 SHALL 遍历 tasks.md 中全部功能点
- **AND** 对每个功能点执行完整 TDD 垂直切片（评估状态 → 写/补测试 → 写/改实现 → 验证通过）
- **AND** SHALL NOT 在早期轮次仅处理"核心"功能点而将其他功能点留给后续轮次

#### Scenario: 测试阶段每轮运行全部用例

- **WHEN** 接口单元测试或 E2E 测试或集成测试阶段子代理执行任意轮次
- **THEN** 子代理 SHALL 运行全部测试用例（全部接口/全部场景/全部集成用例）
- **AND** 已通过的用例仍需重跑以验证无回归
- **AND** 失败的用例记录后进入修复流程

#### Scenario: 代码审查阶段每轮审查全部代码

- **WHEN** 代码审查阶段子代理执行任意轮次
- **THEN** 子代理 SHALL 审查全部代码变更
- **AND** 两视角（安全+规范 / 质量+性能）SHALL 每轮完整执行全部检查项

#### Scenario: 计划阶段每轮审查全部子变更

- **WHEN** 计划阶段子代理执行任意轮次
- **THEN** 子代理 SHALL 遍历全部子变更 tasks.md
- **AND** 对每个子变更执行全部 4 维度检查（任务覆盖完整性/DoD验收标准正确性/HITL标注准确性/任务粒度合理性）

#### Scenario: 缺陷修复阶段每轮遍历全部失败用例

- **WHEN** 缺陷修复阶段子代理执行任意轮次
- **THEN** 子代理 SHALL 遍历全部失败用例
- **AND** 对每个失败用例执行独立分析+修复+验证
- **AND** 单用例 3 次修复上限独立共存于内层

### Requirement: 禁止节奏指引

系统 SHALL NOT 在 prompt 中向子代理提供按轮次分段分配工作重点的节奏指引（如前 N 轮重点执行/中间 N 轮细节优化/后 N 轮验证）。禁止任何形式的"这部分留给后面轮次"的暗示。

#### Scenario: Prompt 中不含分段策略

- **WHEN** 主 Agent 构建子代理 prompt
- **THEN** prompt SHALL NOT 包含类似于「前 6 轮重点执行，后 4 轮验证和边界检查」「前 4 轮重点执行，中间 3 轮细节优化」「前 3 轮重点执行，中间 4 轮细节优化」等分段分配指令
- **AND** prompt SHALL 替换为「每轮遍历全部工作项独立执行完整流程」

#### Scenario: 节奏指引全面移除

- **WHEN** 任一执行类阶段的 SKILL.md 或设计规格中包含「复杂度评估用于生成节奏指引」的描述
- **THEN** 该描述 SHALL 被移除或替换为「复杂度评估仅信息展示，不驱动执行行为」

### Requirement: 每阶段明确定义每轮工作内容

每个执行类阶段的 SKILL.md 和设计规格 SHALL 在「执行流程」章节包含「每轮工作内容」子章节，明确定义每轮全量执行的具体工作项、流程和产物。

#### Scenario: 工作内容定义结构

- **WHEN** 编写或更新执行类阶段的每轮工作内容定义
- **THEN** 定义 SHALL 包含：
  - 遍历哪些工作项（功能点/测试用例/代码变更/子变更任务）
  - 每个工作项执行什么流程（TDD/HTTP请求/Playwright脚本/审查维度）
  - 每轮输出什么产物（traceability.md更新/test-reports轮次报告/审查报告/修复报告）
  - 轮次结束后更新轮次计数器

#### Scenario: 工作内容定义不随时间衰减

- **WHEN** 子代理读取每轮工作内容定义
- **THEN** 全部 10 轮 SHALL 使用相同的工作内容定义
- **AND** 不允许存在"第 N 轮之后可以跳过某类工作项"的豁免条款

### Requirement: Tracer Bullet 在重复制中保留

编码阶段在重复制模式下 SHALL 保持 Tracer Bullet 先行：首轮遍历全部功能点时，每个功能点的首个 RED→GREEN 循环 SHALL 是 Tracer Bullet（端到端最简路径），确保端到端路径在首轮即被打通。

#### Scenario: 首轮全量遍历时 Tracer Bullet 先行

- **WHEN** 编码子代理首轮遍历功能点
- **THEN** 对每个功能点的首个 RED→GREEN 循环 SHALL 采用 Tracer Bullet 方式（横切所有集成层、最简实现、可运行）
- **AND** 后续轮次检查 Tracer Bullet 路径是否仍然畅通（不会被新增代码破坏）

#### Scenario: Tracer Bullet 路径检查

- **WHEN** 编码子代理在后续轮次（Round 2-10）遍历已实现的功能点
- **THEN** SHALL 检查该功能点的 Tracer Bullet 路径是否仍然畅通
- **AND** 若路径被破坏 → 标记为回归并修复

### Requirement: 复杂度评估仅信息展示

复杂度评估公式（功能点数 × 1 + 接口数 × 1.5 + 场景数 × 2）和分级阈值（低 <20 / 中 20-50 / 高 >50）SHALL 保留，但仅作为信息展示写入 .status.md 备注列，不驱动子代理执行行为。

#### Scenario: 计算但不驱动行为

- **WHEN** 执行类阶段启动
- **THEN** 主 Agent SHALL 计算复杂度分
- **AND** 将复杂度分和等级写入 .status.md 备注列作为背景信息
- **AND** SHALL NOT 将分级转化为节奏指引传递给子代理

#### Scenario: 子代理 prompt 中复杂度标注

- **WHEN** 复杂度评估结果出现在子代理 prompt 中
- **THEN** 必须附带标注「仅供参考，不驱动执行行为」
- **AND** 标注后不得跟随任何按轮次分配工作的指令
