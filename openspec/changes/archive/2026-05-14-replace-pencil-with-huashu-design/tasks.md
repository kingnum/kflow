## 1. 设计规格文档更新

- [x] 1.1 重写 `docs/designs/skills/kflow-prototype-design.md` (v1.6.0 → v2.0.0)：委托调用架构、prompt 组装、用户评审循环
- [x] 1.2 更新 `docs/designs/core-mechanisms.md`：产物路径 `prototype.pen` → `prototype/index.html`，allowed-tools 列表
- [x] 1.3 更新 `docs/designs/index.md`：Skill 描述从 Pencil 改为 HTML 原型 + huashu-design 委托
- [x] 1.4 更新 `docs/designs/skills/kflow-design.md`：输入来源从 `prototype.pen` 改为 `prototype/`

## 2. kflow-init 增强

- [x] 2.1 新增 huashu-design Skill 可用性检测逻辑
- [x] 2.2 未安装时输出安装提示：`npx skills add alchaincyf/huashu-design`

## 3. kflow-prototype-design Skill 重写

- [x] 3.1 完全重写 `.claude/skills/kflow-prototype-design/SKILL.md`：编排层模式，委托调用 huashu-design
- [x] 3.2 实现 CHECK 步骤：门控检查 + huashu-design 可用性硬拦截
- [x] 3.3 实现 INPUT 步骤：从 functional-designs/ 和 docs/prototype/（条件）组装 prompt 上下文
- [x] 3.4 实现 DESIGN 步骤：`Skill("huashu-design", prompt)` 委托调用，接收产物写入 `prototype/`
- [x] 3.5 实现 VERIFY 步骤：Playwright 最小点击测试（可用时），不可用时降级手动检查
- [x] 3.6 实现 REVIEW 步骤：AskUserQuestion 用户评审（确认通过 → 下一阶段 / 需修订 → 回 DESIGN）
- [x] 3.7 更新 allowed-tools：移除 `mcp__pencil__*`，新增 `Skill`、`WebSearch`、`WebFetch`
- [x] 3.8 更新 `.claude/skills/kflow-prototype-design/evals/evals.json` 与新版对齐

## 4. 产品级原型系统

- [x] 4.1 创建 `docs/prototype/` 目录结构骨架（screens/、components/、assets/）
- [x] 4.2 创建 `docs/prototype/design-tokens.css` 模板
- [x] 4.3 创建 `docs/prototype/index.html` 总导航模板

## 5. kflow-archive 扩展

- [x] 5.1 新增原型合并步骤：新屏幕追加、修改屏幕覆盖（含用户确认）、CSS 变量追加
- [x] 5.2 实现合并后 `docs/prototype/index.html` 导航更新

## 6. kflow-design 输入更新

- [x] 6.1 更新 SKILL.md 中原型产物引用路径（`prototype.pen` → `prototype/index.html`）
- [x] 6.2 更新门控检查中原型产物的检查逻辑

## 7. 清理

- [x] 7.1 删除 `references/rules/pencil-design-style.md`
- [x] 7.2 更新 `CLAUDE.md`，移除 pencil-design-style.md 引用

## 8. 验证

- [x] 8.1 前后端项目端到端测试：原型设计 → 归档 → 新变更扩展的完整流程
- [x] 8.2 纯后端项目自动跳过验证
- [x] 8.3 用户评审循环验证（确认通过 / 需修订两路径）
- [x] 8.4 huashu-design 不可用时的阻塞提示验证
- [x] 8.5 kflow-skills-auditor 质量门禁
