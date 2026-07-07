## 1. 模板与基础结构更新

- [x] 1.1 更新模板 `docs/designs/templates/changes/{change}/prototype/index.md`：新增「一、产物组织方式」段落（描述文件结构类型：单文件/多页面/含共享资源，标注入口文件路径）；「二、原型文件清单」新增「角色」列（entry/page/tokens/coverage/shared/process）；新增「五、共享资源清单」段落（列出 shared/ 下所有文件及用途）；调整段落编号（设计系统引用→四，修订记录→六）
- [x] 1.2 更新状态模板 `docs/designs/templates/changes/{change}/change-status.md`：原型设计行从 `prototype/index.html` 改为 `prototype/index.md`
- [x] 1.3 更新任务模板 `docs/designs/templates/changes/{change}/change-tasks.md`：原型产物输出任务从 `prototype/index.html` 改为 `prototype/index.md`

## 2. 共享基础设施更新（gate-rules + phase-hooks）

- [x] 2.1 更新 `.claude/skills/kflow-shared/gate-rules.md`：前端子变更门控检查（行 71-73）从逐一检查 `prototype/index.html`、`design-tokens.css`、`element-coverage-tree.md` 改为检查 `prototype/index.md` 存在且清单中包含 entry 角色文件
- [x] 2.2 更新 `.claude/skills/kflow-shared/gate-rules.md`：集成测试门控（行 123）从检查 `prototype/index.html` 改为检查 `prototype/index.md`
- [x] 2.3 更新 `.claude/skills/kflow-shared/gate-rules.md`：恢复验证（行 149）从检查 `prototype/index.html` 改为检查 `prototype/index.md`
- [x] 2.4 更新 `.claude/skills/kflow-shared/phase-hooks.md`：PRE_HOOK 表（行 21-25）中 plan/code/code-review/e2e-test 行，将前端SC 条件产物从 `prototype/design-tokens.css, prototype/element-coverage-tree.md` 合并为 `prototype/index.md(条件,前端SC)`
- [x] 2.5 更新 `.claude/skills/kflow-shared/phase-hooks.md`：RELOAD 表（行 204-208）中 plan/code/code-review/e2e-test 行，将前端SC 条件产物从分散的三个文件合并为 `prototype/index.md(条件,前端SC)`

## 3. SKILL.md 运行时文件更新

- [x] 3.1 更新 `.claude/skills/kflow-plan/SKILL.md`：输入表（行 57）将「原型核心产物」行替换为 `prototype/index.md`（✅ 必须，前端SC）；前端功能点全展开模板（行 189）将 `prototype/{page}.html, prototype/design-tokens.css, prototype/element-coverage-tree.md` 改为从 `prototype/index.md` 获取；质量检查表（行 369）将硬编码的三个文件改为 `prototype/index.md`
- [x] 3.2 更新 `.claude/skills/kflow-code/SKILL.md`：输入表（行 53）将「原型核心产物」行替换为 `prototype/index.md`（✅ 必须，前端SC）；输入限定规则（行 56）改为基于 `prototype/index.md` 中声明的角色过滤；原型转译四阶段流程（行 418-445）将直接引用 `prototype/index.html` 改为从 `prototype/index.md` 获取文件路径；降级表（行 451-453）调整为基于清单角色的降级逻辑；验收标准（行 730）对齐新规则
- [x] 3.3 更新 `.claude/skills/kflow-code-review/SKILL.md`：输入表（行 48）将 `prototype/design-tokens.css` 替换为 `prototype/index.md`（🔶 条件，前端SC）；执行流程（行 117、192）改为从 `prototype/index.md` 清单获取 tokens 和 coverage 文件路径
- [x] 3.4 更新 `.claude/skills/kflow-e2e-test/SKILL.md`：输入表（行 54）将 `prototype/index.html` 替换为 `prototype/index.md`（🔶 条件）；视觉一致性评分（行 215）改为从 `prototype/index.md` 获取入口文件路径；条件分支（行 223-224）改为检查 `prototype/index.md` 存在性；报告模板（行 399）对齐新引用
- [x] 3.5 更新 `.claude/skills/kflow-verify/SKILL.md`：验收标准（行 45、76）将 `prototype/index.html` 改为 `prototype/index.md`
- [x] 3.6 更新 `.claude/skills/kflow-resume/SKILL.md`：产物存在性检查（行 201）将 `prototype/index.html` 改为 `prototype/index.md`；恢复上下文表（行 257）将 `prototype/index.html` 改为 `prototype/index.md`
- [x] 3.7 更新 `.claude/skills/kflow-prototype-design/SKILL.md`：输出产物表（行 108）强化 `index.md` 为原型产物清单，新增角色列要求；修订模式检测（行 146）改为检测 `prototype/index.md` 存在性；修订逻辑（行 796）改为更新 `index.md` 清单反映修订后的产物全貌；子代理委托完成验证（行 431）改为验证 `index.md` 存在且含 entry 角色文件

## 4. 设计文档同步更新（docs/designs/skills/）

