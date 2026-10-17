# Tasks

> **范围说明**：本任务清单仅含变更的实际交付工作。归档（`/opsx:archive`）、Git commit、版本自增、打包等元工作流任务由 `CLAUDE.md` 的「归档后规则」自动驱动，不列入本清单。
>
> **实现顺序**：按 `design.md` 的 Migration Plan——配置项 → 脚本 → 规范 → 切片 → 读取纪律 → 粒度 → 自动机制 → 存量入口 → 门控 → 存量优化 → 端到端验证。
>
> **时序约束**：第 9 组的存量文档优化（9.4）MUST 在第 6、7 组全部落地之后执行——否则优化完的文档会被旧规则写回。
>
> **范围裁决（2026-10-17）**：本变更的实施过程 SHALL NOT 操作消费方项目 `software-dev-agent`。外部项目侧的配置与存量优化由交付物自身承担——项目级配置（`autoCompactWindow`、门控 hook）由 `kflow-init` 在目标项目执行时写入；存量文档优化由 `kflow-doc-optimize` 在目标项目被调用时执行。因此第 8 组的 8.4 与第 9 组整体改由**消费方执行**，本变更只交付其能力与规约，不在本仓库实施期间对该项目动手。

## 1. 配置项与脚本基线（波次 1）

- [x] 1.1 更新 `skills/kflow-init/references/permission-model.md`：新增 §「上下文配置」小节，声明 kflow-init 须写入的 `autoCompactWindow: 300000` 与主 Agent 门控的 PreToolUse hook 注册项；验证方式：该文件内可检索到 `autoCompactWindow` 与门控 hook 的声明条目及其写入位置说明
- [x] 1.2 更新 `skills/kflow-init/SKILL.md` 的步骤 3.5（PERM_CONFIG）：新增写入 `autoCompactWindow` 与注册门控 hook 的动作，明确「已存在且取值更小则不覆盖」「项目自定义 hook 条目保持不变」两条幂等规则；验证方式：SKILL.md 步骤 3.5 内可检索到两条幂等规则，且输出产物章节列出更新后的 settings.json 内容
- [x] 1.3 升级 `scripts/sync-references.sh`：由「校验副本一致性」改为「从权威源生成切片副本 + 校验」，保留归一化比对作为校验段，不一致时以非零退出码报告差异位置；验证方式：在**尚无切片**的当前状态下运行该脚本，退出码为 0 且输出与升级前的校验结论一致（行为等价性验证）
- [x] 1.4 运行 `python scripts/validate-frontmatter.py`、`bash scripts/sync-references.sh`、`bash scripts/validate-injection-scope.sh`；验证方式：三条命令均以退出码 0 结束

## 2. 规范层 —— 上下文预算、状态分层与读取纪律（波次 1）

- [x] 2.1 更新 `docs/designs/core-mechanisms/07-agent-model.md` §15.3：在「主 Agent 职责边界硬线」处补入强制机制说明——硬线由阶段感知的工具级门控实施，声明性约束不再作为唯一手段；验证方式：§15.3 内可检索到门控机制的描述且指向 `main-agent-execution-gating` 能力
- [x] 2.2 更新 `docs/designs/core-mechanisms/09-phase-hooks.md`：新增阶段边界节流规则（阶段收尾落盘交接摘要、下一阶段由子代理独立上下文承接、全程零用户操作）；验证方式：该文件内可检索到「交接摘要」的字段清单与「不要求用户执行任何命令」的约束
- [x] 2.3 更新 `docs/designs/core-mechanisms/03-status-and-tasks.md`：新增 `.status.md` 分层结构定义（当前状态字段清单、100 行约束、`status-log.md` 的承载内容与写入时机、读取场景边界）；验证方式：该文件内可检索到两个文件各自承载的字段划分表
- [x] 2.4 更新 `docs/designs/core-mechanisms/02-directory-structure.md`：在变更目录结构中新增 `status-log.md` 与 `revision-history.md` 落位，并标注前者的读取场景（恢复/审计）与后者的读取场景（版本追溯）；验证方式：目录结构树内出现两个新文件且各附读取场景说明
- [x] 2.5 更新 `docs/designs/overview.md` 与 `docs/designs/index.md` 的核心设计决策表：新增「上下文预算管理」与「文档留存边界」两行决策；验证方式：两个文件均含该两行
- [x] 2.6 更新 `docs/designs/core-mechanisms/07-agent-model.md` §17：将加载粒度由「阶段类型」下沉到「具体阶段 + 子代理职责」，列出各阶段的精确加载清单；验证方式：§17 的加载清单表粒度落到阶段级而非层级级，且含章节级定位说明

