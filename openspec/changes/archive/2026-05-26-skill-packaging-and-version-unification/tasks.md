## 1. 统一版本号管理

- [x] 1.1 创建仓库根目录 `VERSION` 文件，初始内容 `0.0.1`
- [x] 1.2 移除 kflow-guide SKILL.md 中的 `version:` 字段
- [x] 1.3 移除 kflow-explore SKILL.md 中的 `version:` 字段
- [x] 1.4 移除 kflow-prototype-design SKILL.md 中的 `version:` 字段
- [x] 1.5 移除 kflow-design SKILL.md 中的 `version:` 字段
- [x] 1.6 移除 kflow-plan SKILL.md 中的 `version:` 字段
- [x] 1.7 移除 kflow-code SKILL.md 中的 `version:` 字段
- [x] 1.8 移除 kflow-code-review SKILL.md 中的 `version:` 字段
- [x] 1.9 移除 kflow-api-test SKILL.md 中的 `version:` 字段
- [x] 1.10 移除 kflow-e2e-test SKILL.md 中的 `version:` 字段
- [x] 1.11 移除 kflow-integration-test SKILL.md 中的 `version:` 字段
- [x] 1.12 移除 kflow-bug-fix SKILL.md 中的 `version:` 字段
- [x] 1.13 移除 kflow-audit SKILL.md 中的 `version:` 字段
- [x] 1.14 移除 kflow-archive SKILL.md 中的 `version:` 字段
- [x] 1.15 移除 kflow-status SKILL.md 中的 `version:` 字段
- [x] 1.16 移除 kflow-init SKILL.md 中的 `version:` 字段
- [x] 1.17 移除 kflow-resume SKILL.md 中的 `version:` 字段

## 2. 打包机制

- [x] 2.1 创建 `targets/` 目录，添加 `.gitkeep`
- [x] 2.2 编写打包脚本：扫描 16 个 `kflow-*` Skills、生成 VERSION.txt、输出 `targets/kflow-devflow-skills-x.x.x.zip`
- [x] 2.3 验证打包产物：解压 zip 确认结构完整、16 个 Skills 齐全、references/ 文件正确

## 3. CLAUDE.md 规则注入

- [x] 3.1 新增归档后打包规则：`/opsx:archive` 完成后 → 版本自增判定 → 打包 → git commit
- [x] 3.2 确认规则与现有 CLAUDE.md 规则不冲突

## 4. 设计文档同步

- [x] 4.1 更新 `docs/designs/skills/kflow-init.md` 中的版本号引用和打包说明
- [x] 4.2 更新 `docs/designs/skills/kflow-archive.md` 中的版本号引用和打包说明
- [x] 4.3 使用 `/skill-creator` 根据变更后的设计文档更新对应运行时 Skill（kflow-init、kflow-archive 的 SKILL.md），同步打包和版本号相关内容
