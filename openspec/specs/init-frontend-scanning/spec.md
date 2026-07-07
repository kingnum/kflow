## Requirements

### Requirement: L2.5 前端工程扫描层

kflow-init LEGACY 模式 SHALL 在 L2（后端目录结构扫描）和 L3（源码语义扫描）之间，对前后端项目执行 L2.5 前端工程扫描。纯后端项目 SHALL 跳过 L2.5。

#### Scenario: 前后端项目执行 L2.5 扫描

- **WHEN** 项目类型检测为前后端项目
- **AND** L2 后端目录扫描完成
- **THEN** 系统执行 L2.5 前端工程扫描
- **AND** 扫描前端工程目录（src/、app/、pages/ 等）下的路由配置、菜单组件、页面组件

#### Scenario: 纯后端项目跳过 L2.5

- **WHEN** 项目类型检测为纯后端项目
- **THEN** 系统跳过 L2.5 扫描
- **AND** 直接进入 L3 源码语义扫描

### Requirement: 前端路由配置扫描

L2.5 SHALL 扫描前端路由配置文件，提取页面路径、组件映射和嵌套层级。

#### Scenario: 识别 Vue Router 配置

- **WHEN** 项目存在 `src/router/` 目录或 `src/router.ts`
- **THEN** 系统解析路由定义，提取 path → component 映射
- **AND** 从嵌套路由中提取层级关系（父路由 → 子路由）

#### Scenario: 识别 React Router 配置

- **WHEN** 项目存在 `src/routes.tsx` 或包含 `<Route>` 组件的路由文件
- **THEN** 系统解析路由定义，提取 path → element/component 映射
- **AND** 从路由嵌套中提取层级关系

#### Scenario: 识别 Next.js 路由

- **WHEN** 项目使用 Next.js（`src/app/` 或 `pages/` 目录结构）
- **THEN** 系统从目录结构推断路由层级
- **AND** 从 `page.tsx`/`layout.tsx` 文件中提取页面组件

#### Scenario: 无标准路由配置时降级

- **WHEN** 前端工程未检测到标准路由配置（如纯 HTML 多页应用）
- **THEN** 系统从页面文件目录结构推断层级
- **AND** 标注"由目录结构推断，待确认"
- **AND** 提示用户手动提供功能菜单结构

### Requirement: 前端菜单配置扫描

L2.5 SHALL 扫描前端菜单/导航配置，提取一级菜单、二级菜单及权限控制信息。

#### Scenario: 识别独立菜单配置文件

- **WHEN** 项目存在菜单配置文件（如 `src/config/menu.ts`、`src/config/navigation.ts`）
- **THEN** 系统解析菜单定义，提取菜单项 name/path/children/icon/permission
- **AND** 构建一级菜单 → 二级菜单 → 页面的完整映射

#### Scenario: 识别组件内菜单定义

- **WHEN** 菜单定义嵌入在布局组件中（如 `<Menu>`、`<Sidebar>`、`<Nav>` 组件）
- **THEN** 系统扫描布局组件，提取菜单项定义
- **AND** 构建菜单层级映射

#### Scenario: 无显式菜单配置

- **WHEN** 项目未检测到独立的菜单配置或组件内菜单定义
- **THEN** 系统以路由层级作为菜单层级的近似
- **AND** 标注"由路由结构推断，待确认菜单命名"

### Requirement: 前端页面组件扫描

L2.5 SHALL 扫描页面组件文件，提取页面标题、表单字段定义和操作按钮信息。

#### Scenario: 提取页面标题

- **WHEN** 页面组件文件被扫描
- **THEN** 系统从 `document.title`、`<title>`、组件名、或国际化 key 推断页面标题
- **AND** 优先使用中文标签（如从国际化文件匹配）

#### Scenario: 提取表单字段定义

- **WHEN** 页面组件包含表单（`<form>`、`<el-form>`、`<a-form>` 等）
- **THEN** 系统提取表单字段的 name/label/rules/required/placeholder
- **AND** 填充到功能点的"表单项定义"章节

#### Scenario: 提取操作按钮

- **WHEN** 页面组件包含按钮或操作元素
- **THEN** 系统提取按钮文本/事件处理函数名
- **AND** 推断可执行操作（如"新增"→新增操作、"删除"→删除操作）

### Requirement: 模块按菜单划分

L2.5 扫描完成后，系统 SHALL 按提取的一级菜单划分功能模块，每个一级菜单对应一个产品级 functional-designs 子目录。

#### Scenario: 按一级菜单创建目录

- **WHEN** L2.5 扫描提取到菜单结构
- **THEN** 系统以每个一级菜单的 kebab-case 命名创建子目录
- **AND** 目录位于 `docs/designs/functional-designs/{一级菜单}/`
- **AND** 每个目录包含 index.md + 至少一个 part-NN.md

#### Scenario: 内容较多时拆分

- **WHEN** 一个一级菜单下的功能点数量超过 30
- **THEN** 系统拆分为多个 part-NN.md 分册
- **AND** index.md 包含分册总览表

#### Scenario: 多级菜单的功能点归属

- **WHEN** 菜单结构包含二级菜单
- **THEN** 二级菜单作为 part-NN.md 内的功能点分组维度
- **AND** 不在文件系统层面为二级菜单创建独立目录