- [x] 4.1 更新 `docs/designs/skills/kflow-plan.md`：输入表（行 54-56）将三行独立原型产物合并为 `prototype/index.md`（✅ 必须，前端SC）；前端功能点模板（行 359）将 `prototype/index.html` 改为从清单获取
- [x] 4.2 更新 `docs/designs/skills/kflow-code.md`：门控规则（行 42）改为检查 `prototype/index.md`；输入表（行 56-60）将三个独立产物行合并为 `prototype/index.md`；输入限定规则（行 60）基于清单角色过滤；原型转译执行流程（行 107、122-124）改为从清单获取文件路径
- [x] 4.3 更新 `docs/designs/skills/kflow-code-review.md`：输入表（行 51）将 `prototype/design-tokens.css` 改为 `prototype/index.md`（🔶 条件，前端SC）
- [x] 4.4 更新 `docs/designs/skills/kflow-e2e-test.md`：输入表（行 63）将 `prototype/index.html` 改为 `prototype/index.md`（🔶 条件）；视觉一致性评分表（行 231）和条件分支（行 239-240）和报告模板（行 406）同步更新
- [x] 4.5 更新 `docs/designs/skills/kflow-verify.md`：验收标准（行 118）将三个硬编码文件改为 `prototype/index.md`
- [x] 4.6 更新 `docs/designs/skills/kflow-resume.md`：产物存在性检查（行 158）和恢复上下文（行 217）将 `prototype/index.html` 改为 `prototype/index.md`
- [x] 4.7 更新 `docs/designs/skills/kflow-prototype-design.md`：输出表（行 97-102）强化 `index.md` 为清单入口；执行流程中修订模式检测（行 127）和修订逻辑（行 427、443、464、475）改为基于 `index.md`；产物验证（行 535）改为验证 `index.md` 完整性

## 5. 核心机制文档同步更新（docs/designs/core-mechanisms/）

- [x] 5.1 更新 `docs/designs/core-mechanisms/03-status-and-tasks.md`：示例状态（行 62）将 `prototype/index.html` 改为 `prototype/index.md`；任务检查项（行 221）将 `prototype/index.html` 改为 `prototype/index.md`
- [x] 5.2 更新 `docs/designs/core-mechanisms/04-gates-and-transitions.md`：输入流（行 104）将 `prototype/index.html (🔶)` 改为 `prototype/index.md (🔶)`
- [x] 5.3 更新 `docs/designs/core-mechanisms/08-governance.md`：治理白名单（行 30）将 `prototype/index.html` 改为 `prototype/index.md`

## 6. 模板文件同步更新

- [x] 6.1 更新 `docs/designs/templates/subchanges/{subchange}/e2e-round-report.md`：报告模板（行 55）将 `prototype/index.html` 改为 `prototype/index.md`
- [x] 6.2 更新 `docs/designs/templates/changes/{change}/e2e-tests/index.md`：元素覆盖树引用（行 48、64）将 `prototype/element-coverage-tree.md` 改为从 `prototype/index.md` 清单获取路径

## 7. openspec 规格文件归档合并

- [x] 7.1 归档合并 delta spec → `openspec/specs/prototype-manifest/spec.md`（新建）
- [x] 7.2 归档合并 delta spec → `openspec/specs/prototype-design-index/spec.md`（MODIFIED 覆盖）
- [x] 7.3 归档合并 delta spec → `openspec/specs/subchange-input-source/spec.md`（MODIFIED 覆盖）
- [x] 7.4 归档合并 delta spec → `openspec/specs/prototype-to-code-consistency/spec.md`（MODIFIED 覆盖）
- [x] 7.5 归档合并 delta spec → `openspec/specs/conditional-product-refs/spec.md`（MODIFIED 覆盖）
- [x] 7.6 归档合并 delta spec → `openspec/specs/html-prototype-workflow/spec.md`（MODIFIED 覆盖）

## 8. SKILL.md 同步更新（openspec-apply-change 阶段执行）

- [x] 8.1 使用 `/skill-creator` 根据变更后的设计文档（`docs/designs/skills/kflow-plan.md`）同步更新运行时 `.claude/skills/kflow-plan/SKILL.md`——设计文档 → SKILL.md 同步（已在任务 3.1 直接完成）
- [x] 8.2 使用 `/skill-creator` 根据变更后的设计文档（`docs/designs/skills/kflow-code.md`）同步更新运行时 `.claude/skills/kflow-code/SKILL.md`——设计文档 → SKILL.md 同步（已在任务 3.2 直接完成）
- [x] 8.3 使用 `/skill-creator` 根据变更后的设计文档（`docs/designs/skills/kflow-code-review.md`）同步更新运行时 `.claude/skills/kflow-code-review/SKILL.md`——设计文档 → SKILL.md 同步（已在任务 3.3 直接完成）
- [x] 8.4 使用 `/skill-creator` 根据变更后的设计文档（`docs/designs/skills/kflow-e2e-test.md`）同步更新运行时 `.claude/skills/kflow-e2e-test/SKILL.md`——设计文档 → SKILL.md 同步（已在任务 3.4 直接完成）
- [x] 8.5 使用 `/skill-creator` 根据变更后的设计文档（`docs/designs/skills/kflow-prototype-design.md`）同步更新运行时 `.claude/skills/kflow-prototype-design/SKILL.md`——设计文档 → SKILL.md 同步（已在任务 3.7 直接完成）
- [x] 8.6 使用 `/skill-creator` 根据变更后的共享基础设施设计同步更新 `.claude/skills/kflow-shared/gate-rules.md` 和 `.claude/skills/kflow-shared/phase-hooks.md`——设计文档 → SKILL.md 同步（已在任务 2.1-2.5 直接完成）
