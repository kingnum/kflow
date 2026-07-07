## 1. 基础设施：.kflow-runtime/ 和 .gitignore

- [x] 1.1 在 `.gitignore` 新增 `.kflow-runtime/` 条目

## 2. 核心机制：phase-hooks.md 增强

- [x] 2.1 PRE_HOOK §2.4/§2.5（✅ 后端 / ✅ 前后端）：将 `READ_SERVICE_GUIDE` 从单步「直接读取」扩展为四阶段「检测→验证→询问→持久化」流程：DETECT（检测存在性）→ VALIDATE（验证内容完整+外部服务依赖连接信息+配置状态标记）→ COLLECT（AskUserQuestion 收集缺失项）→ PERSIST（写入 service-guide.md + 更新配置状态标记）
- [x] 2.2 PRE_HOOK §2.2（🔶 浏览器）：增加 `.kflow-runtime/playwright/` 就绪检测步骤，检测 `node_modules/playwright` 是否存在，不存在则 `cd .kflow-runtime/playwright && npm init -y && npm install playwright && npx playwright install chromium`
- [x] 2.3 POST_HOOK §3.2/§3.4（BROWSER_CLEANUP）：更新 `playwright-cli kill-all` 执行说明，明确从项目根目录执行，不在 prototype/ 下产生残留文件

## 3. 核心机制：service-lifecycle.md 更新

- [x] 3.1 更新 §1（with_server.py 调用规范）：在 `--start-cmd` 和 `--port` 说明中引用新的 READ_SERVICE_GUIDE 就绪检测机制
- [x] 3.2 更新 §6（浏览器进程清理）：增加 `.kflow-runtime/playwright/` 引用，明确 playwright 安装和使用路径

## 4. 运行时 Skill：kflow-prototype-design 更新

- [x] 4.1 VERIFY §6.4（Playwright 全覆盖验证）子代理 prompt：修改 `/playwright-cli` 调用方式，工作目录固定为项目根目录，HTML 文件通过 `docs/changes/{change}/prototype/index.html` 相对路径引用
- [x] 4.2 VERIFY §6.4 Playwright 不可用降级：增加 `.kflow-runtime/playwright/` 安装引导，优先使用隔离安装而非降级

## 5. 运行时 Skill：kflow-code 更新

- [x] 5.1 §步骤3（SERVICE — 服务指引管理）：在 service-guide.md 生成流程中增加外部服务依赖识别步骤（扫描配置文件识别数据库/缓存/MQ/对象存储等依赖）
- [x] 5.2 §步骤3：在 AskUserQuestion 确认环节增加外部服务连接信息询问（dev 环境主机地址、端口等）
- [x] 5.3 §步骤3：service-guide.md 生成完成后写入配置状态标记 `✅ 已就绪` 或 `⏳ 待配置`

## 6. 模板更新

- [x] 6.1 `docs/designs/templates/docs/service-guide.md`：增强「服务依赖」章节格式，增加「配置状态」元信息字段（配置状态 + 上次检测时间戳）

## 7. 设计文档同步

- [x] 7.1 `docs/designs/core-mechanisms/05-execution-services.md` §7.1.1：增加首次运行就绪检测流程说明和外部服务依赖管理说明
- [x] 7.2 `docs/designs/skills/kflow-prototype-design.md` §8 VERIFY：同步 playwright-cli 工作目录隔离约束

## 8. 运行时 SKILL.md 同步（设计文档 → SKILL.md）

- [x] 8.1 使用 `/skill-creator` 更新 `.claude/skills/kflow-shared/phase-hooks.md`：将 PRE_HOOK READ_SERVICE_GUIDE 增强（四阶段流程）、🔶 浏览器 playwright 就绪检测、POST_HOOK BROWSER_CLEANUP 变更同步到运行时文件
- [x] 8.2 使用 `/skill-creator` 更新 `.claude/skills/kflow-shared/service-lifecycle.md`：同步 playwright 安装路径和浏览器清理引用变更
- [x] 8.3 使用 `/skill-creator` 更新 `.claude/skills/kflow-prototype-design/SKILL.md`：同步 VERIFY §6.4 playwright-cli 工作目录隔离和 `.kflow-runtime/playwright/` 引用
- [x] 8.4 使用 `/skill-creator` 更新 `.claude/skills/kflow-code/SKILL.md`：同步 §步骤3 外部服务依赖识别和配置状态标记写入
