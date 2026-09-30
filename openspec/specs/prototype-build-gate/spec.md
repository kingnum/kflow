# prototype-build-gate Specification

## Purpose

定义原型设计阶段的构建门控（BUILD）步骤与审查方式选择机制。BUILD 以四项纯静态检查作为原型阶段唯一必做的验证环节，通过后由用户选择「人工审查」或「子代理自动审查验证」，据此决定后续自动验证与自审的启停。

## Requirements


### Requirement: 原型构建门控

系统 SHALL 在原型产物生成（DESIGN）之后、审查方式选择之前执行 BUILD 步骤，依次执行 CDN 外部依赖扫描、交叉引用完整性检查、必检产物存在性检查、清单与磁盘一致性检查四项静态检查。此处的"构建"指静态一致性检查，原型为纯 HTML 产物，SHALL NOT 引入编译或打包步骤。

#### Scenario: 四项静态检查执行

- **WHEN** 原型产物生成（DESIGN）完成，进入 BUILD 步骤
- **THEN** 系统 SHALL 依次执行以下四项静态检查：
  - CDN 外部依赖扫描：以 Grep 检索 `https?://`，命中 `<link>`、`<script>`、`<img>` 或 `@import` 中的外部 URL 即判定不通过
  - 交叉引用完整性：校验产品级原型目录 `docs/designs/prototypes/` 下所有 `<a href>` 与 `<iframe src>` 的目标文件真实存在
  - 必检产物存在：`docs/designs/prototypes/design-system/MASTER.md` 与 `docs/designs/prototypes/design-tokens.css` 均存在
  - 清单与磁盘一致：`docs/designs/prototypes/manifest.md` 声明的文件与实际磁盘文件双向一致
- **AND** 四项检查 SHALL 全部执行，SHALL NOT 因前一项结论跳过后续检查

#### Scenario: 检查不通过时修复重跑

- **WHEN** 四项静态检查中任一项不通过
- **THEN** 系统 SHALL 修复问题后重跑 BUILD 的全部四项检查
- **AND** SHALL NOT 进入后续步骤（审查方式选择、用户评审）
- **AND** 修复-重跑循环 SHALL 持续至四项检查全部通过为止

#### Scenario: 检查通过后进入审查方式选择

- **WHEN** 四项静态检查全部通过
- **THEN** 系统 SHALL 进入审查方式选择
- **AND** BUILD 步骤 SHALL 为原型阶段唯一必做的验证环节

### Requirement: 构建门控零子代理约束

系统 SHALL 由主 Agent 直接执行 BUILD 步骤的全部四项静态检查，SHALL NOT 为 BUILD 启动任何子代理。

#### Scenario: BUILD 不启动子代理

- **WHEN** 主 Agent 执行 BUILD 步骤
- **THEN** 四项静态检查 SHALL 在主 Agent 上下文内直接完成
- **AND** SHALL NOT 以 `Agent(subagent_type="claude")` 或其他方式启动子代理执行 BUILD 检查

#### Scenario: 与子代理验证步骤的边界

- **WHEN** 审查方式为"子代理自动审查验证"
- **THEN** 导航验证、Playwright 验证、UX 规则审查与 SELFREV SHALL 由子代理执行
- **AND** 对比度检测 SHALL 在该路径下执行，报告输出到 `self-reviews/prototype/contrast-check/report.md`
- **AND** BUILD 步骤 SHALL 仍由主 Agent 直接执行，不受该路径影响

### Requirement: 审查方式选择

系统 SHALL 在 BUILD 四项静态检查全部通过后，以 AskUserQuestion 询问用户选择审查方式，提供"人工审查"与"子代理自动审查验证"两个选项，并 SHALL 将选择结果记录到变更的 `.status.md`。

#### Scenario: 提供两个审查方式选项

- **WHEN** BUILD 四项静态检查全部通过
- **THEN** 系统 SHALL 通过 AskUserQuestion 提供"人工审查"与"子代理自动审查验证"两个选项
- **AND** SHALL NOT 在 BUILD 未通过时发起该询问

#### Scenario: 记录选择结果

- **WHEN** 用户选定审查方式
- **THEN** 系统 SHALL 将选择结果记录到变更的 `.status.md` 原型阶段条目
- **AND** 后续 VERIFY 与 SELFREV 步骤 SHALL 依据该记录决定是否执行

#### Scenario: 恢复执行时读取选择结果

- **WHEN** 变更从 `.status.md` 恢复执行且已记录审查方式
- **THEN** 系统 SHALL 读取已记录的审查方式
- **AND** SHALL NOT 重复询问审查方式

### Requirement: 人工审查路径

用户选择"人工审查"时，系统 SHALL 跳过全部自动验证与原型阶段 SELFREV，直接进入用户评审（REVIEW）。

#### Scenario: 跳过自动验证

- **WHEN** 审查方式为"人工审查"
- **THEN** 系统 SHALL 跳过导航验证、Playwright 验证、UX 规则审查与原型阶段 SELFREV
- **AND** 系统 SHALL 跳过对比度检测，SHALL NOT 产出 `self-reviews/prototype/contrast-check/report.md`
- **AND** SHALL NOT 启动任何子代理执行原型验证
- **AND** 系统 SHALL 直接进入用户评审（REVIEW）步骤

#### Scenario: 人工审查路径的产物范围

- **WHEN** 审查方式为"人工审查"
- **THEN** 系统 SHALL 产出 BUILD 报告到 `self-reviews/prototype/cdn-crossref-check/report.md`
- **AND** SHALL NOT 产出 `self-reviews/prototype/nav-check/`、`self-reviews/prototype/playwright-check/` 下的轮次报告与自审报告

### Requirement: 子代理自动审查验证路径

用户选择"子代理自动审查验证"时，系统 SHALL 执行导航验证、Playwright 验证、UX 规则审查与原型阶段 SELFREV。

#### Scenario: 执行四项自动验证

- **WHEN** 审查方式为"子代理自动审查验证"
- **THEN** 系统 SHALL 依次执行 5 轮导航验证、5 轮 Playwright 验证、5 轮 UX 规则审查
- **AND** 系统 SHALL 执行对比度检测（WCAG 相对亮度计算，标记 <4.5:1 的颜色对），报告输出到 `self-reviews/prototype/contrast-check/report.md`
- **AND** 系统 SHALL 执行原型阶段 SELFREV，轮次按 self-review 分级规则确定
- **AND** 各项验证 SHALL 串行执行，SHALL NOT 并行启动多个子代理

#### Scenario: 自动验证不通过时修复后继续

- **WHEN** 某一轮自动验证发现问题
- **THEN** 主 Agent SHALL 修复原型产物后启动下一轮
- **AND** SHALL NOT 提前终止尚未完成的轮次
- **AND** 系统 SHALL 完成全部规定轮次后方可进入用户评审（REVIEW）
