# Tasks

## 1. 修正打包脚本

- [x] 1.1 将 `scripts/package-skills.sh` 的 `SKILLS_DIR` 由 `$REPO_ROOT/.claude/skills` 改为 `$REPO_ROOT/skills`，并把「扫描 .claude/skills/kflow-* ...」的过期提示文本改为动态引用扫描根（消除过期字面量而非删除该行）；验证：运行 `bash scripts/package-skills.sh clarify-version-management` 输出「共打包 18 个 Skills」，且 zip 目录清单含 18 个 `kflow-*` 目录与 18 个 `SKILL.md`
- [x] 1.2 在扫描循环后加入空集合断言：`SKILL_COUNT` 为 0 时输出错误、清理工作目录并以非零状态退出；并让版本一致性校验统计实际校验数，与打包数不符时同样失败（空集合会使该校验空转通过）；验证：临时将 `SKILLS_DIR` 指向不存在的目录运行脚本，脚本报错退出且不生成 zip
- [x] 1.3 校验版本一致性在真实不一致时失败；验证：把 `skills/kflow-code/SKILL.md` 的 `version` 改为 `0.0.0` 运行脚本，脚本报出该文件与 `VERSION` 不一致并以非零状态退出（在实际管线中由打包前的 front matter 门控拦截，早于打包扫描，见 7.2）；随后运行 `bash scripts/sync-version.sh` 恢复

## 2. 规格层收敛

- [x] 2.1 重写 `openspec/specs/unified-version/spec.md`：删除「SKILL.md 版本字段移除」需求；「Single version source for all documents」改为三层载体规则（仓库级 `VERSION` / Skill 级 SKILL.md `version` 字段 / 文档级「参见 VERSION」）并删除「SKILL.md frontmatter SHALL NOT contain version」子句；「统一版本号文件」去掉写死的 16 个 Skills 计数；新增「SKILL.md 版本字段同步」「打包前版本一致性校验」「消费方查看已安装版本」「归档后版本流程顺序」「版本管理规则唯一性」五个需求；验证：`openspec validate unified-version --type spec` 通过且 `grep -c '^### Requirement:'` 为 9
- [x] 2.2 删除 `openspec/specs/version-tracking/` 与 `openspec/specs/version-field-removal-rule/` 两个目录；验证：两个路径均不存在，且 `openspec list --specs` 不再列出这两个能力
- [x] 2.3 修正 `openspec/specs/skill-packaging/spec.md`：「打包范围与排除规则」扫描根改为 `skills/kflow-*` 并说明 `.claude/skills/` 不得作为扫描根，新增「扫描根为仓库内实现目录」「扫描结果为空时打包失败」「路径引用按消费方布局重写」场景；「打包触发时机」补入 SKILL.md 同步前置条件、新增「同步未完成时不打包」场景，并把 zip 产物改为不随 commit 提交；验证：`openspec validate skill-packaging --type spec` 通过
- [x] 2.4 运行 `openspec validate clarify-version-management --type change --strict`，确认变更与四个规格增量全部通过校验

## 3. 规则载体同步

- [x] 3.1 在 `CLAUDE.md` 新增「归档后规则」章节，陈述六步顺序（判定自增级别 → 更新 VERSION → 运行 `sync-version.sh` → 更新 README → 运行 `package-skills.sh` → git commit）与失败不阻塞归档；把「版本管理」章节的字面示例改为相对描述（patch 位 +1 / minor 位 +1 且 patch 归零 / major 位 +1 且其余归零）；验证：`grep -n '归档后规则' CLAUDE.md` 命中章节标题，且 `grep -c '0\.18\.0' CLAUDE.md` 为 0
- [x] 3.2 设计文档 → SKILL.md 同步：更新 `skills/kflow-init/SKILL.md` 注入规则 Marker 2 第 7 条，补入运行 `sync-version.sh` 同步 SKILL.md 版本字段的环节，并把「将 VERSION、targets/ 和归档产物一并提交」改为「提交 VERSION、SKILL.md 版本变更与 README 版本条目（zip 产物受 .gitignore 排除，不提交）」；验证：`sed -n '342p' skills/kflow-init/SKILL.md` 的文本含 `sync-version.sh` 且不含 `targets/`
- [x] 3.3 同步更新 `docs/designs/skills/kflow-init.md` 第 609 行的同段注入规则源文本，使其与 3.2 的 SKILL.md 措辞一致；验证：`grep -n 'targets/' docs/designs/skills/kflow-init.md` 不再命中注入规则段
- [x] 3.4 更新 `docs/designs/core-mechanisms/08-governance.md` §18.5 第 2 条，把「若确认，则在 commit 前执行版本自增和打包」展开为与 3.1 一致的六步顺序；验证：该节文本含 `sync-version.sh` 与六个步骤的先后关系

## 4. 过期计数与失效表述清理

