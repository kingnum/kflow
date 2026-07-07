## Why

kflow-init LEGACY 模式通过代码逆向分析生成的产品级文档存在三处根本性缺陷：模块按代码目录结构划分而非功能菜单划分、内容密度远低于变更级文档、技术设计文档维度缺失（无配置项/错误处理），导致产品级文档基线无法作为归档合并的有效载体，迫使每次归档时"草稿实质上被丢弃而非被增强"。

## What Changes

- **BREAKING** 功能设计文档组织方式：从平铺文件 `functional-designs/{module}.md` 改为按一级菜单目录结构 `functional-designs/{menu}/index.md` + `part-NN.md`，与变更级目录化结构对齐
- **BREAKING** 模块划分逻辑：前后端项目从 L2 代码目录扫描改为 L2.5 前端工程扫描（路由/菜单/页面组件），按真实功能菜单划分模块
- **BREAKING** 纯后端项目功能设计改用独立简化模板 `backend-domain.md`，去掉 UX 密集型章节（页面与菜单、表单项定义、交互约束），替换为后端特有章节（设计域、接口参数定义、调用约束）
- 产品级 technical-designs 从 4 文件扩展为 6 文件，新增 `config-items.md` 和 `error-handling.md`，完整对齐 detailed-design.md 六大部分
- kflow-init LEGACY 扫描层次新增 L2.5（前端工程扫描），对前后端项目提取路由配置、菜单结构、页面组件中的表单字段和操作按钮
- kflow-archive MERGE 步骤适配新的目录结构合并逻辑
- 模板体系更新：新增 4 个模板（菜单级索引、产品级分册、纯后端简化模板、config-items、error-handling），废弃 module.md，修订 4 个技术设计模板

## Capabilities

### New Capabilities
- `init-frontend-scanning`: L2.5 前端工程扫描层——对前后端项目扫描前端路由配置、菜单/导航组件、页面组件，提取菜单层级、表单字段、操作按钮以推断功能点
- `product-config-items-doc`: 产品级配置项设计文档（`config-items.md`），对齐 detailed-design.md §五配置项设计，由 init LEGACY 预生成骨架、archive 合并更新
- `product-error-handling-doc`: 产品级错误处理设计文档（`error-handling.md`），对齐 detailed-design.md §六错误处理设计，由 init LEGACY 预生成骨架、archive 合并更新
- `backend-domain-template`: 纯后端项目功能设计简化模板，按设计域（controllers/services/models）划分，去除 UX 密集章节，替换为后端特有章节

### Modified Capabilities
- `init-legacy-reverse-analysis`: L2.5 前端扫描、模块按菜单/域划分、前后端差异化内容填充策略、7 类文档生成逻辑更新
- `archive-design-merge`: 合并目标从平铺文件改为目录结构、技术设计从 4 文件扩展为 6 文件合并、去草稿逻辑适配目录结构
- `devflow-init`: 8 项产品文档检测逻辑更新（functional-designs 从文件数改为目录数/文件数检测）、LEGACY 输出产物格式变更
- `stage-doc-templates`: 新增 5 个模板、废弃 module.md、修订 4 个技术设计模板、模板目录结构更新
- `doc-naming-convention`: `{module}.md` 概念替换为 `{menu}/` 目录 + `part-NN.md`（前后端）和 `{domain}.md`（纯后端）
- `functional-design-content`: 新增纯后端简化模板的内容维度定义（设计域/接口参数定义/调用约束替代 UX 章节）

## Impact

- 受影响 SKILL 实现：`kflow-init/SKILL.md`（LEGACY 步骤重大修订）、`kflow-archive/SKILL.md`（MERGE 步骤修订）
- 受影响设计文档：`kflow-init.md`、`kflow-archive.md`、`core-mechanisms.md`、`overview.md`、`templates/index.md`
- 受影响模板：新增 5、废弃 1（module.md）、修订 4（architecture/data-model/api-catalog/nfr-baseline）
- 受影响 specs：上述 6 个 Modified Capabilities 对应的 spec 文件
- 已有产品文档如存在平铺的 `functional-designs/{module}.md` 需在首次重新执行 init 时迁移到目录结构
