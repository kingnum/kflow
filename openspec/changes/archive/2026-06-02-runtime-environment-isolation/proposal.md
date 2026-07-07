## Why

当前体系在两个场景中存在运行时环境泄漏和配置缺失问题：首次启动服务时无外部依赖连接信息检测机制，导致服务启动后无法连接数据库/缓存等外部服务而阻塞；`/playwright-cli` 在 `prototype/` 目录下触发 `npm install` 污染设计文档目录，破坏了原型目录的纯文档属性。需要在测试阶段 PRE_HOOK 中增加服务配置就绪检测并持久化外部服务连接信息，同时将 playwright 运行时隔离到项目根目录 `.kflow-runtime/` 下。

## What Changes

- **新增 service-guide.md 首次运行就绪检测机制**：测试阶段 PRE_HOOK 中检测 service-guide.md 是否存在、内容是否完整（非模板占位符）、外部服务依赖连接信息是否已填写。缺失时通过 AskUserQuestion 收集并持久化，后续会话不重复询问
- **新增外部服务依赖连接信息管理**：自动识别 service-guide.md 中列出的外部服务（数据库、Redis、消息队列、对象存储等），首次检测到新依赖时询问用户提供可访问的连接信息
- **新增 .kflow-runtime/ 运行时隔离目录**：项目根目录下 `.kflow-runtime/` 作为运行时环境隔离区，按需创建独立子目录（如 `playwright/`），纳入 `.gitignore`
- **变更 playwright-cli 工作目录策略**：原型设计 VERIFY 步骤和交互式调试中，确保 playwright 安装和运行不发生在 `prototype/` 目录下，工作目录固定为项目根目录
- **更新相关阶段钩子和服务生命周期文档**：PRE_HOOK READ_SERVICE_GUIDE 增强、POST_HOOK BROWSER_CLEANUP 引用 `.kflow-runtime/`、service-lifecycle.md 同步更新

## Capabilities

### New Capabilities

- `service-dependency-detection`: 测试阶段首次运行服务时，检测 service-guide.md 就绪状态（存在性+内容完整+外部服务连接信息），缺失时通过 AskUserQuestion 收集用户输入并持久化，后续会话自动跳过
- `kflow-runtime-isolation`: 项目根目录 `.kflow-runtime/` 运行时隔离区，按需创建独立工具子目录，纳入 .gitignore，确保运行时环境不污染设计文档目录

### Modified Capabilities

- `centralized-service-management`: READ_SERVICE_GUIDE 步骤从「直接读取」增强为「检测→验证→询问→持久化」四阶段流程
- `phase-hooks`: PRE_HOOK 中 READ_SERVICE_GUIDE 子步骤增强；POST_HOOK 中 BROWSER_CLEANUP 增加 `.kflow-runtime/` 目录引用
- `service-guide-generation`: kflow-code 生成 service-guide.md 时增加外部服务依赖识别和用户询问
- `prototype-playwright-5round-verification`: playwright-cli 调用增加工作目录约束（项目根目录），确保不在 prototype/ 下触发 npm install

## Impact

- **受影响的运行时文件**: `.claude/skills/kflow-shared/phase-hooks.md`, `.claude/skills/kflow-shared/service-lifecycle.md`
- **受影响的 Skill**: `.claude/skills/kflow-prototype-design/SKILL.md`, `.claude/skills/kflow-code/SKILL.md`, `.claude/skills/kflow-api-test/SKILL.md`, `.claude/skills/kflow-e2e-test/SKILL.md`, `.claude/skills/kflow-integration-test/SKILL.md`
- **受影响的模板**: `docs/designs/templates/docs/service-guide.md`
- **受影响的配置文件**: `.gitignore`（新增 `.kflow-runtime/` 条目）
- **受影响的规格**: `centralized-service-management`, `phase-hooks`, `service-guide-generation`, `prototype-playwright-5round-verification`
