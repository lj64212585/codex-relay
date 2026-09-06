# Codex Relay

[English](../README.md) · [简体中文](../readme/README.zh-CN.md)

![Codex Relay](../readme/assets/hero.svg)

**按职责分工，按任务选择调度。**

默认选择 Explore，让父会话持续理解、实现和验证；只有需要委派确定的实施切片、独立审核或优先预算时才选择另外两种模式。Skill 和 Agent 名称表示职责，模型由配置决定。

| 模式 | 适用任务 | 实施与上下文 | 主要风险 |
|---|---|---|---|
| [Explore Relay](../relay/explore-relay/README.md) | 默认；质量敏感、核心交互、复杂实现 | 父会话实施，4 个只读角色收集证据 | 遗漏或过期证据；父会话必须理解关键路径 |
| [Implementation Relay](../relay/implementation-relay/README.md) | 行为已确定的实施切片、针对性独立审核 | 父会话掌握核心实现；4 探索、3 实施、2 审核 | 小范围仍可能包含复杂判断，必须先过实施不确定性检查 |
| [Budget Relay](../relay/budget-relay/README.md) | 预算优先、行为和边界已确定 | 有界执行、风险审核、技术集成 | 不能继承强模型的全部实施判断；高不确定性提前转交 |

推荐父会话使用 Astra；Skill 不会自动切换父模型。Explore 保留 Luna Max ×3 / Terra Max ×1；Implementation 保留 Luna Max ×6 / Terra Max ×3，父会话掌握核心实现；Budget 的规划和集成使用 `gpt-6-astra` xHigh，其余 Luna／Terra 配置不变。模型升级无需再次更名角色。

## 工作规则

委派包包含固定约束、决策用途、预算和停止条件；证据报告包含 Coverage 和 Snapshot。“范围内没找到”不代表不存在。父会话深入阅读核心调用链，避免重做广泛检索。单次等待超时不代表失败，但可在预算耗尽、证据足够或问题失效后记录理由结束委派；复用资源或移交写入权前必须确认停止并核查状态。验收使用匹配的运行、视觉或交互证据，避免重复已通过且未受影响的检查。

## 安装和迁移

```powershell
.\tools\relay-installer\start.ps1
```

旧名 `sol-explore-relay` → `explore-relay`，`sol-led-relay` → `implementation-relay`，`poor-relay` → `budget-relay`。`sol-pair-relay` 及其本轮临时名称 `plan-execute-relay` 已删除。Explore Agent 使用 `explore_*`，Implementation 和 Budget 保留原有职责型 Agent 名称。

旧安装不会因为源码更名自动消失。优先使用安装器预检和确认切换：已识别的旧版先备份，自定义文件阻止自动操作。旧名称仅用于迁移识别和历史版权归属，不再提供可调用别名。同一任务域使用一种主导模式；Implementation 仅在适合有界写入或针对性审核时选用，保留现有 Skill 隐式发现设置。

[安装器配置、备份和 Win64 打包说明](../tools/relay-installer/README.md)

```powershell
.\packaging\build-win64.bat
```

## 验证

```powershell
python -X utf8 relay/explore-relay/skills/explore-relay/scripts/validate_explore_relay.py
python -X utf8 relay/implementation-relay/skills/implementation-relay/scripts/validate_implementation_relay.py
python -X utf8 relay/budget-relay/skills/budget-relay/scripts/validate_budget_relay.py
python tools/relay-installer/relay_installer.py --check
Push-Location tools/relay-installer
python -m unittest discover -s tests
Pop-Location
```

静态检查证明包和安装器一致性，不证明新任务中的 Agent 发现、实际权限隔离或质量／成本提升。真实评估应在相同任务起点、工具和验收条件下对比直接 Astra、旧 Explore＋Astra 与修订 Explore＋Astra，记录缺陷、人工介入、全部 Agent 消耗与耗时。仓库不再展示未经实测的质量或成本百分比。

## 目录

```text
relay/explore-relay/       # Parent implementation + evidence
relay/implementation-relay/  # Settled slices + targeted risk review
relay/budget-relay/        # Budget-oriented bounded implementation
tools/relay-installer/     # Install, switch, backup, rollback
packaging/                # Win64 build
readme/                   # Chinese overview and SVG assets
```
