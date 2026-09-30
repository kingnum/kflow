# 恢复优先级链与流程规范

> **版本**: 1.0.0
> **来源**: core-mechanisms/06-recovery.md §12.2-12.3
> **适用范围**: kflow-resume Skill
> **加载层级**: 恢复层
> **适用阶段**: 仅恢复场景


## 1. checkpoint 文件存储（两级）

checkpoint 按操作级别分开存储：

### 1.1 变更级 checkpoint

位置：`docs/changes/{change}/checkpoints/`

```
docs/changes/{change}/checkpoints/
├── 20260430-143000-checkpoint.md       # 手动保存（设计/集成测试/归档阶段）
├── 20260430-150000-checkpoint-auto.md  # 自动保存
└── 20260430-163000-checkpoint.md       # 手动保存
```

### 1.2 子变更级 checkpoint

位置：`docs/changes/{change}/subchanges/{subchange}/checkpoints/`

```
docs/changes/{change}/subchanges/{subchange}/checkpoints/
├── 20260430-143000-checkpoint.md       # 手动保存（计划/编码/审查/测试阶段）
├── 20260430-150000-checkpoint-auto.md  # 自动保存
└── 20260430-163000-checkpoint.md       # 手动保存
```

### 1.3 归属规则

| 阶段 | checkpoint 级别 |
|------|-----------------|
| 设计探索、原型设计、详细设计 | 变更级 |
| 计划、编码、代码审查、接口单元测试、E2E测试 | 子变更级 |
| 集成测试、归档 | 变更级 |
| 缺陷修复 | 子变更级（从子变更测试触发） |

### 1.4 checkpoint 过期清理规则

| 规则 | 说明 |
|------|------|
| 自动 checkpoint 保留期限 | 7 天，超期自动删除 |
| 手动 checkpoint 保留期限 | 30 天，超期提示用户确认后删除 |
| 归档时清理 | 变更归档时删除所有关联 checkpoint |
| 变更废弃时清理 | 变更目录被删除时同步清理 checkpoint |

## 2. 恢复查找优先级链

```
恢复优先级链（由 kflow-resume 实施）:

优先级 1: 子变更级 checkpoint
  └── docs/changes/{change}/subchanges/*/checkpoints/*.md
      按 timestamp 降序，取最近

优先级 2: 变更级 checkpoint
  └── docs/changes/{change}/checkpoints/*.md
      按 timestamp 降序，取最近

优先级 3: 子变更 .status.md
  └── docs/changes/{change}/subchanges/*/.status.md
      读取各子变更的「当前阶段」和阶段状态矩阵

优先级 4: 变更级 .status.md
  └── docs/changes/{change}/.status.md
      读取「当前阶段」字段和阶段状态表

优先级 5: tasks.md (兜底)
  └── docs/changes/{change}/tasks.md
      从 checkbox 反推: 第一个有未勾选任务的阶段 = 当前阶段
```

在每一层命中后立即使用该层信息定位断点，不再继续向下查找。

## 3. 恢复流程（kflow-resume）

中断恢复由 `kflow-resume` Skill 实施，通过 `kflow-guide` 的 RESUME 路由触发。

```
kflow-resume 恢复流程:

┌─────────────────────────────────────────────────────────────┐
│                  RESUME WORKFLOW (kflow-resume)              │
├─────────────────────────────────────────────────────────────┤
│  1. VERIFY    → 变更存在性验证                                │
│  │   ├── docs/changes/{change}/ 目录存在？                    │
│  │   ├── 不在 docs/changes/archive/ 下？                              │
│  │   ├── 不存在 → 报错：变更不存在                             │
│  │   └── 已归档 → 报错：变更已归档，无法恢复                   │
│  2. STATE     → 按优先级链读取状态（见 §2 优先级链）          │
│  │   ├── Priority 1: 子变更 checkpoint → 最近 timestamp       │
│  │   ├── Priority 2: 变更级 checkpoint                       │
│  │   ├── Priority 3: 子变更 .status.md                       │
│  │   ├── Priority 4: 变更级 .status.md                       │
│  │   └── Priority 5: tasks.md checkbox 反推                  │
│  3. LOCATE    → 定位恢复断点                                  │
│  │   ├── 确定当前阶段                                         │
│  │   ├── 确定当前子变更（子变更级阶段时）                       │
│  │   ├── 确定待执行任务列表（未勾选 checkbox）                  │
│  │   └── 处理阶段回退状态（⚠️ 需修订 → 回退目标阶段）         │
│  4. GATE      → 快速门控验证                                  │
│  │   ├── 按当前阶段 Skill 的 gates.md 正向门控规则检查        │
│  │   ├── 门控通过 → 继续                                      │
│  │   └── 门控失败 → 提示缺失的前置条件                         │
│  5. SUMMARIZE → 输出恢复摘要                                  │
│  │   ├── 变更信息（描述、类型、项目类型）                       │
│  │   ├── 恢复断点（当前阶段、当前子变更、断点来源）             │
│  │   ├── 流程位置图（✅/🔄/⏳/⏭️/⚠️ 标注）                  │
│  │   └── 待执行任务列表                                       │
│  6. DISPATCH  → 直接调度阶段 Skill                            │
│      ├── 阶段 = ❌ 阻塞 → 输出阻碍信息，不调度                │
│      ├── 阶段 = ⚠️ 需修订 → 调度回退目标阶段                  │
│      └── 正常 → 按调度映射表调度对应阶段 Skill                 │
└─────────────────────────────────────────────────────────────┘
```

## 4. 调度映射表

| 当前阶段 | 调度 Skill |
|---------|-----------|
| 设计探索 | `kflow-explore` |
| 原型设计 | `kflow-prototype-design` |
| 详细设计 | `kflow-design` |
| 计划 | `kflow-plan` |
| 编码 | `kflow-code` |
| 代码审查 | `kflow-code-review` |
| 接口单元测试 | `kflow-api-test` |
| E2E测试 | `kflow-e2e-test` |
| 集成测试 | `kflow-integration-test` |
| 审计 | `kflow-audit` |
| 归档 | `kflow-archive` |

## 5. 触发方式

- 用户输入「继续 {change-name}」→ `kflow-guide` 识别 RESUME 模式 → 路由到 `kflow-resume`
- 用户输入「恢复 {change-name}」→ 同上
- 用户输入「继续」（无变更名）→ guide 按活跃变更数量判断后路由
