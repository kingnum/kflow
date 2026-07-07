## 1. 核心机制文档更新

- [x] 1.1 更新 core-mechanisms.md 功能点上限（20→10）
- [x] 1.2 更新 core-mechanisms.md 新增子变更上限（最大20个）
- [x] 1.3 更新 core-mechanisms.md 新增项目类型区分规则
- [x] 1.4 更新 core-mechanisms.md 阶段流转规则（前后端项目7阶段，纯后端项目5阶段）
- [x] 1.5 更新 core-mechanisms.md 归档条件简化（统一为状态文件检查）
- [x] 1.6 更新 core-mechanisms.md 目录结构新增（docs/changes/index.md, docs/service-guide.md, docs/skill-suggestion.md）
- [x] 1.7 更新 core-mechanisms.md 状态文件示例数值同步

## 2. 概述文档更新

- [x] 2.1 更新 overview.md 功能点上限同步（10）
- [x] 2.2 更新 overview.md Skills 清单（新增 devflow-archive, devflow-guide）
- [x] 2.3 更新 overview.md 技能清单测试阶段重命名（devflow-qa → devflow-e2e-qa）
- [x] 2.4 更新 overview.md 项目类型区分流程图
- [x] 2.5 更新 overview.md 核心设计决策新增项目类型区分

## 3. Skills 索引文档更新

- [x] 3.1 更新 skills/index.md Skills 清单表格
- [x] 3.2 更新 skills/index.md 测试阶段 Skill 重命名
- [x] 3.3 更新 skills/index.md 触发时机新增项目类型判断
- [x] 3.4 更新 skills/index.md 阶段依赖关系图更新
- [x] 3.5 更新 skills/index.md 阶段流转示意图更新

## 4. 设计探索 Skill 规格更新

- [x] 4.1 更新 devflow-explore.md 新增项目类型检测流程
- [x] 4.2 更新 devflow-explore.md 输出产物新增项目类型字段
- [x] 4.3 更新 devflow-explore.md 检测规则定义（前端工程标识）
- [x] 4.4 更新 devflow-explore.md 用户确认项目类型流程

## 5. 详细设计 Skill 规格更新

- [x] 5.1 更新 devflow-design.md 输出产物区分（前后端 vs 纯后端）
- [x] 5.2 更新 devflow-design.md 前后端项目输出 e2e-tests.md
- [x] 5.3 更新 devflow-design.md 纯后端项目不输出 e2e-tests.md
- [x] 5.4 更新 devflow-design.md 示例文件数值同步

## 6. 计划阶段 Skill 规格更新

- [x] 6.1 更新 devflow-plan.md 任务细化规则（功能点级全展开）
- [x] 6.2 更新 devflow-plan.md 每功能点 7-9 个 checkbox 标准模板
- [x] 6.3 更新 devflow-plan.md 任务粒度判断标准更新

## 7. 编码阶段 Skill 规格更新

- [x] 7.1 更新 devflow-code.md 新增自动化服务循环流程图
- [x] 7.2 更新 devflow-code.md 新增 service-guide 检测/生成流程
- [x] 7.3 更新 devflow-code.md 新增服务指引文档格式定义
- [x] 7.4 更新 devflow-code.md 新增接口单元测试报告输出要求
- [x] 7.5 更新 devflow-code.md 新增编译→重启→测试自动化循环描述
- [x] 7.6 更新 devflow-code.md 门控检查新增 service-guide 存在性

## 8. 测试阶段 Skill 规格更新（重命名）

- [x] 8.1 重命名 devflow-qa.md 为 devflow-e2e-qa.md
- [x] 8.2 更新 devflow-e2e-qa.md 基本信息描述（浏览器自动化功能测试）
- [x] 8.3 更新 devflow-e2e-qa.md 门控检查新增项目类型判断
- [x] 8.4 更新 devflow-e2e-qa.md 新增前置数据浏览器录入流程
- [x] 8.5 更新 devflow-e2e-qa.md 失败用例详情新增上下文环境字段
- [x] 8.6 更新 devflow-e2e-qa.md 明确禁止接口调用测试规则
- [x] 8.7 更新 devflow-e2e-qa.md 每轮完整执行所有用例规则
- [x] 8.8 更新 devflow-e2e-qa.md 无法自动解决时咨询用户规则

## 9. 缺陷修复 Skill 规格更新

- [x] 9.1 更新 devflow-fix.md 新增自动标记逻辑描述
- [x] 9.2 更新 devflow-fix.md 所有子变更通过才提示归档规则
- [x] 9.3 更新 devflow-fix.md 测试阶段一轮通过自动跳过缺陷修复

## 10. 状态总结 Skill 规格更新

- [x] 10.1 更新 devflow-status.md 保持对话输出（不产生文件）
- [x] 10.2 更新 devflow-status.md 输出内容增加索引文件读取
- [x] 10.3 更新 devflow-status.md 输出格式与变更状态汇总一致

## 11. 新增变更归档 Skill 规格

- [x] 11.1 创建 skills/devflow-archive.md 基本信息定义
- [x] 11.2 创建 devflow-archive.md 门控检查定义（状态文件检查）
- [x] 11.3 创建 devflow-archive.md 输入要求定义
- [x] 11.4 创建 devflow-archive.md 输出产物定义（状态更新、索引更新）
- [x] 11.5 创建 devflow-archive.md 执行流程图
- [x] 11.6 创建 devflow-archive.md 归档后禁止操作规则
- [x] 11.7 创建 devflow-archive.md 与其他 Skill 关系

## 12. 新增流程指引 Skill 规格

- [x] 12.1 创建 skills/devflow-guide.md 基本信息定义
- [x] 12.2 创建 devflow-guide.md 意图识别关键词映射表
- [x] 12.3 创建 devflow-guide.md 活跃变更检测流程
- [x] 12.4 创建 devflow-guide.md 项目类型判断逻辑
- [x] 12.5 创建 devflow-guide.md 流程概览输出格式
- [x] 12.6 创建 devflow-guide.md 指引错误记录规则
- [x] 12.7 创建 devflow-guide.md 与其他 Skill 关系

## 13. 示例文档新增

- [x] 13.1 创建 examples/service-guide.md 项目服务指引示例
- [x] 13.2 创建 examples/skill-suggestion.md Skills 优化建议记录示例
- [x] 13.3 创建 examples/change-index.md 变更管理索引示例
- [x] 13.4 更新 examples/index.md 新增示例索引

## 14. 状态示例文档更新

- [x] 14.1 更新 examples/change-status.md 功能点数示例值（10）
- [x] 14.2 更新 examples/change-status.md 新增项目类型字段
- [x] 14.3 更新 examples/change-status.md 阶段表格新增浏览器自动化测试跳过示例
- [x] 14.4 更新 examples/subchange-status.md 功能点数示例值（10）
- [x] 14.5 更新 examples/subchange-tasks.md 任务数示例值同步

## 15. 文档索引更新

- [x] 15.1 更新 docs/designs/index.md Skills 详细规格索引
- [x] 15.2 更新 docs/designs/index.md 附录示例索引