## 3. references 按阶段切片（波次 2）

- [x] 3.1 确定并写入切片规则：在 `docs/designs/core-mechanisms/07-agent-model.md` §17 补充「切片规则」小节（按规则的作用对象阶段归属；跨阶段通用规则进入所有相关 skill；无法归属时保留全量形态并登记）；验证方式：该小节含三条归属规则与一条降级规则
- [x] 3.2 切片 `gates.md`（10 个 skill）：每个 skill 的副本仅保留门控标注通用约定 + 本阶段的正向门控、回退门控与专属规则章节；验证方式：`kflow-code/references/gates.md` 与 `kflow-e2e-test/references/gates.md` 比对存在实质差异，且前者不含缺陷修复快车道章节
- [x] 3.3 切片 `repetition.md`（8 个 skill）：每个 skill 的副本仅保留本阶段适用的执行模型、子代理 prompt 规范、隔离规则与轮间摘要机制；验证方式：任取两个 skill 的副本比对存在实质差异，且各自含本阶段的工作量分片与验收条款
- [x] 3.4 切片 `state-values.md`（10 个 skill）：每个 skill 的副本仅保留本阶段产生或消费的状态值；验证方式：任取两个副本比对存在实质差异，且各自的状态值集合与设计文档 §17 的加载清单一致
- [x] 3.5 切片 `self-review.md`（3 个 skill）与 `phase-transition.md`（11 个 skill）：前者仅保留本设计阶段的自审维度，后者仅保留本阶段的衔接决策分支；验证方式：`kflow-explore/references/self-review.md` 与 `kflow-design/references/self-review.md` 的维度列表不同，且各 `phase-transition.md` 的调度目标限于本阶段的下游
- [x] 3.6 切片 `service-lifecycle.md`（6 个测试相关 skill）：仅保留本阶段适用的服务生命周期章节；验证方式：`kflow-api-test/references/service-lifecycle.md` 不含仅 E2E 阶段使用的浏览器清理章节
- [x] 3.7 移除无效引用条目：从各执行类阶段 `SKILL.md` 与 `references/repetition.md` §10 的引用加载清单中，删除「读取自身 `SKILL.md`」与「读取 `tdd-checklist.md`」两项；验证方式：18 个 `SKILL.md` 与其 `repetition.md` 内均检索不到要求子代理读取自身 SKILL.md 的条目
- [x] 3.8 运行 `bash scripts/sync-references.sh` 与 `python scripts/validate-frontmatter.py`，确认切片后生成物与权威源一致、front matter 完整；验证方式：两条命令均以退出码 0 结束，且切片后的副本两两比对不再逐字节相同
- [x] 3.9 **设计文档 → SKILL.md 同步**：将 §3.2~§3.6 的切片结果同步至 `skills/kflow-*/references/` 全部 18 个 skill 目录；验证方式：`skills/` 与 `docs/designs/` 中关于 references 切片范围的描述一致，且无 skill 的副本残留其他阶段的章节

## 4. 子代理任务粒度上限（波次 3）

- [x] 4.1 更新 8 份执行类阶段的 `references/repetition.md` §10（子代理 prompt 规范）：新增工作量分片条款（单个子代理不超过 3 个功能点或 10 个 TDD 步骤；超限返回并落盘；显式区分工作量上限与轮数上限，禁止项保持不变）；验证方式：8 份文件的 §10 均含工作量分片条款，且「禁止项」小节仍保留「禁止任何轮数上限数值」
- [x] 4.2 更新 `docs/designs/core-mechanisms/07-agent-model.md` §15 与 `docs/designs/skills/kflow-code.md` 等设计规格：同步工作量分片条款；验证方式：设计文档与实现层对分片上限的表述一致（3 个功能点 / 10 个 TDD 步骤）
- [x] 4.3 更新 7 个执行类阶段 `SKILL.md` 的子代理调度步骤：新增「本子代理承担的功能点范围」字段与超限时的分片动作；验证方式：各 SKILL.md 的多 Agent 步骤内可检索到功能点范围声明
- [x] 4.4 **设计文档 → SKILL.md 同步**：确认 `docs/designs/skills/kflow-*.md` 的分片规则已完整落到对应 `skills/kflow-*/SKILL.md`；验证方式：逐阶段比对设计规格与 SKILL.md 的分片条款无差异

## 5. 读取纪律（波次 3）

