## 1. 编码/代码审查自动遍历全部子变更

- [x] 1.1 更新 kflow-code.md 执行流程 §执行流程 第2步"构建阶段专属提示词"：将重复制遍历指令从"遍历全部功能点"改为"遍历全部未完成编码的子变更，每个子变更内遍历全部功能点"
- [x] 1.2 更新 kflow-code.md 执行流程 §每轮工作内容：明确外层遍历子变更、内层遍历功能点的双层结构
- [x] 1.3 更新 kflow-code.md 验收结果处理：确保全部子变更遍历完成后才进入验收
- [x] 1.4 更新 kflow-code-review.md 同步修改：代码审查阶段遍历全部待审查子变更
- [x] 1.5 更新 core-mechanisms.md 执行类阶段说明：补充子变更自动遍历机制描述

## 2. 原型设计修订模式

- [x] 2.1 更新 kflow-prototype-design.md CHECK 步骤：在门控检查通过后增加"修订模式检测"逻辑（检测 prototype/index.html 是否存在）
- [x] 2.2 新增 kflow-prototype-design.md §修订模式章节：定义修订模式流程（加载现有原型+design-prompt.md+合并用户修订需求→DESIGN）
- [x] 2.3 新增 kflow-prototype-design.md §修订模式 AskUserQuestion：现有原型存在但用户无明确修订需求时询问用户
- [x] 2.4 更新 kflow-prototype-design.md §修订模式跳过 INPUT 和 OPTIMIZE：修订模式直接使用已有约束
- [x] 2.5 更新 kflow-prototype-design.md §修订模式底层 skill 可替换：检测可用原型 skill，不硬编码 huashu-design
- [x] 2.6 更新 kflow-prototype-design.md 执行流程图：在 CHECK 后增加修订模式分支

## 3. CLAUDE.md 全局 skill-suggestion 捕获规则

- [x] 3.1 更新 kflow-init 相关设计规格：增加向 CLAUDE.md 注入 `## Skill 改进建议自动捕获` section 的规则
- [x] 3.2 更新 CLAUDE.md：新增 `## Skill 改进建议自动捕获` section，定义三种触发模式（因...无法.../因...导致.../用户纠正后AI附和）和处理规则
- [x] 3.3 更新 skill-suggestion-logging spec：扩展三种新的自动捕获场景（spec 已包含，无需修改）

## 4. 集成测试通过后用户验收确认

- [x] 4.1 创建 user-acceptance-gate spec：定义用户验收确认的门控规则和 AskUserQuestion 交互（spec 已存在，内容完整）
- [x] 4.2 更新 kflow-archive.md 门控检查：增加用户验收确认状态验证（✅ 已确认 或 ⏭️ 用户跳过后才放行）
- [x] 4.3 更新 kflow-archive.md 执行流程：归档前先检查用户验收状态，未确认时启动服务+AskUserQuestion
- [x] 4.4 更新 kflow-archive.md 服务启动流程：集成测试通过后按 service-guide.md 启动服务并健康检查
- [x] 4.5 更新 core-mechanisms.md 状态值定义：新增「用户验收确认」状态行到 .status.md 模板
- [x] 4.6 更新 core-mechanisms.md 门控规则：新增归档门控第8条（用户验收确认检查）

## 5. 中断恢复产物完整性验证

- [x] 5.1 创建 resume-product-gate spec：定义阶段产物完整性验证规则和映射表（spec 已存在，内容完整）
- [x] 5.2 更新 kflow-resume.md GATE 步骤：增加"产物完整性验证"子步骤
- [x] 5.3 新增 kflow-resume.md §产物验证映射表：阶段→验证项（轮次计数器/产物文件/traceability 覆盖率）
- [x] 5.4 更新 kflow-resume.md 调度映射：验证不通过时回退到对应阶段重新执行
- [x] 5.5 更新 core-mechanisms.md 门控规则：新增产物验证条目到阶段正向门控检查

## 6. 文档一致性检查和最终验证

- [x] 6.1 检查所有修改的设计文档中引用的一致性（cross-references 指向正确的章节号）
- [x] 6.2 验证 core-mechanisms.md 中所有门控规则编号连续且正确
- [x] 6.3 运行 kflow-skills-auditor 检查变更涉及的 Skill 设计文档规范符合性
- [x] 6.4 最终检查：确认所有 spec 文件中的 ADDED/MODIFIED 操作与 proposal Capabilities 一一对应
