# Spec Delta

## MODIFIED Requirements

### Requirement: 条件产物引用规范化

系统 SHALL 在所有 Skill 文档中使用标准化图例标注输入/输出产物的必须性，并将前端SC 的原型产物入口统一为产品级原型清单 `docs/designs/prototypes/manifest.md` 与变更级原型改动清单 `prototype-changes.md`。阶段级产物除按项目类型标注外，SHALL 支持按变更档位标注为不适用。

#### Scenario: 产物表格使用标准图例

- **WHEN** Skill 文档定义输入要求或输出产物
- **THEN** 使用标准化图例：✅ 必须、🔶 条件、⏭️ 不适用
- **AND** 每个产物按项目类型（前后端/纯后端）分别标注
- **AND** 阶段级产物额外标注其适用的变更档位（`轻量` 档下的裁剪条件，或标注为不裁剪）
- **AND** 前端SC 的原型产物 SHALL 以产品级 `docs/designs/prototypes/manifest.md`（✅ 必须，前端SC）与变更级 `prototype-changes.md`（✅ 必须，前端SC）为统一入口
- **AND** SHALL NOT 在输入表中单独列出 `docs/designs/prototypes/index.html`、`docs/designs/prototypes/design-tokens.css`、变更级 `element-coverage-tree.md`

#### Scenario: 门控检查中显式处理跳过

- **WHEN** 门控检查涉及可选阶段的产物（如 prototype）
- **THEN** 检查逻辑区分三种情况：跳过（通过）、完成有文件（通过）、待开始（阻塞）
- **AND** 不因产物不存在而误报阻塞

#### Scenario: 按变更档位不适用而跳过

- **WHEN** 门控检查涉及某阶段产物 且 该阶段因变更档位为 `轻量` 而被标记为 `⏭️ 不适用`
- **THEN** 检查逻辑 SHALL 追加第四种情况：声明不适用且产物不存在（通过）
- **AND** SHALL NOT 将该情况与「待开始（阻塞）」或「产物缺失（阻塞）」混淆
- **AND** 判定依据 SHALL 为变更级 `.status.md` 中的阶段适用性声明

#### Scenario: 按项目类型跳过与按档位跳过的区分

- **WHEN** 某阶段同时存在两种跳过依据（如纯后端项目的 E2E测试）
- **THEN** 按项目类型的跳过 SHALL 优先判定，且与变更档位无关
- **AND** 按变更档位的跳过 SHALL 仅在项目类型判定为适用时进一步判定
