## Context

产品经 5+ 次变更后 functional-designs/ 膨胀，RELOAD 加载量线性增长。

## Goals / Non-Goals

**Goals:**
- 归档合并后生成模块级摘要
- 后续变更 RELOAD 优先加载摘要而非全文

**Non-Goals:**
- 不改变归档合并流程本身
- 不改变 functional-designs/ 的存储结构

## Decisions

### D1: 摘要文件格式

`docs/designs/functional-designs/module-summary.md`:
```markdown
# 功能模块摘要

> 最后更新: {归档日期} | 来源变更: {change-name}

| 模块 | 核心功能 | FP-ID 范围 | 文档位置 |
|------|---------|-----------|---------|
| 用户管理 | 注册/登录/权限/个人信息 | FP-001~FP-015 | user-management/index.md |
| 订单系统 | 下单/支付/退款/订单查询 | FP-016~FP-030 | order-system/index.md |
| ... | ... | ... | ... |
```

### D2: 生成时机

归档阶段设计合并完成后，自动更新 module-summary.md。

### D3: RELOAD 引用

explore/design/plan 等阶段的 RELOAD 清单新增 `module-summary.md` 为可选加载项。当子变更涉及特定模块时才加载该模块全文。

## Risks / Trade-offs

| 风险 | 缓解 |
|------|------|
| 摘要与全文不一致 | 每次归档合并后强制更新摘要；kflow-audit 检查一致性 |
| 首次创建摘要时需要全量扫描 | 仅首次需要，后续增量更新 |
