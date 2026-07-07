# prototype-offline-constraint Specification

## Purpose
定义原型 HTML 文件的离线自包含约束：禁止外部 CDN 依赖，所有资源内联或相对路径引用，字体使用系统默认字体栈，VERIFY 步骤增加 CDN 扫描检查。

## Requirements

### Requirement: 原型文件离线自包含

系统 SHALL 确保所有原型 HTML 文件完全自包含，可在浏览器中离线打开，不依赖任何外部 CDN 资源。

#### Scenario: 禁止外部 CSS 依赖
- **WHEN** 原型 HTML 文件被生成
- **THEN** 所有 CSS SHALL 为内联 `<style>` 标签或相对路径 `<link>` 引用
- **AND** SHALL NOT 包含对 `http://` 或 `https://` 外部域名的 CSS 引用
- **AND** SHALL NOT 包含 Google Fonts、Adobe Fonts、CDN CSS 框架等外部字体/样式引用

#### Scenario: 禁止外部 JavaScript 依赖
- **WHEN** 原型 HTML 文件被生成
- **THEN** 所有 JavaScript SHALL 为内联 `<script>` 标签或相对路径 `<script src>` 引用
- **AND** SHALL NOT 包含对 `http://` 或 `https://` 外部域名的脚本引用
- **AND** 必要的库文件（如 React、Babel）SHALL 内联或存为本地文件

#### Scenario: 使用系统默认字体栈
- **WHEN** 原型 HTML 文件定义字体
- **THEN** SHALL 使用系统默认字体栈（如 `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif`）
- **AND** SHALL NOT 通过 `@import` 或 `@font-face` 引用外部字体服务

#### Scenario: 图片资源自包含
- **WHEN** 原型 HTML 文件包含图片资源
- **THEN** 图片 SHALL 使用 base64 data URI 内联，或存为 `prototype/` 目录下的本地文件并通过相对路径引用
- **AND** SHALL NOT 通过 `http://` 或 `https://` URL 引用远程图片

#### Scenario: VERIFY 步骤增加 CDN 扫描
- **WHEN** 原型 HTML 文件生成完成，进入 VERIFY 步骤
- **THEN** 系统 SHALL 扫描 `prototype/` 目录下所有 `.html` 文件
- **AND** 检测是否存在 `http://` 或 `https://` 模式的外部资源引用
- **AND** 若发现外部依赖，SHALL 在验证报告中列出违规文件和具体引用
- **AND** 标记为验证不通过，需返回 DESIGN 步骤修复

#### Scenario: CDN 扫描通过
- **WHEN** CDN 扫描未发现任何外部资源引用
- **THEN** 验证报告中记录"离线自包含检查通过"
- **AND** 继续后续验证步骤（Playwright 点击测试）
