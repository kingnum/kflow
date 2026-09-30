## MODIFIED Requirements

### Requirement: verify D3.2 输出越界检查

kflow-verify D3 维度 SHALL 在现有 D3.1 输入源检查基础上，新增 D3.2 输出越界检查。

#### Scenario: 后端子变更越界检测

- **WHEN** verify D3.2 对后端子变更执行越界检测
- **THEN** 系统 SHALL 在子变更源码目录中 grep 检测以下模式：
  - `.tsx`、`.jsx`、`.vue`、`.svelte` 文件 → 🟡 警告「后端SC 含前端组件文件」
  - 大量硬编码颜色值（`#[0-9a-fA-F]{3,6}` 或 `rgb(` 模式出现 ≥ 5 次）→ 🔵 建议「后端SC 含疑似样式代码」
  - `docs/designs/prototypes/` 路径引用（import/require 语句）→ 🟡 警告「后端SC 引用了原型文件」
- **AND** 越界检测结果 SHALL 标记为 🟡 警告（不阻塞流程）

#### Scenario: 前端子变更越界检测

- **WHEN** verify D3.2 对前端子变更执行越界检测
- **THEN** 系统 SHALL 在子变更源码目录中 grep 检测以下模式：
  - 数据库迁移脚本（`migrations/` 或 `schema.sql` 或 `*.prisma`）→ 🟡 警告「前端SC 含数据库脚本」
  - ORM 模型定义文件（`@Entity`、`@Table`、`prisma.model`、`mongoose.Schema` 等注解模式）→ 🟡 警告「前端SC 含 ORM 模型定义」
  - 服务端路由注册语句（`app.use(`、`app.post(`、`router.get(`、`@PostMapping`、`@GetMapping` 等模式）→ 🟡 警告「前端SC 含服务端路由注册」
- **AND** 越界检测结果 SHALL 标记为 🟡 警告（不阻塞流程）

#### Scenario: 误报排除

- **WHEN** 越界检测发现匹配项
- **THEN** 系统 SHALL 排除以下误报路径：
  - `node_modules/`、`.next/`、`dist/`、`build/`、`.git/`
  - 类型定义文件（`*.d.ts`）
  - 测试文件（`*.test.*`、`*.spec.*`、`__tests__/`）
  - mock 数据目录（`mocks/`、`__mocks__/`）
- **AND** 误报排除后的结果 SHALL 写入 verify 诊断报告

#### Scenario: 纯后端项目跳过越界检测

- **WHEN** 项目类型为纯后端
- **THEN** D3.2 越界检测 SHALL 仅执行后端子变更检测（不涉及前端子变更）
- **AND** 前端子变更检测项 SHALL 标记为 ⏭️ 不适用
