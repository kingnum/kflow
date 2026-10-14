# Spec Delta

## MODIFIED Requirements

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
