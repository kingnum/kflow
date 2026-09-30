# Spec Delta

## MODIFIED Requirements

### Requirement: KFlow 权限声明集中定义

系统 SHALL 在 `skills/kflow-init/references/permission-model.md` 中集中定义 kflow Skills 执行所需的全部权限清单，作为权限配置的 source of truth。

#### Scenario: 权限声明文件存在且包含必需权限

- **WHEN** `skills/kflow-init/references/permission-model.md` 被读取
- **THEN** 文件 SHALL 包含以下节：
  - §1 全局必需权限（所有 Skill 共享）
  - §2 权限聚合规则
  - §3 环境适配指引
  - §4 权限配置幂等规则

#### Scenario: 全局必需权限清单完整性

- **WHEN** `permission-model.md` §1 全局必需权限节被读取
- **THEN** 权限清单 SHALL 包含：
  - Bash 工具类：`Bash(npm *)`, `Bash(yarn *)`, `Bash(pnpm *)`, `Bash(npx *)`, `Bash(node *)`, `Bash(git *)`, `Bash(curl *)`, `Bash(python *)`, `Bash(python3 *)`
  - 文件操作类：`Read`, `Write`, `Edit`, `Glob`, `Grep`
  - 子代理调用：`Agent`
  - 文档查询：`WebFetch`

#### Scenario: 权限清单跟随 Skill 分发

- **WHEN** `package-skills.sh` 执行打包
- **THEN** `permission-model.md` SHALL 作为 `kflow-init` 的 `references/` 内容被包含在打包产物中
- **AND** 该包含 SHALL 由 `kflow-*/` 的 skill 目录通配完成，SHALL NOT 依赖一个独立的 `kflow-shared/` 目录

### Requirement: kflow-init 自动配置目标项目权限

kflow-init SHALL 在目标项目首次执行时，读取 `skills/kflow-init/references/permission-model.md` 中的权限声明，自动配置目标项目的 `.claude/settings.json`。

#### Scenario: 目标项目不存在 settings.json

- **WHEN** kflow-init 执行 PERM_CONFIG 步骤
- **AND** 目标项目的 `.claude/settings.json` 不存在
- **THEN** kflow-init SHALL 通过 AskUserQuestion 询问用户是否创建
- **AND** 用户确认后 SHALL 创建 `.claude/settings.json`，写入 `permission-model.md` 中定义的全部权限

#### Scenario: 目标项目存在 settings.json 但缺少部分权限

- **WHEN** kflow-init 执行 PERM_CONFIG 步骤
- **AND** 目标项目的 `.claude/settings.json` 已存在
- **AND** `permissions.allow` 中缺少 `permission-model.md` 定义的部分权限
- **THEN** kflow-init SHALL 通过 AskUserQuestion 列出缺失权限并询问是否追加
- **AND** 用户确认后 SHALL 追加缺失权限到 `permissions.allow` 列表
- **AND** SHALL NOT 删除或修改已有的权限条目

#### Scenario: 目标项目权限已齐全

- **WHEN** kflow-init 执行 PERM_CONFIG 步骤
- **AND** 目标项目的 `.claude/settings.json` 已包含 `permission-model.md` 定义的全部权限
- **THEN** kflow-init SHALL 输出"权限配置齐全"
- **AND** SHALL NOT 修改 settings.json

#### Scenario: 用户拒绝权限配置

- **WHEN** kflow-init 通过 AskUserQuestion 询问权限配置
- **AND** 用户选择跳过
- **THEN** kflow-init SHALL NOT 创建或修改 settings.json
- **AND** SHALL 在 toolchain.md 中标注"权限未配置，子代理后台执行可能失败"

#### Scenario: 权限配置幂等

- **WHEN** kflow-init 在同一目标项目重复执行
- **AND** settings.json 已包含全部所需权限
- **THEN** kflow-init SHALL NOT 重复添加权限条目
- **AND** SHALL NOT 重复询问用户确认

#### Scenario: 权限声明读取路径不依赖集中式目录

- **WHEN** kflow-init 读取权限声明
- **THEN** 读取路径 SHALL 为 `skills/kflow-init/references/permission-model.md`（dev）或 `.claude/skills/kflow-init/references/permission-model.md`（consumer）
- **AND** SHALL NOT 为 `.claude/skills/kflow-shared/permission-model.md` 或任何 `kflow-shared/` 下的路径
