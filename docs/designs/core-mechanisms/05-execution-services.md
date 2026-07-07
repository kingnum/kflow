# KFlow Skills 核心运行机制

> **版本**: 参见仓库根目录 `VERSION` 文件
> **创建时间**: 2026-04-29
> **更新时间**: 2026-05-17

> **加载层级**: 服务层
> **适用阶段**: api-test/e2e-test/integration-test

本文档定义 KFlow Skills 体系的核心运行机制，包括目录结构、状态文件、任务清单、阶段流转规则、回退机制和条件产物引用规范。

---


## 七、服务管理职责归属

### 7.1 职责划分

服务生命周期管理（启动、停止、编译、重启、健康检查）的职责完全归属于变更级 agent。

| 职责 | 变更级 agent | 子变更 agent |
|------|------------|------------|
| 服务启动/停止/重启 | ✅ 独占执行 | ❌ 禁止 |
| 编译（后端/前端） | ✅ 独占执行 | ❌ 禁止 |
| 数据库迁移执行 | ✅ 独占执行 | ❌ 禁止 |
| 健康检查（/health, /db-health） | ✅ 独占执行 | ❌ 禁止 |
| 崩溃恢复 | ✅ 独占执行 | ❌ 禁止 |
| 连接已知端口使用服务 | — | ✅ 允许 |
| 检测服务就绪状态（curl） | — | ✅ 允许 |
| 服务不可用上报 | — | ✅ 必须 |

### 7.1.1 服务启动配置来源

变更级 agent 在执行服务启停操作时，**必须**从 `docs/service-guide.md` 读取启动命令和环境配置，不得自行推断。具体规则详见 `centralized-service-management` 规格。

#### 首次运行就绪检测

测试阶段（api-test / e2e-test / integration-test）PRE_HOOK 首次读取 `docs/service-guide.md` 时，SHALL 执行四阶段就绪检测流程：

```
READ_SERVICE_GUIDE 四阶段就绪检测:

PHASE 1: DETECT（检测存在性）
  ├── docs/service-guide.md 存在？
  │   ├── NO  → 进入 PHASE 3 全量收集
  │   └── YES → 进入 PHASE 2

PHASE 2: VALIDATE（验证完整性）
  ├── dev 环境启动命令 ≠ 模板占位符？
  ├── dev 环境端口值实际存在且为有效数字？
  ├── 「服务依赖」章节存在且每项外部服务连接信息完整？
  ├── 配置状态标记 = ✅ 已就绪？
  │   ├── ALL PASS → 直接使用，跳过后续阶段
  │   └── FAIL    → 进入 PHASE 3（仅询问缺失项）

PHASE 3: COLLECT（收集用户输入）
  ├── AskUserQuestion 逐项收集缺失配置
  └── 用户选择「稍后配置」→ ❌ 阻塞当前阶段

PHASE 4: PERSIST（持久化）
  ├── 写入 service-guide.md
  ├── 记录配置状态标记: > **配置状态**: ✅ 已就绪
  └── 后续会话自动跳过询问
```

#### 外部服务依赖管理

首次检测 service-guide.md 时，SHALL 解析「服务依赖」章节表格，自动识别外部依赖：

- 提取所有服务名称和对应 dev 环境连接地址
- 标记连接地址为非 `localhost`/`127.0.0.1` 且非环境变量占位符（`${...}`）的条目为「需确认的外部服务」
- 需确认的依赖 SHALL 通过 AskUserQuestion 询问用户确认或补充连接信息
- 用户确认后 SHALL 持久化到 service-guide.md 并更新配置状态标记

### 7.2 子变更 agent 服务使用约束

子变更 agent 为纯服务消费者：
1. 接收变更级 agent 发出的「服务就绪」信号
2. 连接已知端口使用服务（端口从 docs/service-guide.md 获取）
3. 不得自行启动、停止或重启服务
4. 不得执行编译或迁移操作
5. 检测到服务不可用时上报变更级 agent，不自行处理

### 7.3 服务不可用上报流程

```
子变更 agent 检测到服务不可用:

1. curl localhost:{port} → Connection Refused
2. 上报变更级 agent（标记受影响子变更和端口）
3. 标记当前测试用例为「阻塞等待服务恢复」
4. 变更级 agent 执行崩溃恢复（见 7.5）
5. 服务恢复后变更级 agent 通知子变更 agent 继续
```

