# functional-design-content Specification

## Purpose

定义功能设计文档的内容维度规范，包括前后端项目的完整章节结构和纯后端项目的简化模板章节结构。

## Requirements

### Requirement: 纯后端功能点内容维度定义

纯后端项目的功能点定义 SHALL 使用以下章节结构，与前后端项目共享核心章节但替换 UX 密集型章节。

#### Scenario: 设计域归属
- **WHEN** 纯后端功能点被定义
- **THEN** 每个功能点包含"所属设计域"字段
- **AND** 设计域从 L2 目录扫描提取（如 controllers 域、services 域、models 域）

#### Scenario: 接口参数定义
- **WHEN** 纯后端功能点涉及 API 参数
- **THEN** 每个功能点包含"接口参数定义"列表
- **AND** 每个参数定义：参数名、位置（query/body/path）、类型、必填、校验规则、默认值

#### Scenario: 调用约束定义
- **WHEN** 纯后端功能点有调用限制
- **THEN** 每个功能点包含"调用约束"列表
- **AND** 约束类型包含：限流约束、权限约束、超时约束、幂等约束

### Requirement: 纯后端功能设计完整章节清单

纯后端简化模板 SHALL 包含以下完整章节：

#### Scenario: 章节清单
- **WHEN** 纯后端功能设计文档被生成
- **THEN** 文档包含：功能点ID/名称/优先级、用户故事（API 消费者视角）、所属设计域、可执行操作（API 操作/服务调用）、接口参数定义、业务规则、业务流程上下文（服务调用链视角）、功能行为矩阵、调用约束、修订记录
- **AND** 不包含：所属页面与菜单、表单项定义、交互约束

### Requirement: 功能点包含页面导航信息

每个功能点 SHALL 标注其所属页面和菜单路径。

#### Scenario: 功能点标注页面归属
- **WHEN** functional-designs/ 中定义功能点
- **THEN** 每个功能点包含"所属页面"字段
- **AND** 包含"菜单路径"字段（如适用）
- **AND** 页面和菜单使用用户可见的名称

#### Scenario: 多级模块与功能结构描述
- **WHEN** 应用包含多个业务模块
- **THEN** functional-designs/index.md 包含"三、功能结构树"
- **AND** 以树状图展示模块→功能点层级，每个节点标注 FP-ID、功能名、优先级（[P0]/[P1]/[P2]）和一句话功能简述
- **AND** 明确每个功能点的模块归属

### Requirement: 功能点包含可执行操作清单

每个功能点 SHALL 列出用户在页面上可执行的具体操作。

#### Scenario: 操作清单定义
- **WHEN** functional-designs/ 中定义功能点
- **THEN** 每个功能点包含"可执行操作"列表
- **AND** 每个操作标注触发方式（按钮点击/链接跳转/表单提交/快捷键/手势）
- **AND** 每个操作标注可见条件（如"仅管理员可见"、"登录后显示"）

#### Scenario: 操作与功能点关联
- **WHEN** 一个操作涉及多个功能点
- **THEN** 操作关联到主要功能点
- **AND** 在关联功能点中交叉引用

### Requirement: 功能点包含详细表单项定义

涉及表单输入的功能点 SHALL 定义完整的表单项信息。

#### Scenario: 表单项必需字段
- **WHEN** 功能点涉及表单输入
- **THEN** 每个表单项定义：字段名、显示标签、输入类型（文本框/下拉/日期选择/开关等）
- **AND** 定义校验规则（必填/格式/长度/取值范围）
- **AND** 定义默认值（如有）
- **AND** 定义占位提示文本

#### Scenario: 表单交互行为
- **WHEN** 表单项有联动或条件显示
- **THEN** 定义联动规则（如"选择A时B字段显示"）
- **AND** 定义条件显示逻辑

### Requirement: 功能点包含业务规则定义

每个功能点 SHALL 定义完整的业务规则，包括前置条件、校验规则、触发条件和后置结果。

#### Scenario: 前置条件定义
- **WHEN** 功能点需要满足特定条件才可用
- **THEN** 明确列出所有前置条件
- **AND** 前置条件使用业务语言描述（如"用户已登录"、"购物车非空"）

#### Scenario: 校验规则定义
- **WHEN** 功能点涉及数据验证
- **THEN** 列出所有校验规则
- **AND** 每条规则包含：校验对象、校验条件、不通过时的提示信息

#### Scenario: 触发条件与后置结果
- **WHEN** 功能点由特定事件触发
- **THEN** 明确触发条件（用户操作/系统事件/定时任务）
- **AND** 明确执行成功后的后置结果（状态变更/通知/后续跳转）
- **AND** 明确执行失败时的后置结果（回滚/错误提示/重试）

### Requirement: 业务流程闭环检查

系统 SHALL 在 functional-designs/ 中确保所有业务流程形成完整闭环。

#### Scenario: 业务流程闭环图
- **WHEN** functional-designs/index.md 生成
- **THEN** 包含核心业务流程图
- **AND** 每个流程从触发点到最终结果形成完整路径
- **AND** 标注流程中的分支条件和异常路径

#### Scenario: 断点检测
- **WHEN** explore 自审执行闭环性检查
- **THEN** 检查每个业务流程是否无断点
- **AND** 检查是否存在"无处可去"的中间状态

### Requirement: 功能结构树内容要求

functional-designs/index.md 中的"三、功能结构树" SHALL 以模块→功能点的两级树状结构展示，替代原有的"三、页面导航结构图"。

