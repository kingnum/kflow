# devflow-audit Specification

## Purpose

定义对使用 DevFlow Skills 的项目进行使用情况审计的能力，涵盖单一子代理执行的四项记账职责（阶段门控校验、覆盖率与产物存在性校验、阶段耗时汇总、阻塞级问题兜底）、自动与手动两种触发方式、发现问题的两级严重度处理与按归属阶段回退，以及结构化审计报告的输出。

## Requirements

### Requirement: 审计由单一子代理执行

审计 SHALL 由单个子代理（Agent subagent）执行，SHALL NOT 由主 Agent 直接执行，SHALL NOT 拆分为多个并行子代理。该约束适用于全部变更档位。系统 SHALL NOT 因变更档位而改变审计的执行方式或职责集合。子代理 SHALL 先完成全部职责的事实采集并逐项呈现判定依据，再输出检查项结论。

#### Scenario: 全部档位由单一子代理执行

- **WHEN** 进入审计阶段，无论变更档位为 `轻量` 或 `标准`
- **THEN** 系统 SHALL 启动一个审计子代理执行全部四项记账职责
- **AND** 主 Agent SHALL NOT 直接执行审计工作
- **AND** SHALL NOT 启动多个并行审计子代理

#### Scenario: 审计子代理异常时的处置

- **WHEN** 审计子代理意外停止、报错退出或返回不完整结果
- **THEN** 主 Agent MUST 重新创建新的子代理执行审计
- **AND** SHALL NOT 在主 Agent 上下文中接管审计工作
- **AND** 最多重试 3 次，全部失败后标记 ⚠️ 阻塞并提示用户

#### Scenario: 证据先于评分

- **WHEN** 审计子代理执行四项记账职责
- **THEN** 子代理 SHALL 先完成全部职责的事实采集
- **AND** SHALL 逐项呈现判定依据
- **AND** SHALL 在事实采集完成后才输出检查项结论
- **AND** SHALL NOT 在事实采集未完成时输出结论

### Requirement: 审计四维度评估

系统 SHALL 以四项记账职责执行审计：(a) 校验各阶段门控是否全部通过（读取变更级 `.status.md` 的阶段状态与终止结果字段）；(b) 校验 traceability 覆盖率与阶段产物存在性；(c) 汇总各阶段耗时数据并输出效率摘要；(d) 兜底扫出未被前序环节关闭的阻塞级问题。系统 SHALL NOT 计算加权总评分，SHALL NOT 输出四维度评分表，SHALL NOT 对阶段产物质量作独立评审——产物质量评审由签署清单自证、单轮验证与交叉审查承担。

#### Scenario: 流程合规性审计

- **WHEN** 执行审计
- **THEN** 系统 SHALL 读取变更级 `.status.md` 并校验各阶段门控是否全部通过
- **AND** 检查是否存在跳阶段情况
- **AND** 检查可选阶段是否正确处理（跳过 vs 执行）
- **AND** 检查回退是否走正规流程（⚠️ 需修订 → 修订 → 完成）
- **AND** 检查阶段的终止结果取值是否合法（`验证通过` / `验证发现问题({N})` / `执行完成`，历史取值 `收敛` / `未收敛` 按读取侧归并规则处理）
- **AND** SHALL NOT 将具有阶段适用性声明依据的 `⏭️ 不适用` 阶段判定为跳阶段
- **AND** 本场景的检查项 SHALL 归属记账职责 (a) 门控校验

#### Scenario: 产物完整性审计

- **WHEN** 执行审计
- **THEN** 系统 SHALL 校验各阶段必须产物是否存在（.status.md、functional-designs/、detailed-design.md、tasks.md、traceability.md）
- **AND** 检查条件产物是否正确处理（🔶 / ⏭️ 图例）
- **AND** 检查产物内容非空且无占位符
- **AND** SHALL NOT 将合法裁剪阶段缺失的 `api-tests/`、`e2e-tests/`、`test-reports/integration/` 判定为缺项
- **AND** 本场景的检查项 SHALL 归属记账职责 (b) 覆盖率与产物存在性校验

#### Scenario: 审查质量审计

- **WHEN** 执行审计
- **THEN** 系统 SHALL 校验 `traceability.md` 的覆盖率是否达 100%
- **AND** SHALL 校验自审报告 `self-reviews/{phase}/report.md` 是否存在（份数为 1 为正常形态）
- **AND** SHALL NOT 因缺少超出该档位要求的视角报告而判为缺项
- **AND** SHALL NOT 因自审报告仅 1 份而判为缺项或轮次超标
- **AND** 本场景的检查项 SHALL 归属记账职责 (b) 覆盖率与产物存在性校验

#### Scenario: 测试充分性审计

- **WHEN** 执行审计
- **THEN** 系统 SHALL 校验接口单元测试、E2E 测试与集成测试阶段（适用时）的门控是否通过
- **AND** SHALL 校验其执行报告是否存在且定向重验结果是否通过
- **AND** SHALL NOT 将合法裁剪的测试阶段判定为缺项
- **AND** 本场景的检查项 SHALL 归属记账职责 (a) 门控校验

#### Scenario: 缺陷管理审计

- **WHEN** 执行审计
- **THEN** 系统 SHALL 兜底扫出未被前序环节关闭的阻塞级问题
- **AND** 检查根因分类是否执行
- **AND** 检查修复是否闭环
- **AND** 检查设计错误是否正确触发回退
- **AND** 记录该问题的归属阶段以支持回退路由
- **AND** 本场景的检查项 SHALL 归属记账职责 (d) 阻塞级问题兜底