### 7.4 服务崩溃恢复

```
变更级 agent 崩溃恢复流程:

1. 收到服务崩溃上报
2. 执行 playwright-cli kill-all 清理残留浏览器进程
3. 执行完整编译重启流程（停止→编译→迁移→启动→健康检查）
4. 健康检查通过后通知所有受影响的子变更 agent 继续
```

### 7.5 with_server.py 工具脚本

变更级 agent 使用 `skills/kflow-code/scripts/with_server.py` 作为服务管理的工具脚本，支持两种运行模式。

#### 一次性模式（保持现有行为）

```bash
# 单服务
python skills/kflow-code/scripts/with_server.py \
  --server "mvn spring-boot:run" --port 8080 \
  -- <test_command>

# 双服务（前后端）
python skills/kflow-code/scripts/with_server.py \
  --server "cd backend && mvn spring-boot:run" --port 8080 \
  --server "cd frontend && npm run dev" --port 5173 \
  -- <test_command>
```

一次性模式：服务在执行后续命令期间运行，命令执行完毕后自动停止并清理进程。

#### 持久化模式（`--daemon`）

编码阶段的编译验证不需要持久服务，测试阶段需要持久运行的服务。测试阶段使用持久化模式：

```bash
# 启动后端服务（持久化）
python skills/kflow-code/scripts/with_server.py \
  --server "mvn spring-boot:run -Dspring-boot.run.profiles=dev" --port 8080 \
  --daemon --state-file docs/changes/{change}/.service-state.json

# 启动前后端服务（持久化）
python skills/kflow-code/scripts/with_server.py \
  --server "cd backend && mvn spring-boot:run" --port 8080 \
  --server "cd frontend && npm run dev" --port 5173 \
  --daemon --state-file docs/changes/{change}/.service-state.json

# 查询服务状态
python skills/kflow-code/scripts/with_server.py --status --state-file docs/changes/{change}/.service-state.json

# 健康检查
python skills/kflow-code/scripts/with_server.py --health --port 8080

# 停止所有持久化服务
python skills/kflow-code/scripts/with_server.py --stop-all --state-file docs/changes/{change}/.service-state.json
```

持久化模式特性：
- 服务在后台保持运行，不自动停止
- 服务信息（PID、端口、启动命令、启动时间、健康状态）写入 `--state-file` 指定的 JSON 文件
- 通过 `--status` 查询运行状态
- 通过 `--health` 执行单端口健康检查
- 通过 `--stop-all` 停止所有服务并清理状态文件

配置来源：`docs/service-guide.md` 的 dev 环境启动命令和端口。变更级 agent 在调用 with_server.py 前必须先读取 service-guide.md 获取准确的启动命令。

### 7.6 运行时服务状态文件（`.service-state.json`）

持久化模式使用 `.service-state.json` 追踪服务运行时状态：

```json
{
  "services": [
    {
      "name": "backend",
      "port": 8080,
      "pid": 12345,
      "start_command": "mvn spring-boot:run -Dspring-boot.run.profiles=dev",
      "started_at": "2026-05-28T10:30:00",
      "last_health_check": "2026-05-28T10:35:00",
      "health_status": "ok"
    }
  ],
  "browser_sessions": []
}
```

状态文件位置：`docs/changes/{change}/.service-state.json`，与 `.status.md` 同一目录。

状态文件生命周期：
- 创建：首次 `--daemon` 启动服务时
- 更新：每次健康检查后更新 `last_health_check` 和 `health_status`
- 清理：所有服务停止后删除

### 7.7 端口冲突检测

> 完整规范参见 `各 skill 的 references/service-lifecycle.md` §二 和 `各 skill 的 references/hooks.md` §八

### 7.8 服务停止超时链

> 完整规范参见 `各 skill 的 references/service-lifecycle.md` §二

---

## 八、编译验证与测试服务刷新

> **v1.9.0 变更**：编译验证与测试服务刷新明确分离。编码阶段仅执行编译验证（不启动持久服务），测试阶段每轮执行完整服务刷新（STOP→编译→迁移→START→健康检查），每轮测试后必须 STOP 服务。

### 8.1 编译验证同步点（编码阶段）

编码阶段的编译验证仅验证代码可编译，不启动持久服务。

