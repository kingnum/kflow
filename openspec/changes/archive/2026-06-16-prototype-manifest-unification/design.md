## Context

当前原型设计产物（prototype/ 目录）的下游消费方式存在耦合：

1. **输入表硬编码三个文件**：`kflow-plan`、`kflow-code`、`kflow-code-review` 的输入表直接写死 `prototype/index.html`、`prototype/design-tokens.css`、`prototype/element-coverage-tree.md`，假设产物结构固定。
2. **原型产物结构不可变**：不同原型设计 Skill（`huashu-design`、`frontend-design`）产出的文件数量和结构不同，但下游阶段无法感知差异。
3. **`prototype/index.md` 未被下游消费**：原型设计阶段已生成 `index.md`（原型索引），但下游输入表不包含它，形成了"有索引无人读"的断裂。

已有 86 处硬编码引用，分布在 10 个 SKILL.md 和 8 个设计文档中。

## Goals / Non-Goals

**Goals:**
- `prototype/index.md` 成为原型产物的**唯一消费入口**（Prototype Manifest），下游阶段通过读取它发现所有原型文件
- 移除下游输入表中对 `prototype/index.html`、`design-tokens.css`、`element-coverage-tree.md` 的硬编码引用
- 扩展 `index.md` 内容结构，新增「产物组织方式」和「共享资源清单」段落
- 门控检查和阶段钩子同步调整为检查 `prototype/index.md` 的存在性和完整性

**Non-Goals:**
- 不改变原型设计阶段本身的执行流程（huashu-design 委托、Playwright 验证等不变）
- 不改变后端子变更的输入源定义
- 不改变 `prototype/` 目录的产物组织规则（多文件结构、离线自包含约束等不变）
- 不改变代码审查阶段的原型对账逻辑（仅改输入获取方式）

## Decisions

### Decision 1: `prototype/index.md` 升级为 Prototype Manifest（而非新建文件）

**选择**：扩展现有 `prototype/index.md` 的内容结构，不新建 `prototype-manifest.json` 或 `prototype/manifest.md`。

**理由**：
- `index.md` 已存在且包含文件清单和页面清单，是天然入口
- 新增两个段落即可覆盖所有消费场景
- 避免引入新概念增加复杂度

**备选方案**：新建 `prototype-manifest.json`（结构化但需解析 JSON）、新建 `prototype/manifest.md`（语义更明确但增加文件数量）。

### Decision 2: `prototype/index.md` 新增「产物组织方式」和「共享资源清单」段落

在 `index.md` 现有四个段落（文件清单、页面清单、设计系统引用、修订记录）之间插入：
- **「产物组织方式」**：描述本次原型的文件结构（单文件/多页面/含共享资源）、入口文件路径
- **「共享资源清单」**：列出 `shared/` 子目录下的共享样式、组件、状态管理器等资源

### Decision 3: 下游阶段输入表统一为 `prototype/index.md`

**规则**：
- 前端SC 的输入表中，原型相关行合并为一行：`prototype/index.md`（✅ 必须，前端SC）
- 输入限定规则改为：前端子变更 SHALL 仅使用 `prototype/index.md` 中声明的原型产物，SHALL NOT 读取 `prototype/design-prompt.md` 或 `design-system/MASTER.md`
- 执行流程中的文件引用改为：从 `prototype/index.md` 获取文件列表后按角色动态读取

### Decision 4: 门控检查从"三文件检查"改为"清单完整性检查"

**当前**：分别检查 `index.html` 存在、`design-tokens.css` 存在、`element-coverage-tree.md` 存在。

**改为**：检查 `prototype/index.md` 存在，且其「原型文件清单」中包含 `index.html`（或入口文件）条目。降级情况仍从 `prototype/*.html` 中提取缺失信息。

### Decision 5: 阶段钩子（phase-hooks.md）RELOAD 列表统一

**当前**：PRE_HOOK 和 RELOAD 分别列出三个原型文件。

**改为**：RELOAD 列表统一为 `prototype/index.md`（条件，前端SC）。阶段执行时读取 index.md 后按需加载具体文件。

### Decision 6: `index.md` 新鲜度由阶段边界保证

**规则**：`prototype/` 目录的写权限仅限于原型设计阶段（kflow-prototype-design）。其他阶段（plan、code、code-review、e2e-test 等）对 `prototype/` 目录**只读**，不得修改其中任何文件。

**`index.md` 更新时机**：
- 原型设计阶段结束时（用户确认通过）：自动生成/更新 `index.md`
- 原型设计修订循环结束时（新一轮用户确认通过）：重新生成 `index.md`
- code 阶段回退到原型设计阶段触发修订时：修订完成后更新 `index.md`

**不需要额外的新鲜度校验**：阶段边界保证了其他阶段不会修改 `prototype/` 目录，因此 `index.md` 在下游阶段读取时必然是最新的。其他阶段若发现原型有问题，应通过回退到原型设计阶段处理，不得直接修改产物。

## Risks / Trade-offs

**[Risk] 原型设计阶段未生成或更新 index.md** → Mitigation：门控检查验证 index.md 存在性，缺失时阻塞而非降级。

**[Risk] 不同原型 Skill 产出的 index.md 格式不一致** → Mitigation：扩展 index.md 模板（`docs/designs/templates/changes/{change}/prototype/index.md`）为强制格式，所有原型 Skill 须遵守。

**[Risk] 代码审查等阶段对 `design-tokens.css` 的直接引用需要保留** → Mitigation：代码审查阶段的对账逻辑不变，但获取 `design-tokens.css` 路径的方式改为从 `prototype/index.md` 清单中读取，而非硬编码路径。

**[Risk] 回退到原型设计阶段后 index.md 未及时更新** → Mitigation：原型修订后（用户再次确认通过），系统自动重新生成 design-tokens.css、element-coverage-tree.md，并同步更新 index.md 的文件清单和版本号。回退流程中此步骤为强制环节。
