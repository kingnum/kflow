## 1. 设计文档更新——prototype-design 阶段

- [x] 1.1 修改 `docs/designs/skills/kflow-prototype-design.md`：§8 COMPLETE 步骤中废弃 element-spec.md 和 nav-tree.md 生成，改为生成 prototype/element-coverage-tree.md（初始版，TC-ID 为空）；更新 §8.1 自动提取设计规格说明
- [x] 1.2 更新 design-tokens.css 提取逻辑保留不变，仅移除 element-spec.md 和 nav-tree.md 的提取步骤
- [x] 1.3 确认修订模式（§R）下原型迭代后重新生成树的逻辑已覆盖

## 2. 设计文档更新——design 阶段

- [x] 2.1 修改 `docs/designs/skills/kflow-design.md`：§7 E2ETESTS 新增前置子步骤 EXPLORE（7.0 确认树时效性 → 7.1 EXPLORE 探索生成树 → 7.2 DESIGN 映射 TC-ID → 7.3 VERIFY 覆盖率检查）
- [x] 2.2 EXPLORE 步骤文档：描述双路径——有原型（静态 HTML 解析）和无原型（playwright-cli 逐页探索）
- [x] 2.3 DESIGN 步骤文档：TC-ID 映射规则，树节点元数据填充格式
- [x] 2.4 VERIFY 步骤文档：TC-ID 覆盖率 100% 门控检查规则，未覆盖元素清单输出格式
- [x] 2.5 更新 §输出产物 表：新增 element-coverage-tree.md 条件产物（前后端项目必须），标注 element-spec.md 和 nav-tree.md 已废弃
- [x] 2.6 更新 §输入要求 表：将 prototype/index.html 从"设计参考"改为"元素覆盖树生成来源（条件）"

## 3. 设计文档更新——e2e-test 阶段

- [x] 3.1 修改 `docs/designs/skills/kflow-e2e-test.md`：§执行流程 PRE_HOOK 的 RELOAD 步骤新增 element-coverage-tree.md 加载项
- [x] 3.2 新增「元素触达率统计」章节：描述每轮测试后对照树标记 ✅/❌ 的流程
- [x] 3.3 更新 §测试报告格式：round-{n}.md 新增元素触达率统计段，summary.md 新增 10 轮趋势
- [x] 3.4 更新 §健康评分数据采集映射：新增「元素覆盖率」评分维度（可选，树存在时启用）
- [x] 3.5 更新 §输入要求 表：新增 element-coverage-tree.md 为条件输入（前后端项目 + 文件存在时）
- [x] 3.6 更新 §常见陷阱：新增陷阱「忽略元素覆盖树」——未加载树直接执行测试

## 4. 模板更新

- [x] 4.1 修改 `docs/designs/templates/changes/{change}/e2e-tests/index.md`：新增「二、元素覆盖树」章节，引用 element-coverage-tree.md 并包含覆盖率说明
- [x] 4.2 修改 `docs/designs/templates/changes/{change}/e2e-tests/part-NN.md`：每个 TC 的基本信息新增「覆盖元素」字段，列出该场景覆盖的元素树路径
- [x] 4.3 新增 `element-coverage-tree.md` 产物格式规范（在 templates 或设计文档中定义四层树结构 + 符号约定 + 节点元数据格式）
- [x] 4.4 更新 `docs/designs/templates/changes/{change}/traceability.md`：无需改表结构，但需在维护规则中注明 E2E 测试列填写时同步更新树的 TC-ID 映射

## 5. Spec 与 Core-mechanisms 更新

- [x] 5.1 新增 `openspec/specs/e2e-element-coverage-tree/spec.md`（由 openspec-apply-change 从 delta 合并到正式 spec 目录）
- [x] 5.2 修改 `openspec/specs/prototype-to-code-consistency/spec.md`：应用 delta spec（移除 element-spec.md + nav-tree.md requirements，新增 element-coverage-tree.md requirements）
- [x] 5.3 修改 `openspec/specs/playwright-cli-e2e-workflow/spec.md`：应用 delta spec（新增元素覆盖树 RELOAD + 触达率统计 + 探索生成 requirements）
- [x] 5.4 修改 `openspec/specs/e2e-data-tracing/spec.md`：应用 delta spec（新增元素树节点数据来源标注 requirement）
- [x] 5.5 检查 `docs/designs/core-mechanisms/` 中是否有文件引用了 element-spec.md 或 nav-tree.md，如有则更新引用

## 6. 运行时 Skill 同步

> 任务说明：设计文档变更完成后，使用 `/skill-creator` 将设计文档变更同步到对应的运行时 SKILL.md。

- [x] 6.1 同步 `.claude/skills/kflow-prototype-design/SKILL.md`：COMPLETE 步骤改为生成 element-coverage-tree.md，移除 element-spec.md 和 nav-tree.md 生成
- [x] 6.2 同步 `.claude/skills/kflow-design/SKILL.md`：§7 E2ETESTS 新增 EXPLORE 子步骤 + 双路径探索 + 覆盖率门控
- [x] 6.3 同步 `.claude/skills/kflow-e2e-test/SKILL.md`：RELOAD 步骤新增树加载 + 每轮触达率统计 + 轮次报告增强

## 7. 验证与审查

- [x] 7.1 确认 prototype-to-code-consistency spec 的 code-review 对账逻辑数据源已切换到 element-coverage-tree.md
- [x] 7.2 确认纯后端项目不受影响（三阶段均跳过且不生成树）
- [x] 7.3 确认 prototype-design 跳过时 design 阶段的路径 B（playwright-cli 探索）可正常触发
- [x] 7.4 确认树的 TC-ID 覆盖率 100% 门控规则在 design 阶段自审和四视角审查中生效
- [x] 7.5 运行 `kflow-skills-auditor` 对更新后的 3 个运行时 Skill 进行规范审查
