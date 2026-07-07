## Context

当前体系通过 `docs/service-guide.md` 管理项目服务配置（启动命令、端口、数据库、外部依赖等），由 `kflow-init`（老项目逆向）或 `kflow-code`（新项目自动分析）生成。测试阶段（api-test / e2e-test / integration-test）的 PRE_HOOK 通过 `READ_SERVICE_GUIDE` 步骤读取该文件获取启动参数。

两个缺口：
1. **首次启动无就绪检测**：`READ_SERVICE_GUIDE` 步骤假设文件已存在且内容完整。若 code 阶段未完成或用户跳过 service-guide.md 生成，测试阶段将直接阻塞（RELOAD 规则：文件不存在→❌ 阻塞）。即使文件存在，外部服务依赖（数据库/Redis/消息队列）的连接信息可能是模板占位符，导致服务启动失败。
2. **playwright 污染原型目录**：`kflow-prototype-design` 的 VERIFY 步骤使用 `/playwright-cli` 打开 `prototype/` 目录下的 HTML 文件。若 playwright 未全局安装，npm 会在当前工作目录（`prototype/`）下执行 `npm install playwright`，产生 `node_modules/`、`package.json` 等运行时文件，污染纯设计文档目录。此外，原型设计调试和前端实现效果分析中也存在同样的污染风险。

约束：
- service-guide.md 是服务配置的唯一真相源，不得引入第二配置源
- 外部服务连接信息需持久化，避免每次会话重复询问
- `.kflow-runtime/` 需纳入 `.gitignore`，不提交到版本管理
- `/playwright-cli` 为外部 Skill，我们只能控制调用方式和前置环境，不能修改其内部行为

## Goals / Non-Goals

**Goals:**
- 测试阶段 PRE_HOOK 首次启动服务前自动检测 service-guide.md 就绪状态（存在+完整+外部服务连接）
- 缺失信息通过 AskUserQuestion 收集，持久化到 service-guide.md，后续会话自动跳过
- 项目根目录 `.kflow-runtime/` 作为运行时隔离区，所有运行时依赖（playwright 等）统一管理
- prototype/ 目录保持纯设计文档，不含任何运行时环境文件

**Non-Goals:**
- 不修改 `/playwright-cli` Skill 的内部行为
- 不引入新的全局配置文件（仍然以 service-guide.md 为单一真相源）
- 不处理 playwright 以外的运行时工具（预留扩展性但不实现）
- 不改变服务启动的底层机制（仍使用 with_server.py）

## Decisions

### Decision 1: READ_SERVICE_GUIDE 增强为四阶段流程

**选择**：将 PRE_HOOK 中的 `READ_SERVICE_GUIDE` 从单步「直接读取」扩展为四阶段「检测→验证→询问→持久化」流程。

```
READ_SERVICE_GUIDE 增强流程:

PHASE 1: DETECT（检测存在性）
├── docs/service-guide.md 存在？
│   ├── NO  → 进入 PHASE 3（COLLECT）全量收集
│   └── YES → 进入 PHASE 2（VALIDATE）

PHASE 2: VALIDATE（验证完整性）
├── dev 环境启动命令 ≠ 模板占位符（{命令}、{端口}、{框架名称}）？
├── dev 环境端口值实际存在且为有效数字？
├── 外部服务依赖章节存在且每项连接信息完整？
│   ├── ALL PASS → 直接使用，跳过 PHASE 3
│   └── FAIL    → 进入 PHASE 3（仅询问缺失项）

PHASE 3: COLLECT（收集用户输入）
├── AskUserQuestion: "检测到以下配置缺失，请提供:"
│   ├── [缺失项 1] 后端启动命令和端口
│   ├── [缺失项 2] 数据库连接信息（类型/主机/端口/数据库名）
│   ├── [缺失项 3] Redis 连接信息（主机/端口）
│   └── [缺失项 N] ...
├── 用户提供信息 → 写入 service-guide.md
└── 用户选择「稍后配置」→ ❌ 阻塞当前阶段

PHASE 4: PERSIST（持久化）
├── 将用户输入写入 service-guide.md 对应章节
├── 记录配置完成标记（如 `> **配置状态**: ✅ 已就绪`）
└── 后续会话 PHASE 2 检测到标记后自动跳过询问
```

**替代方案**：在 `kflow-init` 中完成全部配置。不采用原因：init 阶段用户可能还不清楚具体服务配置；外部服务连接信息在开发过程中可能变化；增加了 init 阶段的复杂度。

**替代方案 2**：在 `kflow-code` 中完成。部分采用——code 阶段仍负责初始生成（如不存在），但测试阶段 PRE_HOOK 作为兜底验证。

**外部服务依赖识别规则**：解析 service-guide.md 中「服务依赖」章节的表格，识别非 localhost 或占位符格式（`${...}`）的条目作为「需确认的外部服务」。

