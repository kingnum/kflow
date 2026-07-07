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
- **AND** 保持 `kflow-shared/scripts/` 原始目录结构

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