#### Scenario: 树状结构格式
- **WHEN** functional-designs/index.md 生成功能结构树
- **THEN** 树状结构 SHALL 以应用名称为根节点
- **AND** 一级节点为业务模块（以 `📁` 前缀标识，标注功能点数量）
- **AND** 二级节点为功能点（标注 FP-ID、功能名、优先级 [P0]/[P1]/[P2]、一句话简述）
- **AND** 模块划分 SHALL 基于业务域，与菜单结构对齐

#### Scenario: 功能简述规范
- **WHEN** 功能结构树中描述功能点
- **THEN** 每个功能点 SHALL 使用 `— {一句话简述}` 格式
- **AND** 简述 SHALL 概括核心行为和价值
- **AND** 简述长度 SHALL 控制在 40 字以内
- **AND** 存在依赖关系时 SHALL 在简述后标注（如"依赖: FP-xxx"）

#### Scenario: 与下游阶段的对接
- **WHEN** 功能结构树生成完成
- **THEN** 原型设计阶段 SHALL 以功能结构树为页面/功能全景参考
- **AND** 详细设计阶段 SHALL 以功能结构树的模块划分为技术设计分组依据
- **AND** 功能结构树 SHALL 与功能点清单表格（第二章）保持一一对应

### Requirement: 功能点包含关联配置项信息

每个功能点 SHALL 标注其关联的配置项，描述配置项与功能行为的关联关系。

#### Scenario: 功能点关联配置项定义

- **WHEN** functional-designs/part-NN.md 中定义功能点
- **THEN** 每个功能点 SHALL 包含"关联配置项"章节
- **AND** 该章节 SHALL 包含一个表格，字段为：配置项名称、关联功能点ID、关联类型、配置值变化→功能行为变化描述
- **AND** 关联类型 SHALL 从以下枚举中选择：控制可见性、控制数据范围、控制校验规则、控制流程分支、控制权限

#### Scenario: 功能点无关联配置项

- **WHEN** 功能点不依赖任何配置项
- **THEN** "关联配置项"章节 SHALL 标注"本功能点无关联配置项"
- **AND** SHALL NOT 省略该章节

### Requirement: 功能设计索引包含全局配置项影响矩阵

functional-designs/index.md SHALL 包含一个汇总所有功能点配置项关联的全局矩阵。

#### Scenario: 全局配置项影响矩阵格式

- **WHEN** functional-designs/index.md 生成或更新
- **THEN** SHALL 包含"配置项影响矩阵"章节
- **AND** 矩阵 SHALL 包含字段：配置项名称、类型、默认值、受影响功能点ID列表、影响类型汇总
- **AND** 矩阵内容 SHALL 与各分册中功能点定义的"关联配置项"章节保持一致

## ADDED by design-change-record

### Requirement: 功能设计索引包含修订记录不重复

functional-designs/index.md SHALL 仅包含一张修订记录表，不再包含独立的需求变更记录表。

#### Scenario: 合并后的修订记录表

- **WHEN** functional-designs/index.md 被创建或修订
- **THEN** SHALL 仅包含"八、修订记录"节
- **AND** 表 SHALL 包含列：版本、日期、修订类型、修订内容、影响功能点、触发阶段
- **AND** 修订类型枚举 SHALL 包含"需求变更"以区分需求层面的变更

#### Scenario: 不再包含独立的需求变更记录

- **WHEN** functional-designs/index.md 被生成
- **THEN** SHALL NOT 包含独立的"需求变更记录"节
- **AND** 原需求变更记录的内容 SHALL 纳入统一修订记录表

## ADDED by subchange-type-enforcement

### Requirement: 功能点清单包含类型列

functional-designs/index.md 的功能点清单 SHALL 包含「类型」列，标记每个功能点为后端或前端。

#### Scenario: 类型列位置

- **WHEN** functional-designs/index.md 生成功能点清单
- **THEN** 表格 SHALL 在「简述」和「优先级」之间增加「类型」列
- **AND** 「类型」列 SHALL 在「优先级」之前显示
- **AND** 列值为枚举：`后端` | `前端`

#### Scenario: 后端 FP 判定标准

- **WHEN** 功能点涉及 API 实现、服务逻辑、数据模型、数据库操作、业务规则或外部服务集成
- **THEN** SHALL 标记为「后端」

#### Scenario: 前端 FP 判定标准

- **WHEN** 功能点涉及页面、组件、路由、状态管理、样式或 CSS 变量注入
- **THEN** SHALL 标记为「前端」

#### Scenario: 无法归类则拆分

- **WHEN** 功能点同时涉及后端和前端判定标准的内容
- **THEN** SHALL 判定为粒度过粗
- **AND** MUST 拆分为独立的后端 FP 和前端 FP
- **AND** 两个 FP 在「关联功能点」列相互引用

#### Scenario: 统计信息包含类型统计

- **WHEN** functional-designs/index.md 生成统计信息
- **THEN** 统计表 SHALL 增加「后端 FP 数量」和「前端 FP 数量」两行

### Requirement: 功能点标注跨层关联

后端 FP 如影响前端展示或表单字段，SHALL 在「关联功能点」列显式标注受影响的前端 FP-ID。

#### Scenario: Schema→UI 影响标注

- **WHEN** 后端 FP 涉及数据库 Schema 变更
- **AND** 该 Schema 变更影响前端展示
- **THEN** 后端 FP 的「关联功能点」列 SHALL 包含受影响前端 FP-ID
- **AND** 前端 FP 的「依赖功能点」列 SHALL 包含后端 FP-ID
- **AND** 关联关系类型 SHALL 标注为「数据模型变更」
