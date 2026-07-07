## ADDED Requirements

### Requirement: 原型产物清单（Prototype Manifest）存在性

每个有原型设计的变更 SHALL 在原型设计阶段用户确认通过后，生成或更新 `prototype/index.md` 作为原型产物清单（Prototype Manifest），供下游阶段读取。

#### Scenario: 原型产物清单在用户确认通过后生成

- **WHEN** 原型设计阶段用户确认通过（REVIEW 步骤选择"确认通过"）
- **THEN** 系统 SHALL 从 prototype/ 目录下实际生成的文件中生成/更新 `prototype/index.md`
- **AND** `prototype/index.md` SHALL 反映最终产物全貌，而非初始模板

#### Scenario: 修订后重新生成产物清单

- **WHEN** 原型设计阶段进入修订循环且新一轮用户确认通过
- **THEN** 系统 SHALL 重新扫描 prototype/ 目录
- **AND** 更新 `prototype/index.md` 中的文件清单和版本号
- **AND** 同步更新 design-tokens.css 和 element-coverage-tree.md

#### Scenario: 无原型设计的变更不生成

- **WHEN** 原型设计阶段被跳过（⏭️ 跳过）
- **THEN** `prototype/index.md` SHALL NOT 被生成
- **AND** 下游阶段 SHALL NOT 尝试读取 `prototype/index.md`

### Requirement: 原型产物目录写权限归属

`prototype/` 目录的写权限 SHALL 仅归属于原型设计阶段（kflow-prototype-design）。其他阶段对 `prototype/` 目录只读，不得修改其中任何文件。`index.md` 的新鲜度由阶段边界天然保证，无需额外校验机制。

#### Scenario: 其他阶段不得修改原型产物

- **WHEN** 下游阶段（plan、code、code-review、e2e-test、integration-test）执行过程中发现原型产物存在问题
- **THEN** 系统 SHALL 通过回退机制触发原型设计阶段的修订流程（REVISION 模式）
- **AND** SHALL NOT 直接修改 `prototype/` 目录下的任何文件（含 index.md、HTML 文件、CSS 文件等）
- **AND** 回退修订完成后由原型设计阶段负责更新 `index.md`

#### Scenario: index.md 更新仅在原型设计阶段结束时发生

- **WHEN** 原型设计阶段用户确认通过（初始生成或修订后确认）
- **THEN** 系统 SHALL 在确认通过的同时点自动更新 `prototype/index.md`
- **AND** `index.md` SHALL 反映当前 prototype/ 目录的最终产物全貌
- **AND** 此后的任何阶段均不得修改 `index.md`，直到下一次回退触发原型设计阶段修订

### Requirement: 原型产物清单内容结构

`prototype/index.md` SHALL 包含以下六个段落（按此顺序）：

#### Scenario: 一、产物组织方式

- **WHEN** 系统生成 `prototype/index.md`
- **THEN** SHALL 包含「产物组织方式」段落
- **AND** 描述本次原型的文件结构类型（单文件/多页面/含共享资源）
- **AND** 标注入口文件路径（默认 `index.html`，允许其他入口）

#### Scenario: 二、原型文件清单（含角色标注）

- **WHEN** 系统生成「原型文件清单」段落
- **THEN** SHALL 列出 prototype/ 目录下所有文件
- **AND** 每个文件 SHALL 标注角色：入口页面（entry）/ 独立页面（page）/ 设计令牌（tokens）/ 元素覆盖树（coverage）/ 共享资源（shared）/ 过程产物（process）
- **AND** 下游阶段 SHALL 仅消费角色为 entry、page、tokens、coverage、shared 的文件
- **AND** 过程产物（design-prompt.md、style-decision.md） SHALL 标记为 process 角色

#### Scenario: 三、页面清单（页面-文件映射）

- **WHEN** 系统生成「页面清单」段落
- **THEN** 每个页面 SHALL 标注：页面名称、路由路径、对应原型 HTML 文件路径、所含区域列表
- **AND** 对应原型 HTML 文件路径 SHALL 为相对 prototype/ 目录的实际路径（可能为 `index.html` 内部锚点、`page-xxx.html` 等）

#### Scenario: 四、设计系统引用

- **WHEN** 系统生成「设计系统引用」段落
- **THEN** SHALL 包含色彩方案、字体系统、间距系统、组件库引用及其在 design-system/MASTER.md 中的来源章节

#### Scenario: 五、共享资源清单

- **WHEN** 原型产物包含 `shared/` 子目录
- **THEN** SHALL 列出 shared/ 下所有文件及其用途说明
- **AND** 包含：共享样式文件、共享组件脚本、状态管理器等

#### Scenario: 六、修订记录

- **WHEN** 系统生成「修订记录」段落
- **THEN** SHALL 包含版本号、日期、修订类型、修订内容、影响功能点、触发阶段

### Requirement: 下游阶段通过原型产物清单获取原型文件

下游阶段（plan、code、code-review、e2e-test）SHALL 通过读取 `prototype/index.md` 动态获取原型文件列表，不再硬编码具体文件路径。