- [x] 5.1 更新 `docs/designs/core-mechanisms/02-directory-structure.md` 与 `docs/designs/core-mechanisms/09-phase-hooks.md`：写入按需分片读取规则（经索引定位后读目标分册或行区间；片段注入优先于读取指令）；验证方式：两个文件内均可检索到「按需分片读取」与「片段注入」的规则条目
- [x] 5.2 更新各阶段 `references/hooks.md`（6 个下游 skill）的 RELOAD 清单：把整体读取项改为按章节行区间读取，并标注定位方式；验证方式：清单中每一条目均给出定位来源（index.md 或章节号）
- [x] 5.3 更新 8 份 `references/repetition.md`：新增读取去重条款（同阶段内同一文件不重复全文读取；文件 mtime 变化后重新读取；不依赖上一阶段上下文残留）；验证方式：8 份文件均含三条去重规则
- [x] 5.4 更新 `skills/kflow-resume/SKILL.md` 与 `skills/kflow-audit/SKILL.md`：新增 `status-log.md` 的读取动作；验证方式：两个 SKILL.md 的读取步骤中列出 `status-log.md` 作为恢复/审计场景的输入
- [x] 5.5 更新 18 个 `SKILL.md` 的状态写入步骤：阶段完成与回退时向 `status-log.md` 追加记录并刷新 `.status.md`；验证方式：各 SKILL.md 的状态更新步骤含双文件写入
- [x] 5.6 **设计文档 → SKILL.md 同步**：确认读取纪律与状态分层的设计要求已完整落到 `skills/kflow-*/SKILL.md`；验证方式：抽样 3 个阶段比对设计规格与 SKILL.md 的读取/写入条款无差异

## 6. 文档留存边界与产品级文档拆分（波次 4）

- [x] 6.1 更新 `docs/designs/core-mechanisms/02-directory-structure.md`：补入修订记录留存边界（头部保留最近 3 条、超出部分按层级移入 `revision-history.md` / `docs/designs/changelog.md`、历史承载位置不参与常规读取）；验证方式：该文件内可检索到 3 条保留规则与两处历史承载位置的说明
- [x] 6.2 更新全部产出文档模板（`docs/designs/templates/**`，含 `functional-designs/index.md` 与 `part-NN.md`、`detailed-design.md`、`api-tests/*`、`e2e-tests/*`、`integration-tests/*`、`audit-report.md`、`element-coverage-tree.md`、`shared-types/README.md`、`design-templates/**`）的修订记录章节：补入留存边界说明（保留最近 3 条、超出移入历史承载位置）；验证方式：全部含 `## 修订记录` 的模板均可检索到留存边界说明
- [x] 6.3 更新 `docs/designs/core-mechanisms/02-directory-structure.md` 与 `docs/designs/skills/kflow-archive.md`：补入产品级文档的两档体积规则（> 30 KB 提供章节索引 / > 80 KB 拆分为目录化结构 / 术语表例外）；验证方式：两文件内可检索到两档阈值与术语表例外条款
- [x] 6.4 更新 `skills/kflow-archive/SKILL.md` 的 MERGE 步骤：新增「裁剪产品级文档修订记录」「同步维护章节索引」「体积跨越分片阈值时触发拆分并同步引用」三项动作，并声明这三项全程自动、无需用户操作；验证方式：MERGE 步骤内可检索到三项动作且含「无需用户操作」声明
- [x] 6.5 更新 `skills/kflow-archive/SKILL.md`：新增「变更级产物修订记录同步裁剪」动作（超出保留条数部分移入变更目录下 `revision-history.md`，按产物文件分组）；验证方式：SKILL.md 内可检索到 `revision-history.md` 的写入动作与分组规则
- [x] 6.6 新增 `docs/designs/templates/changes/{change}/revision-history.md` 模板；验证方式：模板含按产物文件分组的记录结构，且字段与各产物修订记录表一致
- [x] 6.7 **设计文档 → SKILL.md 同步**：确认 `docs/designs/skills/kflow-archive.md` 的合并职责变更已完整落到 `skills/kflow-archive/SKILL.md`；验证方式：逐条比对设计规格与 SKILL.md 的三项新增动作无差异

## 7. 文档优化 Skill（波次 4）

