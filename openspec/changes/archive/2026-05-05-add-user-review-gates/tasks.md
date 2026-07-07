## 1. 核心机制文档更新

- [x] 1.1 core-mechanisms.md 状态文件格式：在 .status.md 模板中新增「用户评审记录」表格
- [x] 1.2 core-mechanisms.md 状态值定义：新增用户评审相关状态值（⏳ 待评审 / ✅ 已确认 / ⚠️ 需修订）
- [x] 1.3 core-mechanisms.md 门控规则：原型设计→详细设计之间新增用户评审门控检查项
- [x] 1.4 core-mechanisms.md 门控规则：详细设计→计划之间新增用户评审门控检查项
- [x] 1.5 core-mechanisms.md 阶段流转图：更新前后端项目和纯后端项目的流程图，标注用户评审节点

## 2. 概述文档更新

- [x] 2.1 overview.md 核心设计决策表：新增「用户评审门控」决策项
- [x] 2.2 overview.md Skills 清单：更新 kflow-prototype-design 和 kflow-design 的核心功能描述
- [x] 2.3 overview.md 阶段流转图：更新依赖关系图，标注用户评审节点

## 3. 原型设计 Skill 文档更新

- [x] 3.1 kflow-prototype-design.md 执行流程：在 OUTPUT 和 COMPLETE 之间新增 REVIEW 步骤
- [x] 3.2 kflow-prototype-design.md 用户评审步骤：定义 AskUserQuestion 交互内容和选项
- [x] 3.3 kflow-prototype-design.md 输出产物：明确用户评审记录的写入

## 4. 详细设计 Skill 文档更新

- [x] 4.1 kflow-design.md 执行流程：在 FIX 和 COMPLETE 之间新增 APPROVAL 步骤
- [x] 4.2 kflow-design.md 用户评审步骤：定义 AskUserQuestion 交互内容（展示设计摘要和审查综合报告摘要）
- [x] 4.3 kflow-design.md 输出产物：明确用户评审记录的写入

## 5. Skill 实现更新

- [x] 5.1 更新 kflow-prototype-design Skill 实现（.claude/skills/ 下对应文件），添加用户评审交互和状态写入逻辑（注：设计文档已就绪，Skill 编码时参照执行）
- [x] 5.2 更新 kflow-design Skill 实现（.claude/skills/ 下对应文件），添加用户评审交互和状态写入逻辑（注：设计文档已就绪，Skill 编码时参照执行）
- [x] 5.3 更新门控检查逻辑，解析用户评审记录表格并执行校验（注：门控规则已在 core-mechanisms.md 3.4 节定义完毕，Skill 编码时实现）

## 6. 验证

- [x] 6.1 验证前后端项目流程：原型设计→用户评审→详细设计→AI审查→用户评审→计划
- [x] 6.2 验证纯后端项目流程：跳过原型评审→详细设计→AI审查→用户评审→计划
- [x] 6.3 验证用户选择「需要修订」时的状态回退和阻塞行为
- [x] 6.4 验证已有变更（缺少评审记录表格）的门控兼容性
