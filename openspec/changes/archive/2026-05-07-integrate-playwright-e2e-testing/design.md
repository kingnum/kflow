# Design: Integrate Playwright E2E Testing

## Context

当前 `kflow-e2e-qa` 的执行流程高度抽象化——「启动浏览器自动化工具」一个步骤概括了全部技术细节。实际执行时，agent 面临三个悬而未决的问题：(1) 元素选择器从哪来？(2) 不同页面类型该走什么路径？(3) 健康评分的原始数据怎么采集？同时，服务生命周期管理职责模糊——编码阶段的「自动化服务循环」和测试阶段的「服务刷新同步点」由谁执行、何时执行、是否重复启动，都没有明确的契约。

`references/playwright-cli` 提供了以 CLI 命令为中心的浏览器交互模式，核心优势是 snapshot+ref 自动元素定位和交互代码自动生成。`references/webapp-testing` 提供了服务生命周期的 `with_server.py` 和决策树方法论。本设计将这些最佳实践吸收为 KFlow 技能体系的核心能力。

## Goals / Non-Goals

**Goals:**
- 将 playwright-cli 的 snapshot+ref 模式标准化为 E2E 测试的核心元素定位方法
- 明确服务生命周期管理职责：变更级 agent 独占管理权，子变更 agent 为纯消费者
- 建立「每轮编译重启 + 批量同步推进」的测试节奏
- 健康评分各维度映射到可复现的命令行数据采集
- 重命名 `kflow-e2e-qa` → `kflow-e2e-test`

**Non-Goals:**
- 不改变 playright-cli 本身（它是外部 CLI 工具）
- 不改变 `with_server.py` 的核心逻辑（直接复用）
- 不改变子变更的编码阶段流程
- 不改变归档流程
- 不在本变更中实现 Skill 代码（仅设计规格）

## Decisions

### Decision 1: playwright-cli 作为 E2E 测试的统一入口

**选择**: 所有浏览器交互通过 `playwright-cli` 命令序列执行，不再使用「写 Python Playwright 脚本」模式。

**理由**:
- snapshot+ref 系统消除了元素选择器的手工编写需求——每次导航后 `playwright-cli snapshot` 自动输出带有 ref 编号（e15, e22 等）的元素列表
- 每次交互自动生成对应的 Playwright TypeScript 代码，可收集为可复用的测试脚本
- 内置 DevTools 集成（console, network, tracing）直接对应健康评分的数据采集需求
- CLI 命令比 Python 脚本更简洁，减少上下文窗口占用

**替代方案**: 继续使用 Python Playwright 脚本（webapp-testing 模式）。拒绝理由：需要手工编写选择器，无自动代码生成，需要额外的页面侦查代码。

### Decision 2: 变更级 agent 独占服务生命周期管理

**选择**: 服务启动/停止/编译/重启/健康检查全部由变更级 agent 负责。子变更 agent 仅通过「服务就绪」信号消费已启动的服务。

**理由**:
- 消除多 agent 并发时的服务实例冲突——多个子变更 agent 同时尝试重启服务会导致端口争用
- 服务管理决策（何时编译、何时迁移、使用哪个端口）需要全局视角
- 崩溃恢复和中断恢复需要知道完整上下文（哪些迁移已执行、哪些子变更已完成）
- 服务编译+迁移是变更级操作（迁移脚本在变更级管理），自然应由变更级 agent 执行

**替代方案**: 子变更 agent 自行管理服务（当前隐含模式）。拒绝理由：多 agent 并发时必然出现端口冲突和迁移重复执行。

### Decision 3: 每轮测试前重新编译重启

**选择**: 每轮 E2E 测试和集成测试开始前，变更级 agent 执行完整的编译+重启+健康检查流程。

**理由**:
- 上一轮测试可能引入了代码修复，必须重新编译才能生效
- 浏览器自动化测试可能产生状态残留（cookie、localStorage、session），服务重启是确保环境清洁的最可靠方式
- 迁移脚本可能在一轮修复后产生了新的迁移，需要重新执行
- 与「变更级同步收敛」的设计一致——集中编译是收敛点

**替代方案**: 仅热重载或手动重启。拒绝理由：热重载不可靠，手动重启容易遗漏步骤。

### Decision 4: 批量同步推进（非独立推进）

**选择**: 所有子变更完成当前轮次测试和修复后，统一等待变更级 agent 重启服务，再进入下一轮。
每轮流程：`变更级编译启动 → 各子变更并行测试 → 收集失败 → 修复 → 变更级再次编译启动 → 下一轮`

**理由**:
- 如果一个子变更的修复改变了共享代码或接口，其他子变更必须在新编译上测试才能发现回归
- 批量同步避免了「子变更 A 在第 3 轮、子变更 B 在第 1 轮」导致的服务状态不一致
- 变更级 agent 可以在每轮结束时做全局冲突检查

**替代方案**: 各子变更独立推进轮次。拒绝理由：共享代码变更时无法保证测试有效性。

### Decision 5: with_server.py 作为变更级 agent 的工具

**选择**: `scripts/with_server.py` 是变更级 agent 执行服务管理的工具脚本，不作为独立 Skill 或 agent。

使用方式：
```bash
# 单服务
python scripts/with_server.py \
  --server "mvn spring-boot:run" --port 8080 \
  -- <test_command>

# 双服务（前后端）
python scripts/with_server.py \
  --server "cd backend && mvn spring-boot:run" --port 8080 \
  --server "cd frontend && npm run dev" --port 5173 \
  -- <test_command>
```

配置来源：`docs/service-guide.md` 的 dev 环境启动命令。

**替代方案**: 独立 Skill 或直接嵌入变更级 agent 指令中。拒绝理由：作为脚本工具更灵活，可直接继承 `references/webapp-testing/scripts/with_server.py` 的实现。

### Decision 6: 测试脚本保留在子变更级

**选择**: playwright-cli 自动生成的 `.spec.ts` 文件保留在 `subchanges/{subchange}/test-reports/e2e/generated-test.spec.ts`，不在归档时合并到产品级文档。

**理由**:
- 测试代码 ≠ 设计文档，页面实现变化后选择器可能失效
- 核心价值在同一子变更的下一轮测试中（直接运行，跳过元素侦查）
- 产品级保留设计文档和测试用例描述，不保留具体实现代码
- 如后续需要回归脚本，应从 playwright-cli snapshot 重新生成

## Risks / Trade-offs

| Risk | 缓解措施 |
|------|---------|
| playwright-cli 未安装在目标环境 | `kflow-init` 阶段检测并安装 `npm install -g @playwright/cli@latest` |
| snapshot ref 在页面动态变化时不稳定 | 优先使用 snapshot ref，备用 `getByRole()` / `getByTestId()` |
| 每轮编译重启增加测试耗时 | 仅在前后端项目 E2E 阶段执行；后端编译可利用增量编译；编译失败时复用上次编译产物 |
| 变更级 agent 成为单点 | 变更级 agent 仅做协调和编译启动，测试执行由子变更 agent 并行处理；崩溃恢复有明确流程 |
| with_server.py 不支持 Windows | 使用 Git Bash 执行（项目已配置 bash shell）；Shell 命令自动适配 |
| 批量同步可能让快的子变更等待慢的 | 子变更独立测试执行可并行；等待仅在「进入下一轮」时发生，不是每步都等 |

## Open Questions

1. 对于后端编译时间超过 2 分钟的大型项目，是否需要「仅重启（skip 编译）」的快速路径？还是严格执行每轮完整编译？
2. `scripts/with_server.py` 是直接复制 `references/webapp-testing/scripts/with_server.py` 还是基于它修改？
