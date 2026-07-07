## 1. 核心机制更新

- [x] 1.1 更新 `docs/designs/core-mechanisms.md` §15：将「Agent 迭代执行模式」章节改写为「重复制（执行类阶段）」——移除节奏指引描述、新增每轮全量遍历定义、复杂度评估标注为仅信息展示、保留强制子代理+10轮下限+主Agent验收闭环

## 2. 编码和审查阶段

- [x] 2.1 更新 `docs/designs/skills/kflow-plan.md`：执行模式改为重复制，新增「每轮工作内容」子章节（遍历全部子变更 tasks.md，4 维度全量检查），移除节奏指引，保留复杂度评估（仅信息展示）
- [x] 2.2 更新 `.claude/skills/kflow-plan/SKILL.md`：同步设计规格变更，更新执行流程章节
- [x] 2.3 更新 `docs/designs/skills/kflow-code.md`：执行模式改为重复制，新增「每轮工作内容」子章节（遍历全部功能点，每个 FP 完整 TDD+Tracer Bullet），移除节奏指引，保留复杂度评估（仅信息展示）
- [x] 2.4 更新 `.claude/skills/kflow-code/SKILL.md`：同步设计规格变更，更新执行流程章节
- [x] 2.5 更新 `docs/designs/skills/kflow-code-review.md`：执行模式改为重复制，新增「每轮工作内容」子章节（遍历全部代码变更，2 视角全量审查），移除节奏指引，保留复杂度评估（仅信息展示）
- [x] 2.6 更新 `.claude/skills/kflow-code-review/SKILL.md`：同步设计规格变更，更新执行流程章节

## 3. 测试阶段

- [x] 3.1 更新 `docs/designs/skills/kflow-api-test.md`：执行模式改为重复制，新增「每轮工作内容」子章节（遍历 api-tests/ 全部接口用例，逐条 curl/HTTP 执行），移除节奏指引，保留复杂度评估（仅信息展示）
- [x] 3.2 更新 `.claude/skills/kflow-api-test/SKILL.md`：同步设计规格变更，更新执行流程章节
- [x] 3.3 更新 `docs/designs/skills/kflow-e2e-test.md`：执行模式改为重复制，新增「每轮工作内容」子章节（遍历 e2e-tests/ 全部场景，逐条 Playwright 执行），移除节奏指引，保留复杂度评估（仅信息展示）
- [x] 3.4 更新 `.claude/skills/kflow-e2e-test/SKILL.md`：同步设计规格变更，更新执行流程章节
- [x] 3.5 更新 `docs/designs/skills/kflow-integration-test.md`：执行模式改为重复制，新增「每轮工作内容」子章节（遍历全部集成场景，逐条多服务协作验证），移除节奏指引，保留复杂度评估（仅信息展示）
- [x] 3.6 更新 `.claude/skills/kflow-integration-test/SKILL.md`：同步设计规格变更，更新执行流程章节

## 4. 缺陷修复阶段

- [x] 4.1 更新 `docs/designs/skills/kflow-bug-fix.md`：执行模式改为重复制，新增「每轮工作内容」子章节（遍历全部失败用例，每个独立分析+修复+验证，内层 3 次上限独立共存），移除节奏指引，保留复杂度评估（仅信息展示）
- [x] 4.2 更新 `.claude/skills/kflow-bug-fix/SKILL.md`：同步设计规格变更，更新执行流程章节

## 5. 关联文档同步

- [x] 5.1 更新 `docs/designs/index.md`：将「10 轮自审机制」「Agent 迭代执行」等术语描述与重复制统一模式对齐
- [x] 5.2 更新 `docs/designs/overview.md`：同步机制描述变更

## 6. 验证

- [x] 6.1 全局搜索残留的「节奏指引」「前 N 轮重点执行」「分段分配」等术语，确认全部替换
- [x] 6.2 对比 7 个阶段的每轮工作内容定义，确认无矛盾和不一致
- [x] 6.3 验证每个阶段的「执行模式」摘要行已从「Agent 迭代执行」改为「重复制」
