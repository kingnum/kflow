# 验证记录：optimize-context-budget

> **记录时间**: 2026-10-17
> **范围裁决**: 2026-10-17 用户裁决——本变更实施过程 SHALL NOT 操作消费方项目 `software-dev-agent`。项目级配置由 `kflow-init` 在目标项目执行时写入；存量文档优化由 `kflow-doc-optimize` 在目标项目被调用时执行。因此 8.4 与第 9 组整体改由消费方执行。

---

## 8.1 门控实现路径探针

### 执行环境

- Claude Code 2.1.278，headless 会话（`claude -p`）
- 独立测试项目：`E:/leadal/aicode/_kflow_gate_probe`
- 临时 hook：`PreToolUse`（matcher `Edit|Write|Bash`）将原始 stdin 追加到 `.claude/hook-stdin.jsonl`
- 原始记录留档：`openspec/changes/optimize-context-budget/probe-records.jsonl`

### 探针 1：主 Agent 与子代理的 stdin 差异

| 字段 | 主 Agent（Edit） | 子代理（Edit） |
|------|-----------------|---------------|
| `session_id` | `2c6737fb-...` | `85739a54-...` |
| `transcript_path` | `...\2c6737fb-....jsonl`（会话级） | `...\85739a54-....jsonl`（会话级，**不含 `/subagents/`**） |
| `agent_id` | **无** | **`ab194a415d1f0dfd0`** |
| `agent_type` | **无** | **`general-purpose`** |
| `tool_name` | `Edit` | `Edit` |
| `permission_mode` | `acceptEdits` | `acceptEdits` |

**结论**：`agent_id` / `agent_type` 在子代理输入中存在、主 Agent 中不存在——**路径 A 成立**。`transcript_path` 在当前版本为会话级路径，不能用于区分主/子代理。

### 探针 2：会话级 deny 与子代理 permissionMode

- 配置：`.claude/settings.json` 的 `permissions.deny: ["Edit"]`；自定义子代理 `probe-editor`（`tools: Read, Edit`、`permissionMode: acceptEdits`）
- 观察：子代理被成功创建，但其会话仅暴露 `Read` 工具，`Edit` / `Write` 不可用；目标文件未被修改
- **结论**：会话级 `permissions.deny` 同样约束子代理，子代理的 `permissionMode` **不能解除** deny——**路径 B 不成立**

### 探针 3：`Task` / `Agent` 拦截点

- 配置：新增 matcher `Task|Agent` 的 PreToolUse hook
- 观察：主 Agent 成功派发子代理（`subagent_stats.spawned = 1`、`completed = 1`），但该 hook **零触发**（`hook-stdin.jsonl` 无记录）
- **结论**：`Task` / `Agent` 工具的 PreToolUse 拦截点在本版本不可达，且即使可达也管不住主 Agent 自行 `Edit`——**路径 C 不成立**

### 路径选择

采用**路径 A**：以 stdin 的 `agent_id` / `agent_type` 判子代理。实现已附带降级与风险标注：

- 字段缺失时按主 Agent 处理（保证门控生效）
- `agent_id` / `agent_type` 为未文档化字段，升级后可能变化；上游移除时子代理会被误判，可设置 `KFLOW_GATING_DISABLE=1` 临时关闭
- `transcript_path` 启发式在当前版本无效，保留代码但不再作为有效判据

---

## 8.2 门控脚本的五类输入测试

脚本：`skills/kflow-init/scripts/kflow-main-agent-gate.py`
测试方式：以合成 stdin JSON + `CLAUDE_PROJECT_DIR` 指向临时测试项目（`targets/gate-test/`）离线执行。

| # | 输入 | 期望 | 实际 |
|---|------|------|------|
| 1 | 执行类阶段（编码）+ 主 Agent + `Edit src/app.py` | 拒绝 | ✅ 输出 `permissionDecision: deny`，含 `hookEventName: PreToolUse` |
| 2 | 执行类阶段 + 主 Agent + `Bash "pytest -q"` | 拒绝 | ✅ 输出 deny JSON |
| 3 | 设计类阶段（详细设计）+ 主 Agent + `Write detailed-design.md` | 放行 | ✅ 无输出、退出码 0 |
| 4 | 执行类阶段 + 主 Agent + `Edit .status.md` | 放行（白名单） | ✅ 无输出 |
| 5 | 无 `.status.md`（无法判定阶段） | 放行 | ✅ 无输出 |

**扩展用例**：

| # | 输入 | 期望 | 实际 |
|---|------|------|------|
| 6 | 执行类阶段 + 主 Agent + `Edit status-log.md` | 放行（白名单，保障状态双写） | ✅ 放行 |
| 7 | 执行类阶段 + 子代理（`agent_type` 存在）+ `Edit src/app.py` | 放行 | ✅ 放行 |
| 8 | 执行类阶段 + 主 Agent + `Bash "git status"` | 放行（只读） | ✅ 放行 |
| 9 | 执行类阶段 + 主 Agent + `Bash "npm run build"` | 拒绝（长输出） | ✅ deny |
| 10 | 执行类阶段 + 主 Agent + `Write docs/skill-suggestion.md` | 放行（白名单） | ✅ 放行 |

> 拒绝 JSON 结构均包含 `hookSpecificOutput.hookEventName = "PreToolUse"` 与 `permissionDecisionReason`，符合 `design.md` D-9 的实现约定。

---

## 8.3 安装落位

