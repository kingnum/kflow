# Spec Delta

## ADDED Requirements

### Requirement: 变更概述包含非功能期望

functional-designs/index.md 的变更概述章节 SHALL 包含「非功能期望」小节，记录用户视角的非功能期望，作为详细设计 NFR 章节的需求输入。期望描述 SHALL 使用业务语言，SHALL NOT 定义技术目标值（如并发数、P95 指标——技术指标由详细设计阶段 NFR 章节定义）。

#### Scenario: 非功能期望表结构

- **WHEN** functional-designs/index.md 生成
- **THEN** 变更概述章节包含「非功能期望」小节
- **AND** 每条期望包含：期望维度（性能感受/安全与合规/可用性/兼容性/其他，开放枚举）、期望描述（用户语言）、关联功能点

#### Scenario: 无显式期望时标注

- **WHEN** 用户未表达任何非功能期望
- **THEN** 「非功能期望」小节 SHALL 标注「本变更无特殊非功能期望」
- **AND** SHALL NOT 省略该小节

#### Scenario: 业务语言边界

- **WHEN** 用户表达的非功能期望含技术性表述（如具体指标数值）
- **THEN** 探索阶段 SHALL 记录为用户原意描述并标注口径来源
- **AND** SHALL NOT 将其转写为可度量技术目标值（该转译由详细设计 NFR 章节执行）

### Requirement: 功能设计索引包含页面清单

functional-designs/index.md SHALL 包含「页面清单」章节，以页面为视角汇总变更涉及的页面及页面级结构描述（区块级文字描述，非视觉稿），作为原型设计阶段的输入基线，并为跳过原型设计的变更提供页面结构的最低承载。

#### Scenario: 页面清单表结构

- **WHEN** functional-designs/index.md 生成且变更涉及前端功能点
- **THEN** 包含「页面清单」章节，位置紧随「功能结构树」之后
- **AND** 每行包含：页面名称、菜单路径、类型（新建/修改/复用）、页面结构描述（区块级）、涉及功能点

#### Scenario: 无前端功能点时标注

- **WHEN** 变更为纯后端项目或不含前端功能点
- **THEN** 「页面清单」章节 SHALL 标注「本变更无涉及页面」
- **AND** SHALL NOT 省略该章节

#### Scenario: 页面清单与功能点页面归属一致

- **WHEN** 页面清单生成
- **THEN** 各功能点「所属页面与菜单」中出现的页面 SHALL 均在页面清单中
- **AND** 页面清单中每个页面的涉及功能点 SHALL 与功能点页面归属互相一致（无孤页、无漏页）

#### Scenario: 轻量档简化

- **WHEN** 变更档位为轻量
- **THEN** 页面清单保留简表（页面结构描述可合并为一句）
- **AND** SHALL NOT 因轻量档省略该章节
