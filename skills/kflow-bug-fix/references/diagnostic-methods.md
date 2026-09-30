# Feedback Loop 构建 — 10 种方法优先级

## 概述

缺陷修复的第一步是构建一个快速、确定性、Agent 可运行的 pass/fail 信号，用于验证缺陷是否存在及修复是否有效。

## 10 种方法优先级排序

按优先级从高到低尝试，自动化优先：

| 优先级 | 方法 | 说明 | 适用场景 |
|--------|------|------|---------|
| 1 | 失败测试 at nearest seam | 运行最近接口的已有失败测试 | 接口单元测试框架可用 |
| 2 | Curl/HTTP 脚本 | 针对 dev server 运行 HTTP 请求脚本 | 后端 API 缺陷 |
| 3 | CLI 调用 with fixture | 输入 fixtured 数据 → diff snapshot 输出 | CLI 工具、数据处理 |
| 4 | Headless 浏览器脚本 | Playwright/Puppeteer 脚本 | 前端 UI 缺陷 |
| 5 | Replay captured trace | 回放捕获的 HAR/请求 trace | 有抓包 trace 可用 |
| 6 | Throwaway harness | 最小化子系统 harness | 复杂集成场景 |
| 7 | Property/Fuzz loop | 1000 随机输入 fuzz 循环 | 数据相关缺陷 |
| 8 | Bisection harness | git bisect run 自动化 | 回归缺陷 |
| 9 | Differential loop | 旧版本 vs 新版本 diff 对比 | 性能回归 |
| 10 | HITL bash script (last resort) | 人工操作的脚本 | 需要手动步骤的缺陷 |

## Loop 优化

构建成功后，尝试优化：

| 优化维度 | 目标 | 方法 |
|---------|------|------|
| 速度 | 2 秒确定性 loop 优于 30 秒不稳定 loop | 缓存 setup、跳过无关 init |
| 信号清晰度 | 断言具体症状，非模糊"不对劲" | 精确断言失败模式 |
| 确定性 | 每次运行结果一致 | 固定时间、随机种子、文件系统隔离 |

## 无法构建 Loop 时的处理

所有 10 种方法均失败时：

1. 停止并明确列出已尝试方法
2. 请求用户提供：
   - a) 可复现环境访问权限
   - b) 捕获的 artifact（HAR 文件、日志 dump、core dump、带时间戳的屏幕录制）
   - c) 添加临时生产 instrumentation 的授权
3. 禁止不通过 feedback loop 直接进入假设阶段