#### Scenario: 计划阶段读取原型产物清单

- **WHEN** kflow-plan 为前端子变更生成 tasks.md
- **THEN** 系统 SHALL 读取 `prototype/index.md`
- **AND** 从中获取页面清单（页面-文件映射）作为前端功能点全展开模板的输入源
- **AND** 从中获取设计令牌文件路径（角色为 tokens 的文件）
- **AND** 从中获取元素覆盖树文件路径（角色为 coverage 的文件）

#### Scenario: 编码阶段读取原型产物清单

- **WHEN** kflow-code 为前端子变更执行原型转译
- **THEN** 系统 SHALL 读取 `prototype/index.md`
- **AND** 从「产物组织方式」获取入口文件路径，用于工程骨架搭建的全局布局提取
- **AND** 从「页面清单」获取各页面对应的 HTML 文件路径，用于逐页转译
- **AND** 从「原型文件清单」获取设计令牌文件路径，用于 CSS 变量注入

#### Scenario: 代码审查阶段读取原型产物清单

- **WHEN** kflow-code-review 对前端子变更执行原型对账
- **THEN** 系统 SHALL 读取 `prototype/index.md`
- **AND** 从清单中获取设计令牌文件路径和元素覆盖树文件路径
- **AND** 使用获取的路径执行硬编码颜色值检测和元素覆盖对账

#### Scenario: E2E 测试阶段读取原型产物清单

- **WHEN** kflow-e2e-test 执行视觉一致性对比
- **THEN** 系统 SHALL 读取 `prototype/index.md`
- **AND** 从清单中获取入口文件路径（角色为 entry 的文件）
- **AND** 使用获取的入口文件路径作为视觉对比基准

### Requirement: 门控检查基于原型产物清单

前端子变更的门控检查 SHALL 验证 `prototype/index.md` 的存在性和完整性，而非逐一检查三个原型文件。

#### Scenario: 前端子变更门控检查

- **WHEN** 前端子变更进入 plan 或 code 阶段
- **THEN** 门控检查 SHALL 验证 `prototype/index.md` 存在
- **AND** 验证其「原型文件清单」中包含角色为 entry 的文件条目
- **AND** 验证其「原型文件清单」中包含角色为 tokens 的文件条目（如存在）
- **AND** 验证其「原型文件清单」中包含角色为 coverage 的文件条目（如存在）

#### Scenario: 原型产物清单缺失时的处理

- **WHEN** 前端子变更进入 plan 或 code 阶段
- **AND** `prototype/index.md` 不存在
- **THEN** 门控检查 SHALL 标记 ⚠️ 阻塞
- **AND** 提示原型设计阶段未完成

#### Scenario: 原型设计跳过时的门控处理

- **WHEN** 原型设计阶段状态为 ⏭️ 跳过
- **THEN** 前端子变更的门控检查 SHALL 不要求 `prototype/index.md` 存在
- **AND** 后续阶段 SHALL NOT 执行原型相关的转译或对账步骤

### Requirement: 阶段钩子使用原型产物清单加载

`phase-hooks.md` 中前端SC 相关的 PRE_HOOK 和 RELOAD 产物列表 SHALL 使用 `prototype/index.md` 替代三个分散的原型文件引用。

#### Scenario: PRE_HOOK 产物加载

- **WHEN** plan/code/code-review 阶段 PRE_HOOK 加载前端SC 条件产物
- **THEN** SHALL 加载 `prototype/index.md`（条件，前端SC）
- **AND** SHALL NOT 单独列出 `prototype/design-tokens.css` 和 `prototype/element-coverage-tree.md`
- **AND** 阶段执行时从 `prototype/index.md` 按需读取具体文件路径

#### Scenario: RELOAD 产物加载

- **WHEN** plan/code/code-review 阶段 RELOAD 加载条件产物
- **THEN** SHALL 加载 `prototype/index.md`（条件，前端SC）
- **AND** SHALL NOT 单独列出 `prototype/design-tokens.css` 和 `prototype/element-coverage-tree.md`

### Requirement: 输入限定规则基于清单声明

前端子变更的输入限定规则 SHALL 改为基于 `prototype/index.md` 中声明的产物，保留过程产物排除规则。

#### Scenario: 限定为清单声明的产物

- **WHEN** 前端子变更编码阶段引用原型产物
- **THEN** 系统 SHALL 仅使用 `prototype/index.md` 中角色为 entry/page/tokens/coverage/shared 的文件
- **AND** SHALL NOT 读取角色为 process 的文件（design-prompt.md、style-decision.md）
- **AND** SHALL NOT 读取 `design-system/MASTER.md`

#### Scenario: 设计令牌来源唯一

- **WHEN** 前端子变更需要设计令牌
- **THEN** 系统 SHALL 从 `prototype/index.md` 清单中角色为 tokens 的文件获取设计令牌
- **AND** SHALL NOT 从 HTML 内联样式中硬编码提取（降级处理除外）