- [x] 7.1 新增 `docs/designs/skills/kflow-doc-optimize.md` 设计规格：含定位（独立维护 Skill，非流程阶段）、五步流程（SCAN → REPORT → CONFIRM → EXECUTE → VERIFY）、内容保真约束、引用完整性校验；验证方式：规格文件含五步流程与两条约束
- [x] 7.2 实现 `skills/kflow-doc-optimize/SKILL.md`：按设计规格编写，front matter 含 `kflow-doc-optimize` 名称、`version` 字段、中英混合 description 与中文触发词（文档优化 / 文档瘦身 / 拆分文档 / 清理修订记录）；验证方式：`python scripts/validate-frontmatter.py` 通过，且 description 含全部中文触发词
- [x] 7.3 实现 `skills/kflow-doc-optimize/references/` 下的辅助规则：SCAN 的阈值判定规则（修订记录条数按 `artifact-revision-record-retention`，体积按 30 / 80 KB 两档）、EXECUTE 的搬移与拆分步骤、VERIFY 的引用校验步骤；验证方式：`references/` 含三份规则文件且各规则与 `specs/` 中的对应 requirement 一致
- [x] 7.4 更新 `skills/kflow-guide/SKILL.md`：在关键词映射表中新增「文档优化 / 文档瘦身 / 拆分文档 / 清理修订记录」到 `kflow-doc-optimize` 的路由行，并在流程概览中加入该 Skill 作为独立维护工具的说明；验证方式：SKILL.md 内可检索到该路由行与概览条目，且明确「无活跃变更时同样可路由」
- [x] 7.5 校验新 Skill 被正确识别：运行 `python scripts/validate-frontmatter.py` 与 `bash scripts/validate-injection-scope.sh`；验证方式：两条命令均以退出码 0 结束，且打包产物中 skill 数量从 18 增至 19
- [x] 7.6 **设计文档 → SKILL.md 同步**：确认 `docs/designs/skills/kflow-doc-optimize.md` 已完整落到 `skills/kflow-doc-optimize/`，且 `docs/designs/skills/index.md` 已登记新 Skill；验证方式：设计规格与实现逐条比对无差异，索引文件含新条目
- [x] 7.7 更新 `skills/kflow-init/SKILL.md` 的 INJECT 步骤与 `skills/kflow-init/references/`：在「变更流程强制规则」注入内容的规则清单中新增 `kflow-doc-optimize` 条目，并声明其不受变更流程适用边界约束；验证方式：注入模板的规则清单内含该条目，且含「不受适用边界约束」的声明
- [x] 7.8 确认 `skills/kflow-init/SKILL.md` 的项目自定义规则区块保护规则未被改动；验证方式：逐条比对「不读取、不替换、不删除」三条保护规则与变更前一致

## 8. 主 Agent 禁手门控（波次 5）

> **8.1 执行状态**：已在独立测试项目 `_kflow_gate_probe`（Claude Code 2.1.278）执行三条探针——探针 1 确认子代理输入含 `agent_id`/`agent_type`、主 Agent 不含（路径 A 成立）；探针 2 确认会话级 deny 同样约束子代理且 `permissionMode` 不能解除（路径 B 不成立）；探针 3 未观测到 `Task`/`Agent` hook 触发（路径 C 不成立）。原始记录见 `verification.md` 与 `probe-records.jsonl`。

- [x] 8.1 执行 `design.md` D-1 的三条探针，确定实现路径：探针 1（hook 原样转储 stdin，分别由主 Agent 与子代理触发 `Edit`/`Bash`，比对是否含 `agent_id`/`agent_type`）→ 探针 2（写入 `permissions.deny` 后由子代理尝试调用被禁工具，观察是否放行）→ 探针 3（`Task`/`Agent` 工具拦截点的可达性）；验证方式：三条探针的原始观测结果写入 `verification.md`，并据结果选定路径 A / B / C 或「门控不实现」并说明理由
- [x] 8.2 实现门控脚本：按 `main-agent-execution-gating` 能力的判定规则（阶段判定来源、白名单、黑名单命令模式、无法判定时放行、拒绝文案指导性）与 `design.md` D-9 的实现约定（`hookSpecificOutput.permissionDecision` + 必填 `hookEventName`、`$CLAUDE_PROJECT_DIR` 解析路径、matcher 限定 `Edit`/`Write`/`Bash`）实现；验证方式：脚本对五类输入（执行类阶段越界写 / 执行类阶段长输出命令 / 设计类阶段写入 / 白名单路径 / 无法判定阶段）分别返回预期的放行或拒绝结果，且拒绝输出的 JSON 结构含 `hookEventName`
- [x] 8.3 更新 `skills/kflow-init/references/permission-model.md` 与 `skills/kflow-init/SKILL.md`：写入门控脚本的安装落位与 hook 注册动作；验证方式：kflow-init 的产物清单含门控脚本文件，且注册条目指向该文件
- [ ] 8.4 在 `software-dev-agent` 实测门控：以执行类阶段主 Agent 尝试 `Edit` 生产代码与运行 `pytest`；验证方式：两次调用均被拒绝且拒绝原因可读，随后主 Agent 能够改为创建子代理执行；实测记录写入 `verification.md`
- [x] 8.5 更新 `docs/designs/core-mechanisms/08-governance.md`：新增审计阶段对主 Agent 职责边界遵守情况的核验项（以门控拒绝记录与工具调用分布为依据）；验证方式：该文件内可检索到该核验项

