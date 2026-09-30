---
stage: 产品级
skill: kflow-prototype-design
version: 1.0.0
created_at: 2026-09-29
template_for: docs/designs/prototypes/manifest.md
---

# 产品级原型清单：{项目名称}

> **版本**: 1.0.0
> **创建时间**: {YYYY-MM-DD}
> **最后更新时间**: {YYYY-MM-DD HH:MM}
> **产品类型**: {前后端项目}

本清单登记产品级原型目录 `docs/designs/prototypes/` 下的全部产物及其来源变更，是下游阶段（plan、code、code-review、e2e-test）获取全产品原型文件列表的唯一入口。

---

## 一、产物组织方式

- **文件结构类型**: {单文件 | 多页面 | 含共享资源}
- **入口文件路径**: `index.html`（默认，允许其他入口）
- **共享资源目录**: {components/、assets/ | 无}

> 描述产品级原型的整体组织方式。单文件：所有页面在入口 HTML 内部锚点跳转；多页面：多个独立 HTML 文件；含共享资源：存在 `components/`、`assets/` 子目录存放共享组件与静态资源。

---

## 二、原型文件清单

| 文件 | 说明 | 角色 | 来源变更 | 版本 |
|------|------|------|---------|------|
| index.html | 全产品导航入口（卡片网格按功能模块分组） | entry | {change-name} | 1.0.0 |
| screens/{screen}.html | {屏幕名称} | page | {change-name} | 1.0.0 |
| components/{component}.js | {共享组件} | shared | {change-name} | 1.0.0 |
| assets/{asset} | {静态资源} | shared | {change-name} | 1.0.0 |
| design-tokens.css | 设计令牌（CSS 变量：色板/字号/间距/圆角/阴影） | tokens | {change-name} | 1.0.0 |
| design-system/MASTER.md | 设计系统主文档 | process | {change-name} | 1.0.0 |

> **角色枚举**: entry（入口页面）/ page（独立页面）/ tokens（设计令牌）/ coverage（元素覆盖树）/ shared（共享资源）/ process（过程产物）
> **清单范围**: 本清单仅登记产品级原型目录下的产物。变更级 `element-coverage-tree.md`（角色 coverage）与变更级 `prototype-plan/`（角色 process）**不计入**本清单，改由变更级 `prototype-changes.md` 登记。
> **下游消费规则**: 下游阶段仅消费 entry/page/tokens/shared 角色文件，不消费 process 角色文件。
> **版本独立性**: 每个文件的版本号独立标注，与清单自身版本号不绑定。

---

## 三、页面清单

| 页面名称 | 路由路径 | 对应原型文件 | 所含区域 |
|----------|---------|------------|---------|
| {页面名} | {路由} | {相对 docs/designs/prototypes/ 的文件路径} | {区域列表} |

> 对应原型文件路径为相对 `docs/designs/prototypes/` 目录的实际路径（可能为 `index.html` 内部锚点 `#section`、`screens/{screen}.html` 等独立文件）。

---

## 四、设计系统引用

| 属性 | 值 | design-system/MASTER.md 来源章节 |
|------|-----|-------------------------------|
| 色彩方案 | {主色/背景色/文字色/状态色} | {章节名} |
| 字体系统 | {标题字体/正文字体} | {章节名} |
| 间距系统 | {间距规格} | {章节名} |
| 组件库 | {组件库引用} | {章节名} |

> 如 `docs/designs/prototypes/design-system/MASTER.md` 尚不存在，本节标注"⏳ 待生成"，并在原型设计阶段后续步骤中更新。

---

## 五、共享资源清单

| 文件 | 说明 | 用途 |
|------|------|------|
| {components/xxx.js} | {共享组件脚本} | {通用组件/状态管理器等} |
| {assets/xxx.css} | {共享样式文件} | {全局样式/主题变量等} |

> 如产品级原型产物不包含共享资源子目录，本节标注"不适用"。

---

## 六、修订记录

| 版本 | 日期 | 修订类型 | 修订内容 | 影响功能点 | 触发阶段 |
|------|------|---------|---------|-----------|---------|
| 1.0.0 | {YYYY-MM-DD} | 初始版本 | 初始版本 | — | 原型设计 |

> 每次归档登记原型改动时，追加一条修订记录。格式与 `functional-designs/index.md`、`detailed-designs/index.md` 中的修订记录一致。
