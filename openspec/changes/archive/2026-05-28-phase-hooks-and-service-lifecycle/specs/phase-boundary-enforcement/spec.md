## ADDED Requirements

### Requirement: 阶段门控包含 RELOAD 步骤

每个阶段的门控检查 SHALL 在检查文件存在性之后、进入核心执行流程之前，增加 RELOAD 步骤，强制执行基础信息文件的重读。

#### Scenario: 门控检查增强

- **WHEN** 任何阶段 Skill 进入执行流程
- **THEN** 门控检查 SHALL 在原有的文件存在性检查之后，增加 RELOAD 步骤
- **AND** RELOAD 步骤 SHALL 按照钩子配置表中该阶段定义的 RELOAD 清单，重新读取所有基础信息文件的最新内容
- **AND** RELOAD 步骤 SHALL 在阶段核心逻辑执行之前完成

#### Scenario: RELOAD 步骤阻塞

- **WHEN** RELOAD 步骤中某文件不存在或无法读取
- **THEN** SHALL 标记当前阶段为 ❌ 阻塞
- **AND** SHALL 提示缺失的文件路径
- **AND** SHALL NOT 使用过时的缓存内容继续执行

#### Scenario: RELOAD 与存在性检查的关系

- **WHEN** 现有门控检查已验证文件存在
- **THEN** RELOAD 步骤 SHALL 在存在性检查之后执行
- **AND** RELOAD 专注于读取最新内容（非检查存在性）
- **AND** 若文件在检查后被删除（极端情况），RELOAD 失败 SHALL 触发阻塞
