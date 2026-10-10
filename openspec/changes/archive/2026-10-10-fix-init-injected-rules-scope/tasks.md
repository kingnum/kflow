# Tasks

## 1. 设计规格修正（docs/designs）

- [x] 1.1 修正 `docs/designs/skills/kflow-init.md` 的「变更流程强制规则」注入模板段：删除规则 7（归档后 git commit + 版本自增 + 打包）与规则 8（首次 init 询问 git init），section 收敛为 6 条路由约束/用户接口/流程概览；版本行由「参见 VERSION 文件（统一版本管理）」改为「模板版本: {kflow-init 的 version 值}」；补充 `## 项目自定义规则` 区块说明。验证：该段与 `openspec/changes/fix-init-injected-rules-scope/specs/init-claude-md-injection/spec.md` 的要求逐条对应，且不含 git 规则与版本自增表述
- [x] 1.2 修正 `docs/designs/core-mechanisms/08-governance.md` 中「kflow-init 注入的 git 规则」两条的表述：移除版本自增六步流程，改为声明注入模板不含 git 规则，归档后 git commit 由 `kflow-archive` 承载、git init 询问由 `kflow-init` 步骤 13 承载。验证：该段落检索 `sync-version.sh`、`package-skills.sh`、`targets/`、`README` 版本条目均无命中

## 2. 运行时 SKILL.md 同步（设计文档 → SKILL.md 同步）

- [x] 2.1 按 1.1 修正 `skills/kflow-init/SKILL.md` 步骤 11 的 Marker 2 模板：删除规则 7、8。验证：Marker 2 模板块内规则项为 6 条，检索无 git commit 询问、版本自增、打包相关表述
- [x] 2.2 按 1.1 修正 Marker 2 与 Marker 3 的版本标注：Marker 2 头部版本行改为 `> **模板版本**: {kflow-init 的 version 值}`，Marker 3 的固定字面量版本改为同一取值方式。验证：两处模板块均不含 `VERSION 文件` 引用，取值来源在模板中标注为 kflow-init 自身 front matter 的 `version` 字段
- [x] 2.3 修正步骤 11 的幂等策略：Marker 2 替换判据按 design.md 决策 2 展开为「未读到版本行／读到但无法解析／读到且不同 → 全量替换；读到且相同 → 仅更新时间戳」三分支。验证：幂等策略段完整列出四个判定分支及其动作
- [x] 2.4 在步骤 11 中新增 `## 项目自定义规则` marker 的创建规则与不受管声明，并同步修正「幂等策略」与「section 边界识别」两处使该区块不参与版本比较与替换。验证：受管 marker 为 3 个（项目画像、变更流程强制规则、Skill 改进建议自动捕获），`## 项目自定义规则` 明确标注为不覆盖
- [x] 2.5 确认本变更不需向 `.claude/skills/` 同步：该目录下未注册任何 `kflow-*` 副本。验证：`ls .claude/skills/` 输出仅含 `grilling`、`skill-creator`、`to-spec`

## 3. 注入模板作用域校验脚本

- [x] 3.1 新增 `scripts/validate-injection-scope.sh`：提取 `skills/kflow-init/SKILL.md` 中的注入模板代码块，对黑名单词汇（`scripts/sync-version.sh`、`scripts/package-skills.sh`、`targets/`、`VERSION 文件`、README 版本条目相关表述）匹配，命中时输出词汇与行号并以非零状态退出；未提取到任何模板块时同样以非零状态退出。验证：在 2.1~2.4 修正后的 SKILL.md 上运行返回 0，并打印校验的模板块数量
- [x] 3.2 对 3.1 做负向验证：在 SKILL.md 的注入模板块中临时插入 `scripts/package-skills.sh` 一词，运行脚本应返回非零并输出该词汇与行号；还原后再次运行返回 0。验证：负向运行输出命中词汇及行号，还原后校验通过

## 4. 规格 Purpose 对齐

- [x] 4.1 修正 `openspec/specs/init-claude-md-injection/spec.md` 的 Purpose：「双层 marker」表述改为与实现的三个 marker 一致，并说明该能力为 CLAUDE.md marker 注入规则的唯一权威定义位置。验证：Purpose 中 marker 数量与正文 Requirement 覆盖的 marker 一致（项目画像、变更流程强制规则、Skill 改进建议自动捕获、项目自定义规则）
- [x] 4.2 修正 `openspec/specs/devflow-init/spec.md` 的 Purpose：移除 CLAUDE.md 注入职责的表述，收敛为工具推荐矩阵与 GAP 能力缺口检测。验证：Purpose 不再声称定义 CLAUDE.md 注入规则，且与移除 delta 后的剩余 Requirement 对应

## 5. 集成验证

- [x] 5.1 re-init 替换演练：在临时目录构造含旧版 Marker 2 区块（含归档后 git commit 询问、版本自增与打包表述、`参见 VERSION 文件` 版本行）的 CLAUDE.md，按修正后的幂等策略执行一次注入，确认该区块被全量替换、替换后不含 git 与版本自增规则、`## 项目自定义规则` 新区块被创建、区块之外的既有内容未被修改。验证：演练后的 CLAUDE.md 逐项符合上述四点
- [x] 5.2 校验脚本无回归：运行 `./scripts/validate-injection-scope.sh`、`./scripts/sync-references.sh`、`python scripts/validate-frontmatter.py`。验证：三者均以零状态退出
- [x] 5.3 残留检索：在 `skills/kflow-init/` 与 `docs/designs/skills/kflow-init.md` 中检索 `sync-version.sh`、`package-skills.sh`、`targets/`、`VERSION`。验证：命中仅出现在「本仓库归档后流程」的说明语境中，不存在将其表述为消费方 CLAUDE.md 注入规则或 kflow-init 注入规则的文本
