## 1. 脚本工具

- [x] 1.1 创建 `scripts/sync-version.sh`：从 `VERSION` 读取版本号，批量更新所有 `skills/kflow-*/SKILL.md` front matter 中的 `version` 字段
- [x] 1.2 创建 `scripts/sync-references.sh`：校验同名 references 文件（repetition.md, hooks.md, gates.md, state-values.md, service-lifecycle.md, self-review.md）在多个 skill 间的差异，输出不一致报告
- [x] 1.3 更新 `scripts/package-skills.sh`：增加路径替换逻辑（`skills/` → `.claude/skills/`），增加版本一致性校验（所有 SKILL.md version 须与 VERSION 一致）

## 2. kflow-shared 内容拆分 — 单引用文件

- [x] 2.1 创建 `skills/kflow-archive/references/archive-rules.md`（从 `kflow-shared/archive-rules.md` 提取，118 行）
- [x] 2.2 创建 `skills/kflow-resume/references/recovery-protocol.md`（从 `kflow-shared/recovery-protocol.md` 提取，161 行）
- [x] 2.3 创建 `skills/kflow-init/references/permission-model.md`（从 `kflow-shared/permission-model.md` 提取，138 行）
- [x] 2.4 为设计阶段 skill（kflow-explore, kflow-prototype-design, kflow-design）各创建 `references/self-review.md`（从 `kflow-shared/self-review.md` 提取，228 行，三份内容相同）

## 3. kflow-shared 内容拆分 — 多引用核心文件

- [x] 3.1 为 8 个执行类 skill（kflow-code, kflow-api-test, kflow-e2e-test, kflow-integration-test, kflow-plan, kflow-code-review, kflow-bug-triage, kflow-bug-fix）各创建 `references/repetition.md`（从 `kflow-shared/repetition-model.md` 提取，472 行）
- [x] 3.2 为 12 个 skill（kflow-code, kflow-api-test, kflow-e2e-test, kflow-integration-test, kflow-plan, kflow-code-review, kflow-audit, kflow-archive, kflow-bug-triage, kflow-bug-fix, kflow-explore, kflow-design, kflow-prototype-design）各创建 `references/hooks.md`（从 `kflow-shared/phase-hooks.md` 提取，每 skill 仅含自身阶段对应章节）
- [x] 3.3 为 10 个 skill（kflow-code, kflow-api-test, kflow-e2e-test, kflow-integration-test, kflow-plan, kflow-code-review, kflow-design, kflow-explore, kflow-prototype-design, kflow-bug-fix）各创建 `references/gates.md`（从 `kflow-shared/gate-rules.md` 提取，每 skill 仅含当前阶段门控）
- [x] 3.4 为 9 个 skill（kflow-code, kflow-api-test, kflow-e2e-test, kflow-integration-test, kflow-plan, kflow-code-review, kflow-design, kflow-explore, kflow-prototype-design）各创建 `references/state-values.md`（从 `kflow-shared/state-values.md` 提取，54 行，内容相同）
- [x] 3.5 为 4 个服务管理类 skill（kflow-code, kflow-api-test, kflow-e2e-test, kflow-integration-test）各创建 `references/service-lifecycle.md`（从 `kflow-shared/service-lifecycle.md` 提取，349 行）

## 4. SKILL.md 重构 — 设计阶段 skill

- [x] 4.1 重构 `skills/kflow-explore/SKILL.md`：核心流程保留，辅助规则下沉 references/，新增 version 字段，更新子代理加载指令
- [x] 4.2 重构 `skills/kflow-prototype-design/SKILL.md`：核心流程保留，辅助规则下沉 references/，新增 version 字段，更新子代理加载指令
- [x] 4.3 重构 `skills/kflow-design/SKILL.md`：核心流程保留，辅助规则下沉 references/，新增 version 字段，更新子代理加载指令

## 5. SKILL.md 重构 — 执行阶段 skill

- [x] 5.1 重构 `skills/kflow-plan/SKILL.md`：核心流程保留，重复制/钩子/门控/状态值规则下沉 references/，新增 version 字段
- [x] 5.2 重构 `skills/kflow-code/SKILL.md`：核心流程保留，重复制/钩子/门控/状态值/服务生命周期规则下沉 references/，新增 version 字段
- [x] 5.3 重构 `skills/kflow-code-review/SKILL.md`：核心流程保留，重复制/钩子/门控/状态值规则下沉 references/，新增 version 字段
- [x] 5.4 重构 `skills/kflow-api-test/SKILL.md`：核心流程保留，重复制/钩子/门控/状态值/服务生命周期规则下沉 references/，新增 version 字段
- [x] 5.5 重构 `skills/kflow-e2e-test/SKILL.md`：核心流程保留，重复制/钩子/门控/状态值/服务生命周期规则下沉 references/，新增 version 字段
- [x] 5.6 重构 `skills/kflow-integration-test/SKILL.md`：核心流程保留，重复制/钩子/门控/状态值/服务生命周期规则下沉 references/，新增 version 字段

## 6. SKILL.md 重构 — 管理与辅助 skill

- [x] 6.1 重构 `skills/kflow-bug-fix/SKILL.md`：核心流程保留，重复制/钩子/门控规则下沉 references/，新增 version 字段
- [x] 6.2 重构 `skills/kflow-bug-triage/SKILL.md`：核心流程保留，重复制/钩子规则下沉 references/，新增 version 字段
- [x] 6.3 重构 `skills/kflow-audit/SKILL.md`：核心流程保留，钩子规则下沉 references/，新增 version 字段
- [x] 6.4 重构 `skills/kflow-archive/SKILL.md`：核心流程保留，钩子/归档规则下沉 references/，新增 version 字段
- [x] 6.5 重构 `skills/kflow-guide/SKILL.md`：核心流程保留，新增 version 字段（无 references 依赖）
- [x] 6.6 重构 `skills/kflow-status/SKILL.md`：新增 version 字段（无 references 依赖）
- [x] 6.7 重构 `skills/kflow-resume/SKILL.md`：核心流程保留，恢复协议规则下沉 references/，新增 version 字段
- [x] 6.8 重构 `skills/kflow-init/SKILL.md`：核心流程保留，权限声明规则下沉 references/，新增 version 字段
- [x] 6.9 重构 `skills/kflow-verify/SKILL.md`：新增 version 字段（无 references 依赖）

## 7. 清理与迁移

- [x] 7.1 迁移 `kflow-shared/scripts/with_server.py` 至 `skills/kflow-code/scripts/with_server.py`，更新 kflow-api-test、kflow-e2e-test、kflow-integration-test 中对 with_server.py 的引用路径
- [x] 7.2 删除 `skills/kflow-shared/` 整个目录
- [x] 7.3 执行 `scripts/sync-version.sh`，确保所有 SKILL.md 的 version 字段与 VERSION 一致

## 8. 文档与配置更新

- [x] 8.1 更新 `CLAUDE.md`：移除 kflow-shared 相关描述，更新项目结构说明
- [x] 8.2 更新 `docs/designs/skills/` 中涉及 kflow-shared 引用路径的设计文档
- [x] 8.3 更新 `docs/designs/core-mechanisms/` 中涉及 kflow-shared 引用路径的设计文档