#### Scenario: 效率指标审计

- **WHEN** 执行审计
- **THEN** 系统 SHALL 汇总各阶段的耗时与子代理轮次数据
- **AND** SHALL 输出效率摘要（含总耗时、各阶段耗时占比、最耗时阶段）
- **AND** SHALL 统计缺陷发现-修复周期
- **AND** 终止结果为 `验证发现问题({N})` 或 `定向重验失败` 的阶段 SHALL 核验存在对应的处理记录
- **AND** 该摘要 SHALL 仅作信息展示，SHALL NOT 参与门控判定
- **AND** 本场景的检查项 SHALL 归属记账职责 (c) 耗时数据汇总

#### Scenario: Post-mortem 汇总审计

- **WHEN** 执行审计
- **THEN** 系统 SHALL 读取全部子变更 fix-report 的关联建议
- **AND** 按类型归类架构改进机会（测试 seam / 模块耦合 / 接口契约 / 其他）
- **AND** 汇总到审计报告的改进建议章节
- **AND** 本场景的检查项 SHALL 归属记账职责 (c) 耗时数据汇总

#### Scenario: 加权总分不参与门控

- **WHEN** 审计完成并作出判定
- **THEN** 判定 SHALL 仅依据问题清单的严重度分级（阻塞 / 建议）作出
- **AND** 审计报告 SHALL NOT 包含加权总分与四维度评分表
- **AND** SHALL NOT 存在任何评分参与门控判定的路径

### Requirement: 审计触发机制

系统 SHALL 支持两种审计触发方式：归档前自动触发和随时手动调用。

#### Scenario: 归档前自动触发

- **WHEN** 集成测试通过后进入归档流程
- **THEN** 系统自动执行审计作为归档门控
- **AND** 审计通过后方可继续归档

#### Scenario: 手动调用审计

- **WHEN** 用户直接调用 kflow-audit
- **THEN** 系统对指定变更或全部活跃变更执行审计
- **AND** 输出审计报告

### Requirement: 审计结果分级处理

系统 SHALL 按严重度对审计发现的问题分级处理，分级 SHALL 为两级：`阻塞` 与 `建议`。

#### Scenario: 阻塞级问题处理

- **WHEN** 审计发现阻塞级问题（缺少必须产物、阶段门控未通过、阶段跳转、审查未闭环、裁剪无声明依据）
- **THEN** 系统 SHALL 阻断归档
- **AND** SHALL 要求修复后重新审计

#### Scenario: 严重级问题处理

- **WHEN** 审计发现的问题不构成阻塞但不构成建议（如 traceability 覆盖率不足但产物齐全）
- **THEN** 系统 SHALL 阻断归档
- **AND** SHALL 记录该问题的归属阶段以支持回退路由
- **AND** SHALL 建议修复后重新审计

#### Scenario: 建议级问题处理

- **WHEN** 审计发现建议级问题（文档格式不规范、耗时数据缺失、效率异常）
- **THEN** 系统 SHALL NOT 阻断归档
- **AND** SHALL 记录改进建议到 `docs/skill-suggestion.md`

### Requirement: 审计回退路由

系统 SHALL 在审计发现问题时按问题归属阶段触发回退，作为第 4 种回退触发来源。

#### Scenario: 审计发现设计阶段问题

- **WHEN** 审计发现的问题归属为设计探索或详细设计阶段
- **THEN** 对应设计阶段标记为 ⚠️ 需修订
- **AND** 重置后续全部阶段为 ⏳ 待开始

#### Scenario: 审计发现编码阶段问题

- **WHEN** 审计发现的问题归属为编码阶段
- **THEN** 编码阶段标记为 ⚠️ 需修订
- **AND** 修复代码后重新审查

#### Scenario: 审计发现测试阶段问题

- **WHEN** 审计发现的问题归属为测试阶段
- **THEN** 对应测试阶段标记为 ⚠️ 需修订
- **AND** 补充测试后重新验证

### Requirement: 审计报告输出

系统 SHALL 输出结构化的审计报告，报告 SHALL 包含：四项记账职责各自的检查结论、阶段耗时与效率摘要、按严重度分级（阻塞 / 建议）的问题清单、改进建议。报告 SHALL NOT 包含四维度评分表或加权总分。全部变更档位 SHALL 采用同一报告形态。

#### Scenario: 审计报告内容

- **WHEN** 审计完成
- **THEN** 审计报告 SHALL 包含四项记账职责各自的检查结论
- **AND** SHALL 包含阶段耗时与效率摘要
- **AND** SHALL 包含按严重度分级的问题清单
- **AND** SHALL 包含改进建议
- **AND** SHALL NOT 包含四维度评分表与加权总分

#### Scenario: 轻量档审计记录形态

- **WHEN** 变更档位为 `轻量` 且审计完成
- **THEN** 审计报告 SHALL 采用与 `标准` 档相同的形态
- **AND** SHALL NOT 存在按档位分化的简化审计路径

#### Scenario: 历史变更的完整档取值按标准档审计

- **WHEN** 变更级 `.status.md` 的 `变更档位` 字段读取到历史遗留的 `完整` 取值
- **THEN** 审计 SHALL 按 `标准` 档的记录形态输出
- **AND** SHALL NOT 因该历史取值而要求四视角审查产物