### Decision 2: .kflow-runtime/ 目录结构与生命周期

**选择**：项目根目录 `.kflow-runtime/` 下按工具类型创建独立子目录，由各阶段 PRE_HOOK 按需初始化。

```
.kflow-runtime/
├── playwright/              ← playwright npm 包 + 浏览器二进制
│   ├── node_modules/
│   ├── package.json
│   └── package-lock.json
└── .gitkeep                 ← 确保空目录可追踪（如需要）
```

**生命周期**：

| 事件 | 执行者 | 操作 |
|------|--------|------|
| 创建 `.kflow-runtime/` | 🔶 浏览器 阶段 PRE_HOOK | `mkdir -p .kflow-runtime` |
| 安装 playwright | 🔶 浏览器 阶段 PRE_HOOK | `cd .kflow-runtime && npm init -y && npm install playwright`（如未安装） |
| 使用 playwright | 子代理（prototype VERIFY / e2e-test） | 工作目录固定为项目根目录 |
| 清理浏览器进程 | POST_HOOK | `playwright-cli kill-all`（不变） |
| 目录排除 | 一次性 | `.gitignore` 新增 `.kflow-runtime/` |

**替代方案**：使用全局 playwright 安装（`npm install -g playwright`）。不采用原因：全局安装需要用户手动执行，可能在 CI/新环境中不可用；版本不一致可能导致不同开发者之间行为差异。`.kflow-runtime/` 方案确保每个项目的 playwright 版本一致且可复现。

**替代方案 2**：将 playwright 安装在 `.claude/tools/playwright/`。不采用原因：`.claude/` 是 Skills 体系的目录，混合运行时依赖会增加 Skill 打包的复杂度；`.kflow-runtime/` 语义更清晰（KFlow 运行时，非 Claude 配置）。

### Decision 3: playwright-cli 工作目录隔离

**选择**：在调用 `/playwright-cli` 前，将 shell 工作目录切换到项目根目录，HTML 文件通过绝对路径或相对项目根的路径引用。

```
变更前（污染 prototype/）:
  cd docs/changes/{change}/prototype/
  /playwright-cli open index.html
  → npm install playwright 在 prototype/ 下执行

变更后（隔离到 .kflow-runtime/）:
  cd {project_root}
  # PRE_HOOK 已确保 .kflow-runtime/playwright/ 就绪
  /playwright-cli open docs/changes/{change}/prototype/index.html
  → playwright 使用 .kflow-runtime/playwright/ 中的安装
```

**PLAYWRIGHT_PATH 约定**：在 PRE_HOOK 中设置环境变量或通过 `--cwd` 参数引导 playwright-cli 使用 `.kflow-runtime/playwright/` 下的安装。具体机制取决于 `/playwright-cli` Skill 支持的参数——若不支持显式指定，通过 `PATH` 或 `npm prefix` 环境变量引导。

**适用场景**：
- prototype-design VERIFY §6.4：自动化 5 轮验证
- prototype-design 调试分析：用户主动使用 `/playwright-cli` 分析原型交互问题
- code 阶段调试分析：用户主动使用 `/playwright-cli` 分析前端实现效果问题
- e2e-test：E2E 浏览器自动化测试

### Decision 4: 外部服务连接信息持久化格式

**选择**：在 service-guide.md 中增加「配置状态」标记，区分「已确认就绪」和「待配置」状态。

```markdown
> **配置状态**: ✅ 已就绪 (2026-06-02 确认)
> **上次检测**: 2026-06-02T15:00:00
```

PHASE 2 VALIDATE 检查此标记：
- `✅ 已就绪` + 内容完整 → 跳过询问
- `⏳ 待配置` 或标记缺失 → 进入 PHASE 3

当 service-guide.md 被用户手动修改或外部依赖发生变化时，标记更新为 `⏳ 待配置`，触发下次 PRE_HOOK 重新检测。

## Risks / Trade-offs

- **[风险] `/playwright-cli` 不支持自定义 playwright 安装路径** → 缓解：PRE_HOOK 中通过 `npm link` 或 `PATH` 环境变量确保 `.kflow-runtime/playwright/node_modules/.bin/` 在 PATH 最前；若 `/playwright-cli` 完全不受控，降级为全局安装提示
- **[风险] 外部服务检测误判** → 缓解：仅对非 localhost/127.0.0.1 且非环境变量占位符的地址触发询问；用户可以选择「本地已有，无需配置」
- **[权衡] 每次测试阶段 PRE_HOOK 都执行检测** → 成本低（仅读取 service-guide.md + 检查标记），远低于每次询问用户的时间成本
- **[权衡] `.kflow-runtime/` 增加项目根目录文件** → 已在 `.gitignore` 排除，不影响版本管理；约 200-300MB（playwright + chromium），磁盘成本可接受
