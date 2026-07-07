## 1. 设计文档更新

- [x] 1.1 更新 `docs/designs/skills/kflow-prototype-design.md`：DESIGN 步骤改为子代理委托调用（Agent + design-prompt.md），VERIFY 步骤新增 6.3 导航合理性验证（5 轮子代理串行）+ 6.4 Playwright 验证升级为 5 轮全覆盖（每轮全 5 项），OPTIMIZE 步骤新增 4.5 design-prompt.md 文件输出（7 章节模板），SELFREV 从分工制改为重复制（每轮全 4 维度），版本号升级
- [x] 1.2 更新 `docs/designs/skills/kflow-explore.md`：OUTPUT 步骤中"三、页面导航结构图"替换为"三、功能结构树"（树状图+FP-ID+优先级+简述），SELFREV 从分工制改为重复制（每轮全 4 维度），版本号升级
- [x] 1.3 更新 `docs/designs/core-mechanisms.md`：SELFREV 章节的轮次分配规则从分工制更新为重复制（仅 explore 和 prototype，design 保持分工制），新增 VERIFY 子代理验证机制说明

## 2. 技能实现更新

- [x] 2.1 更新 `.claude/skills/kflow-prototype-design/SKILL.md`：DESIGN 步骤改为 `Agent(subagent_type="claude")` 子代理调用，子代理 prompt 指令为"读取 prototype/design-prompt.md → 调用 Skill('huashu-design')"，VERIFY 步骤重构（6.1 CDN + 6.2 交叉引用 + 6.3 导航验证 5 轮子代理串行 + 6.4 Playwright 5 轮子代理串行），OPTIMIZE 步骤新增输出 design-prompt.md 并用户确认，SELFREV 改为重复制，版本号升级至 2.2.0
- [x] 2.2 更新 `.claude/skills/kflow-explore/SKILL.md`：OUTPUT 步骤新增生成"三、功能结构树"（替换原"三、页面导航结构图"），SELFREV 改为重复制，版本号升级至 2.1.0

## 3. 模板更新

- [x] 3.1 更新 `docs/designs/templates/changes/{change}/functional-designs/index.md`：将"三、页面导航结构图"模板替换为"三、功能结构树"模板（树状图格式+FP-ID+优先级+简述）
- [x] 3.2 更新 `docs/designs/templates/design-templates/functional-designs/index.md`（归档用模板）：同步功能结构树格式
- [x] 3.3 创建 `docs/designs/templates/changes/{change}/prototype/design-prompt.md`：原型设计提示词模板（7 章节：项目背景与设计目标、设计系统、菜单与导航结构、页面详细规格、业务流程脚本、硬约束、高保真要求）

## 4. 规格文件回写

- [x] 4.1 用 delta spec 更新 `openspec/specs/phase-self-review/spec.md`：explore 和 prototype 自审改为重复制
- [x] 4.2 用 delta spec 更新 `openspec/specs/html-prototype-workflow/spec.md`：子代理委托、导航验证、5 轮 Playwright、design-prompt.md
- [x] 4.3 用 delta spec 更新 `openspec/specs/functional-design-content/spec.md`：功能结构树替换页面导航结构图

## 5. 质量验证

- [x] 5.1 运行 `kflow-skills-auditor` 审查 kflow-prototype-design SKILL.md
- [x] 5.2 运行 `kflow-skills-auditor` 审查 kflow-explore SKILL.md
- [x] 5.3 验证设计文档、技能实现、模板之间的规格一致性
