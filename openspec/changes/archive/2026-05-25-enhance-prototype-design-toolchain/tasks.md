## 1. 更新 kflow-prototype-design 设计文档

- [x] 1.1 重写 DESIGN 步骤：拆分为 5.1 STYLE（风格/布局推荐）和 5.2 GENERATE（按选定风格生成）两个子阶段
- [x] 1.2 新增 5.1 STYLE 详细规则：子代理推荐 3 个差异化风格方向、AskUserQuestion 展示、style-decision.md 记录
- [x] 1.3 重写 5.2 GENERATE 详细规则：按 toolchain.md 锁定的工具链执行、合并 design-prompt.md + style-decision.md 为最终 prompt
- [x] 1.4 VERIFY 步骤增强：新增 6.5 UX 规则审查（5 轮子代理串行，内置 20-30 条精简核心规则）
- [x] 1.5 VERIFY 步骤增强：新增 6.6 对比度检测（WCAG 相对亮度计算公式，标记 <4.5:1 的颜色对）
- [x] 1.6 VERIFY 步骤增强：新增 design-system/MASTER.md 产物必检项
- [x] 1.7 SELFREV 步骤细化：一致性维度增强（设计令牌对比：色彩/字体/间距/组件一致性检查）
- [x] 1.8 更新执行流程 ASCII 图：反映新步骤顺序
- [x] 1.9 更新 CHECK 步骤：从硬编码 huashu-design 拦截改为扫描所有设计相关 Skills
- [x] 1.10 更新输出产物表格：新增 style-decision.md、design-system/MASTER.md、ux-check-round-{1..5}.md、contrast-check.md
- [x] 1.11 更新门控检查：huashu-design 可用性硬拦截改为 prototype-gen 角色至少 1 个 Skill 的通用拦截
- [x] 1.12 更新修订模式（REVISION）：对齐 STYLE/GENERATE 拆分和 toolchain 锁定逻辑

## 2. 更新 kflow-init 设计文档

- [x] 2.1 更新工具推荐矩阵：原型设计阶段从硬编码 `huashu-design` 改为多方案描述（方案 A/B/C）
- [x] 2.2 更新 GAP 检测逻辑：检测 prototype-gen 角色 Skill 存在性而非单一 huashu-design
- [x] 2.3 更新 toolchain.md 模板格式：原型设计阶段支持多方案配置

## 3. 使用 /skill-creator 更新运行时 Skill

> **强制规则**：运行时 SKILL.md 的更新必须通过 `/skill-creator` 工作流（编写草稿 → 测试用例 → 定量评测 → 反馈改进 → 重复），禁止直接编辑 `.claude/skills/` 下的 SKILL.md 文件。

### 3.1 更新 kflow-prototype-design 运行时 Skill

- [x] 3.1.1 使用 `/skill-creator` 加载 `.claude/skills/kflow-prototype-design/SKILL.md`
- [x] 3.1.2 将 CHECK 步骤从硬编码 huashu-design 拦截改为扫描所有设计相关 Skills（prototype-gen 角色至少 1 个）
- [x] 3.1.3 新增 SCAN + TOOLCHAIN 步骤：环境扫描设计 Skills、角色分类、多方案推荐、AskUserQuestion 选择、写入 toolchain.md 锁定
- [x] 3.1.4 将 DESIGN 步骤拆分为 5.1 STYLE（风格/布局推荐）和 5.2 GENERATE（按 toolchain.md 锁定的工具链执行）
- [x] 3.1.5 VERIFY 步骤增强：新增 6.5 UX 规则审查（内置 20-30 条精简核心规则，5 轮子代理串行）
- [x] 3.1.6 VERIFY 步骤增强：新增 6.6 对比度检测（WCAG 相对亮度计算公式）
- [x] 3.1.7 VERIFY 步骤增强：新增 design-system/MASTER.md 产物必检项
- [x] 3.1.8 SELFREV 步骤细化：一致性维度增强（设计令牌对比）
- [x] 3.1.9 更新执行流程 ASCII 图：反映新步骤顺序
- [x] 3.1.10 更新输出产物表格：新增 style-decision.md、design-system/MASTER.md、ux-check-round-{1..5}.md、contrast-check.md
- [x] 3.1.11 更新修订模式（REVISION）：对齐 STYLE/GENERATE 拆分和 toolchain 锁定逻辑
- [x] 3.1.12 skill-creator 迭代：跑测试用例 → 评测 → 反馈改进 → 直到通过

### 3.2 更新 kflow-init 运行时 Skill

- [x] 3.2.1 使用 `/skill-creator` 加载 `.claude/skills/kflow-init/SKILL.md`
- [x] 3.2.2 更新工具推荐矩阵：原型设计阶段从硬编码 `huashu-design` 改为多方案描述（方案 A/B/C）
- [x] 3.2.3 更新 GAP 检测逻辑：检测 prototype-gen 角色 Skill 存在性（≥1 个）而非单一 huashu-design
- [x] 3.2.4 更新 toolchain.md 模板格式：原型设计阶段支持多方案配置
- [x] 3.2.5 skill-creator 迭代：跑测试用例 → 评测 → 反馈改进 → 直到通过

## 4. 归档 openspec specs 到 openspec/specs/

- [x] 3.1 合并 specs/prototype-design-toolchain/spec.md 到 openspec/specs/（新增）
- [x] 3.2 合并 specs/prototype-design-system-output/spec.md 到 openspec/specs/（新增）
- [x] 3.3 更新 specs/prototype-subagent-delegation/spec.md（MODIFIED：子代理委托从硬编码改为按 toolchain 锁定）
- [x] 3.4 更新 specs/devflow-init/spec.md（MODIFIED：工具推荐矩阵原型设计多方案 + GAP 检测更新）

## 5. 更新关联文档

- [x] 5.1 更新 core-mechanisms.md 流程图中原型设计阶段的步骤定义
- [x] 5.2 新增 prototype/style-decision.md 模板到 docs/templates/changes/{change}/prototype/
- [x] 5.3 更新 docs/designs/index.md 中 kflow-prototype-design 版本号和变更摘要