| 触发条件 | 执行者 | 说明 |
|---------|--------|------|
| 所有子变更编码完成后 | 变更级 agent | 一次性编译验证 |

编译验证步骤：

```
1. COMPILE_BE → 执行后端编译（参考 service-guide.md，如 mvn compile）
2. COMPILE_FE → 执行前端编译（前后端项目，如 npm run build 或 tsc --noEmit）
```

编译验证通过后释放代码审查阶段门控。编译失败则 ❌ 阻塞编码阶段，修复后重新编译。

编译验证 SHALL NOT 包含：服务启动、数据库迁移、健康检查。

### 8.2 测试服务刷新同步点（测试阶段）

测试阶段每轮前执行完整服务刷新，每轮后停止服务。

| 触发条件 | 执行者 | 说明 |
|---------|--------|------|
| 所有子变更编码+审查完成后，进入首轮测试前 | 变更级 agent | Round 1 服务刷新 |
| 所有子变更完成当前轮次测试+修复后，进入下一轮前 | 变更级 agent | Round N 服务刷新 |
| 中断恢复到测试阶段 | 变更级 agent | 恢复时服务刷新 |

> 每轮编译重启标准步骤详见 `各 skill 的 references/service-lifecycle.md` §三

每轮测试后 SHALL 停止所有服务并清理 .service-state.json。全部轮次测试通过后直接输出 summary.md 标记测试完成。

### 8.3 迁移保护规则

后续轮次编译重启时，跳过已执行迁移：

1. 扫描 `migrations/` 目录收集所有迁移脚本，按序号排序
2. 读取 `migrations/migration-log.md`，排除已标记为「已执行」的脚本
3. 仅执行自上次同步以来新增的迁移脚本
4. 每执行完一个迁移即记录到 `migration-log.md`
5. Round 1（首轮）执行所有迁移；后续轮次仅执行新增迁移

---

## 九、批量同步推进

### 9.1 同步机制

所有子变更完成当前轮次测试和缺陷修复后，统一等待变更级 agent 重启服务，再进入下一轮。

```
批量同步推进流程:

Round N:
  变更级编译启动
      │
      ├── 子变更 A: E2E 测试 → 通过 → ⏸️ 等待同步
      ├── 子变更 B: E2E 测试 → 失败 → 修复 → 重测通过 → ⏸️ 等待同步
      └── 子变更 C: E2E 测试 → 通过 → ⏸️ 等待同步
      │
      ▼
  所有子变更完成 Round N → 变更级重新编译启动
      │
      ▼
Round N+1:
  变更级通知所有子变更「服务就绪，开始 Round N+1」
      │
      ├── 子变更 A: E2E 测试 → ...
      ├── 子变更 B: E2E 测试 → ...
      └── 子变更 C: E2E 测试 → ...
```

### 9.2 状态使用规则

| 场景 | 状态值 | 说明 |
|------|--------|------|
| 子变更完成当前轮次测试且通过，其他子变更未完成 | ⏸️ 等待同步 | 不自行推进到下一轮 |
| 收到变更级「服务就绪」信号 | ⏸️ → 🔄 进行中 | 开始执行下一轮测试 |
| 当前轮次所有子变更测试全部通过 | — | 不执行下一轮编译重启，直接输出 summary.md |

### 9.3 仅部分子变更失败时的处理

```
1. 失败的子变更 → 进入 kflow-bug-fix 缺陷修复流程
2. 通过的子变更 → ⏸️ 等待同步（等待失败子变更修复完成）
3. 全部修复完成后 → 变更级编译重启进入下一轮
4. 已通过的子变更在下一轮中重新测试以验证无回归
```

---

## 十、辅助脚本使用原则

### 10.1 黑盒优先原则

使用辅助脚本（如 with_server.py）时遵循黑盒优先策略：

| 步骤 | 操作 | 说明 |
|------|------|------|
| 1 | `python scripts/{script}.py --help` | 首先查看帮助信息了解用法 |
| 2 | 直接调用脚本执行 | 根据 --help 输出的参数执行 |
| 3 | 仅错误时读取源码 | 仅在 --help 信息不足且脚本执行报错时读取 |

### 10.2 例外条件

