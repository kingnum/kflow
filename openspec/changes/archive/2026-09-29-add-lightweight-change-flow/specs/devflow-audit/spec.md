# Spec Delta

## ADDED Requirements

### Requirement: 轻量档审计降级为轻量自检

变更档位为 `轻量` 时，审计 SHALL 由七维度加权评分子代理审计降为主 Agent 轻量自检，且 SHALL 保留归档门控地位。轻量自检 SHALL 输出简化审计记录，SHALL NOT 输出七维度评分报告。

#### Scenario: 轻量档走轻量自检

- **WHEN** 变更档位为 `轻量` 且进入审计阶段
- **THEN** 系统 SHALL 由主 Agent 执行轻量自检
- **AND** SHALL NOT 启动七维度评估子代理
- **AND** SHALL NOT 计算加权总评分

#### Scenario: 轻量自检检查项

- **WHEN** 执行轻量自检
- **THEN** 系统 SHALL 检查阶段完整性（无越界的阶段跳转）
- **AND** SHALL 检查阶段产物存在性与无占位符
- **AND** SHALL 检查每个 `⏭️ 不适用` 阶段均有阶段适用性声明依据

#### Scenario: 轻量自检保留归档门控地位

- **WHEN** 轻量自检发现阻塞级问题（缺少必须产物、越界跳阶段、裁剪无声明依据）
- **THEN** 审计 SHALL 判定为不通过
- **AND** SHALL 阻断归档

#### Scenario: 轻量档审计报告形态

- **WHEN** 轻量自检完成
- **THEN** 系统 SHALL 输出简化审计记录，包含检查项结论与发现的问题清单
- **AND** SHALL NOT 输出七维度评分表与加权总分

#### Scenario: 标准档与完整档维持七维度审计

- **WHEN** 变更档位为 `标准` 或 `完整`
- **THEN** 审计 SHALL 按七维度加权评分执行
- **AND** SHALL NOT 降级为轻量自检

## MODIFIED Requirements

### Requirement: 审计六维度评估

系统 SHALL 支持对使用 DevFlow Skills 的项目进行六维度使用情况评估，各维度判定 SHALL 以变更档位为基准，不因轻量档按设计裁剪流程而误判缺项。

#### Scenario: 流程合规性审计

- **WHEN** 执行审计
- **THEN** 系统检查阶段顺序是否被遵守（门控检查）
- **AND** 检查是否存在跳阶段情况
- **AND** 检查可选阶段是否正确处理（跳过 vs 执行）
- **AND** 检查回退是否走正规流程（⚠️ 需修订 → 修订 → 完成）
- **AND** SHALL NOT 将变更档位为 `轻量` 时的零轮自审判定为跳阶段或流程违规
- **AND** SHALL NOT 将具有阶段适用性声明依据的 `⏭️ 不适用` 阶段判定为跳阶段

#### Scenario: 产物完整性审计

- **WHEN** 执行审计
- **THEN** 系统检查必须产物是否存在（.status.md, functional-designs/, detailed-design.md, tasks.md）
- **AND** 检查条件产物是否正确处理（🔶 / ⏭️ 图例）
- **AND** 检查产物内容质量（非空、无占位符）
- **AND** SHALL NOT 将变更档位为 `轻量` 时缺失的 self-reviews/ 目录判定为缺项
- **AND** SHALL NOT 将合法裁剪阶段缺失的 `api-tests/`、`e2e-tests/`、`test-reports/integration/` 判定为缺项

#### Scenario: 审查质量审计

- **WHEN** 执行审计
- **THEN** 系统检查设计审查是否按变更档位要求的形态执行（完整档四视角、标准档两视角、轻量档单 Agent 综合）
- **AND** 检查代码审查是否按变更档位要求的形态执行（标准档与完整档两视角、轻量档单 Agent）
- **AND** 检查审查问题是否闭环（追踪矩阵全部关闭）
- **AND** SHALL NOT 因缺少超出该档位要求的视角报告而判为缺项或扣分

#### Scenario: 测试充分性审计

- **WHEN** 执行审计
- **THEN** 系统检查接口单元测试通过率（该阶段适用时）
- **AND** 检查 E2E 测试通过率（仅前后端项目且该阶段适用时）
- **AND** 检查集成测试是否执行且通过（该阶段适用时）
- **AND** 检查多轮测试是否有记录
- **AND** SHALL NOT 将合法裁剪的测试阶段判定为缺项

#### Scenario: 缺陷管理审计

- **WHEN** 执行审计
- **THEN** 系统检查根因分类是否执行
- **AND** 检查修复是否闭环
- **AND** 检查设计错误是否正确触发回退

#### Scenario: 效率指标审计

- **WHEN** 执行审计
- **THEN** 系统统计各阶段耗时
- **AND** 统计测试轮次，并以变更档位基线为达标基准（轻量 1 轮 / 标准 3 轮 / 完整 10 轮）
- **AND** SHALL NOT 以固定轮次阈值判定轻量档或标准档轮次偏多
- **AND** 统计缺陷发现-修复周期
