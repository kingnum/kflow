## MODIFIED Requirements

### Requirement: 打包范围与排除规则

系统 SHALL 扫描 `.claude/skills/kflow-*` 目录，包含所有运行时 Skills 的完整文件（含 `scripts/` 子目录），排除 `kflow-skills-auditor`。

#### Scenario: 扫描并收集 Skills 文件

- **WHEN** 执行打包流程
- **THEN** 系统扫描 `.claude/skills/kflow-*/` 下所有目录
- **AND** 收集范围包含所有 kflow-* Skills（含 kflow-shared）
- **AND** 每个 Skill 目录下所有文件均纳入打包（SKILL.md + references/ + scripts/ + 其他附属文件）

#### Scenario: kflow-shared 包含运行时脚本

- **WHEN** 打包 kflow-shared
- **THEN** 系统纳入 `kflow-shared/scripts/` 目录下所有文件
- **AND** 包含 `with_server.py` 等服务生命周期管理脚本
- **AND** 保持 `kflow-shared/scripts/` 原始目录结构不变

#### Scenario: 排除 kflow-skills-auditor

- **WHEN** 扫描 Skills 目录
- **THEN** `kflow-skills-auditor` 目录被排除，不纳入打包

#### Scenario: ZIP 包中 kflow-shared 结构

- **WHEN** 解压生成的 zip 文件
- **THEN** `kflow-shared/` 目录下包含 `phase-hooks.md`、`service-lifecycle.md` 和 `scripts/` 目录
- **AND** `scripts/` 目录下包含 `with_server.py`

#### Scenario: 安装后脚本可执行

- **WHEN** 用户将 zip 内容解压到目标项目 `.claude/skills/` 目录
- **THEN** 路径 `.claude/skills/kflow-shared/scripts/with_server.py` 存在且可执行
- **AND** 执行 `python .claude/skills/kflow-shared/scripts/with_server.py --help` 输出帮助信息
- **AND** `service-lifecycle.md` 中的引用路径 `kflow-shared/scripts/with_server.py` 与实际文件位置一致

## ADDED Requirements

### Requirement: 打包触发时机

本仓库中 `/opsx:archive` 归档完成后，系统 SHALL 在执行 git commit 之前触发运行时 Skills 打包流程。

#### Scenario: 归档完成后自动打包

- **WHEN** `/opsx:archive` 完成变更归档（文件移动、索引更新均已完成）
- **AND** 版本号自增判定已完成且 VERSION 文件已更新
- **THEN** 系统启动打包流程
- **AND** 打包完成后将 zip 产物纳入 git commit

#### Scenario: 打包失败不阻塞归档

- **WHEN** 打包过程发生错误（如磁盘空间不足、工具不可用）
- **THEN** 系统提示打包失败原因
- **AND** 归档操作本身不受影响
- **AND** 提示用户手动打包或修复后重试

### Requirement: ZIP 包结构与内容

打包产物 SHALL 为位于 `targets/` 目录下的 ZIP 文件，命名格式为 `kflow-devflow-skills-x.x.x.zip`，内部根目录为 `kflow-devflow-skills-x.x.x/`。

#### Scenario: 生成标准 ZIP 结构

- **WHEN** 打包执行
- **THEN** 系统在 `targets/` 目录下生成 `kflow-devflow-skills-x.x.x.zip`
- **AND** zip 内部根目录名为 `kflow-devflow-skills-x.x.x/`
- **AND** 根目录下包含 `VERSION.txt` 文件
- **AND** 根目录下包含所有 Skills 子目录（每个含完整文件，含 kflow-shared）

#### Scenario: VERSION.txt 内容

- **WHEN** 生成 VERSION.txt 文件
- **THEN** 文件内容包含版本号（`x.x.x`）
- **AND** 包含构建时间（`YYYY-MM-DD HH:MM` 格式）
- **AND** 包含来源变更名称（如 `skill-packaging-and-version-unification`）

#### Scenario: 目标项目可安装

- **WHEN** 用户解压 zip 文件到目标项目的 `.claude/skills/` 目录
- **THEN** 所有 Skills 的文件结构保持完整
- **AND** 每个 Skill 的 `references/` 文件位于正确位置
- **AND** 运行 `/kflow-init` 可正常扫描并初始化

### Requirement: 跨平台 zip 兼容

系统 SHALL 在 Windows 和 Linux/macOS 环境下均能正常生成 zip 包。

#### Scenario: Windows 环境打包

- **WHEN** 在 Windows 环境下执行打包
- **THEN** 系统优先使用 Git Bash 自带的 `tar` 命令
- **AND** 备选使用 PowerShell `Compress-Archive -Path ... -DestinationPath ...`

#### Scenario: Linux/macOS 环境打包

- **WHEN** 在 Linux/macOS 环境下执行打包
- **THEN** 系统使用 `tar -czf` 或 `zip -r` 命令

#### Scenario: 打包工具不可用

- **WHEN** 所有打包工具均不可用
- **THEN** 系统提示"未找到可用的打包工具（tar/zip/Compress-Archive）"
- **AND** 打包步骤失败（不阻塞归档）
- **AND** 提示用户手动打包

### Requirement: CLAUDE.md 打包规则注入

本仓库的 CLAUDE.md SHALL 包含 `/opsx:archive` 完成后的打包规则，确保每次归档 AI 自动执行打包。

#### Scenario: 规则注入

- **WHEN** 执行变更实现
- **THEN** 系统在 CLAUDE.md 中新增归档后打包规则
- **AND** 规则内容包含：版本自增判定 → 更新 VERSION → 扫描 Skills → 打包 zip → git commit
- **AND** 规则格式与现有 CLAUDE.md 规则风格一致