## 9. 端到端验证（波次 6）

- [ ] 9.1 在 `software-dev-agent` 上跑一个中等规模真实变更，完整执行 explore → archive 全流程；验证方式：变更产出的全部阶段产物齐全、门控与读取纪律在运行中生效、无流程阻塞
- [ ] 9.2 核验自动机制生效：检查该变更归档后产品级文档的修订记录是否被裁剪至 3 条、被移出记录是否进入 `changelog.md`、章节索引是否同步；验证方式：三项均可观测，结果写入 `verification.md`
- [ ] 9.3 用本次分析脚本（缓存读取量聚合、阶段分段测算、references 加载成本）度量该变更的 token 消耗，并与 18.28 B 基线对比；验证方式：产出前后对比表写入 `verification.md`，实际降幅与 `proposal.md` 预期的 4.2x 一并记录（未达预期时须给出归因）
- [ ] 9.4 在 `software-dev-agent` 上执行一次存量文档优化：调用 `/kflow-doc-optimize`，对 `CONTEXT.md`、`docs/designs/**`、`docs/open/**` 与活跃变更目录执行清单识别 → 用户确认 → 执行 → 引用校验；验证方式：产出优化报告（含实际执行项、体积变化、更新过的引用清单），且引用校验无断链；执行前须产出受影响引用清单并留档以备反向还原
- [ ] 9.5 抽取该变更的主会话与子代理 transcript，核验三项设计要求是否落实——主 Agent 未直接执行阶段主工作、references 加载仅含本阶段章节、大文档未整体读取；验证方式：三项均有可观测证据，结果写入 `verification.md`
- [ ] 9.6 在 `software-dev-agent` 的 `CLAUDE.md`「项目自定义规则」区块中，为 `kflow-doc-optimize` 增加适用边界例外声明（该区块由项目自行维护，kflow-init 不覆盖，故为**项目侧手工改动**）；验证方式：区块内可检索到该例外声明，且区块的其余内容未被改动；须在 9.4 执行存量优化**之前**完成，否则该 Skill 会被项目自身的适用边界挡住

## 10. 优化能力补强与工程修复（用户裁决追加，2026-10-17）

- [x] 10.1 修复 `scripts/package-skills.sh` 的打包格式：优先用 `zip` 命令或 Python `zipfile` 产出真正的 zip；PowerShell `Compress-Archive` 作为后备；均不可用时降级为 `.tar.gz` 并使用正确扩展名，避免「.zip 实为 gzip」；验证方式：产物经 `file` 识别为 Zip archive，且 zip 内包含新增 Skill 与门控脚本
- [x] 10.2 补强 `kflow-doc-optimize` 的可执行能力：新增 `scripts/scan_docs.py`（按 3 条 / 30 KB / 80 KB 阈值扫描并输出清单）、`scripts/check_refs.py`（引用扫描、留档、替换与校验）、`references/report-template.md`（优化报告格式）；验证方式：三个脚本在临时项目上分别通过自测，引用替换与断链检测行为符合预期
- [x] 10.3 补强 `kflow-init` 的配置校验能力：新增 `scripts/verify_project_config.py`，校验 `autoCompactWindow`、门控注册条目、matcher 与门控脚本落位；在 SKILL.md 步骤 3.5 与 `permission-model.md` §5.4 声明校验动作；验证方式：合规配置退出码 0，缺失 `autoCompactWindow` 时退出码 1 且输出缺失项
- [x] 10.4 同步更新 `CLAUDE.md`：核心内容与项目结构加入 `references-src/`；Skill 开发规范加入 references 生成规则；新增「文档与状态治理」章节；更新打包格式说明；验证方式：上述条目均可检索到
- [x] 10.5 回归验证：`sync-references.sh`、`validate-frontmatter.py`、`validate-injection-scope.sh`、`package-skills.sh`、`openspec validate` 全部通过
