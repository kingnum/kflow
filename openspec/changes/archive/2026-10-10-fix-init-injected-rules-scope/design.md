# Design

## Context

见 `proposal.md` — Why。设计层需要处理的既存约束：

- `kflow-init` 的 SKILL.md 内嵌三段注入模板（Marker 1「项目画像」、Marker 2「变更流程强制规则」、Marker 3「Skill 改进建议自动捕获」），由 AI 读取模板后写入消费方 CLAUDE.md。模板文本是运行时产物，不是设计文档的副本——因此设计文档与 SKILL.md 必须同批修改，否则下次任一侧被单独编辑时泄漏会复发。
- 消费方 CLAUDE.md 的既有注入区块由已发布的旧版模板生成，无法追溯其内容。修正必须对存量项目生效，不能只对新项目生效。
- 本仓库无 CI 流程，既有校验均为手动运行的脚本模式（`scripts/sync-references.sh`、`scripts/validate-frontmatter.py`、`scripts/package-skills.sh`），新校验须与之一致。
- `.claude/skills/` 下未注册任何 `kflow-*` Skill 副本（仅 `grilling`、`skill-creator`、`to-spec`），本变更的运行时载体为 `skills/kflow-init/SKILL.md`，不涉及 `.claude/skills/` 同步。

## Goals / Non-Goals

**Goals:**

- 让「变更流程强制规则」section 的职责边界在模板、设计文档、规格三处表述一致——只承载路由约束、用户接口约定与流程概览。
- 让修正对存量消费方项目可自愈：`re-init` 必须能替换掉含旧规则的区块，无需用户手工清理。
- 为注入模板建立可运行的开发态词汇校验，使同类泄漏在提交前即可被脚本拦下。

**Non-Goals:**

- 不改变 `kflow-archive` 归档后的 git commit 行为，不改变 `kflow-init` 步骤 13 的 git 仓库检测行为。
- 不改变本仓库 `/opsx:archive` 的版本自增与打包流程（`unified-version`、`skill-packaging` 保持原样）。
- 不重构 Marker 1「项目画像」的字段与扫描逻辑。
- 不引入 CI 平台配置，校验以可手动运行的脚本形态交付。

## Decisions

### 决策 1：区块版本标识改用 kflow-init 自身的 `version` 字段

Marker 区块头部的版本行由 `> **版本**: 参见 VERSION 文件（统一版本管理）` 改为 `> **模板版本**: {kflow-init 的 version 值}`，取值来自 `skills/kflow-init/SKILL.md` front matter 的 `version` 字段（在消费方为 `.claude/skills/kflow-init/SKILL.md`）。

- **理由**：该字段由 `scripts/sync-version.sh` 统一维护，随 Skills 体系版本递增；`re-init` 时 AI 可直接从自身 SKILL.md 读到，消费方无需存在任何额外文件。原表述指向消费方不存在的 `VERSION` 文件，判据无法解析，是修复无法抵达存量项目的直接原因。
- **替代方案（未采用）**：保持字面量版本号（如 Marker 3 的 `1.0.0`）。字面量需随模板变更手工递增，漏改即静默失效；front matter 版本由脚本统一同步，无漏改面。
- **替代方案（未采用）**：以区块内容与模板渲染结果比对作为唯一判据。该方案同样鲁棒，但会使「版本一致仅更新时间戳」的既有语义失去落点，且无法回答"该区块由哪个版本生成"。版本标识另有可读性价值。

### 决策 2：替换判据含兜底分支，旧版无版本行一律替换

替换判据三态：

```
读取区块版本行
  ├── 未能读到版本行（旧版模板产物 / 用户删改） -> 视为版本不同 -> 全量替换
  ├── 读到但无法解析为版本号                   -> 视为版本不同 -> 全量替换
  ├── 读到且等于当前 version                   -> 仅更新生成时间戳
  └── 读到且不等于当前 version                 -> 全量替换
```

- **理由**：存量消费方 CLAUDE.md 中的区块由旧模板生成，其中版本行引用 `VERSION` 文件，解析必然失败——走上分支即被替换，修复因此对所有存量项目生效，无需用户手工删除区块。
- **替代方案（未采用）**：仅比对版本号，无兜底分支。旧版区块因解析失败会被判定为"无变化"，修复对存量项目静默失效。

### 决策 3：项目自定义规则使用独立 marker `## 项目自定义规则`

`kflow-init` 在首次注入时创建 `## 项目自定义规则` 区块（含"本区块由项目自行维护，kflow-init 不覆盖"说明），此后任何 `re-init` 均不读取、不修改、不删除该区块。

- **理由**：框架区块是全量替换语义，用户若把自有规则写进框架区块内必然被覆盖——这是本次"用户无法自救"的成因。给出一个框架明确不触碰的区块，把"框架管理的"与"项目维护的"在结构上分开。
- **边界**：marker 边界识别（marker 行到下一个 `## ` 之前）保持不变；该区块不参与版本比较。

