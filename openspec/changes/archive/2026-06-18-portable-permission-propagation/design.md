## Context

上一个变更 `flexible-repetition-subagent-enforcement` 在本项目（kflow-devflow-skills）中创建了 `.claude/settings.json`，预配置了 16 条 kflow 所需权限，解决子代理后台运行因权限不足而失败的问题。

当前状态：

```
本项目（kflow-devflow-skills）
├── .claude/settings.json        ← 硬编码 16 条权限（手动创建）
├── .claude/settings.local.json  ← 开发过程中积累的细粒度权限
└── .claude/skills/kflow-*/     ← Skills 代码

打包分发（package-skills.sh）
├── .claude/skills/kflow-*/     ← ✅ 包含
└── .claude/settings.json        ← ❌ 不包含

目标项目
├── .claude/skills/kflow-*/     ← 解压得到
└── .claude/settings.json        ← 不存在 → 子代理无权限
```

此外，`kflow-shared/repetition-model.md §12.5` 硬编码了权限列表，`subagent-enforcement-notice` 和 `subagent-isolation-rule` 两个 specs 要求"项目 SHALL 预配置 `.claude/settings.json`"，但这些只是规范性要求，没有自动化执行机制。

## Goals / Non-Goals

**Goals:**

1. 权限声明跟随 Skill 分发——`kflow-shared/permission-model.md` 作为权限的 source of truth，随打包分发到所有目标项目
2. kflow-init 自动配置目标项目权限——读取声明后生成 `.claude/settings.json`，幂等合并不覆盖
3. 后台子代理权限失败时自动回退前台子代理——韧性机制，不依赖权限配置是否完美
4. 消除本项目硬编码的 `settings.json`——改为 kflow-init 生成

**Non-Goals:**

1. 不支持 Claude Code 之外的 AI 工具权限适配（当前无其他工具有标准化权限配置机制，`permission-model.md` 预留环境适配指引节但暂不实现具体适配逻辑）
2. 不修改 `package-skills.sh` 打包逻辑（权限声明在 `kflow-shared/` 目录下，已在打包范围内）
3. 不引入 `allowed_tools` 等尚不稳定的子代理权限控制参数
4. 不改变前台子代理的默认推荐策略（前台模式仍为推荐首选）

## Decisions

### Decision 1：权限声明的载体——`kflow-shared/permission-model.md`

**选择**：在 `kflow-shared/` 下新增 `permission-model.md`，定义权限清单和配置规则。

**备选方案**：
- A. 每个 SKILL.md 的 frontmatter 中声明 `required_permissions` → 权限分散在各文件中，聚合复杂，且 frontmatter 无此标准字段
- B. 独立的 `permissions.json` 配置文件 → 增加文件类型复杂度，不如 Markdown 与现有体系一致
- C. `kflow-shared/permission-model.md`（选中）→ 集中定义，跟随打包分发，与现有 shared 文件体系一致

**理由**：
- `kflow-shared/` 已有 9 个共享机制文件，权限模型加入其中最自然
- 已在 `package-skills.sh` 打包范围内（`kflow-*/` 通配包含 `kflow-shared/`）
- 集中定义比分散在各 SKILL.md 中更容易维护和聚合

**文件结构**：
```
kflow-shared/permission-model.md
├── §1 全局必需权限
│   ├── Bash 工具类权限清单
│   ├── 文件操作类权限清单
│   ├── 子代理调用权限
│   └── 文档查询权限
├── §2 权限聚合规则
│   └── kflow-init 读取本声明后合并为 settings.json 的规则
├── §3 环境适配指引
│   ├── Claude Code → .claude/settings.json 格式映射
│   └── 其他工具 → 待定义（预留节）
└── §4 权限配置幂等规则
    ├── 检测已有 settings.json
    ├── 合并策略（追加缺失，不覆盖已有）
    └── 重复执行不重复添加
```

### Decision 2：kflow-init 权限配置步骤的插入位置

**选择**：在 SCAN 步骤之后、MATCH 步骤之前插入新的 PERM_CONFIG 步骤。

**备选方案**：
- A. 在 SCAN 步骤中合并 → SCAN 已有三层感知逻辑，再加权限配置会职责不清
- B. 在 OUTPUT 步骤后 → toolchain.md 已输出，权限配置结果无法体现在 toolchain.md 中
- C. SCAN 之后、MATCH 之前（选中）→ 权限配置完成后，MATCH 步骤可以基于已配置的权限做更准确的工具推荐

**理由**：
- 权限配置影响后续所有阶段的子代理执行能力
- 配置完成后，MATCH 步骤可感知权限状态（如某些工具需要特定 Bash 权限才能运行）
- toolchain.md 可以输出权限配置状态

**流程变更**：
```
原流程: DETECT → SCAN → PROFILE → MATCH → GAP → COMPAT → ...
新流程: DETECT → SCAN → PROFILE → PERM_CONFIG → MATCH → GAP → COMPAT → ...
                                            ↑ 新增
```

