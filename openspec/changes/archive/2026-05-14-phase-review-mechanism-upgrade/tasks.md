# Tasks: phase-review-mechanism-upgrade

## 1. 核心机制文档更新

- [x] 1.1 更新 `docs/designs/core-mechanisms.md` — 新增"10 轮自循环审查机制"章节，包含三阶段自审维度定义、自审流程、时间戳命名规范、审查目录结构（self-reviews/ + cross-reviews/）
- [x] 1.2 更新 `docs/designs/core-mechanisms.md` — 新增"阶段边界强制"章节，包含文档白名单模式、标准产物强制生成规则、信息不足溢出路径、禁止越界规则
- [x] 1.3 更新 `docs/designs/core-mechanisms.md` — 调整审查相关目录结构定义，`review-reports/` 重命名为 `cross-reviews/`，新增 `self-reviews/` 目录及子目录规范
- [x] 1.4 更新 `docs/designs/core-mechanisms.md` — 版本号递增并追加修订记录

## 2. Skill 设计文档更新 — kflow-explore

- [x] 2.1 更新 `docs/designs/skills/kflow-explore.md` — 输出产物表格中 functional-designs/ 扩展内容要求：新增页面菜单、可执行操作、表单项定义、业务规则章节
- [x] 2.2 更新 `docs/designs/skills/kflow-explore.md` — 执行流程新增 10 轮自审步骤（在 OUTPUT 步骤之后、COMPLETE 步骤之前）
- [x] 2.3 更新 `docs/designs/skills/kflow-explore.md` — 新增"阶段边界约束"章节，明确域内（用户视角）和域外（技术架构/数据模型/接口/代码）边界
- [x] 2.4 更新 `docs/designs/skills/kflow-explore.md` — 新增"10 轮自审"章节，定义完整性/闭环性/必要性/清晰性四个维度和检查规则
- [x] 2.5 更新 `docs/designs/skills/kflow-explore.md` — 版本号递增并追加修订记录

## 3. Skill 设计文档更新 — kflow-prototype-design

- [x] 3.1 更新 `docs/designs/skills/kflow-prototype-design.md` — 执行流程新增 10 轮自审步骤（在 DESIGN 步骤之后、REVIEW 步骤之前），自审聚焦覆盖性检查
- [x] 3.2 更新 `docs/designs/skills/kflow-prototype-design.md` — 新增"阶段边界约束"章节，明确域内（UI原型/交互流程/视觉风格）和域外（功能决策/业务规则/技术实现）边界
- [x] 3.3 更新 `docs/designs/skills/kflow-prototype-design.md` — 新增"10 轮自审"章节，定义覆盖性/一致性/可用性/完整性四个维度和检查规则
- [x] 3.4 更新 `docs/designs/skills/kflow-prototype-design.md` — 用户评审流程调整：明确自审全部完成后才进入用户评审（AskUserQuestion）
- [x] 3.5 更新 `docs/designs/skills/kflow-prototype-design.md` — 版本号递增并追加修订记录

## 4. Skill 设计文档更新 — kflow-design

- [x] 4.1 更新 `docs/designs/skills/kflow-design.md` — 执行流程新增 10 轮自审步骤（在 DESIGN 步骤之后、REVIEW 步骤之前），自审完成后进入四视角审查
- [x] 4.2 更新 `docs/designs/skills/kflow-design.md` — 审查流程中审查报告路径从 `review-reports/` 更新为 `cross-reviews/{timestamp}/`
- [x] 4.3 更新 `docs/designs/skills/kflow-design.md` — 新增"阶段边界约束"章节，明确域内（架构/数据模型/接口/NFR/测试用例）和域外（功能决策/UI布局）边界
- [x] 4.4 更新 `docs/designs/skills/kflow-design.md` — 新增"10 轮自审"章节，定义一致性/完备性/可行性/可测性四个维度和检查规则
- [x] 4.5 更新 `docs/designs/skills/kflow-design.md` — synthesis.md 格式扩展：新增审查批次索引表格
- [x] 4.6 更新 `docs/designs/skills/kflow-design.md` — 版本号递增并追加修订记录

## 5. 模板文件更新与新增

- [x] 5.1 更新 `docs/designs/templates/change/functional-designs/part-NN.md` — 新增页面菜单、可执行操作、表单项定义、业务规则、业务流程上下文章节
- [x] 5.2 更新 `docs/designs/templates/change/functional-designs/index.md` — 新增页面导航结构图、核心业务流程图章节
- [x] 5.3 新建 `docs/designs/templates/change/self-reviews/review-round.md` — 自审轮次报告模板（含维度得分表、新发现问题、上轮问题验证、改进内容、仍存在问题）
- [x] 5.4 更新 `docs/designs/templates/change/review-reports/review-synthesis.md` — 新增审查批次索引表格
- [x] 5.5 更新 `docs/designs/templates/index.md` — 新增 self-reviews/ 模板条目，更新 cross-reviews/ 条目

## 6. 设计入口更新

- [x] 6.1 更新 `docs/designs/index.md` — 核心设计决策表中新增 10 轮自审机制、阶段边界强制、功能设计升维决策项
- [x] 6.2 更新 `docs/designs/index.md` — 审查目录结构描述更新（review-reports/ → self-reviews/ + cross-reviews/）
- [x] 6.3 更新 `docs/designs/index.md` — 版本号从 1.8.0 递增至 1.9.0，追加修订记录
