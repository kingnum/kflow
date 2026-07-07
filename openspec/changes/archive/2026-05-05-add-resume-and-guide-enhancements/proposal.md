# Proposal: add-resume-and-guide-enhancements

## Why

当前系统缺少跨会话的中断恢复能力和针对特定变更的定向指引能力。用户在会话中断后无法通过指定变更名称来恢复执行，也无法对特定变更单独获取指引。这降低了长周期变更的连续性和用户的使用效率。

## What Changes

- **新增 `kflow-resume` Skill**：支持通过变更标识名称恢复中断的变更执行。读取状态文件和 checkpoint 定位精确断点，输出恢复摘要后直接调度对应阶段 Skill 继续执行。
- **增强 `kflow-guide` Skill**：
  - 支持解析用户输入中的变更标识名称，实现定向指引（"指引 add-user-auth"）
  - 新增 NEW CHANGE 指引分支：分类变更类型（产品需求/功能需求/功能缺陷），检测项目类型，建议变更名称，执行跨变更冲突预检，输出下一步操作建议。不创建任何文件。
  - 新增 RESUME 路由：识别"继续/恢复 {change-name}"模式，路由到 `kflow-resume`
- **增强 `kflow-init` Skill**：在输出 toolchain.md 后，向 CLAUDE.md 注入「变更流程强制规则」，要求所有用户变更必须通过 `kflow-guide` 进行流程指引。

## Capabilities

### New Capabilities

- `resume-skill`: 中断恢复 Skill（kflow-resume），读取状态文件+checkpoint 定位断点，输出恢复摘要，直接调度对应阶段 Skill
- `guide-targeted-guidance`: kflow-guide 定向指引增强，支持变更标识名解析、NEW CHANGE 指引分支、RESUME 路由

### Modified Capabilities

- `devflow-init`: 增加 CLAUDE.md 注入步骤，写入变更流程强制规则，禁止跳过 kflow-guide
- `devflow-guide`: 意图识别增强——变更标识名解析、NEW CHANGE 指引（分类+命名建议+冲突预检）、RESUME 路由

## Impact

- **设计文档**: `docs/designs/skills/kflow-resume.md`（新增），`kflow-guide.md`、`kflow-init.md`、`index.md`、`overview.md`、`core-mechanisms.md`（修改）
- **Skills 实现**: `.claude/skills/kflow-resume/`（新增），`.claude/skills/kflow-guide/`（修改），`.claude/skills/kflow-init/`（修改）
- **CLAUDE.md**: 由 kflow-init 注入变更流程强制规则 section
- **阶段 Skill**：无修改需求——文档驱动架构天然支持 resume，阶段 Skill 从文件重建上下文后自然从断点继续执行