- [x] 4.1 修正 `docs/designs/skills/kflow-archive.md` 与 `docs/designs/skills/kflow-init.md` 页头的「（统一版本管理，16 个运行时 Skills 共享版本号）」为 18 个；验证：`grep -rn '16 个运行时 Skills' docs/` 无命中
- [x] 4.2 修正 `README.md` 目录结构速查中的「16 个 kflow-* Skills」为 18 个（变更历史条目 `v0.15.0`/`v0.16.0` 附近的字面计数不改写）；验证：`grep -n '16 个 kflow' README.md` 仅命中版本历史条目
- [x] 4.3 全库扫描确认失效表述已清除；验证：`grep -rn 'SKILL.md 不应包含独立版本号\|SHALL NOT contain `version:`\|移除 frontmatter 中的独立' openspec/specs/ docs/ skills/ CLAUDE.md README.md` 无命中

## 5. 验证闭环

- [x] 5.1 验证规格集合对版本字段给出唯一结论；验证：`grep -rln 'version:' openspec/specs/` 后逐文件检查，确认关于 SKILL.md 是否含 `version:` 字段的要求仅出现在 `unified-version/spec.md` 且为「须包含」
- [x] 5.2 端到端验证版本流程可执行；验证：依次运行 `bash scripts/sync-version.sh`（输出 18 个已同步）与 `bash scripts/package-skills.sh clarify-version-management`（输出 18 个 Skills 并生成 zip），解压 zip 核对 18 个 `kflow-*/SKILL.md` 的 `version: 0.18.0`
- [x] 5.3 验证消费方路径重写在修正后仍正确；验证：解压 zip 后对解压目录运行 `grep -rnE '(^|[^./])skills/kflow-code/'` 无命中（即不存在未被 `.claude/` 前缀的源布局路径），且 `grep -rn '.claude/skills/kflow-code/'` 命中的每个路径在该解压目录下均真实存在
- [x] 5.4 运行 `openspec validate --specs --strict` 与 `openspec validate clarify-version-management --type change --strict`，两者均通过

## 10. 既有 strict 校验失败修复

`openspec validate --specs --strict` 暴露 5 处既有格式问题——不在本变更交付物内，也不受本变更影响。经确认一并修复，使 5.4 的全量断言成立。修复只涉及 Purpose 描述与 RFC 2119 关键词，不改变任何需求语义。

- [x] 10.1 补齐 4 个能力的 Purpose 至 50 字符以上：`archive-design-merge`、`archive-manual-entry`、`code-review-phase`、`defect-root-cause`；验证：四者的 Purpose 段落均超过 50 字符且与各自需求内容一致
- [x] 10.2 `resume-product-gate` 的需求「产物验证不影响未验证阶段」补入 SHALL / SHALL NOT 措辞；验证：该需求正文含 RFC 2119 关键词
- [x] 10.3 验证：`openspec validate --specs --strict` 输出 128 passed, 0 failed

## 6. 移除已不存在的 kflow-skills-auditor 残留

`kflow-skills-auditor` 已确认不再存在（见 design.md 的风险条目）。规格与打包脚本中针对它的排除条款指向不存在的对象，且在 `skills/` 扫描根下恒为空操作、无从验证。已归档变更中的历史记录不改写。

- [x] 6.1 移除 `openspec/specs/skill-packaging/spec.md` 与本变更增量 `specs/skill-packaging/spec.md` 中「排除 `kflow-skills-auditor`」的表述及其场景；验证：`grep -rn 'kflow-skills-auditor' openspec/specs/skill-packaging/ openspec/changes/clarify-version-management/specs/skill-packaging/` 无命中
- [x] 6.2 移除 `scripts/package-skills.sh` 的 `EXCLUDE_SKILL` 变量与排除分支；验证：`grep -n 'EXCLUDE_SKILL\|kflow-skills-auditor' scripts/package-skills.sh` 无命中，且打包仍输出 18 个 Skills
- [x] 6.3 同步 `proposal.md` 与 `design.md`：删除「打包时被排除」的失效表述，design.md 的风险条目由「待确认后清理」改为「已移除」，Non-Goals 由「不处理其定位问题」收敛为「不改写归档记录」；验证：`grep -n '打包时被排除' openspec/changes/clarify-version-management/` 无命中
- [x] 6.4 确认活跃规格中残留清零；验证：完成 2.1、2.2 后，`grep -rn 'kflow-skills-auditor' openspec/specs/ scripts/ docs/ skills/ CLAUDE.md README.md` 在活跃规格与实现文件（openspec/specs/、scripts/、docs/、skills/、CLAUDE.md）中无命中；README.md 仅剩 v0.18.0 版本更新说明中「残留清理」一条叙述性记录（描述本次变更清除了什么），按 4.2 已确立的「变更历史条目不改写」原则保留（`unified-version` 的例外条款随「SKILL.md 版本字段移除」需求整体移除，`version-field-removal-rule` 随目录删除，二者均由 2.1、2.2 承载）

## 7. 打包前置 front matter 校验

