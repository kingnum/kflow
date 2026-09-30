# Spec Delta

## MODIFIED Requirements

### Requirement: 打包范围与排除规则（自包含 Skill 目录）

系统 SHALL 扫描仓库内实现目录 `skills/kflow-*`，包含所有运行时 Skills 的完整文件（含 `scripts/` 子目录）。`.claude/skills/` 为运行期注册目录（受 `.gitignore` 忽略，仅承载 `skill-creator`、`to-spec` 等非交付 Skill），SHALL NOT 作为打包扫描根。

#### Scenario: 扫描并收集 Skills 文件

- **WHEN** 执行打包流程
- **THEN** 系统扫描 `skills/kflow-*/` 下所有目录
- **AND** 收集范围为所有 `kflow-*` Skills，每个 Skill 自包含其 `references/` 与 `scripts/`
- **AND** 收集范围 SHALL NOT 包含独立的 `kflow-shared/` 目录
- **AND** 每个 Skill 目录下所有文件均纳入打包（SKILL.md + references/ + scripts/ + 其他附属文件）

#### Scenario: 扫描根为仓库内实现目录

- **WHEN** 打包流程定位待打包的 Skills
- **THEN** 扫描根 SHALL 为 `skills/`
- **AND** SHALL NOT 为 `.claude/skills/`
- **AND** 扫描结果 SHALL 覆盖 `skills/` 下的全部 kflow-* Skill

#### Scenario: 扫描结果为空时打包失败

- **WHEN** 打包扫描未匹配到任何 kflow-* Skill
- **THEN** 系统 SHALL 判定打包失败并以非零状态退出
- **AND** SHALL NOT 生成 zip 产物
- **AND** 依赖打包扫描结果的版本一致性校验 SHALL NOT 以空集合通过

#### Scenario: front matter 非法时打包失败

- **WHEN** 待打包的任一 SKILL.md 的 front matter 无法被解析（如未加引号的 plain scalar 内含 ASCII `": "`）
- **THEN** 打包 SHALL 在复制文件之前中止并以非零状态退出
- **AND** SHALL NOT 生成 zip 产物
- **AND** 系统 SHALL 指明失败的文件与原因——该缺陷会使 `npx skills add` 静默跳过对应 Skill，安装数量少于实际数量而不报错

#### Scenario: 运行时脚本随 kflow-code 分发

- **WHEN** 打包包含 `kflow-code` 的目录
- **THEN** 系统纳入 `skills/kflow-code/scripts/` 目录下所有文件
- **AND** 包含 `with_server.py` 等服务生命周期管理脚本
- **AND** 保持 `scripts/` 相对该 Skill 目录的位置不变

#### Scenario: 路径引用按消费方布局重写

- **WHEN** 打包复制 `skills/<skill-name>/` 下的 Markdown 与脚本（`*.py`）文件
- **THEN** 文件中的 `skills/<任意 kflow-* 名称>/` 路径段 SHALL 被重写为 `.claude/skills/<该名称>/`
- **AND** 该重写 SHALL 覆盖跨 Skill 引用——`kflow-api-test` 等 Skill 的 `references/` 中指向 `kflow-code` 脚本的路径同样被改写
- **AND** 已带 `.claude/` 前缀的路径 SHALL NOT 被重复加前缀
- **AND** 重写后的路径 SHALL 与消费方解压后的实际文件位置一致

#### Scenario: ZIP 包中各 Skill 的自包含结构

- **WHEN** 解压生成的 zip 文件
- **THEN** 每个 `kflow-*/` 目录 SHALL 包含自身的 `references/` 子目录
- **AND** `kflow-code/` SHALL 额外包含 `scripts/` 目录，其中含 `with_server.py`
- **AND** 解压结果 SHALL NOT 包含 `kflow-shared/` 目录

#### Scenario: 安装后脚本可执行

- **WHEN** 用户将 zip 内容解压到目标项目 `.claude/skills/` 目录
- **THEN** 路径 `.claude/skills/kflow-code/scripts/with_server.py` 存在且可执行
- **AND** 执行 `python .claude/skills/kflow-code/scripts/with_server.py --help` 输出帮助信息
- **AND** 各 skill `references/service-lifecycle.md` 中的引用路径与实际文件位置一致

### Requirement: 打包触发时机

本仓库中 `/opsx:archive` 归档完成后，系统 SHALL 在执行 git commit 之前触发运行时 Skills 打包流程，且 SHALL 在 `VERSION` 文件更新与 SKILL.md 版本同步完成之后触发。

#### Scenario: 归档完成后自动打包

- **WHEN** `/opsx:archive` 完成变更归档（文件移动、索引更新均已完成）
- **AND** 版本号自增判定已完成且 VERSION 文件已更新
- **AND** `scripts/sync-version.sh` 已同步全部 SKILL.md 的 `version` 字段
- **THEN** 系统启动打包流程
- **AND** 打包产物位于 `targets/`，受 `.gitignore` 排除，不随 git commit 提交

#### Scenario: 同步未完成时不打包

- **WHEN** `VERSION` 已更新但 SKILL.md 的 `version` 字段尚未同步
- **THEN** 打包前版本一致性校验 SHALL 失败
- **AND** 系统 SHALL NOT 生成 zip 产物

#### Scenario: 打包失败不阻塞归档

- **WHEN** 打包过程发生错误（如磁盘空间不足、工具不可用）
- **THEN** 系统提示打包失败原因
- **AND** 归档操作本身不受影响
- **AND** 提示用户手动打包或修复后重试
