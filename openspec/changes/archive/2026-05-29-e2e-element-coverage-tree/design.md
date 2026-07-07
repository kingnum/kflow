## Context

当前系统中，原型设计与 E2E 测试之间通过两个分散文件桥接：

```
prototype/element-spec.md  →  kflow-code (编码约束) + kflow-code-review (对账)
prototype/nav-tree.md      →  kflow-code (路由约束) + kflow-code-review (路由对账)
prototype/index.html       →  kflow-e2e-test (仅视觉一致性对比)
```

存在三个问题：

1. **E2E 测试用例缺乏系统化的元素级输入**：design 阶段编写 e2e-tests/ 时，没有强制机制从原型中穷举所有交互元素并确保每个元素都有对应测试场景
2. **element-spec.md 信息不完整**：缺少交互状态（hover/focus/loading/empty/error/disabled）、操作驱动的动态元素（浮窗/下拉/弹窗/Toast）、页面跳转链路
3. **产物分散**：页面结构信息（nav-tree.md）和元素信息（element-spec.md）分离，E2E 测试用例需要同时参考两个文件

本次变更引入 `element-coverage-tree.md` 作为统一产物，替代 element-spec.md 和 nav-tree.md，并按探索来源分两种情况生成。

## Goals / Non-Goals

**Goals:**
- 统一产物：用一个树状文件替换 element-spec.md + nav-tree.md，包含页面导航、元素清单、交互状态、操作链
- 强制覆盖：design 阶段门控检查树中每个元素+状态都有对应 TC-ID
- 动态验证：e2e-test 执行阶段每轮加载树并统计元素触达率，未触达 = 回归信号
- 双路径生成：有原型时解析 prototype HTML，无原型时 playwright-cli 探索实际页面
- 维护清晰：每次进入 design 阶段确认树的时效性，支持重新生成或增量更新

**Non-Goals:**
- 不改变纯后端项目的 E2E 跳过逻辑
- 不修改 e2e-tests/part-NN.md 的核心测试场景格式（仅新增元素引用字段）
- 不影响 prototype-design 阶段的 DESIGN/VERIFY/REVIEW 流程（仅修改 COMPLETE 步骤）
- 不改变 traceability.md 的 FP 级覆盖矩阵（元素树是互补维度）

## Decisions

### D1: 文件统一——element-spec.md + nav-tree.md → element-coverage-tree.md

**选择**: 废弃 element-spec.md，nav-tree.md 内容合并入 element-coverage-tree.md。

**理由**: element-spec.md 的信息（按钮/表单/弹窗清单）是元素覆盖树的子集；nav-tree.md 的信息（页面可达关系）可作为树的顶层骨架。两个文件各自不完整，合并后一个文件即可同时服务于 code 约束、code-review 对账、E2E 测试覆盖三个消费场景。

**替代方案**: 保留 element-spec.md + nav-tree.md，新增第三个文件做 E2E 覆盖。被拒绝理由：三个文件的信息高度重叠，维护成本高，一致性难以保证。

**落点规则**:

| 条件 | 落点 |
|------|------|
| prototype/index.html 存在 | `prototype/element-coverage-tree.md`（树在原型目录下，e2e-tests 引用） |
| 无 prototype + 前端项目 | `e2e-tests/element-coverage-tree.md`（树在 E2E 目录下） |
| 纯后端项目 | 无 |

### D2: 双路径探索——静态解析 vs playwright-cli 探索

**选择**: 按 prototype 是否存在分两条生成路径。

**路径 A — 有原型（静态 HTML 解析）**:
```
prototype-design COMPLETE:
  1. 解析 prototype/*.html 的 DOM 树
  2. 提取所有交互元素: <button>, <a>, <input>, <select>, <textarea>, <dialog>, [role="dialog"]
  3. 提取 CSS 伪类状态: :hover, :active, :focus, :disabled（通过扫描 stylesheet 和内联 style）
  4. 提取 JS 事件绑定: onclick, addEventListener, @click（Vue）, onClick（React）
  5. 构建初始树（含页面导航 + 元素 + 状态 + 操作链，TC-ID 列为空）
  6. 输出 prototype/element-coverage-tree.md
```

**路径 B — 无原型（playwright-cli 动态探索）**:
```
kflow-design §7.1 EXPLORE:
  1. 读取路由配置获取全部页面路径
  2. 逐页 playwright-cli 探索:
     a. open {url} → waitForLoadState → snapshot 获取静态元素
     b. 逐个按钮 click → snapshot 观察变化（弹窗/下拉/跳转）
     c. 逐个 input focus + fill → 观察校验状态和建议列表
     d. 逐个 hover 触发元素 → 观察 tooltip/popover
     e. 表单: 空提交（观察校验错误）、合法提交（观察成功反馈+跳转）
     f. 网络监听: page.on('response') → 提取 API 调用路径
  3. 汇总构建 e2e-tests/element-coverage-tree.md（含 TC-ID 映射）
```

**理由**: 原型 HTML 是静态声明式的，DOM 解析 + CSS/JS 扫描足够覆盖；实际前端页面是动态渲染的 SPA，只有 playwright-cli 能捕获完整真相。不做降级方案（如静态分析前端源码），因为遗漏的返工成本远高于探索成本。

### D3: 树结构设计——四层 + 操作链

