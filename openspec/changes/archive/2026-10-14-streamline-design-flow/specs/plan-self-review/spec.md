# Spec Delta

## MODIFIED Requirements

### Requirement: 计划阶段审查维度（定制）

kflow-plan 自审 SHALL 覆盖以下 4 个定制维度，主 Agent 的签署自证与验证子代理的验证均 SHALL 覆盖全部维度，SHALL NOT 因单轮化而减少维度或检查项。

#### Scenario: 任务覆盖完整性检查

- **WHEN** plan 自审执行任务覆盖完整性维度
- **THEN** 检查是否所有 detailed-design.md 中该子变更的功能点都有对应任务
- **AND** 覆盖率必须 = 100%
- **AND** 检查是否所有 api-tests/ 和 e2e-tests/ 中的测试用例在任务清单中有对应的测试编写步骤
- **AND** 标记缺失任务的功能点

#### Scenario: DoD 验收标准正确性检查

- **WHEN** plan 自审执行 DoD 验收标准正确性维度
- **THEN** 检查每功能点是否包含 Happy Path(≥1) + Error Path(≥2) + Edge Case(≥1) + Quality(≥1)
- **AND** 检查每条验收标准是否使用 WHEN/THEN 格式
- **AND** 检查 Happy Path 是否验证正常业务流程
- **AND** 检查 Error Path 是否覆盖至少 2 种异常场景
- **AND** 检查 Edge Case 是否覆盖边界值
- **AND** 检查 Quality 是否验证性能/安全等质量属性
- **AND** 标记格式错误或数量不足的功能点

#### Scenario: HITL 标注准确性检查

- **WHEN** plan 自审执行 HITL 标注准确性维度
- **THEN** 检查所有 HITL 子变更是否包含决策点列表
- **AND** 检查 `[HITL D{n}]` 标注是否在正确的任务位置（Step 2 或 Step 3 之间）
- **AND** 检查每个决策点是否有明确的决策内容和至少 2 个选项
- **AND** 检查默认建议是否标注
- **AND** 检查 AFK 子变更是否不包含 HITL 标注
- **AND** 标记缺失标注或位置不当的决策点

#### Scenario: 任务粒度合理性检查

- **WHEN** plan 自审执行任务粒度合理性维度
- **THEN** 检查每任务是否符合 2-5 分钟可完成的标准
- **AND** 检查 TDD 循环是否完整（Step 1-7：编写测试→RED→实现→GREEN→质量检查→重构→验证）
- **AND** 标记过粗任务（包含多个独立操作）
- **AND** 标记过细任务（实现细节级别）

### Requirement: plan 自审报告

验证子代理 SHALL 输出一份验证报告到 `self-reviews/plan/report.md`。

#### Scenario: 报告路径

- **WHEN** plan 验证子代理完成单轮验证
- **THEN** 报告保存路径为 `self-reviews/plan/report.md`
- **AND** SHALL NOT 产出按轮次编号的多份报告

#### Scenario: 报告内容

- **WHEN** 子代理完成验证
- **THEN** 报告包含 4 维度签署清单打假结果（维度名、自证结论、证据锚点、打假结论）
- **AND** 包含新发现问题清单（序号、问题描述、严重度）
- **AND** 包含范围外观察小节（为空时记「（空）」）
- **AND** 包含全量遍历证明（4 维度与全部子变更 tasks.md 均已遍历）
- **AND** 包含验证结论（终止结果取值 `验证通过` 或 `验证发现问题({N})`）

### Requirement: 边审边修规则

验证子代理 SHALL NOT 修改任何阶段产物，仅将发现的问题记入验证报告。全部发现项 SHALL 由主 Agent 在单轮验证完成后统一修复。

#### Scenario: 发现问题直接修复

- **WHEN** 验证子代理在验证过程中确认了 DoD 格式错误或任务缺失
- **THEN** 子代理 SHALL NOT 修改任何 tasks.md 文件
- **AND** SHALL 将该问题记入验证报告
- **AND** 主 Agent 在验证完成后统一修复对应子变更的 tasks.md 并生成「本阶段修复清单」
- **AND** 主 Agent SHALL 仅修复确认的问题，不做额外改进
- **AND** SHALL NOT 新增功能点任务（遵循「非必要不增加新功能」原则）

### Requirement: 计划阶段收敛驱动的子代理自审

