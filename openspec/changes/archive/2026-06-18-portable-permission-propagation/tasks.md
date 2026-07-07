## 1. 权限声明文档（permission-model.md）

- [x] 1.1 创建 `kflow-shared/permission-model.md`，编写 §1 全局必需权限清单（Bash 工具类 9 项 + 文件操作类 5 项 + Agent + WebFetch）
- [x] 1.2 编写 §2 权限聚合规则（kflow-init 读取声明后合并为 settings.json 的规则）
- [x] 1.3 编写 §3 环境适配指引（Claude Code → settings.json 格式映射，其他工具预留节）
- [x] 1.4 编写 §4 权限配置幂等规则（检测已有配置、合并不覆盖、重复执行不重复添加）

## 2. repetition-model.md 更新

- [x] 2.1 §12.5 权限预配置：移除硬编码权限列表，改为引用 `kflow-shared/permission-model.md`
- [x] 2.2 §12.5 新增说明：kflow-init SHALL 根据 permission-model.md 在目标项目中自动配置权限
- [x] 2.3 新增 §12.7 后台权限失败回退前台子代理机制（权限错误模式检测、创建新前台子代理规则、主 Agent 禁止接管硬线、不计入重试上限、前台也失败标记阻塞）

## 3. kflow-init 权限配置步骤

- [x] 3.1 设计文档 `docs/designs/skills/kflow-init.md`：新增 PERM_CONFIG 步骤设计（插入位置：SCAN 之后、MATCH 之前）
- [x] 3.2 设计文档：新增 PERM_CONFIG 步骤流程（读取 permission-model.md → 检测 settings.json → 用户确认 → 创建/追加/跳过 → 输出到 toolchain.md）
- [x] 3.3 设计文档：新增权限配置状态节到 toolchain.md 格式模板
- [x] 3.4 运行时 SKILL.md `kflow-init/SKILL.md`：执行流程新增 PERM_CONFIG 步骤
- [x] 3.5 运行时 SKILL.md：输出产物表新增权限配置状态输出
- [x] 3.6 运行时 SKILL.md：环境感知层次新增权限配置状态感知

## 4. 执行类阶段 SKILL.md 更新（7 个）

- [x] 4.1 `kflow-plan/SKILL.md`：子代理强制规则框新增第 5 条规则（后台权限失败回退前台子代理，主 Agent SHALL NOT 直接接管）
- [x] 4.2 `kflow-code/SKILL.md`：同上
- [x] 4.3 `kflow-code-review/SKILL.md`：同上
- [x] 4.4 `kflow-api-test/SKILL.md`：同上
- [x] 4.5 `kflow-e2e-test/SKILL.md`：同上
- [x] 4.6 `kflow-integration-test/SKILL.md`：同上
- [x] 4.7 `kflow-bug-fix/SKILL.md`：同上

## 5. Specs 更新（2 个）

- [x] 5.1 更新 `openspec/specs/subagent-enforcement-notice/spec.md`：Permission pre-configuration 需求改为 kflow-init 自动配置，新增后台权限失败回退前台子代理场景
- [x] 5.2 更新 `openspec/specs/subagent-isolation-rule/spec.md`：权限预配置需求改为 kflow-init 自动配置，新增权限回退场景，规则框从 4 条扩展为 5 条

## 6. 核心机制文档更新

- [x] 6.1 更新 `docs/designs/core-mechanisms/07-agent-model.md` §15.3：新增 §12.7 后台权限失败回退前台子代理机制说明

## 7. 设计文档更新

- [x] 7.1 更新 `docs/designs/skills/kflow-init.md`：新增 PERM_CONFIG 步骤设计、权限配置状态输出到 toolchain.md 格式（设计文档 → SKILL.md 同步）

## 8. 模板文件更新

- [x] 8.1 更新 `docs/designs/templates/docs/toolchain.md`：新增权限配置状态节模板

## 9. 本项目配置清理

- [x] 9.1 删除 `.claude/settings.json`（硬编码的权限配置文件，改为 kflow-init 自动生成）

## 10. 运行时 SKILL.md 同步（使用 /skill-creator）

- [x] 10.1 使用 /skill-creator 根据 `docs/designs/skills/kflow-init.md` 更新 `kflow-init/SKILL.md`（设计文档 → SKILL.md 同步）