打包的失败模式必须可见：front matter 非法会使 `npx skills add` 静默跳过对应 Skill，安装数量少于实际数量而不报错；这与本变更修正的「空集合同样报告成功」属同一类缺陷。

- [x] 7.1 新增 `scripts/validate-frontmatter.py`：校验 `skills/kflow-*/SKILL.md` 的 front matter 可解析、`name`/`description` 必填、`name` 与目录名一致、`version` 与 `VERSION` 一致、`description` 含中文触发词，并覆盖 `.claude/skills/*` 与设计规格的 `yaml` 代码块（模板占位符解析前替换）；验证：`python scripts/validate-frontmatter.py` 输出 39 项通过、退出码 0
- [x] 7.2 在 `package-skills.sh` 接入阻断式门控：校验未通过则输出错误、以非零状态退出且不进入打包；验证：把某 `SKILL.md` 的 `description` 中的全角冒号改回 ASCII `": "`，运行脚本在产包前中止且退出码非零
- [x] 7.3 规格层补入对应场景；验证：本变更增量与 `openspec/specs/skill-packaging/spec.md` 均含「front matter 非法时打包失败」场景

## 8. 修正打包的跨 Skill 路径重写

任务 5.3 首次真实打包验证暴露：路径重写以当前 Skill 名作为替换目标，导致其他 Skill 的 `references/` 中对 `kflow-code` 脚本的跨 Skill 引用（94 处）与 `with_server.py` 的示例路径未被改写，消费方解压后指向消费项目中不存在的源布局路径。此前扫描根错误产出空包，该重写从未真正执行过，缺陷因此未被发现。

- [x] 8.1 扩展 `scripts/package-skills.sh` 的路径重写：替换目标由 `skills/$skill_name/` 泛化为全部 `skills/kflow-*/`，文件范围由 `*.md` 扩展到 `*.py`，并以前置字符断言规避对已带 `.claude/` 前缀的路径重复加前缀；验证：重新打包后按 5.3 的断言扫描解压目录，源布局路径 0 命中，无 `.claude/.claude` 重复前缀
- [x] 8.2 规格层同步：本变更增量与 `openspec/specs/skill-packaging/spec.md` 的「路径引用按消费方布局重写」场景由 `skills/<skill-name>/` 泛化为 `skills/<任意 kflow-* 名称>/`，并补入跨 Skill 引用、`*.py` 覆盖与不重复加前缀三条断言；验证：`openspec validate clarify-version-management --type change --strict` 通过

## 9. 修复悬空引用

任务 5.3 的路径重写修正后，扫描发现 32 处引用指向不存在的文件。这些引用在源仓库中早已存在（非本次引入），逐类修复：

- [x] 9.1 类别 1——路径写错：8 个 Skill 的 `references/repetition.md` 中指向 `<自身>/references/permission-model.md` 的 32 处引用改为 `skills/kflow-init/references/permission-model.md`（该文件的唯一所有者，引用文本本就是「kflow-init 依据该文件配置权限」）；验证：`grep -rn 'permission-model\.md' skills/*/references/repetition.md` 全部指向 kflow-init
- [x] 9.2 类别 2——模板冗余：9 个 Skill 的 `references/hooks.md`「服务生命周期操作步骤」章节中指向 `<自身>/references/service-lifecycle.md` 的 9 处引用改为 `skills/kflow-code/references/service-lifecycle.md`；验证：`grep -rn '服务生命周期具体操作指令定义在' skills/*/references/hooks.md` 全部指向 kflow-code
- [x] 9.3 类别 3——基础层文件遗漏：补齐 `skills/kflow-bug-fix/references/state-values.md`（按 `07-agent-model.md` §分层加载表属基础层、适用全部阶段）；验证：与主流版 md5 一致
- [x] 9.4 类别 4——引用描述不当：`skills/kflow-resume/references/recovery-protocol.md` 的 GATE 步骤引用由 `<自身>/references/gates.md` 改为「当前阶段 Skill 的 gates.md」（各 Skill 的 gates.md 按阶段裁剪，无单一副本可补），并把该 ASCII 框行宽由 77 校正为 65 与相邻行对齐
- [x] 9.5 规格层同步：`skill-self-contained` 的「Zero external dependency after installation」场景补入跨 Skill 引用白名单（共享脚本、单一所有者规则文件）与「引用路径须在安装布局中真实存在」断言，修正其与「with_server.py relocated to kflow-code」需求的冲突；验证：`openspec validate skill-self-contained --type spec` 通过
- [x] 9.6 端到端验证：重新打包后 5.3 两项断言均通过，且全库无悬空引用
- [x] 9.7 设计文档同步：`docs/designs/skills/kflow-resume.md` 中 2 处指向 `skills/kflow-resume/references/gates.md` §2 规则 9 的失效引用（该文件与「规则 9」章节均不存在）改指向 `skills/kflow-resume/SKILL.md` 步骤 4——产物验证映射的实现载体；验证：设计文档层悬空引用扫描为 0