以下情况允许读取脚本源码：
- 脚本执行报错且 `--help` 信息不足以定位问题
- `--help` 输出为空或关键参数说明缺失
- 需要了解脚本的输出格式以进行后续处理

### 10.3 上下文管理原则

- **快照优先于截图**：优先使用 `playwright-cli snapshot` 获取文本结构（轻量），仅在需要视觉对比时使用 `playwright-cli screenshot`
- **增量轮次报告**：每轮报告仅记录本轮新增的成败变化，不重复完整用例清单
- **选择性读取**：读取 detailed-design.md 时仅提取当前子变更相关的 NFR 章节

---

## 十一、文档禁止规则

> **借鉴**：superpowers writing-plans 禁止占位符规则

以下占位符在正式文档中禁止出现：

| 禁止内容 | 说明 | 正确做法 |
|---------|------|---------|
| TODO / TBD / 待补充 | 表示未完成 | 完成内容或删除段落 |
| {待填写} / {xxx} | 占位符格式 | 填写具体值或删除 |
| ...（表示未完成） | 省略号表示缺失 | 完整描述或删除 |
| 空白表格单元格（必填项） | 必填项为空 | 填写具体内容 |

### 文档验收检查

阶段产物文档输出前检查：

```markdown
文档验收检查:
- [ ] 无 TODO/TBD/待补充 占位符
- [ ] 无 {xxx} 格式占位符
- [ ] 必填表格单元格已填写
- [ ] 文档内容完整可执行
```

## 十三、多 Agent 审查结果合并机制

> **借鉴**：gstack Review Army fingerprint 去重机制

### 13.1 问题 fingerprint 定义

每个审查发现计算唯一 fingerprint：

```
fingerprint = sha256(file_path:line_range:category:description)
```

示例：
```
fingerprint: a1b2c3d4...
file_path: src/auth/login.ts
line_range: 45-52
category: security
description: 密码未加密存储
```

### 13.2 去重合并规则

| 场景 | 处理方式 | 合并结果 |
|------|---------|---------|
| 多 Agent 发现相同问题 | fingerprint 相同 | 合并为一条，标注发现者列表 |
| 相似问题（描述不同） | fingerprint 不同但位置相同 | 保留两条，标注可能重复 |
| 不同视角相同问题 | fingerprint 相同 | 合并，标注多视角确认 |

### 13.3 审查报告合并流程

```
审查结果合并流程:

┌─────────────────────────────────────────────────────────────┐
│                  MERGE WORKFLOW                               │
├─────────────────────────────────────────────────────────────┤
│  1. COLLECT   → 收集所有 Agent 的审查报告                    │
│  │   ├── cross-reviews/{timestamp}/business-review.md        │
│  │   ├── cross-reviews/{timestamp}/technical-review.md       │
│  │   ├── cross-reviews/{timestamp}/security-review.md        │
│  │   └── cross-reviews/{timestamp}/quality-review.md         │
│  2. HASH      → 计算每个问题的 fingerprint                   │
│  3. DEDUP     → 按 fingerprint 去重                          │
│  │   ├── 相同 fingerprint → 合并                             │
│  │   └── 不同 fingerprint → 保留                             │
│  4. RANK      → 按严重程度排序                               │
│  │   ├── 高 → 安全问题、数据问题                             │
│  │   ├── 中 → 性能问题、UI缺陷                               │
│  │   └── 低 → 文档问题、建议                                 │
│  5. SYNTHESIS → 输出综合审查报告                             │
│  │   └── cross-reviews/{timestamp}/synthesis.md              │
└─────────────────────────────────────────────────────────────┘
```

### 13.4 合并后的综合报告格式