- `permission-model.md` §5.2 声明脚本源文件（`skills/kflow-init/scripts/kflow-main-agent-gate.py`）、落位（`.claude/hooks/kflow-main-agent-gate.py`）与注册条目
- `kflow-init` SKILL.md 步骤 3.5 声明复制动作；输出产物表列出 `门控脚本` 行
- 幂等规则：项目自定义 hook 条目保持不变

---

## 8.4 外部实测（转消费方）

按范围裁决，未在 `software-dev-agent` 实测门控。消费方在 `kflow-init` 完成安装后，应执行：

1. 执行类阶段主 Agent 尝试 `Edit` 生产代码 → 期望被拒绝且拒绝原因可读
2. 执行类阶段主 Agent 运行 `pytest` → 期望被拒绝
3. 主 Agent 改为创建子代理执行 → 期望子代理的同类调用被放行

---

## 第 9 组端到端验证（转消费方）

按范围裁决，第 9 组整体转由消费方在 `software-dev-agent` 上执行：

| 任务 | 消费方执行方式 |
|------|--------------|
| 9.1 真实变更全流程 | 在目标项目跑一个中等规模变更，观察门控与读取纪律 |
| 9.2 自动机制核验 | 检查归档后产品级文档修订记录是否裁剪至 3 条、移出记录是否进入 `changelog.md`、章节索引是否同步 |
| 9.3 token 度量 | 用分析脚本对比 18.28 B 基线 |
| 9.4 存量文档优化 | 调用 `/kflow-doc-optimize`，对 `CONTEXT.md`、`docs/designs/**`、`docs/open/**` 与活跃变更目录执行 |
| 9.5 transcript 核验 | 抽取主会话与子代理 transcript，核验三项设计要求 |
| 9.6 项目自定义规则区块例外 | 由项目侧手工在 `CLAUDE.md`「项目自定义规则」区块补入 `kflow-doc-optimize` 例外 |

---

## 仓库内验证记录

| 验证项 | 命令 | 结果 |
|--------|------|------|
| references 切片生成与一致性 | `bash scripts/sync-references.sh` | ✅ 退出码 0；59 个生成条目，7 组校验全部一致 |
| front matter | `python scripts/validate-frontmatter.py` | ✅ 通过 42、失败 0 |
| 注入模板作用域 | `bash scripts/validate-injection-scope.sh` | ✅ 命中数 0 |
| 打包 Skill 数 | `bash scripts/package-skills.sh optimize-context-budget` | ✅ 19 个 Skills（原 18） |

### 切片效果

| 文件 | 权威源行数 | 典型切片行数 | 去重后变体数 |
|------|----------:|------------:|------------:|
| gates.md | 459 | 162（api-test） | 10 份 → 6 种 |
| repetition.md | 717 | 327（api-test） | 8 份 → 3 种 |
| state-values.md | 170 | 73（api-test） | 10 份 → 6 种 |
| self-review.md | 351 | 210 | 3 份 → 3 种 |
| phase-transition.md | 127 | 104 / 85 | 11 份 → 2 种 |
| service-lifecycle.md | 332 | 207（code） | 4 份 → 4 种 |
| hooks.md | 349 | 216 | 13 份 → 13 种 |

> gates.md / repetition.md / state-values.md / phase-transition.md 剩余的同组副本为**规格等价**（同一阶段键或同一执行模型），非未切片残留。

---

## 第 10 组：优化能力补强与工程修复（2026-10-17 用户裁决追加）

### 10.1 打包格式修复

| 项 | 结果 |
|----|------|
| 修复前 | `tar -czf` 产出 gzip 内容但命名为 `.zip`，`zipfile.ZipFile` 无法打开 |
| 修复后 | 优先 `zip` 命令 → Python `zipfile` → PowerShell `Compress-Archive` → 降级 `.tar.gz` |
| 实测 | 本机无 `zip` 与 `Compress-Archive`，经 Python `zipfile` 产出；`file` 识别为 `Zip archive data`；条目 107 个；包含 `kflow-doc-optimize/scripts/*` 与 `kflow-init/scripts/*` |

### 10.2 `kflow-doc-optimize` 能力补强自测

| 脚本/文件 | 测试 | 结果 |
|-----------|------|------|
| `scripts/scan_docs.py` | 对本仓库执行扫描 | ✅ 识别 8 个 >30 KB 且无章节索引的文档，输出清单 |
| `scripts/check_refs.py find --write` | 临时项目中的引用留档 | ✅ 写入清单，保留原路径 |
| `scripts/check_refs.py replace --apply` | 拆分后替换 `docs/open/guide.md` → `docs/open/guide/index.md` | ✅ 同时替换项目根相对路径与引用文件相对路径（`../open/guide.md`）；留档清单记录替换映射、原路径保留 |
| `scripts/check_refs.py verify` | 新文件存在 / 删除后 | ✅ 存在时退出码 0；删除后报 2 条断链、退出码 1 |
| `references/report-template.md` | 结构检查 | ✅ 含扫描范围、执行项、体积变化、引用更新、校验结论、未执行项、反向还原 |

### 10.3 `kflow-init` 配置校验自测

| 输入 | 结果 |
|------|------|
| 合规配置（`autoCompactWindow=300000`、门控注册、脚本存在） | ✅ 退出码 0 |
| 缺失 `autoCompactWindow` | ✅ 退出码 1，输出缺失项；`permissions.allow` 缺项仅告警 |

### 10.4 `CLAUDE.md` 同步

已更新：核心内容与项目结构（`references-src/`）、references 生成规则、新增「文档与状态治理」章节、打包格式说明。
