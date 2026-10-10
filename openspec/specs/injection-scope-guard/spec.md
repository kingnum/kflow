# injection-scope-guard Specification

## Purpose

定义 kflow-init 注入消费方 CLAUDE.md 的模板内容的作用域约束——模板只承载消费态规则，不含技能开发仓库特有的路径、脚本与流程词汇，并定义该约束的自动校验机制，防止开发态流程再次随注入模板泄漏到消费方项目。

## Requirements

### Requirement: 注入模板仅含消费态规则

kflow-init 注入消费方 CLAUDE.md 的模板内容 SHALL 只承载消费方项目可执行的规则。模板 SHALL NOT 出现技能开发仓库特有的脚本、产物目录与文件：`scripts/` 下的技能仓库脚本（含 `sync-version.sh`、`package-skills.sh`）、`targets/` 打包产物目录、仓库根 `VERSION` 文件、`README.md` 版本条目。

#### Scenario: 注入模板不含开发态路径与脚本

- **WHEN** kflow-init 的 CLAUDE.md 注入模板被读取
- **THEN** 模板 SHALL NOT 出现 `scripts/sync-version.sh`、`scripts/package-skills.sh`、`targets/` 目录、`VERSION` 文件或 `README.md` 版本条目
- **AND** 模板中出现的文件路径 SHALL 均为消费方项目在 kflow-init 执行后可能具备的路径

#### Scenario: 注入模板不含 skill 内部执行步骤

- **WHEN** 注入模板的规则 section 被读取
- **THEN** 其中的规则 SHALL 均为跨 skill 的路由约束、用户接口约定或流程概览
- **AND** SHALL NOT 包含由某个 skill 在自身执行流程中完成的步骤（如归档后 git commit 询问、非 git 仓库时的 git init 询问）

### Requirement: 注入模板作用域自动校验

系统 SHALL 提供仓库级校验入口，扫描 kflow-init 的注入模板内容并检测开发态词汇。校验命中时 SHALL 报告命中词汇与所在位置，并以非零状态退出。

#### Scenario: 校验通过

- **WHEN** 运行注入模板作用域校验，且模板内容仅含消费态规则
- **THEN** 校验 SHALL 通过并以零状态退出

#### Scenario: 校验命中开发态词汇

- **WHEN** 运行注入模板作用域校验，且模板中出现 `scripts/sync-version.sh`、`scripts/package-skills.sh`、`targets/`、`VERSION` 文件或 `README.md` 版本条目等开发态词汇
- **THEN** 校验 SHALL 输出命中的词汇与所在行
- **AND** SHALL 以非零状态退出

#### Scenario: 校验对象不得为空集

- **WHEN** 校验入口未匹配到 kflow-init 的注入模板内容
- **THEN** 校验 SHALL 判定为失败并以非零状态退出
- **AND** SHALL NOT 以「未发现开发态词汇」的结论通过校验
