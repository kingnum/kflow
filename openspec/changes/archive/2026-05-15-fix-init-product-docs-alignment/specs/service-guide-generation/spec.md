## MODIFIED Requirements

### Requirement: 服务指引检测

系统 SHALL 在 kflow-init 和 kflow-code 阶段检查 `docs/service-guide.md` 是否存在。

#### Scenario: 服务指引已存在

- **WHEN** docs/service-guide.md 文件存在
- **THEN** 系统直接读取使用配置

#### Scenario: 服务指引不存在

- **WHEN** docs/service-guide.md 文件不存在
- **THEN** 若当前为 kflow-init 老项目逆向分析，系统生成初步草稿
- **AND** 若当前为 kflow-code 编码阶段，系统进入完整生成流程

### Requirement: 项目结构自动分析

系统 SHALL 自动分析项目结构推断服务启动配置。

#### Scenario: 检测项目类型

- **WHEN** 生成服务指引
- **THEN** 系统扫描项目根目录检测项目类型标识文件
- **AND** 根据检测结果推断启动命令

#### Scenario: Java 项目检测

- **WHEN** 存在 pom.xml 或 build.gradle
- **THEN** 系统推断项目类型为 Java/Spring Boot
- **AND** 推断启动命令为 mvn spring-boot:run 或 gradle bootRun

#### Scenario: Node 项目检测

- **WHEN** 存在 package.json 且包含前端框架依赖
- **THEN** 系统推断项目类型为 Node.js
- **AND** 推断启动命令为 npm run dev 或 npm start

### Requirement: 服务指引生成

系统 SHALL 合并自动检测结果和用户确认信息生成 `docs/service-guide.md`。

#### Scenario: kflow-init 生成初步草稿

- **WHEN** kflow-init 老项目逆向分析触发 service-guide.md 生成
- **THEN** 系统基于 L1 配置扫描生成 dev 环境初步配置
- **AND** test/staging/prod 环境标注「待后续补充」
- **AND** 文档标注「由 AI 逆向分析生成，待人工审核」

#### Scenario: kflow-code 生成/补充完整文档

- **WHEN** kflow-code 编码阶段检测到 service-guide.md 不存在或为草稿
- **THEN** 系统进入完整生成流程（自动分析 + 用户交互确认）
- **AND** 补充 test/staging/prod 多环境配置
- **AND** 替换草稿标记为正式内容

## ADDED Requirements

### Requirement: init 预生成 service-guide.md

kflow-init 老项目逆向分析 SHALL 生成 `docs/service-guide.md` 初步版本。

#### Scenario: L1 扫描信息用于 service-guide 生成

- **WHEN** kflow-init 执行老项目逆向分析
- **THEN** 系统将 L1 配置扫描信息用于生成 dev 环境启动配置
- **AND** 包含项目类型、框架、启动命令、端口、数据库信息
- **AND** 标注为草稿

#### Scenario: 用户可审核 service-guide 草稿

- **WHEN** kflow-init 展示逆向分析生成的文档草稿供审核
- **THEN** service-guide.md 草稿与其他产品文档草稿一同展示
- **AND** 用户可选择确认写入、修改后写入或放弃
