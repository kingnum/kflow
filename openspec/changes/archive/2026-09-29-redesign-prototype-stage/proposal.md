# Proposal

## Why

原型设计阶段当前有三个问题，且第三个是体系性缺陷而非优化项：

1. **工具链重复询问**：`TOOLCHAIN` 步骤从不检查 `docs/toolchain.md` 是否已锁定工具链，每次变更都重新扫描环境、重新推荐方案、重新询问用户。而 `docs/toolchain.md` 本就是项目级、跨变更稳定的配置。

2. **验证成本失控**：`VERIFY`（导航 5 轮 + Playwright 5 轮 + UX 5 轮 = 15 个子代理串行）与 `SELFREV`（首次 10 轮 / 非首次 1–10 轮）均被规定为"不允许提前终止"，最坏约 27 个子代理串行执行。

3. **产品级原型只有规格、没有实现**：`product-prototype-system` 与 `archive-design-merge` 规格要求归档时把变更原型合并到产品级，但运行时 `kflow-archive` 明确"原型设计（.html 文件）不合并到产品级，保留在变更级归档目录中"。实际行为是变更目录整体搬进 `archive/`，原型从未流向任何产品级位置——每个变更的原型都是孤岛。同时产品级路径存在 `docs/prototype/`（规格，8 处）与 `docs/designs/prototypes/`（目录规范，1 处）两套互斥写法。

## What Changes

### 工具链默认复用

- `TOOLCHAIN` 步骤改为**默认复用** `docs/toolchain.md` 中已锁定的原型设计工具链，复用时不询问用户。
- 仅在三种情况下重新选择：无已锁定工具链（首次创建）、已锁定工具链引用的 Skill 在环境中已不可用、用户显式要求更换。
- 变更级覆盖文件 `docs/changes/{change}/toolchain.md` 承载"本变更想换工具链"的场景，不新造机制。

### 构建门控 + 审查方式选择

- 新增 **BUILD 步骤**（必做，纯静态，零子代理）：CDN 外部依赖扫描、交叉引用完整性、必检产物存在、清单与磁盘一致。不通过则修复重跑，不进入后续步骤。
- 新增**审查方式选择**（AskUserQuestion），在 BUILD 通过后询问：
  - **人工审查** —— 跳过全部自动验证，直接进入用户评审。
  - **子代理自动审查验证** —— 执行导航验证、Playwright 验证、UX 规则审查与 SELFREV。
- **BREAKING**：`VERIFY` 的 15 轮子代理验证由"无条件强制"改为"仅在选择子代理审查时执行"。
- **BREAKING**：`SELFREV` 在原型阶段由"无条件强制"改为"仅在选择子代理审查时执行"。

### 原型提升到产品级

- 产品级原型目录定为 **`docs/designs/prototypes/`**（追认 `02-directory-structure.md` 的写法，废弃规格中的 `docs/prototype/`），与 `functional-designs/`、`detailed-designs/` 并列。
- **BREAKING**：变更不再维护独立的原型副本目录。变更**直接**写产品级目录；变更级只保留工作记录：`prototype-changes.md`（改动清单 + 改动前哈希）、`prototype-backup/`（改动前副本）、`prototype-plan/`（design-prompt.md、style-decision.md）、`element-coverage-tree.md`、`self-reviews/prototype/`。
- 新增**并发写入检测**：写入产品级原型前比对改动前哈希，不一致时提示该文件已被其他变更修改，交由用户裁决（基于新版本改 / 覆盖 / 人工合并）。
- **BREAKING**：归档由"合并原型到产品级"改为"登记改动到 `docs/designs/prototypes/manifest.md`"。
- 顺带修复规格 ↔ 实现断裂：归档技能、原型设计技能、`archive-design-merge` 规格三方关于"是否合并原型"的表述统一到直写模型。

## Capabilities

### New Capabilities

- `prototype-build-gate`: 原型构建门控（静态四项必做检查）与审查方式选择（人工审查 / 子代理自动审查验证）。
- `prototype-change-tracking`: 变更级原型改动清单、改动前快照与并发写入哈希检测。

### Modified Capabilities

- `product-prototype-system`: 产品级原型路径改为 `docs/designs/prototypes/`；写入模型由"变更级副本 + 归档合并"改为"变更直写"；新增产品级 `manifest.md`。
- `prototype-design-toolchain`: TOOLCHAIN 改为默认复用已锁定工具链，仅例外情况重新选择。
- `archive-design-merge`: 删除原型合并场景，归档改为登记改动。
- `html-prototype-workflow`: 原型产物路径指向产品级目录；移除强制 5 轮 Playwright 验证要求。
- `prototype-navigation-verification`: 5 轮导航验证改为仅在子代理审查路径下执行。
- `prototype-playwright-5round-verification`: 5 轮 Playwright 验证改为仅在子代理审查路径下执行。
- `prototype-review-artifacts`: 验证报告路径与产出条件随审查方式调整。
- `prototype-subagent-delegation`: 子代理生成目标路径改为产品级目录。
- `prototype-revision-mode`: 修订模式检测对象由 `prototype/index.html` 改为 `prototype-changes.md`。
- `prototype-manifest`: 产物清单位置与写权限归属调整。
- `prototype-design-index`: 原型清单由变更级 `index.md` 升为产品级 `manifest.md`。
- `prototype-to-code-consistency`: `design-tokens.css` 归产品级、`element-coverage-tree.md` 归变更级。
- `prototype-design-system-output`: `design-system/MASTER.md` 输出锚定产品级原型目录。
- `subagent-self-review`: prototype 阶段 SELFREV 改为随审查方式触发。
- `design-review-tiering`: prototype 阶段 SELFREV 分级改为随审查方式触发。

## Impact

### 运行时技能（skills/）

- `kflow-prototype-design`（SKILL.md + references/）：步骤重构，改动最大。
- `kflow-archive`（SKILL.md + references/archive-rules.md）：设计合并流程删除原型合并表述。
- `kflow-plan`、`kflow-code`、`kflow-code-review`、`kflow-e2e-test`、`kflow-verify`、`kflow-design`、`kflow-explore`：原型路径引用改口径，共约 30 处。

### 设计文档（docs/designs/）

- `skills/kflow-prototype-design.md`、`skills/kflow-archive.md`、`skills/kflow-code.md`、`skills/kflow-code-review.md`、`skills/kflow-design.md`。
- `core-mechanisms/02-directory-structure.md`（补全产品级原型目录内容）、`core-mechanisms/09-phase-hooks.md`（阶段重载清单路径）。
- `templates/changes/{change}/prototype/*`（模板重定义）、`templates/index.md`、`index.md`、`README.md`。

### 兼容性影响

- 已归档变更的 `prototype/` 目录不受影响（原地保留在 `archive/` 下）。
- 活跃变更若已有变更级 `prototype/` 目录，需要迁移到产品级目录并生成 `prototype-changes.md`。
- 不使用原型设计的变更（纯后端项目、跳过原型）完全不受影响。