系统 SHALL 在 kflow-plan 阶段以「主 Agent 签署自证（零子代理）→ 单轮独立子代理验证」执行 SELFREV。审查轮数 SHALL 恒为 1，SHALL NOT 执行第二轮，SHALL NOT 存在 0 轮豁免路径。验证子代理 SHALL 执行全部 4 个定制维度检查。终止结果 SHALL 为 `验证通过` 或 `验证发现问题({N})`，写入变更级 `.status.md`。签署清单结构、打假契约与终止结果的权威定义见 `signed-checklist-verification` 能力。

#### Scenario: plan SELFREV 步骤位置

- **WHEN** kflow-plan 完成所有子变更 tasks.md 初稿后
- **THEN** 在步骤 8（VERIFY）之后、步骤 9（COMPLETE）之前插入 SELFREV 步骤
- **AND** SELFREV 步骤序号为 8.5，原 COMPLETE 步骤序号顺延为 9

#### Scenario: 轻量档执行至少 1 轮自审

- **WHEN** 变更档位为 `轻量`
- **THEN** kflow-plan SHALL 执行 SELFREV 单轮验证
- **AND** SHALL NOT 跳过 SELFREV，SHALL NOT 存在 0 轮豁免路径
- **AND** 轮数 SHALL 恒为 1，SHALL NOT 执行第二轮
- **AND** 产物完整性门控 SHALL 保留为附加硬门

#### Scenario: 串行执行至收敛

- **WHEN** 验证子代理完成并返回验证报告
- **THEN** 主 Agent 读取验证报告与产物差异
- **AND** 统一修复报告确认的全部问题并生成「本阶段修复清单」
- **AND** 写入终止结果 `验证通过` 或 `验证发现问题({N})`
- **AND** SHALL NOT 启动第二轮子代理

#### Scenario: 子代理串行执行

- **WHEN** 主 Agent 完成 tasks.md 初稿
- **THEN** 主 Agent SHALL 自行完成 4 维度签署自证，SHALL NOT 为签署自证启动子代理
- **AND** 验证环节 SHALL 启动且仅启动 1 个独立子代理
- **AND** SHALL NOT 同时启动多个验证子代理

#### Scenario: 不收敛时升级用户

- **WHEN** 验证子代理意外停止、报错退出或返回不完整结果
- **THEN** 主代理 MUST 分析原因后重新创建新的子代理
- **AND** SHALL NOT 在主 Agent 上下文中接管子代理未完成的工作
- **AND** 最多重试 3 次，全部失败后标记 ⚠️ 阻塞并提示用户

### Requirement: 计划阶段审查对象冻结与范围外观察

主 Agent SHALL 从阶段产物既有内容（各子变更 tasks.md）生成审查对象集合并冻结，审查维度 SHALL 限于本阶段的 4 个定制维度；子代理 SHALL NOT 扩大审查对象集合、SHALL NOT 新增审查维度、SHALL NOT 借审查之名新增功能点或任务。冻结范围之外的发现 SHALL 记为「范围外观察」，SHALL NOT 触发产物修改、SHALL NOT 计入验证发现数，并 SHALL 写入验证报告的「范围外观察」小节。引入范围外新内容的验证轮次 SHALL NOT 被接受为有效验证，主 Agent SHALL 要求子代理在冻结范围内重新验证。主 Agent SHALL 在阶段终止时汇总范围外观察条目并向用户提示。

#### Scenario: 审查对象集合冻结

- **WHEN** 主 Agent 构建验证子代理的 prompt
- **THEN** prompt SHALL 包含由阶段产物既有内容生成的审查对象清单
- **AND** 子代理 SHALL NOT 审查该清单之外的文件或内容

#### Scenario: 审查维度封闭

- **WHEN** plan 单轮验证执行
- **THEN** 审查维度 SHALL 限于任务覆盖完整性、DoD 验收标准正确性、HITL 标注准确性、任务粒度合理性这 4 个定制维度
- **AND** 子代理 SHALL NOT 新增审查维度

#### Scenario: 范围外发现降级为范围外观察

- **WHEN** 子代理在冻结范围之外发现问题
- **THEN** SHALL NOT 修改任何阶段产物
- **AND** SHALL NOT 将该问题计入验证发现数
- **AND** SHALL 记为「范围外观察」写入验证报告的「范围外观察」小节

#### Scenario: 引入范围外新内容的轮次不得判为见证轮

- **WHEN** 子代理的新发现或修改落在冻结的审查对象集合之外
- **THEN** 该验证 SHALL NOT 被接受为有效验证
- **AND** 主 Agent SHALL 要求子代理在冻结范围内重新验证
- **AND** SHALL 将越界事实记录到 `docs/skill-suggestion.md`
