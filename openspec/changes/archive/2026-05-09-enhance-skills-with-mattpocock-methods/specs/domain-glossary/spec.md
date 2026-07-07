## ADDED Requirements

### Requirement: CONTEXT.md 存在性检测

系统 SHALL 在 kflow-init 阶段检测项目根目录 `CONTEXT.md` 文件是否存在，不存在时标记为"待构建"。

#### Scenario: CONTEXT.md 已存在

- **WHEN** kflow-init 执行时检测到 `CONTEXT.md` 存在
- **THEN** 系统 SHALL 读取并加载领域词汇表
- **AND** 在 toolchain.md 或初始化输出中标注"CONTEXT.md 已就绪"

#### Scenario: CONTEXT.md 不存在

- **WHEN** kflow-init 执行时检测到 `CONTEXT.md` 不存在
- **THEN** 系统 SHALL 在初始化输出中标注"CONTEXT.md 待构建"
- **AND** kflow-explore 启动时将自动触发 CONTEXT.md 初始化流程

### Requirement: CONTEXT.md 构建和增补

系统 SHALL 在 kflow-explore 阶段构建和增补 `CONTEXT.md` 领域词汇表，作为项目级唯一真实来源。

#### Scenario: 首次构建 CONTEXT.md

- **WHEN** kflow-explore 执行且 `CONTEXT.md` 不存在
- **THEN** 系统 SHALL 在 CLARIFY 步骤中创建 `CONTEXT.md`
- **AND** 从用户需求描述中提炼初始领域术语
- **AND** 每个术语 SHALL 包含：定义、别名（代码中出现的变体名）、边界（明确什么不是这个概念）

#### Scenario: 增补新术语

- **WHEN** kflow-explore 执行且 `CONTEXT.md` 已存在
- **THEN** 系统 SHALL 在 CLARIFY 步骤中检查是否有新术语需要添加
- **AND** 如果用户使用模糊或过载术语，SHALL 提议精确术语并写入 `CONTEXT.md`
- **AND** 增补完成后 SHALL 更新 `CONTEXT.md` 的修订记录

### Requirement: 领域词汇表消费

所有 KFlow Skills SHALL 在涉及领域概念时引用 `CONTEXT.md` 中的术语而非自行定义。

#### Scenario: 设计阶段引用领域词汇

- **WHEN** kflow-design 执行四视角审查
- **THEN** 审查报告 SHALL 使用 `CONTEXT.md` 中定义的术语
- **AND** 设计文档中的实体名称 SHALL 对齐 `CONTEXT.md` 词汇

#### Scenario: 编码阶段引用领域词汇

- **WHEN** kflow-code 执行 TDD 编码
- **THEN** 代码中的模块/类/函数命名 SHALL 对齐 `CONTEXT.md` 词汇
- **AND** 测试用例描述 SHALL 使用 `CONTEXT.md` 术语描述行为

#### Scenario: 代码审查阶段引用领域词汇

- **WHEN** kflow-code-review 执行
- **THEN** 审查报告 SHALL 使用 `CONTEXT.md` 术语
- **AND** 如果代码命名与 `CONTEXT.md` 冲突，SHALL 标记为问题

### Requirement: CONTEXT.md 格式

`CONTEXT.md` SHALL 遵循 grill-with-docs 的 CONTEXT-FORMAT.md 格式定义。

#### Scenario: CONTEXT.md 文件结构

- **WHEN** `CONTEXT.md` 被创建或读取
- **THEN** 文件 SHALL 包含以下结构：项目名标题、领域术语列表（每个含定义/别名/边界）、修订记录
- **AND** 禁止耦合实现细节，仅包含领域专家能理解的术语
