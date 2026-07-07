## 1. Skill 重命名

- [x] 1.1 将 `docs/designs/skills/kflow-e2e-qa.md` 重命名为 `kflow-e2e-test.md`
- [x] 1.2 更新 `kflow-e2e-test.md` 中的 YAML frontmatter：`name: kflow-e2e-qa` → `name: kflow-e2e-test`
- [x] 1.3 更新 `kflow-e2e-test.md` 中的 description 为新的中英混合触发词
- [x] 1.4 更新 `docs/designs/index.md` 中所有 `kflow-e2e-qa` 引用为 `kflow-e2e-test`
- [x] 1.5 更新 `docs/designs/overview.md` 的 Skills 清单和流程图中所有引用
- [x] 1.6 更新 `docs/designs/skills/index.md` 中所有引用
- [x] 1.7 更新 `docs/designs/core-mechanisms.md` 中所有引用
- [x] 1.8 检查并更新 `.claude/skills/` 下是否存在已实现的 `kflow-e2e-qa` Skill 文件

## 2. playwright-cli 测试工作流集成

- [x] 2.1 重写 `kflow-e2e-test.md` 执行流程：用 playwright-cli 命令序列替代「启动浏览器自动化工具」通用步骤
- [x] 2.2 新增「E2E 测试决策树」章节（静态 HTML / 动态应用 / 服务器状态三个分支）
- [x] 2.3 新增「元素定位方法」章节：snapshot+ref 为主要方法，getByRole/getByTestId 为备用
- [x] 2.4 新增「健康评分数据采集映射」表格（控制台/性能/视觉/可访问性 → playwright-cli 命令）
- [x] 2.5 新增「测试代码自动生成」章节：收集交互代码 → 保存 generated-test.spec.ts
- [x] 2.6 新增「网络 Mock 错误测试」章节：route/unroute 命令使用方法和场景
- [x] 2.7 新增「浏览器会话管理」章节：open/close/kill-all 生命周期
- [x] 2.8 新增输出产物 `subchanges/{subchange}/test-reports/e2e/generated-test.spec.ts`

## 3. 服务管理集中化

- [x] 3.1 在 `core-mechanisms.md` 新增「服务管理职责归属」章节：变更级 agent 独占管理权，子变更 agent 为纯消费者
- [x] 3.2 在 `kflow-e2e-test.md` 明确子变更 agent 的服务使用约束：仅连接已知端口，不启停服务
- [x] 3.3 在 `kflow-e2e-test.md` 新增「服务不可用上报」分支：子变更 agent 检测到端口无响应 → 上报变更级 → 等待恢复
- [x] 3.4 在 `kflow-integration-test.md` 新增集成测试阶段的服务管理约束
- [x] 3.5 引入 `scripts/with_server.py`（从 `references/webapp-testing/scripts/with_server.py` 复制或引用）
- [x] 3.6 在 `kflow-code.md` 的「自动化服务循环」中引用 with_server.py 作为执行工具

## 4. 每轮编译重启机制

- [x] 4.1 在 `core-mechanisms.md` 重写「服务刷新同步点」章节：从一次性门控改为每轮测试前执行
- [x] 4.2 定义每轮编译重启的标准步骤：停止服务 → 编译后端 → 编译前端 → 迁移 → 启动后端 → 启动前端 → 健康检查
- [x] 4.3 在 `kflow-e2e-test.md` 执行流程中增加「等待变更级编译重启」步骤（每轮开始前）
- [x] 4.4 在 `kflow-integration-test.md` 执行流程中增加每轮编译重启步骤
- [x] 4.5 定义迁移保护规则：后续轮次跳过 `migration-log.md` 中已标记为已执行的迁移

## 5. 批量同步推进

- [x] 5.1 在 `core-mechanisms.md` 新增「批量同步推进」章节：所有子变更完成当前轮次+修复后统一进入下一轮
- [x] 5.2 新增状态值「⏸️ 等待同步」的定义和使用规则
- [x] 5.3 在子变更 `.status.md` 模板中增加「⏸️ 等待同步」状态值
- [x] 5.4 在变更级 `.status.md` 模板的子变更进度矩阵中增加「⏸️」状态支持
- [x] 5.5 更新 `kflow-e2e-test.md` 执行流程：子变更完成测试 → 如其他子变更未完成 → 标记 ⏸️ 等待同步

## 6. 崩溃恢复与中断恢复

- [x] 6.1 在 `kflow-e2e-test.md` 新增「崩溃恢复」流程：检测服务不可用 → 上报变更级 → cleanup + 重启 → 继续
- [x] 6.2 在 `kflow-integration-test.md` 新增「崩溃恢复」流程
- [x] 6.3 在 `kflow-resume.md` 更新中断恢复的服务恢复逻辑：先检测服务状态 → 如不可用则走变更级重启 → 再调度测试 Skill

## 7. 常见陷阱与上下文管理

- [x] 7.1 在 `kflow-e2e-test.md` 新增「常见陷阱」章节（至少 7 条：过早检查 DOM / 忘记关闭浏览器 / 硬编码选择器 / 忽略弹窗 / 不捕获控制台 / 会话残留 / Headless 模式）
- [x] 7.2 在 `core-mechanisms.md` 新增「辅助脚本使用原则」章节：黑盒优先、直接调用、例外条件
- [x] 7.3 在 `kflow-e2e-test.md` 新增「上下文管理」小节：快照优先于截图、增量轮次报告、选择性读取

## 8. 交叉引用更新

- [x] 8.1 更新 `kflow-code.md` 中引用 E2E 测试阶段的 Skill 名称为 `kflow-e2e-test`
- [x] 8.2 更新 `kflow-bug-fix.md` 中引用 E2E 测试阶段的 Skill 名称为 `kflow-e2e-test`
- [x] 8.3 更新 `kflow-integration-test.md` 中引用 E2E 测试阶段的 Skill 名称为 `kflow-e2e-test`
- [x] 8.4 更新 `kflow-archive.md` 中引用 E2E 测试阶段的 Skill 名称为 `kflow-e2e-test`
- [x] 8.5 更新 `kflow-resume.md` 的调度映射表中 E2E 测试阶段名称
- [x] 8.6 更新 `kflow-init.md` 中 playwright-cli 环境检测逻辑（如涉及）
- [x] 8.7 全局搜索 `kflow-e2e-qa` 确保无遗漏引用

## 9. 验证

- [x] 9.1 验证所有修改后的文档中无 TODO/TBD 占位符
- [x] 9.2 验证 Skill 名称 `kflow-e2e-test` 在所有文档中一致
- [x] 9.3 验证 E2E 测试流程图与决策树路径一致
- [x] 9.4 验证服务管理职责归属在所有 Skill 文档中描述一致（变更级 vs 子变更级）
