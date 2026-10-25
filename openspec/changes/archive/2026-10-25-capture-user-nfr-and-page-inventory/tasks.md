# Tasks

## 1. 功能设计模板更新

- [x] 1.1 在 `docs/designs/templates/changes/{change}/functional-designs/index.md` §一 变更概述内「预期价值」之后新增「非功能期望」小节：期望维度（开放枚举：性能感受/安全与合规/可用性/兼容性/其他）| 期望描述（用户语言）| 关联功能点 三列表格，附「无显式期望时整节标注『本变更无特殊非功能期望』」说明；验证：模板含该小节、枚举与无期望标注规则
- [x] 1.2 在同模板「三、功能结构树」之后新增「四、页面清单」章节（页面名称 | 菜单路径 | 类型〔新建/修改/复用〕| 页面结构描述〔区块级〕| 涉及功能点），原 §四~§八（核心业务流程图/功能点依赖关系图/分册总览/配置项影响矩阵/修订记录）顺延为 §五~§九，纯后端/无前端 FP 标注「本变更无涉及页面」；验证：章节编号连续无断档、轻量档简表规则在章节说明中体现
- [x] 1.3 全仓 grep 旧章节号引用（「四、核心业务流程图」「五、功能点依赖关系图」「六、分册总览」「七、配置项影响矩阵」「八、修订记录」）并同步为新编号；验证：grep 无旧编号引用残留

## 2. explore 专属 references 更新

- [x] 2.1 `skills/kflow-explore/references/clarify-convergence.md` §1.1 内容域表新增第 6 行「非功能期望：用户视角的性能/安全/可用性/兼容期望是否明确且无歧义」，正文与空清单凭据说明、§六 对比表「触发原因」列的「五个内容域」措辞全部改为「六个内容域」；验证：全文 grep 无「五个内容域」残留
- [x] 2.2 `skills/kflow-explore/references/self-review-dimensions.md` 完整性检查表新增检查项「页面清单一致性：页面清单与各 FP 所属页面一致（无孤页/漏页）」；验证：表含新行且审查维度仍为四维枚举

## 3. kflow-explore 设计文档更新

- [x] 3.1 `docs/designs/skills/kflow-explore.md` CLARIFY 相关章节同步六域：候选清单生成规则（五域→六域）、6b 输出覆盖域清单加「非功能期望」；验证：与 `clarify-convergence.md` 表述一致
- [x] 3.2 同文件输出产物表与 OUTPUT 步骤：功能设计文档内容要求补「非功能期望小节（§一）」与「页面清单（§四）」；TIER 档位影响表与 OUTPUT 步骤的轻量档压缩形态两处由「功能点清单+影响分析+修复/实现范围」扩为「…+非功能期望（一行，无则标注）+页面清单（简表或『无』标注）」；验证：两处轻量档描述已更新且一致
- [x] 3.3 同文件自审「审查维度与检查规则」完整性表加「页面清单一致性」检查项；验证：与 `self-review-dimensions.md` 一致
- [x] 3.4 同文件「域内内容」表与 SKILL.md 域内内容表统一为同一张表（含页面结构/菜单层级、非功能期望、页面清单），消除既有措辞偏差；验证：两表逐行对照一致

## 4. kflow-design 下游消费更新

- [x] 4.1 `docs/designs/skills/kflow-design.md` 执行流程步骤 6（NFR）描述补输入来源：「以 functional-designs/index.md『非功能期望』小节为需求输入，将用户视角期望转译为可度量技术目标值；探索侧标注『无特殊非功能期望』时按既有最小要求自行定义」；`docs/designs/templates/changes/{change}/detailed-design.md` §三 NFR 章节头部加「需求输入」说明行；验证：两处均含输入来源说明

## 5. 设计文档 → SKILL.md 同步

- [x] 5.1 `skills/kflow-explore/SKILL.md` 同步设计文档全部变更：6b/6c 六域表述、输出产物表内容要求、OUTPUT 步骤与轻量档描述、自审完整性检查项、域内内容表、核心提醒补两条（非功能期望业务语言边界、页面清单一致性）；验证：与 `docs/designs/skills/kflow-explore.md` 逐节对照无遗漏（`.claude/skills/` 中无 kflow 条目，无运行时副本需同步）
- [x] 5.2 `skills/kflow-design/SKILL.md` 同步 NFR 步骤输入来源说明；验证：与设计文档 NFR 步骤表述一致

## 6. 集成校验

- [x] 6.1 运行 `openspec validate capture-user-nfr-and-page-inventory --strict` 通过（delta 格式、场景层级、能力路径均合法）
- [x] 6.2 运行 `bash scripts/sync-references.sh` 通过且无 diff（确认 explore 专属 references 改动未影响共享切片生成）
- [x] 6.3 全仓 grep 校验：无「五个内容域」残留、无旧章节号引用残留、「非功能期望」与「页面清单」在设计文档/SKILL.md/模板/references 四类落点均存在
