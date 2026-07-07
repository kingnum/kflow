# Tasks: add-resume-and-guide-enhancements

## 1. 设计文档 — kflow-resume Skill

- [x] 1.1 新建 `docs/designs/skills/kflow-resume.md`，按 Skill 设计规范编写完整设计文档，包含基本信息、门控检查、输入要求、输出产物、执行流程（VERIFY → STATE → LOCATE → GATE → SUMMARIZE → DISPATCH）、调度映射表、恢复摘要输出格式、与其他 Skill 的关系
- [x] 1.2 在 `docs/designs/skills/index.md` Skills 清单中新增 `kflow-resume` 行，在触发时机总览和阶段依赖关系图中增加 resume 相关条目

## 2. 设计文档 — kflow-guide 增强

- [x] 2.1 修改 `docs/designs/skills/kflow-guide.md`：新增变更标识名解析逻辑（正则匹配 RESUME/定向指引模式），新增 NEW CHANGE 指引分支（分类变更类型 + 建议变更名称 + 跨变更冲突预检 + 输出下一步建议），新增 RESUME 路由（识别后调用 kflow-resume）
- [x] 2.2 更新 guide 的意图识别关键词映射表和优先级规则，增加「继续 {change}」「指引 {change}」模式，增加变更类型分类关键词（产品需求/功能需求/功能缺陷）

## 3. 设计文档 — kflow-init 增强

- [x] 3.1 修改 `docs/designs/skills/kflow-init.md`：在执行流程末尾新增 CLAUDE.md 注入步骤，包含注入内容格式、marker 检测幂等策略、注入位置说明
- [x] 3.2 更新 init 的输出产物表，新增 CLAUDE.md 注入为条件产物

## 4. 设计文档 — 核心机制与概览更新

- [x] 4.1 更新 `docs/designs/core-mechanisms.md`：在「中断恢复机制」章节补充 resume 恢复流程（guide 路由 → resume 读取 → 调度阶段 Skill），在 checkpoint 章节明确恢复查找优先级链
- [x] 4.2 更新 `docs/designs/overview.md`：Skills 清单新增 `kflow-resume`，更新实施计划（`kflow-resume` 和 `kflow-guide` 增强的实施顺序）
- [x] 4.3 更新 `docs/designs/index.md`：版本号 + Skills 清单

## 5. Skill 实现 — kflow-resume

- [x] 5.1 创建 `.claude/skills/kflow-resume/` 目录和 `SKILL.md`，按设计文档实现 Skill
- [x] 5.2 实现 VERIFY 步骤：变更目录存在性、归档状态检查
- [x] 5.3 实现 STATE 步骤：按优先级链读取 checkpoint → .status.md → tasks.md
- [x] 5.4 实现 LOCATE 步骤：确定当前阶段、当前子变更、待执行任务列表
- [x] 5.5 实现 GATE 步骤：快速门控验证（前置阶段产物检查）
- [x] 5.6 实现 SUMMARIZE + DISPATCH 步骤：输出恢复摘要后直接调用阶段 Skill

## 6. Skill 实现 — kflow-guide 增强

- [x] 6.1 修改 `.claude/skills/kflow-guide/SKILL.md`：增强意图识别逻辑，增加变更名正则解析
- [x] 6.2 实现 NEW CHANGE 指引分支：变更类型分类、变更名称建议、跨变更冲突预检
- [x] 6.3 实现定向指引分支：读取指定变更 .status.md 并输出定向状态信息
- [x] 6.4 实现 RESUME 路由：将「继续 {change}」请求路由到 `kflow-resume` Skill

## 7. Skill 实现 — kflow-init 增强

- [x] 7.1 修改 `.claude/skills/kflow-init/SKILL.md`：新增 CLAUDE.md 注入步骤
- [x] 7.2 实现 CLAUDE.md 的 marker 检测与幂等替换逻辑