```markdown
# 审查综合报告

## 问题统计

| 严重程度 | 数量 | 来源视角 |
|---------|------|---------|
| 高 | 2 | 安全、技术 |
| 中 | 3 | 业务、质量 |
| 低 | 1 | 质量 |

## 问题清单

| 序号 | fingerprint | 严重程度 | 类别 | 描述 | 发现者 | 状态 |
|------|-------------|---------|------|------|--------|------|
| 1 | a1b2c3d4... | 高 | 安全 | 密码未加密存储 | 安全视角、技术视角 | 待修复 |
| 2 | e5f6g7h8... | 中 | 性能 | N+1 查询问题 | 技术视角 | 待修复 |

## 问题追踪矩阵

| 问题序号 | 严重度 | 修复状态 | 验证方式 | 验证结果 | 关闭时间 |
|----------|--------|---------|---------|---------|---------|
| 1 | 高 | 已修复 | 原视角+安全视角交叉检查 | ✅ | 2026-04-29 18:00 |
| 2 | 中 | 已修复 | 原视角重审 | ✅ | 2026-04-29 17:30 |

## 关闭条件
- [ ] 所有高严重度问题已修复并重新审查通过
- [ ] 所有中严重度问题已修复或已确认可延后处理
- [ ] 综合评估通过，可进入下一阶段

## 重复发现标注

| fingerprint | 发现者列表 | 说明 |
|-------------|-----------|------|
| a1b2c3d4... | 安全视角、技术视角 | 多视角确认同一问题 |
```

---

## 十四、覆盖追溯机制

> **版本**: 1.8.0 新增

### 14.1 概述

覆盖追溯机制通过 `traceability.md` 文件实现从功能点到各阶段产物的全链路覆盖映射，确保每个功能点在所有阶段产物中都有对应落点。覆盖率由阶段门控自动验证，实现 100% 覆盖可验证。

### 14.2 traceability.md 生命周期

```
traceability.md 生命周期:

  创建 ──▶ 填写 ──▶ 验证 ──▶ 归档
   │         │        │        │
   │         │        │        └── kflow-archive 执行前最终检查所有列覆盖率 = 100%
   │         │        │
   │         │        └── 阶段门控时自动验证对应列覆盖率，< 100% 阻塞
   │         │
   │         └── 各执行阶段完成后由该阶段子代理填写对应列
   │
   └── kflow-design 阶段基于 functional-designs/index.md FP 清单初始化空白矩阵
```

| 生命周期阶段 | 执行者 | 时机 | 操作 |
|-------------|--------|------|------|
| 创建 | `kflow-design` | 详细设计阶段完成后 | 基于 functional-designs/index.md 中 FP 清单初始化空白矩阵，功能点ID 列已填充，其余列留空 |
| 填写 | 各执行阶段子代理 | 每个执行阶段完成后 | 该阶段 Agent 迭代子代理填写对应列，不修改其他列 |
| 验证 | 阶段门控 | 进入下一阶段前 | 读取对应列，检查覆盖率 = 100%，< 100% 时阻塞并输出缺口清单 |
| 归档 | `kflow-archive` | 归档前 | 最终检查所有适用列覆盖率 = 100% |

### 14.3 格式规范

详见模板文件 `docs/designs/templates/changes/{change}/traceability.md`，包含以下三个核心表格：

| 表格 | 说明 | 更新方式 |
|------|------|---------|
| 覆盖总览表 | 功能点ID × 阶段产物列 的映射矩阵 | 各阶段完成后独立填写对应列 |
| 阶段覆盖统计表 | 各阶段的覆盖率、状态、更新时间 | 阶段完成时自动计算更新 |
| 缺口追踪表 | 未覆盖功能点的追踪记录 | 门控检查发现缺口时自动添加 |

### 14.4 覆盖率门控规则

覆盖率门控已集成到 [§3.4 门控规则](#34-门控规则) 中：

| 门控点 | 检查列 | 覆盖率要求 |
|--------|--------|-----------|
| 进入计划阶段 | 功能设计(§)、详细设计(§) | 均为 100% |
| 进入 E2E 测试阶段 | 接口测试(ID) | 100% |
| 进入集成测试阶段 | 编码实现(SC)、E2E测试(ID)（前后端项目） | 100% |
| 进入归档阶段 | 所有适用列 | 均为 100% |

### 14.5 缺口自动发现与追踪

门控检查发现覆盖率 < 100% 时：

1. 自动识别未覆盖的功能点（覆盖总览表中对应列为空的功能点ID）
2. 在缺口追踪表中添加记录：功能点ID、缺失阶段、发现时间、状态（待补充）
3. 输出缺口清单供用户和子代理参考
4. 缺口补充后自动更新状态为"已补充"，重新计算覆盖率

### 14.6 各阶段独立维护规则

- 各阶段仅写入自身列，不修改其他阶段已填写的列
- 后续阶段不覆盖已有数据（除非通过阶段回退流程重置）
- 纯后端项目的 E2E测试列标记为 ⏭️

