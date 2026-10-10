# Spec Delta

## MODIFIED Requirements

### Requirement: 项目类型判断

系统 SHALL 在流程指引时读取项目级项目类型记录，并据此展示适用流程阶段。SHALL NOT 在流程指引中重新扫描判定项目类型。项目级记录的读取优先级与降级规则由 `project-type-detection` 能力定义，本能力 SHALL NOT 重复定义。

#### Scenario: 前后端项目

- **WHEN** 读取到的项目类型为前后端项目
- **THEN** 流程包含原型设计和浏览器自动化测试阶段

#### Scenario: 纯后端项目

- **WHEN** 读取到的项目类型为纯后端项目
- **THEN** 流程跳过原型设计和浏览器自动化测试阶段

#### Scenario: 项目级记录缺失时的指引

- **WHEN** 项目级记录不存在
- **THEN** 系统执行扫描检测并在指引输出中展示检测结果
- **AND** 标注该结果待变更创建阶段确认与补写
- **AND** SHALL NOT 在指引阶段创建或修改任何文件
