## 1. 设计文档更新

- [x] 1.1 更新 `docs/designs/skills/kflow-init.md`：新增项目画像 section 定义、产品文档状态字段、老项目逆向分析流程、re-entrant 更新策略、首次 init 后 commit
- [x] 1.2 更新 `docs/designs/skills/kflow-guide.md`：新增 pre-change git commit 检查步骤（git status 检测 → 变更性质分析 → 一行摘要 → 用户确认 → 提交）
- [x] 1.3 更新 `docs/designs/skills/kflow-archive.md`：新增 post-archive commit 步骤（分析归档内容 → 一行摘要 → git add + commit）
- [x] 1.4 更新 `docs/designs/core-mechanisms.md`：新增 git 版本管理机制说明章节

## 2. kflow-init Skill 实现

- [x] 2.1 实现项目画像扫描逻辑：项目类型检测、技术栈提取（语言/框架/数据库/构建工具）、目录结构分析、入口文件识别
- [x] 2.2 实现产品文档状态检测逻辑：7 项产品文档的存在性检测（CONTEXT.md、index.md、domains/、architecture.md、data-model.md、api-catalog.md、nfr-baseline.md）
- [x] 2.3 实现 CLAUDE.md「项目画像」section 注入逻辑：marker 检测、首次追加、幂等替换、时间戳标注、CLAUDE.md 不存在时跳过
- [x] 2.4 扩展 CLAUDE.md「变更流程强制规则」section 注入逻辑：新增 git commit 规则（归档后提交 / 新变更前提交 / init 后提交）
- [x] 2.5 实现老项目逆向分析流程：L1 配置文件扫描 → L2 目录结构扫描 → L3 源码语义扫描 → 生成草稿 → AskUserQuestion 确认 → 写入
- [x] 2.6 实现首次 init 后自动 git commit：分析生成内容 → 生成提交信息 → git add + git commit
- [x] 2.7 实现 re-init 幂等更新：重新扫描项目画像字段、更新产品文档状态、保留用户手动修改的其他 CLAUDE.md 内容

## 3. kflow-guide Skill 实现

- [x] 3.1 实现新变更前 git 状态检查：`git status --porcelain` 检测、首个提交场景处理、干净工作区快速跳过
- [x] 3.2 实现变更内容分析逻辑：`git diff --stat` 文件范围、`git diff` 内容分析、基于路径的变更类型推断（归档类/产品文档类/代码变更类）
- [x] 3.3 实现提交信息生成：按格式 `{动词}: {一行中文摘要}` 生成、展示变更概要、AskUserQuestion 三选项（确认/修改/跳过）
- [x] 3.4 实现提交执行与跳过处理：git add + commit、提交验证、跳过时 checkpoint 记录

## 4. kflow-archive Skill 实现

- [x] 4.1 实现归档内容分析：从归档目录读取变更摘要、提取功能设计关键词、识别受影响设计域
- [x] 4.2 实现归档后 git commit：生成提交信息（`归档变更 {name}: {一行摘要}`）、git add + git commit、提交失败处理（不阻塞归档）

## 5. 集成验证

- [x] 5.1 新项目场景验证：执行 kflow-init → CLAUDE.md 正确注入项目画像（技术栈标注"待确定"） → 流程规则含 git commit 规则
- [x] 5.2 老项目场景验证：执行 kflow-init → 检测产品文档缺失 → 询问确认 → 逆向扫描生成草稿 → 用户确认写入 → 产品文档状态更新 → git commit
- [x] 5.3 Re-init 场景验证：修改产品文档后重新执行 init → 项目画像状态更新 → 其他 section 不被破坏
- [x] 5.4 Pre-change commit 场景验证：有未提交变更时开始新变更 → 分析-总结-确认-提交 → 然后进入正常引导流程
- [x] 5.5 Post-archive commit 场景验证：归档完成 → 自动 commit → 提交信息含变更名称和摘要
