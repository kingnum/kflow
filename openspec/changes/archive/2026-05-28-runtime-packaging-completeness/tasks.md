## 1. 移动 with_server.py 到 kflow-shared/scripts/

- [x] 1.1 创建 `.claude/skills/kflow-shared/scripts/` 目录
- [x] 1.2 将 `scripts/with_server.py` 复制到 `.claude/skills/kflow-shared/scripts/with_server.py`
- [x] 1.3 验证复制后文件内容与原文件一致

## 2. 更新文档引用路径

- [x] 2.1 更新 `kflow-shared/service-lifecycle.md` 中所有 `scripts/with_server.py` 引用为 `kflow-shared/scripts/with_server.py`
- [x] 2.2 更新 `kflow-shared/phase-hooks.md` 中所有 `with_server.py` 引用为 `kflow-shared/scripts/with_server.py`
- [x] 2.3 删除 `service-lifecycle.md` 第七节中 `scripts/migrate.py` 悬空引用行

## 4. 验证打包产物

- [x] 4.1 删除项目根目录 `scripts/with_server.py`（确认副本已到位后）
- [x] 4.2 全仓库搜索确认无其他文件引用旧路径 `scripts/with_server.py`
- [x] 4.3 执行 `scripts/package-skills.sh runtime-packaging-completeness` 生成测试 zip
- [x] 4.4 验证 zip 包含 `kflow-shared/scripts/with_server.py`（非根 scripts/ 下）
- [x] 4.5 验证 zip 中 `kflow-shared/service-lifecycle.md` 引用路径为 `kflow-shared/scripts/with_server.py`