**选择**: 页面 → 区域 → 元素 → 状态 四层结构，状态节点下挂操作链。

```
📄 <页面路径>
├── 🏗️ <区域名称>
│   ├── 🔘 <元素描述> [<元素类型>]
│   │   ├── 🎯 <状态名> → <TC-ID>
│   │   │   ├── 💬 <产生的浮窗名>
│   │   │   │   ├── 🔘 <浮窗内元素> → <TC-ID>
│   │   │   │   └── ...
│   │   │   └── 🔗 跳转 → 📄 <目标页面>
│   │   └── 🎯 <另一状态> → <TC-ID>
│   └── 📝 <表单名>
│       ├── <字段名> [input/select/...]
│       │   ├── 🎯 focus → <TC-ID>
│       │   ├── 🎯 空值校验 → <TC-ID>
│       │   └── 🎯 disabled → <TC-ID>
│       └── <提交 button>
│           ├── 🎯 hover → <TC-ID>
│           ├── 🎯 loading → <TC-ID>
│           └── 🎯 disabled → <TC-ID>
└── 💬 <全局浮窗/Toast>
    ├── 🎯 成功 → <TC-ID>
    └── 🎯 失败 → <TC-ID>
```

**符号约定**:

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

**树节点元数据**（每个叶子节点附带）:

```yaml
# 每个元素/状态节点
element:
  ref: "原型 ref 或 playwright snapshot ref"  # 元素定位引用
  type: "button|input|select|link|dialog|toast|..."
  tc_ids: ["TC-001", "TC-003"]                # design 阶段填充
  data_source: "后端API|前端静态|配置控制|浏览器存储"  # 可选，e2e-data-tracing 扩展
  tested: null                                  # e2e-test 阶段标记: null/✅/❌
```

**理由**: 四层结构在完整性和可维护性间取得平衡。三层（页面→元素→状态）太粗，无法表达页面内的分区组织；五层太细，维护负担大于收益。操作链显式建模解决了"点按钮后出现的浮窗可能被遗漏"的核心痛点。

### D4: 覆盖率语义——100% 是基线，不是目标

**选择**: design 阶段 TC-ID 覆盖率 = 100%（硬性门控），e2e-test 执行阶段每轮元素触达率预期 = 100%（回归检测器）。

**不是**: 10 轮逐步爬坡覆盖——每轮都应触达全部元素。如果 Round 1 触达率 < 100%，说明测试用例设计有遗漏（回退 design）或服务异常。

```
覆盖率检查点:

design 阶段 (静态):
  ├── 所有元素+状态有 TC-ID → 100%（门控通过）
  └── 存在元素无 TC-ID → 门控阻塞，输出未覆盖清单

e2e-test 阶段 (动态):
  Round 1:  触达 156/156 → 100% ✅
  Round 2:  触达 154/156 → ⚠️ 回归信号
             未触达: [批量删除 button]（批量操作栏未出现，bug）
                     [搜索建议下拉]（/api/suggest 500，服务异常）
  ...
  Round 10: 触达 156/156 → 100% ✅ 稳定
```

**理由**: 多轮测试的目的是发现间歇性 bug 和验证修复不引入回归，不是"分工覆盖元素"。每轮都跑全部用例，每轮都应触达全部元素。

### D5: 树的维护策略

**选择**: 每次进入 design 阶段时确认树的时效性。

```
kflow-design §7.0 (CHECK 之后):
  1. 检测树文件是否存在
  2. 若存在:
     a. 读取树的生成时间戳
     b. 有 prototype → 比对 prototype/index.html 修改时间
     c. 若源头已更新 → AskUserQuestion:
        "元素覆盖树可能已过期。是否重新生成？"
        选项: [重新生成] [增量更新] [保持不变]
  3. 若不存在:
     a. 有 prototype → 解析生成（路径 A）
     b. 无 prototype → playwright-cli 探索生成（路径 B）
  4. 进入 §7.1 EXPLORE（如有需要）或 §7.2 DESIGN（直接使用现有树）
```

**理由**: prototype-design 修订模式允许原型在 design 阶段后重新调整，design 阶段自身也可能发现设计缺陷需要回退。在 design 阶段入口处做时效性检查，而非假设树永远是最新的。

## Risks / Trade-offs

- **[风险] 静态 HTML 解析（路径 A）可能遗漏 JS 动态生成的元素** → 缓解：prototype-design 阶段的 Playwright 5 轮验证已确保所有交互按钮/链接可达，遗漏概率低；如仍有遗漏，e2e-test 执行阶段的动态验证（Round 1 触达率 < 100%）会暴露
- **[风险] playwright-cli 逐页探索（路径 B）耗时长** → 缓解：探索在 design 阶段的子代理中执行，不阻塞用户交互；探索结果（树 + TC 映射）为后续 10 轮测试提供精确导航，减少测试阶段的元素侦查时间，总体净节省
- **[权衡] element-spec.md 废弃影响 code/code-review 阶段** → 缓解：element-coverage-tree.md 包含 element-spec.md 的全部信息（按钮/表单/弹窗清单），code-review 的对账逻辑从读取 element-spec.md 改为读取 element-coverage-tree.md 即可
- **[风险] 大变更的树可能过于庞大** → 缓解：树按页面组织，每个页面独立子树，FP > 20 时按子变更分区标注；e2e-test 阶段子代理可按子变更过滤相关页面子树
