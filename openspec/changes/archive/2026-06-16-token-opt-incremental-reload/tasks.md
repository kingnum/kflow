## 1. 增量 RELOAD 规范

- [x] 1.1 定义"已验证文件标记"格式——写入 `kflow-shared/phase-hooks.md` RELOAD 执行规则新增节
- [x] 1.2 定义主 Agent 生成已验证标记的时机和规则
- [x] 1.3 定义子代理收到标记后的行为规则（跳过完整读取 + 保留自行读取权利）

## 2. phase-hooks.md 更新

- [x] 2.1 更新 `kflow-shared/phase-hooks.md` RELOAD 执行规则——添加"增量模式"选项
- [x] 2.2 更新 `09-phase-hooks.md` 设计文档——同步增量 RELOAD 规范

## 3. SKILL.md 更新

- [x] 3.1 更新所有阶段 SKILL.md 的 PRE_HOOK 引用——确认兼容增量 RELOAD 模式

## 4. 验证

- [x] 4.1 确认 phase-hooks.md 包含增量 RELOAD 规范
- [x] 4.2 确认已验证标记格式明确、子代理行为规则清晰
