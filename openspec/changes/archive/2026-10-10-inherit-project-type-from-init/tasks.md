# Tasks

## 1. 设计规格修正（docs/designs）

- [x] 1.1 在 `docs/designs/core-mechanisms/01-project-types.md` 新增「1.4 项目类型记录与继承」节，覆盖四要素：项目级记录真源与三级读取优先级、确认时机（init 首次 / 冲突复核）、静默一致性校验与漂移处理、用户显式覆盖；并声明变更级快照在变更生命周期内冻结。验证：该节四要素齐备，且与 `openspec/changes/inherit-project-type-from-init/specs/project-type-detection/spec.md` 的三条 ADDED 要求逐条对应
- [x] 1.2 修正 `docs/designs/skills/kflow-init.md`：流程块在步骤 1 DETECT 之后新增 CONFIRM 步骤（AskUserQuestion 仅用于记录缺失或扫描与记录冲突时），并补充写入项目级记录与 re-init 静默复用的规则说明。验证：流程块含 CONFIRM 步骤，且文字明确"记录一致时 SHALL NOT 询问用户"
- [x] 1.3 修正 `docs/designs/skills/kflow-explore.md`：步骤 3 TYPEDET 的描述由「检测项目类型」改为「三级回落读取项目级记录」，步骤 4 CONFIRM 改为「静默一致性校验 + 冲突触发复核」，并在记录项说明中保留静默扫描的降级路径。验证：步骤 3 描述含三级优先级（CLAUDE.md 项目画像 → `docs/toolchain.md` → 就地检测），步骤 4 不再将 AskUserQuestion 列为默认路径
- [x] 1.4 修正 `docs/designs/skills/kflow-guide.md`：NEW CHANGE 创建前指引的步骤 2 DETECT 由「检测项目类型」改为「读取项目级项目类型记录」，输出格式的「项目类型」行标注来源。验证：指引流程步骤 2 描述为读取记录，输出格式含来源标注
- [x] 1.5 同步修正 `docs/designs/index.md`、`docs/designs/overview.md`、`docs/designs/skills/index.md` 中「设计探索阶段检测项目类型 / 自动检测项目类型」的表述，改为「继承项目级记录（由 init 一次确认）」。验证：三文件检索「设计探索阶段检测项目类型」与「设计探索阶段自动检测项目类型」均无残留

## 2. 运行时 SKILL.md 同步（设计文档 → SKILL.md 同步）

- [x] 2.1 按 1.2 修正 `skills/kflow-init/SKILL.md`：流程块与步骤 1 之后新增 CONFIRM（AskUserQuestion 仅在项目级记录缺失或扫描冲突时使用），补充写入项目级记录（CLAUDE.md 项目画像 + `docs/toolchain.md` 头部）与 re-init 静默复用规则。验证：流程块含 CONFIRM 步骤，检索含「静默复用」，且步骤 1 与 CONFIRM 的描述不含无条件询问项目类型的表述
- [x] 2.2 按 1.3 修正 `skills/kflow-explore/SKILL.md`：步骤 3 TYPEDET 改写为三级回落读取（含各级判定与来源标注），步骤 4 CONFIRM 改写为静默一致性校验（一致→静默继承并输出来源；冲突→AskUserQuestion 复核并可更新记录；校验失败→沿用记录不阻塞），步骤 1 的状态文件字段说明同步为「项目类型（继承项目级记录）」。验证：检索步骤 3 含三级优先级，步骤 4 的默认路径不含 AskUserQuestion，且含「校验失败不阻塞」
- [x] 2.3 按 1.4 修正 `skills/kflow-guide/SKILL.md`：NEW CHANGE 创建前指引的步骤 2 DETECT 改为读取项目级记录，输出格式的「项目类型」行标注来源，并补充记录缺失时只展示检测结果、不创建文件的说明。验证：指引流程步骤 2 描述为读取记录，输出格式含来源标注，且保留「不创建任何文件」的原则表述
- [x] 2.4 确认本变更不需向 `.claude/skills/` 同步：该目录下未注册任何 `kflow-*` 副本。验证：`ls .claude/skills/` 输出不含 `kflow-` 前缀目录

## 3. 模板与规格 Purpose 对齐

- [x] 3.1 修正 `docs/designs/templates/changes/{change}/functional-designs/index.md`：将「项目类型判断」表（检测项/检测结果/判定依据）改为「来源 / 静默校验结果 / 判定依据」三列，来源取值「项目级记录继承」或「降级检测」。验证：表头三列与 `project-type-detection` delta 的「继承到变更级快照」场景一致
- [x] 3.2 核对 `docs/designs/templates/changes/{change}/change-status.md` 的项目类型字段：确认其取值来源改为项目级记录继承后是否需要来源标注，需要则补充、不需要则在字段说明中显式声明取值为继承值。验证：字段行含来源标注或继承声明，二者必居其一

## 4. 集成验证

- [x] 4.1 一致性检索：在 `skills/kflow-init/`、`skills/kflow-explore/`、`skills/kflow-guide/` 及对应三份设计文档中检索「检测项目类型」「项目类型检测」。验证：命中文本的语境均为「读取优先／记录缺失时降级检测」，不存在将重新扫描作为变更创建默认路径的表述，且探索与指引路径的默认分支不含 AskUserQuestion 确认项目类型
- [x] 4.2 存量路径走查：按 `design.md` 决策 2/3 构造三种项目级记录状态——(a) CLAUDE.md 项目画像含项目类型行、(b) 仅 `docs/toolchain.md` 头部有项目类型字段、(c) 两者皆无——逐一走查读取与降级路径。验证：三种状态分别命中三级读取的对应级别；状态 (c) 的补写落在 `docs/toolchain.md` 头部且不写入 CLAUDE.md「## 项目画像」区块
- [x] 4.3 消费侧无回归确认：确认 `kflow-design`、`kflow-prototype-design`、`kflow-api-test`、`kflow-e2e-test`、`kflow-verify`、`kflow-audit`、`kflow-archive` 的 SKILL.md 未被本次改动触及，其项目类型读取仍指向变更级快照。验证：本次改动文件列表不含上述 7 个 SKILL.md，且其项目类型读取路径的检索结果与改动前一致
- [x] 4.4 校验链回归：运行 `./scripts/sync-references.sh` 与 `python scripts/validate-frontmatter.py`。验证：两者均以零状态退出
