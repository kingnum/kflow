# 老项目逆向分析 — 产品文档生成

## 触发条件

当 `docs/CONTEXT.md` 不存在或 `docs/designs/functional-designs/` 目录为空时，使用 AskUserQuestion 询问用户：

> "检测到产品文档缺失，是否通过代码逆向分析生成产品级文档草稿？"

选项：「生成草稿」「跳过」

## 三层逆向扫描

```
L1: 配置文件扫描
  ├── package.json / pom.xml / build.gradle / requirements.txt / Cargo.toml
  └── 输出: 技术栈、构建工具、依赖列表、配置项

L2: 目录结构扫描
  ├── src/ 子目录、routes/、controllers/、models/、services/
  └── 输出: 模块划分、候选设计域

L2.5: 前端工程扫描（前后端项目条件执行，纯后端跳过）
  ├── 路由配置: Vue Router / React Router / Next.js -> path -> component 映射、嵌套层级
  ├── 菜单配置: 独立配置文件 / 组件内菜单 -> 一级菜单、二级菜单、权限控制
  ├── 页面组件: 页面标题 / 表单字段(name/label/rules) / 操作按钮
  └── 输出: 菜单层级结构、表单字段、操作按钮

L3: 源码语义扫描
  ├── 路由定义、数据模型、API 接口、关键注释、异常处理
  └── 输出: API 目录、数据模型、领域术语、错误码
```

## 生成文档草稿

基于扫描结果生成产品文档草稿（标注 `> 由 AI 逆向分析生成，待人工审核`）：

| 序号 | 文档 | 扫描来源 | 前后端项目 | 纯后端项目 |
|------|------|---------|-----------|-----------|
| 1 | docs/CONTEXT.md | L3 提取 | 领域术语及定义 | 领域术语及定义 |
| 2 | docs/designs/index.md | 综合 | 项目概述、功能模块导航（指向子目录） | 项目概述、功能模块导航（指向平铺文件） |
| 3 | docs/designs/functional-designs/ | L2.5 + L3 | 按菜单子目录: `{menu}/index.md` + `{menu}/part-NN.md` | 按设计域平铺: `{domain}.md` |
| 4 | docs/designs/detailed-designs/architecture.md | L1 + L2 | 系统架构模式推断 + 配置项索引 + 错误处理索引 | 系统架构模式推断 |
| 5 | docs/designs/detailed-designs/data-model.md | L3 实体扫描 | 实体及关键字段聚合 | 实体及关键字段聚合 |
| 6 | docs/designs/detailed-designs/api-catalog.md | L3 路由定义 | API 端点目录 | API 端点目录 |
| 7 | docs/designs/detailed-designs/nfr-baseline.md | L3 注解扫描 | NFR 基线 | NFR 基线 |
| 8 | docs/designs/detailed-designs/config-items.md | L1 配置扫描 | 配置项骨架（新增） | 配置项骨架（新增） |
| 9 | docs/designs/detailed-designs/error-handling.md | L3 异常扫描 | 错误码骨架（新增） | 错误码骨架（新增） |
| 10 | docs/service-guide.md | L1 配置扫描 | dev 环境启动命令、端口、数据库 | dev 环境启动命令、端口、数据库 |

## 产品文档 8 项检测

| # | 文件 | 路径 | 状态值 |
|---|------|------|--------|
| 1 | CONTEXT.md | docs/CONTEXT.md | ✅ 已就绪 / ❌ 不存在 |
| 2 | 设计索引入口 | docs/designs/index.md | ✅ 已就绪 / ❌ 不存在 |
| 3 | 功能设计文档 | docs/designs/functional-designs/ | 前后端：✅ N个模块 / ❌ 不存在；纯后端：✅ N篇 / ❌ 不存在 |
| 4 | 架构全景 | docs/designs/detailed-designs/architecture.md | ✅ 已就绪 / ❌ 不存在 |
| 5 | 数据模型 | docs/designs/detailed-designs/data-model.md | ✅ 已就绪 / ❌ 不存在 |
| 6 | API 目录 | docs/designs/detailed-designs/api-catalog.md | ✅ 已就绪 / ❌ 不存在 |
| 7 | NFR 基线 | docs/designs/detailed-designs/nfr-baseline.md | ✅ 已就绪 / ❌ 不存在 |
| 8 | 服务指引 | docs/service-guide.md | ✅ 已就绪 / ❌ 不存在 |

**侧带检测**（不影响主判断）：config-items.md 和 error-handling.md 缺失时标注"⚠️ 建议补充"。

## 用户审核确认

生成完成后展示文档清单和关键内容摘要，使用 AskUserQuestion 请求用户确认：
- 「确认写入」— 将确认的文档写入对应路径，更新项目画像中的产品文档状态
- 「修改后写入」— 用户自行修改后写入
- 「放弃」— 不写入任何文档，标注产品文档为 ❌ 不存在
