---
stage: 详细设计 / 原型设计
skill: kflow-design / kflow-prototype-design
version: 1.0.0
created_at: 2026-05-29
template_for: element-coverage-tree.md
---

# 元素覆盖树：{change-name}

> **生成时间**: {YYYY-MM-DD HH:MM}
> **来源**: {prototype-design 自动生成 | kflow-design playwright-cli 探索生成}
> **版本**: 1.0.0
> **生成方式**: {路径A-静态HTML解析 | 路径B-playwright-cli探索}
> **TC-ID 覆盖率**: {M}/{N}（{百分比}%）

---

## 符号说明

| 符号 | 含义 | 示例 |
|------|------|------|
| 📄 | 页面 | `📄 /dashboard` |
| 🏗️ | 区域（section） | `🏗️ 搜索区` |
| 🔘 | 按钮 | `🔘 [登录]` |
| 📝 | 输入/表单 | `📝 [用户名 input]` |
| 💬 | 弹窗/浮窗/抽屉/Toast | `💬 [确认对话框]` |
| 📊 | 数据展示区 | `📊 [用户列表表格]` |
| 🔗 | 页面跳转 | `🔗 跳转 → 📄 /detail/{id}` |
| 🎯 | 交互状态 | `🎯 hover 态`、`🎯 loading 态` |

---

## 树结构

### 📄 /{page-path} — {页面名称}

```yaml
# 页面元数据
page:
  path: "/{page-path}"
  name: "{页面名称}"
  prototype_file: "{对应的 HTML 文件名，有原型时填写}"
  tested: null  # e2e-test 阶段标记: null/✅/❌
```

#### 🏗️ {区域名称}

```yaml
# 区域元数据
section:
  name: "{区域名称}"
  trigger_condition: null  # 条件出现的区域注明触发条件，如"选中行后出现"
```

##### 🔘 [{按钮文本}] [button]

```yaml
element:
  ref: "{原型 ref 或 playwright snapshot ref}"
  type: "button"
  tc_ids: ["TC-001"]  # design 阶段填充
  data_source: "N/A"  # 可选: 后端API|前端静态|配置控制|浏览器存储
  tested: null  # e2e-test 阶段标记: null/✅/❌
```

- 🎯 click → TC-001
  - 💬 [{产生的浮窗名}]
    - 🔘 [{浮窗内按钮}] → TC-002
  - 🔗 跳转 → 📄 /{target-page}
- 🎯 hover → TC-003
- 🎯 disabled → TC-004

##### 📝 [{表单名}]

```yaml
element:
  ref: "{原型 ref 或 playwright snapshot ref}"
  type: "form"
  tc_ids: []
  data_source: "N/A"
  tested: null
```

- {字段名} [{input/select/textarea/...}]
  ```yaml
  element:
    ref: "{ref}"
    type: "input"
    tc_ids: ["TC-010"]
    data_source: "后端API"
    tested: null
  ```
  - 🎯 focus → TC-010
  - 🎯 空值校验 → TC-011
  - 🎯 disabled → TC-012
  - 🎯 有效值填写 → TC-013
- [{提交按钮文本}] [button]
  ```yaml
  element:
    ref: "{ref}"
    type: "button"
    tc_ids: ["TC-014", "TC-015"]
    data_source: "前端静态"
    tested: null
  ```
  - 🎯 hover → TC-014
  - 🎯 click → TC-015
  - 🎯 loading → TC-016
  - 🎯 disabled → TC-017

#### 💬 {全局浮窗/Toast 名称}

```yaml
element:
  ref: "{ref}"
  type: "toast"
  tc_ids: ["TC-020", "TC-021"]
  data_source: "前端静态"
  tested: null
```

- 🎯 成功提示 → TC-020
- 🎯 失败提示 → TC-021

---

## TC-ID 索引（反向索引）

| TC-ID | 元素树路径 | 所在分册 |
|-------|-----------|---------|
| TC-001 | 📄 /dashboard → 🏗️ 操作区 → 🔘 [新增] → 🎯 click → 💬 [新增表单] | part-01 |
| TC-002 | 📄 /dashboard → 🏗️ 操作区 → 🔘 [新增] → 🎯 click → 💬 [新增表单] → 🔘 [提交] | part-01 |

---

## 修订记录

| 版本 | 日期 | 修订内容 | 触发阶段 |
|------|------|---------|---------|
| 1.0.0 | {YYYY-MM-DD} | 初始版本 | {prototype-design / kflow-design} |
