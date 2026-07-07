## 1. 核心文档更新（版本号和概述）

- [x] 1.1 更新 docs/designs/index.md 版本号至 1.5.0，新增 kflow-audit 和 kflow-init 条目，更新设计决策表
- [x] 1.2 更新 docs/designs/overview.md Skills 清单、设计决策表、实施计划表
- [x] 1.3 更新 docs/designs/skills/index.md Skills 清单、触发时机表、阶段依赖关系图

## 2. 核心机制更新

- [x] 2.1 更新 docs/designs/core-mechanisms.md 回退触发来源（新增第 4 种：审计发现）
- [x] 2.2 更新 docs/designs/core-mechanisms.md 目录结构（新增 docs/designs/domains/ 和 test-reports/integration/fix-reports/）
- [x] 2.3 更新 docs/designs/core-mechanisms.md 缺陷修复循环（新增变更级集成测试缺陷修复循环）
- [x] 2.4 更新 docs/designs/core-mechanisms.md 归档条件（新增审计门控和设计合并步骤）
- [x] 2.5 更新 docs/designs/core-mechanisms.md 文件命名（design-explore.md → functional-design.md, design.md → detailed-design.md）
- [x] 2.6 新增 docs/designs/core-mechanisms.md 文档拆分策略章节（产品级多文件 + 变更级条件拆分）

## 3. 新增 Skill 设计文档

- [x] 3.1 创建 docs/designs/skills/kflow-audit.md 设计规格（六维度评估、归档门控集成、审计回退路由、手动调用）
- [x] 3.2 创建 docs/designs/skills/kflow-init.md 设计规格（环境能力发现、工具推荐矩阵、组合可行性评估、toolchain.md 输出）

## 4. 现有 Skill 设计文档修改

- [x] 4.1 更新 docs/designs/skills/kflow-bug-fix.md 扩展为两级（单 Skill + 上下文检测、子变更级三分法、变更级四分法、对比表呈现差异）
- [x] 4.2 更新 docs/designs/skills/kflow-archive.md 新增设计合并流程（提取 → 合并 → 溯源标注 → changelog 更新）
- [x] 4.3 更新 docs/designs/skills/kflow-explore.md 输出文件名（design-explore.md → functional-design.md）
- [x] 4.4 更新 docs/designs/skills/kflow-design.md 输入/输出文件名和门控文件名

## 5. 全局文件命名迁移

- [x] 5.1 全局替换所有设计文档中的 design-explore.md → functional-design.md
- [x] 5.2 全局替换所有设计文档中的 design.md → detailed-design.md（注意区分 design.md 指文件 vs 指流程）
- [x] 5.3 更新所有示例文件中的文件引用

## 6. 新增示例文件

- [x] 6.1 创建 docs/designs/examples/audit-report.md 审计报告示例
- [x] 6.2 创建 docs/designs/examples/toolchain.md toolchain 配置示例
- [x] 6.3 创建 docs/designs/examples/integration-fix-report.md 集成测试修复报告示例
- [x] 6.4 创建 docs/designs/examples/product-domain-doc.md 产品级领域文档示例
- [x] 6.5 创建 docs/designs/examples/product-design-index.md 产品级索引入口示例
- [x] 6.6 更新 docs/designs/examples/index.md 新增示例导航
- [x] 6.7 更新 docs/designs/examples/change-status.md 使用新文件命名
- [x] 6.8 更新 docs/designs/examples/change-index.md 归档设计合并字段

## 7. 交叉验证

- [x] 7.1 验证所有门控规则中引用的文件名一致
- [x] 7.2 验证阶段流转图中新增 Skill 位置正确
- [x] 7.3 验证所有文档中图例（✅/🔶/⏭️）使用一致
- [x] 7.4 检查无 TODO/TBD 占位符残留
