# Codex Relay

[English](../README.md) · [简体中文](../readme/README.zh-CN.md)

<p align="center">
  <img src="../readme/assets/hero.svg" width="100%" alt="Codex Relay：父会话掌握探索、实施与验收的关键路径">
</p>

**为 Codex 配置多智能体分工，让父会话掌握关键理解、实施与验收。**

仓库提供三套可安装的 Skill 与 Agent 配置。默认从 **Explore Relay** 开始；需要委派确定的实施切片、针对性审核或优先控制预算时，再选择其他模式。职责名称保持稳定，模型由配置决定。

[选择模式](#选择模式) · [快速开始](#快速开始) · [工作约定](#工作约定) · [验证](#验证)

## 选择模式

| 模式 | 任务与分工 |
| :--- | :--- |
| **[Explore Relay](../relay/explore-relay/README.md)** | **复杂任务的默认选择。** 父会话实施，4 个只读角色收集证据。 |
| **[Implementation Relay](../relay/implementation-relay/README.md)** | **确定的实施切片或针对性审核。** 父会话掌握核心实现；4 探索、3 实施、2 审核。 |
| **[Budget Relay](../relay/budget-relay/README.md)** | **预算优先，边界已确定。** 有界执行、风险审核、技术集成。 |

> **选择依据是实施不确定性。** 范围小不代表判断简单。Explore 需要父会话核查关键证据；Implementation 要先明确实施行为；Budget 遇到高不确定性应尽早转交。

## 快速开始

在 Windows 上准备 **Python 3.11+**，从仓库根目录启动安装器：

```powershell
.\tools\relay-installer\start.ps1
```

选择安装范围与 Relay，检查预检结果，再安装。同一任务域使用一种主导模式；切换时安装器会备份已识别的旧文件，自定义文件冲突会阻止自动操作。

[安装器配置、备份与回滚说明](../tools/relay-installer/README.md)

<details>
<summary>从旧版迁移</summary>

旧名 `sol-explore-relay` → `explore-relay`，`sol-led-relay` → `implementation-relay`，`poor-relay` → `budget-relay`。`sol-pair-relay` 及其本轮临时名称 `plan-execute-relay` 已删除。Explore Agent 使用 `explore_*`，Implementation 和 Budget 保留原有职责型 Agent 名称。

旧安装不会因为源码更名自动消失。优先使用安装器预检和确认切换：已识别的旧版先备份，自定义文件阻止自动操作。旧名称仅用于迁移识别和历史版权归属，不再提供可调用别名。同一任务域使用一种主导模式；Implementation 仅在适合有界写入或针对性审核时选用，保留现有 Skill 隐式发现设置。

</details>

<details>
<summary>构建 Win64 安装器</summary>

```powershell
.\packaging\build-win64.bat
```

[安装器配置、备份与回滚说明](../tools/relay-installer/README.md)

</details>

## 工作约定

1. **委派前明确边界。** 提供固定约束、决策用途、预算和停止条件。
2. **用证据衔接上下文。** 报告包含 Coverage 与 Snapshot；“范围内没找到”不代表不存在。父会话深入阅读核心调用链，避免重做广泛检索。
3. **确认停止，再移交。** 单次超时不代表失败。预算耗尽、证据足够或问题失效时，可记录理由结束委派；复用资源或移交写入权前，确认停止并核查状态。
4. **让验收匹配改动。** 使用相应的运行、视觉或交互证据，避免重复未受影响且已通过的检查。

<details>
<summary>模型配置与父会话</summary>

推荐父会话使用 Astra；Skill 不会自动切换父模型。Explore 保留 Luna Max ×3 / Terra Max ×1；Implementation 保留 Luna Max ×6 / Terra Max ×3，父会话掌握核心实现；Budget 的规划和集成使用 `gpt-6-astra` xHigh，其余 Luna／Terra 配置不变。模型升级无需再次更名角色。

</details>

## 验证

静态检查证明包和安装器一致性，不证明新任务中的 Agent 发现、实际权限隔离或质量／成本提升。真实评估应在相同任务起点、工具和验收条件下对比直接 Astra、旧 Explore＋Astra 与修订 Explore＋Astra，记录缺陷、人工介入、全部 Agent 消耗与耗时。仓库不再展示未经实测的质量或成本百分比。

<details>
<summary>运行包与安装器检查</summary>

```powershell
python -X utf8 relay/explore-relay/skills/explore-relay/scripts/validate_explore_relay.py
python -X utf8 relay/implementation-relay/skills/implementation-relay/scripts/validate_implementation_relay.py
python -X utf8 relay/budget-relay/skills/budget-relay/scripts/validate_budget_relay.py
python tools/relay-installer/relay_installer.py --check
Push-Location tools/relay-installer
python -m unittest discover -s tests
Pop-Location
```

</details>

## 继续阅读

| 入口 | 内容 |
| :--- | :--- |
| [Relay 配置](../relay/) | 三种模式的说明、Skill 与 Agent 文件 |
| [安装器](../tools/relay-installer/) | 安装、切换、备份、回滚 |
| [Win64 打包](../packaging/) | 桌面安装器构建入口 |

[MIT 许可证](../LICENSE)
