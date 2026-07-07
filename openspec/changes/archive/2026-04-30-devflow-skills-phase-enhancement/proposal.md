## Why

现有 DevFlow Skills 设计文档缺少计划阶段、编码阶段、测试阶段、归档阶段的详细规格设计，无法指导实际 Skill 实现。同时，需要区分前后端项目和纯后端项目的开发流程，以适应不同项目类型的开发需求。

## What Changes

- 功能点上限从 20 调整为 10，子变更上限限制为 20
- 新增项目类型区分机制（前后端项目 vs 纯后端项目）
- 增强计划阶段 Skill 规格：任务清单细化规则（功能点级全展开）
- 增强编码阶段 Skill 规格：自动化服务循环流程、service-guide 生成机制、接口单元测试报告
- 重命名测试阶段为"浏览器自动化功能测试"，仅适用于前后端项目
- 新增变更归档阶段 Skill 规格
- 新增流程指引 Skill 规格（含意图识别、项目类型判断）
- 调整状态总结 Skill：保持对话输出，增加索引文件支持
- 新增 skill-suggestion.md 记录机制
- 新增 docs/changes/index.md 变更管理索引文件
- 新增 docs/service-guide.md 项目服务指引（编码阶段生成）

## Capabilities

### New Capabilities

- `devflow-archive`: 变更归档阶段 Skill，支持已完成/未完成变更归档，更新状态文件和索引文件
- `devflow-guide`: 流程指引 Skill，自动检测用户意图、项目类型、活跃变更，引导正确阶段
- `project-type-detection`: 项目类型检测机制，在设计探索阶段自动判断前后端项目或纯后端项目
- `service-guide-generation`: 项目服务指引生成机制，编码阶段自动分析项目结构、交互获取配置、生成服务启动配置
- `skill-suggestion-logging`: Skills 优化建议记录机制，记录流程指引错误和用户纠正反馈

### Modified Capabilities

- `devflow-explore`: 新增项目类型检测，输出到 design-explore.md
- `devflow-design`: 输出产物区分（前后端项目输出 e2e-tests.md，纯后端项目不输出）
- `devflow-plan`: 任务清单细化规则增强，功能点级全展开形式
- `devflow-code`: 自动化服务循环流程增强，接口单元测试报告输出
- `devflow-e2e-qa`: 原 devflow-qa 重命名，仅前后端项目启用，前置数据浏览器录入机制
- `devflow-fix`: 自动标记逻辑增强，所有子变更通过才提示归档
- `devflow-status`: 输出内容增强，支持索引文件读取
- `core-mechanisms`: 功能点上限调整，子变更上限新增，阶段流转规则更新，归档条件简化

## Impact

- 影响所有设计文档：docs/designs/ 下 8 个现有文件需修改
- 新增 7 个设计文档和示例文件
- 新增目录结构：docs/changes/index.md, docs/service-guide.md, docs/skill-suggestion.md
- Skills 清单从 8 个调整为 10 个
- 前后端项目流程保持 7 阶段，纯后端项目流程简化为 5 阶段