## 1. 模板层更新

- [x] 1.1 functional-designs/index.md 模板合并记录表：将"八、需求变更记录"与"九、修订记录"合并为统一的"八、修订记录"表，新增"修订类型"列（枚举：初始版本/需求变更/业务规则/接口签名/数据模型/UI布局/交互行为/架构设计/配置项/其他），调整列顺序为 版本|日期|修订类型|修订内容|影响功能点|触发阶段
- [x] 1.2 创建 prototype/index.md 模板：包含五节——原型文件清单（文件/说明/版本表）、页面清单（页面/路由/原型文件/所含区域表）、设计系统引用（色彩/字体/间距/组件库及其在 design-system/MASTER.md 中的来源章节）、修订记录（统一格式）、版本号头部
- [x] 1.3 detailed-design.md 模板增加修订记录节：在模板末尾新增"修订记录"节（统一格式），单文件模板（FP≤20）和目录化模板（FP>20）均需增加
- [x] 1.4 change-status.md 模板新增"设计修订同步追踪"节：包含序号/修订时间/修订目标/变更简述/影响范围 + 每阶段独立确认列（plan/code/review/api-test/e2e-test/integ-test），每列初始 ⏳

## 2. kflow-guide 集中检测与分流

- [x] 2.1 kflow-guide SKILL.md description 新增设计修订触发词：添加"设计需调整/功能设计需调整/原型.*调整/详细设计.*调整/接口设计.*改/修改.*设计/调整.*设计"等中英文混合触发词
- [x] 2.2 kflow-guide SKILL.md 执行流程新增 DESIGN_REVISION 模式：在 PARSE 阶段增加关键词→目标设计目录映射（功能/需求→functional-designs、原型/UI/交互→prototype、详细/接口/架构→detailed-design），ROUTE 阶段增加分流逻辑（唤醒对应设计 Skill 的 REVISION 模式）
- [x] 2.3 kflow-guide SKILL.md 新增设计修订后处理流程：目标 Skill 完成后 → 更新设计目录 index.md 修订记录 → 更新 .status.md 同步追踪表 → AskUserQuestion 询问回退/暂缓

## 3. 阶段 Skill RELOAD 列表更新

- [x] 3.1 phase-hooks.md 各阶段 RELOAD 列表新增 index.md 文件：design 阶段新增 functional-designs/index.md 和 prototype/index.md；plan/code/code-review/api-test/e2e-test/integration-test 阶段新增 functional-designs/index.md、prototype/index.md（如存在）、detailed-design 修订记录节
- [x] 3.2 受影响的各阶段 Skill SKILL.md 确保 PRE_HOOK 引用指向更新后的 phase-hooks.md

## 4. 设计文档更新

- [x] 4.1 更新 kflow-explore 设计文档（docs/designs/skills/kflow-explore.md）：第 8 节修订记录格式描述更新为合并后的统一格式，增加 REVISION 模式说明
- [x] 4.2 更新 kflow-prototype-design 设计文档（docs/designs/skills/kflow-prototype-design.md）：产物清单新增 prototype/index.md，REVISION 模式增加 index.md 更新步骤
- [x] 4.3 更新 kflow-design 设计文档（docs/designs/skills/kflow-design.md）：产物清单中 detailed-design.md 增加修订记录要求，增加 REVISION 模式说明
- [x] 4.4 更新 core-mechanisms/09-phase-hooks.md：各阶段 RELOAD 清单增加新的 index.md 文件
- [x] 4.5 更新 core-mechanisms/03-status-and-tasks.md：.status.md 新增"设计修订同步追踪"节说明，每阶段独立确认规则

## 5. 运行时 Skill 同步（设计文档 → SKILL.md）

- [x] 5.1 使用 /skill-creator 更新 kflow-guide SKILL.md：根据变更后的设计文档同步更新 description（含 DESIGN_REVISION 触发词）和执行流程（DESIGN_REVISION 模式路由），标注"设计文档 → SKILL.md 同步"
- [x] 5.2 使用 /skill-creator 更新 kflow-explore SKILL.md：根据变更后的设计文档同步更新产物输出规范（合并后的修订记录格式），标注"设计文档 → SKILL.md 同步"
- [x] 5.3 使用 /skill-creator 更新 kflow-prototype-design SKILL.md：根据变更后的设计文档同步更新产物输出规范（prototype/index.md），标注"设计文档 → SKILL.md 同步"
- [x] 5.4 使用 /skill-creator 更新 kflow-design SKILL.md：根据变更后的设计文档同步更新产物输出规范（修订记录），标注"设计文档 → SKILL.md 同步"
