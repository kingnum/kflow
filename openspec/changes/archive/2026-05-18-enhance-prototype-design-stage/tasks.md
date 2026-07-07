## 1. 更新设计规格文档

- [x] 1.1 在 `docs/designs/skills/kflow-prototype-design.md` 的执行流程中新增 OPTIMIZE 步骤（插入在 INPUT 和 DESIGN 之间），更新流程编号和流程图
- [x] 1.2 更新输出产物表：`prototype/index.html`（单文件）→ `prototype/` 目录（多文件，`index.html` 为入口）
- [x] 1.3 新增「步骤 X：OPTIMIZE — 提示词优化与用户确认」章节，包含：菜单树提取、页面元素穷举（按钮/表单/数据展示区/弹窗）、业务流程脚本编写、硬约束注入、AskUserQuestion 确认交互
- [x] 1.4 更新「步骤 3：INPUT — 组装 Prompt 上下文」章节，标注其产出为 OPTIMIZE 步骤的输入基础（机械提取层）
- [x] 1.5 更新「步骤 4：DESIGN」章节，明确 prompt 须来自 OPTIMIZE 产出而非直接来自 INPUT
- [x] 1.6 更新「步骤 5：VERIFY」章节，新增离线自包含检查（CDN 扫描）、多文件交叉引用完整性检查
- [x] 1.7 在阶段边界约束中新增离线自包含约束和业务流程驱动约束

## 2. 更新运行时 Skill 定义

- [x] 2.1 在 `.claude/skills/kflow-prototype-design/SKILL.md` 的「任务」摘要和总流程图中插入 OPTIMIZE 步骤
- [x] 2.2 新增「步骤 3.5：OPTIMIZE — 提示词优化与用户确认」完整章节，包含：
  - 菜单树提取规则（一级/二级/三级菜单 → 对应页面 → 导航模式 → 全局组件）
  - 页面元素穷举规则（布局分区、操作清单、按钮清单、表单清单含字段/类型/校验/默认值、数据展示区、状态覆盖、弹窗/抽屉）
  - 业务流程脚本编写规则（逐步路径描述，端到端用户旅程）
  - 硬约束注入清单（多文件目录、flow demo 模式、离线自包含）
  - AskUserQuestion 确认交互流程
- [x] 2.3 更新输出产物定义：单文件 `index.html` → `prototype/` 目录多文件架构，增加文件结构示例
- [x] 2.4 更新 DESIGN 步骤：明确 prompt 来源为 OPTIMIZE 产出，增加 flow demo 模式强制要求
- [x] 2.5 更新 VERIFY 步骤：增加多文件交叉引用检查、CDN 外部依赖扫描（grep `http://` / `https://`）、业务流程走通验证
- [x] 2.6 更新「核心提醒」章节，增加 OPTIMIZE 步骤、离线约束、业务流程驱动的提醒项

## 3. 验证与审查

- [x] 3.1 用 `kflow-skills-auditor` 审查更新后的 `kflow-prototype-design` SKILL.md，确保 name/description 格式、中英混合触发、Token 效率等符合规范
- [x] 3.2 对照 `docs/designs/skills/kflow-prototype-design.md` 检查 SKILL.md，确保两者内容一致（规格与实现对齐）