### Decision 3：权限配置的用户确认策略

**选择**：创建或修改 settings.json 前，通过 AskUserQuestion 征求用户同意。

**理由**：
- settings.json 是项目级配置，自动修改可能影响其他团队成员
- 用户可能有意不配置某些权限（安全考虑）
- 与 kflow-init 现有的用户确认模式一致（方案选择、git init 均需确认）

**确认场景**：
```
settings.json 不存在:
  → AskUserQuestion: "检测到项目尚未配置 kflow 所需权限，是否自动创建 .claude/settings.json？"
  → 选项: 「创建」「跳过」

settings.json 存在但缺少部分权限:
  → AskUserQuestion: "检测到缺少 {N} 项 kflow 所需权限（{权限列表}），是否追加？"
  → 选项: 「追加缺失权限」「跳过」

settings.json 已齐全:
  → 无需确认，输出"权限配置齐全"即可
```

### Decision 4：后台子代理权限失败回退机制

**选择**：主 Agent 检测到后台子代理因权限失败时，自动创建新的前台子代理重新执行同一任务。

**备选方案**：
- A. 后台失败后标记阻塞，等待用户处理 → 用户体验差，中断执行流
- B. 后台失败后主 Agent 接管执行 → 违反子代理隔离规则，丧失独立性优势
- C. 后台失败后创建前台子代理重新执行（选中）→ 遵守隔离规则，前台模式权限限制更宽松

**理由**：
- 前台子代理在交互式会话中，权限不足时可实时请求用户批准，因此成功概率更高
- 创建新的子代理（而非主 Agent 接管）遵守 `kflow-shared/repetition-model.md §12` 的隔离规则
- 回退不计入轮次级重试的 3 次上限——因为是执行模式切换，不是同一模式的重试

**权限错误模式检测**：
```
主 Agent 从子代理错误输出中匹配以下模式:
├── "permission denied" / "权限不足"
├── "not allowed" / "不允许"
├── "requires approval" / "需要批准"
├── "blocked" / "被阻止"
└── 错误信息包含工具名 + 拒绝语义（如 "Bash command blocked"）
```

**回退执行规则**：
```
1. 主 Agent 输出提示: "检测到子代理因权限问题失败，创建前台子代理重新执行"
2. 构建与原后台子代理相同的 prompt（任务内容、轮次上下文）
3. 调用 Agent 工具: run_in_background=false
4. 前台子代理成功 → 正常继续，更新 .status.md 记录
5. 前台子代理也失败 → 标记 ⚠️ 阻塞，提示用户
6. 主 Agent SHALL NOT 在任何情况下直接接管执行
```

### Decision 5：删除本项目硬编码的 settings.json

**选择**：变更完成后删除 `.claude/settings.json`，通过 kflow-init 重新生成验证。

**理由**：
- 硬编码的 settings.json 是上个变更的临时方案，应被自动生成机制替代
- 保留它会导致混乱——开发者不确定权限配置来自手动创建还是 init 生成
- `.claude/settings.local.json` 保留不变（用户本地开发配置，不属于 Skill 体系）

## Risks / Trade-offs

### [风险] 权限错误模式检测可能误判 → 缓解：模式列表保守，仅匹配高置信度错误

主 Agent 依赖文本匹配来判断子代理是否因权限问题失败。Claude Code 的错误信息格式可能随版本变化，导致检测失效或误判。

缓解：
- 错误模式列表保守，仅包含明确的权限拒绝语义
- 非权限错误走原有轮次级重试机制，不会因误判而跳过重试
- 如果匹配到权限错误但前台子代理也失败，仍然标记阻塞而非无限循环

### [风险] kflow-init 修改目标项目的 settings.json → 缓解：用户确认 + 合并不覆盖

自动修改项目配置文件可能影响其他团队成员或覆盖用户有意配置的规则。

缓解：
- 创建或修改前必须 AskUserQuestion 征得用户同意
- 合并策略仅追加缺失权限，不删除或修改已有条目
- 用户可选择跳过，不强制配置

### [权衡] permission-model.md 当前仅支持 Claude Code 环境适配

虽然设计了环境适配指引节，但当前只实现了 Claude Code 的 settings.json 格式映射。其他 AI 工具的适配是空架子。

这是可接受的权衡——当前团队仅使用 Claude Code，过早适配其他工具是 YAGNI。`permission-model.md` 预留了结构，未来需要时只需补充 §3 中的具体映射规则。

### [权衡] 权限回退机制是 Skill 层面的规范，不是代码级保障

后台子代理权限失败回退前台子代理的机制，是通过 `repetition-model.md` 和 SKILL.md 中的规范文本约束主 Agent 行为，而非代码级的强制执行。

这是可接受的权衡——Claude Code 的 Skill 体系本质上是 prompt 工程，所有规则都通过规范文本约束。与现有的子代理隔离规则（§12）一致性良好。
