## Context

当前 `kflow-prototype-design` 使用 Pencil MCP 生成 `.pen` 格式原型。`.pen` 是加密封闭格式，三个架构性缺陷：

1. **不可合并**：加密格式无法 diff/merge，导致原型无法累积到产品级
2. **不可复用**：每个变更从零画起，组件无法跨变更共享
3. **不可验证**：静态设计无法程序化验证交互正确性

Huashu-Design (`alchaincyf/huashu-design`) 是一套完整可用的 HTML 原型 Skill，产出纯文本 HTML、可交互、可组合。本次替换用 huashu-design 作为执行引擎，`kflow-prototype-design` 作为编排层委托调用。

## Goals / Non-Goals

**Goals:**
- 用 HTML 替代 Pencil 作为原型媒介，huashu-design 作为执行引擎
- 建立产品级原型目录 `docs/prototype/`，实现原型跨变更累积
- 归档时自动合并变更原型到产品级
- 新变更启动时自动加载产品级原型上下文，基于已有设计扩展
- `kflow-init` 检测 huashu-design 可用性

**Non-Goals:**
- 不改变纯后端项目自动跳过原型设计的逻辑
- 不改变阶段门控机制的核心架构
- 不复制 huashu-design 内容到 kflow-prototype-design（委托调用，非内化吸收）

## Decisions

### D1: 架构模型 — 委托调用，非内化吸收

```
kflow-prototype-design (编排层)
├── 阶段门控 + 状态管理 + 用户评审
├── 产品级上下文加载
├── prompt 上下文组装
└── Skill("huashu-design", prompt) → 执行层
```

**为什么不是内化吸收**：huashu-design 是一套持续更新的完整 Skill（60KB+ SKILL.md + assets/ + scripts/ + references/），内化会导致内容膨胀、维护分离、Token 浪费。

### D2: 委托调用的 prompt 组装

传给 huashu-design 的上下文，按存在性分为：

```
✅ 必然存在（前置阶段产物）:
  ├── functional-designs/index.md      → 提取产品概述
  ├── functional-designs/part-NN.md    → 提取 UI 功能点清单
  └── 产出路径: docs/changes/{change}/prototype/index.html

🔶 条件存在（看项目历史 + 变更类型）:
  ├── docs/prototype/design-tokens.css → 已有设计令牌
  ├── docs/prototype/screens/          → 已有屏幕清单
  ├── docs/prototype/index.html        → 产品级全貌
  └── brand-spec.md                    → 品牌资产（涉及品牌时）
```

prompt 模板：

```
做一个交互原型:

## 项目背景
{从 functional-designs/index.md 提取}

## 需要设计的屏幕
{从 functional-designs/ 提取的 UI 功能点清单}

## 设计约束
- CSS 变量: {design-tokens.css 或 "无，请建立"}
- 已有屏幕: {screens/ 清单 或 "无，这是首次原型设计"}
- 新屏幕需能挂入产品级导航 index.html

## 品牌资产
{brand-spec.md 或 "不涉及"}

## 产出要求
- 输出到 docs/changes/{change}/prototype/index.html
- 产出类型: {App交互原型 / Web页面 / 多屏平铺}
```

### D3: 迭代循环 — huashu-design 内部自行迭代

采用方案 A：一次委托，huashu-design 内部执行自己的 Junior Designer 迭代，完成后返回最终产物。用户评审在 kflow-prototype-design 层做：

```
DESIGN → Skill("huashu-design", prompt)
       → huashu-design 内部: placeholder → show → full pass
       → 返回产物
       ↓
REVIEW → AskUserQuestion "原型是否通过?"
       ├─ 确认通过 → COMPLETE → kflow-guide 引导下一阶段
       └─ 需修订   → 收集反馈 → 回到 DESIGN (再次调用 huashu-design)
```

### D4: 产品级原型目录

```
docs/prototype/
├── index.html              # 总导航（卡片网格，按模块分组）
├── design-tokens.css       # CSS 变量（色板/字号/间距/圆角/阴影）
├── screens/                # 所有屏幕原型
├── components/             # 共享组件
└── assets/                 # 共享素材
```

### D5: 原型合并算法（归档时）

| 变更产物 | 产品级已有 | 处理 |
|---------|-----------|------|
| 新屏幕 | 不存在 | 复制到 `screens/` |
| 修改屏幕 | 已存在 | 用户确认后覆盖 |
| 新组件 | 不存在 | 复制到 `components/` |
| 新 CSS 变量 | 不存在 | 追加到 `design-tokens.css` |
| 变更索引 | - | 更新 `index.html` 导航 |

### D6: kflow-init 检测

```
检测 .claude/skills/ 或项目 skill 目录下是否存在 huashu-design
  ├── 存在 → 记录"huashu-design: ✅ 可用"
  └── 不存在 → 提示: npx skills add alchaincyf/huashu-design
```

`kflow-prototype-design` CHECK 步骤中硬拦截：huashu-design 不可用时标记 ⚠️ 阻塞，给出安装命令。

## Risks / Trade-offs

- **huashu-design 未安装阻塞原型设计**: kflow-init 主动检测 + CHECK 步骤硬拦截，给出明确安装命令
- **huashu-design 上游更新**: 通过 prompt 传递具体需求上下文，减少对特定触发词格式的依赖
- **产品级原型膨胀**: index.html 按模块分组，超过 50 屏时建议拆分

## Migration Plan

1. 更新 `kflow-init`，新增 huashu-design 可用性检测
2. 完全重写 `kflow-prototype-design` SKILL.md（编排层，委托调用模式）
3. 更新 `docs/designs/skills/kflow-prototype-design.md` (v2.0.0)
4. 更新 `docs/designs/core-mechanisms.md`（产物路径）
5. 更新 `docs/designs/index.md`（Skill 描述）
6. 更新 `docs/designs/skills/kflow-design.md`（输入来源）
7. 更新 `kflow-archive`（原型合并步骤）
8. 删除 `references/rules/pencil-design-style.md`
9. 已有 `.pen` 文件保留在历史归档中，不转换

## Open Questions

- huashu-design 委托调用时的具体工具选择（`Skill` 工具直接 invoke vs `Agent` 启动子代理），取决于 huashu-design 在目标 Agent 环境中的安装形态
