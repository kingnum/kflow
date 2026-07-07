## 1. 加载层级标注

- [x] 1.1 为 9 个核心机制文档头部添加"加载层级"和"适用阶段"标注
- [x] 1.2 为 kflow-shared/ 下所有文件头部添加"加载层级"和"适用阶段"标注

## 2. 子代理 prompt 构建规范

- [x] 2.1 更新 7 个执行类阶段 SKILL.md 的子代理 prompt 构建章节——列出该阶段需加载的 kflow-shared 文件清单（基础层 + 执行层）
- [x] 2.2 更新 3 个设计类阶段 SKILL.md 的子代理 prompt 构建章节——列出需加载的文件清单（基础层 + 创意层）
- [x] 2.3 更新 3 个测试阶段 SKILL.md 的子代理 prompt 构建章节——列出需加载的文件清单（基础层 + 执行层 + 服务层）

## 3. 核心机制文档更新

- [x] 3.1 更新 `07-agent-model.md` 子代理 prompt 规范——添加分层加载规则
- [x] 3.2 更新 `kflow-shared/repetition-model.md`（如已由 shared-mechanism-extraction 创建）——添加分层加载说明

## 4. 审计规则

- [x] 4.1 `kflow-skills-auditor` 新增检查项：核心机制和 kflow-shared 文件必须有加载层级标注

## 5. 验证

- [x] 5.1 确认所有核心机制和 kflow-shared 文件头部有加载层级标注
- [x] 5.2 确认各阶段 SKILL.md 子代理 prompt 章节列出了正确的文件清单