### 决策 4：作用域校验作为独立脚本交付

新增 `scripts/validate-injection-scope.sh`，从 `skills/kflow-init/SKILL.md` 中提取三段注入模板代码块，对开发态词汇黑名单匹配，命中即输出词汇与行号并以非零状态退出。

黑名单词汇：`scripts/sync-version.sh`、`scripts/package-skills.sh`、`targets/`、`VERSION 文件`、`README` 版本条目（版本条目相关表述）、`README.md` 的版本行。

- **理由**：脚本职责单一（扫描注入模板的开发态词汇），与 `sync-references.sh`（references 副本间差异比对）语义不同，并入会使两个用途的失败信息互相干扰。
- **替代方案（未采用）**：并入 `scripts/sync-references.sh`。该脚本的归一化逻辑（skill 路径段改写）与模板提取逻辑无关，合并后单文件承担两类不相关检查。
- **替代方案（未采用）**：并入 `scripts/validate-frontmatter.py`。后者校验 front matter 结构，与正文模板内容无关。
- **空集保护**：未提取到任何模板块时以非零状态退出，避免"无输入即通过"的假阴性（与 `package-skills.sh` 的同类保护一致）。

### 决策 5：移除的 git 规则不设替代规则

「变更流程强制规则」section 收敛为 6 条，不新增任何替代 git 规则。

- **理由**：归档后 git commit 询问已由 `kflow-archive` 步骤 11 COMMIT 在运行时完成，非 git 仓库时的 git init 询问已由 `kflow-init` 步骤 13 GITINIT 完成。二者均不需要 CLAUDE.md 背书，写入即为双重定义。
- **后果**：消费方项目不再从 CLAUDE.md 获知"归档后会询问是否提交"。该信息属于 skill 运行时的自我说明，其可见性由 `kflow-archive` 的 SKILL.md 与运行时提示承担。

### 决策 6：规格重复定义收敛至 `init-claude-md-injection`

`devflow-init` 的「变更流程强制规则 section 扩展」Requirement 整体移除，CLAUDE.md marker 注入规则统一由 `init-claude-md-injection` 承载（含 Marker 3 注入与项目自定义区块保护）；`devflow-init` 保留工具推荐矩阵与 GAP 检测。

- **理由**：同一 CLAUDE.md marker 的内容要求由两个能力分别定义，是本次泄漏未被及时发现的结构原因——改动模板时只有一处被想起。
- **替代方案（未采用）**：仅从两个 spec 中各删 git 规则、保留双份定义。消除不了重复定义本身，同类问题会再次出现。

## Risks / Trade-offs

- [项目自定义区块对存量项目不存在，首次创建于 CLAUDE.md 位置不定] → 创建规则与既有区块一致（追加到 CLAUDE.md 末尾），并在区块内标注用途；不强制用户迁移已有自定义内容。
- [版本号递增但模板内容未变时，区块仍会全量替换（重写时间戳与相同内容）] → 接受。替换的是框架自有内容，无用户数据损失；换取判据逻辑简单、无内容渲染依赖。
- [黑名单为词汇表，无法拦截未列举的开发态表述] → 黑名单覆盖本次已发生的全部泄漏词汇；新增词汇需同步扩表，扩表成本低于每次泄漏的排查成本。规格中以"技能开发仓库特有的脚本、产物目录与文件"表述目标，黑名单是其当前实现。
- [注入模板由 AI 读取执行，非机器解析，模板改动与脚本校验之间存在人读差异] → 脚本以 SKILL.md 中的 ```markdown 代码块为提取依据，与 AI 读取的是同一段文本；校验失败即阻断提交。
- [移除 git 规则后，消费方 CLAUDE.md 的规则数与设计文档、README 中若有的描述可能不一致] → 本变更同批更新 `docs/designs/skills/kflow-init.md` 与 `docs/designs/core-mechanisms/08-governance.md`；README 未描述该 section 的规则条目，无需联动。

## Migration Plan

存量消费方项目无需额外操作：

1. 发布修正版 Skills（版本号自增，走本仓库既有归档后流程）。
2. 消费方更新已安装 Skills 后执行一次 `kflow-init`（re-init）。
3. Marker 2 区块因旧版版本行无法解析而被全量替换，旧规则随之清除；Marker 1 按原策略更新；`## 项目自定义规则` 区块被创建。

回滚：若替换结果异常，消费方 CLAUDE.md 的区块可由 `git checkout` 恢复（区块内容处于版本控制下）；Skills 版本可回退至上一 zip 产物。

## Open Questions

无。设计所需的判据来源、替换策略、校验落点与规格收敛目标均已确定，可在任务分解中直接实施。
