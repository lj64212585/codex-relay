<p align="right">
  <strong>简体中文</strong> · <a href="../README.md">English</a>
</p>

<p align="center">
  <img src="./assets/hero.svg" width="100%" alt="Codex Relay：在成本优先、Explore-only、双 Sol 新上下文接力与 Sol 全车道控制四种调度策略之间选择">
</p>

<p align="center">
  <strong>四种调度哲学，一套清晰边界。</strong><br>
  为 Codex 项目任务选择成本优先、只外包探索、双 Sol 规划执行接力，或由父级 Sol 控制完整车道。
</p>

<p align="center">
  <a href="https://github.com/lj64212585/codex-relay/releases/tag/v1.0.0"><strong>下载 v1.0.0</strong></a> ·
  <a href="#选择适合你的-relay">选择 Relay</a> ·
  <a href="#相对完美度与成本估算">对比估值</a> ·
  <a href="#使用-relay-installer">网页安装器</a> ·
  <a href="#快速验证">快速验证</a> ·
  <a href="#共同原则">共同原则</a> ·
  <a href="#仓库结构">仓库结构</a>
</p>

## 选择适合你的 Relay

`codex-relay` 收录了四套可独立安装的 Codex 多 Agent 调度包。它们都由 Skill 与 custom Agent profile 组成，不引入新的 Runner 或常驻服务；真正的区别是你希望把哪些工作送出父会话，以及最想守住什么。

| Relay | 首要目标 | 可委派范围 | 适合场景 |
| --- | --- | --- | --- |
| [Poor Relay](../relay/poor-relay/README.md) | 让 Luna 承担大多数工作，只在风险或价值足够高时升级 | 规划、探索、执行、审核与集成按成本分层 | 日常项目、预算敏感、希望减少高成本推理 |
| [Sol Explore Relay](../relay/sol-explore-relay/README.md) | 节约检索上下文，同时让父级 Sol 亲自实现 | **仅 4 个只读 Explore profile** | 质量敏感、共享文件多、希望避免实现交接 |
| [Sol Pair Relay](../relay/sol-pair-relay/README.md) | 让两个 Sol 分别获得干净的规划与执行上下文 | Luna Max 探索、Sol Max 规划、另一个 Sol Max 执行验收 | Luna / Terra 主对话、实现质量优先、需要临时计划防偏 |
| [Sol-led Relay](../relay/sol-led-relay/README.md) | 让父级 Sol 保留决策、集成与交付权 | Explore ×4、Execute ×3、Review ×2 | 复杂项目、适合有界切片与独立审核 |

## 相对完美度与成本估算

以下数值是面向**同一个中高复杂度工程任务**的相对估值：由单个 Sol 在同一主会话独立完成探索、实现、检查与验收，记为 `100%`。任务实现完美度是相对质量指数，不是绝对成功率，因此可以高于 `100%`；实现成本统计各参与 Agent 的总体模型推理消耗，不包含人工、设备、发布或外部系统验收成本。

| 调度方式 | 任务实现完美度 | 实现成本 | 估值依据 |
| --- | ---: | ---: | --- |
| 单个 Sol 独立完成 | **100%** | **100%** | 基准；没有交接损耗，也没有独立上下文带来的复核增益 |
| [Poor Relay](../relay/poor-relay/README.md) | ${\color[RGB]{154,103,0}\mathbf{95\\%}}$ | ${\color[RGB]{26,127,55}\mathbf{45\\%}}$ | Luna 承担探索与常规实现，Terra 和 Sol 只在风险、规划或集成节点介入；成本最低，但细腻实现与全局一致性略让位于预算 |
| [Sol Explore Relay](../relay/sol-explore-relay/README.md) | ${\color[RGB]{26,127,55}\mathbf{110\\%}}$ | ${\color[RGB]{26,127,55}\mathbf{90\\%}}$ | Luna / Terra 隔离高噪声探索，父级 Sol 保留完整实现权；减少上下文污染，以少量派发和复核开销换取质量提升 |
| [Sol Pair Relay](../relay/sol-pair-relay/README.md) | ${\color[RGB]{26,127,55}\mathbf{120\\%}}$ | ${\color[RGB]{207,34,46}\mathbf{180\\%}}$ | 两个全新的 Sol Max 分别规划和实现验收，质量上限最高；重复理解、计划交接与双 Sol 推理也使成本最高 |
| [Sol-led Relay](../relay/sol-led-relay/README.md) | ${\color[RGB]{26,127,55}\mathbf{115\\%}}$ | ${\color[RGB]{26,127,55}\mathbf{85\\%}}$ | 父级 Sol 保留决策与集成，Luna 执行有界切片，Terra 独立复核；在多角色协调开销下仍兼顾较高质量与较低成本 |

> 这些数值用于比较调度取向，不是实测 benchmark。一步式小任务通常无法摊薄派发成本；任务越复杂、探索噪声越大、切片边界越清晰，Relay 的相对收益越接近表中估值。
>
> 你可以按自己的任务复杂度、质量目标和预算，调整每种调度中各 profile 的模型推理强度（`model_reasoning_effort`）；上表数值只对应仓库默认配置，调整后完美度与成本估值也会随之变化。

### Poor Relay — 成本优先

Luna 负责高上下文调查、常规实现和自检；Terra 只在自动化证据覆盖不了关键风险时审核，Sol 保留多步骤规划、失败升级与最终技术集成。

**完整指南：[relay/poor-relay/README.md](../relay/poor-relay/README.md)**

### Sol Explore Relay — 只外包探索

四个只读 Explorer 分别追踪仓库、核对官方资料、分析单一运行问题或对齐跨系统矛盾证据。父级 Sol 复核关键切片后，自行规划、编辑、测试、审核真实 diff 并交付；没有任何写入或审核子角色。

**完整指南：[relay/sol-explore-relay/README.md](../relay/sol-explore-relay/README.md)**

### Sol Pair Relay — 双 Sol 新上下文接力

Luna 或 Terra 保持主对话，Luna Max 只负责压缩可选探索证据；一个全新的 Sol Max 只写临时 `plan.md`，另一个全新的 Sol Max 按计划实现、运行检查、审阅真实 diff 并完成技术验收。两个 Sol 不共享长对话，只共享已批准计划和少量决策关键证据。

**完整指南：[relay/sol-pair-relay/README.md](../relay/sol-pair-relay/README.md)**

### Sol-led Relay — 全车道控制

父级 Sol 负责需求、架构、共享文件协调、结果接纳与最终交付，同时把来源、范围、检查和停止条件明确的任务切片送入 Explorer、Executor 与 Reviewer 专用回路。

**完整指南：[relay/sol-led-relay/README.md](../relay/sol-led-relay/README.md)**

## 使用 Relay Installer

Windows 用户可直接从 GitHub Releases 下载 **[Relay Installer v1.0.0](https://github.com/lj64212585/codex-relay/releases/tag/v1.0.0)**。Release Assets 同时提供单文件 Win64 可执行程序及其 SHA-256 校验和。

如果希望从源码运行安装器，可以从仓库根目录启动配置驱动的本地网页版本。该方式要求 Python 3.11 或更高版本，仅监听 `127.0.0.1`，首次打开默认英文，并提供中英文切换与夜间模式。

```powershell
.\tools\relay-installer\start.ps1
```

打开网页后：

1. 在“安装范围”选择“全局”或“项目”。全局只作用于当前 Windows 用户；项目模式可输入目标根目录，或点击“浏览目录”。
2. 在“Relay 类型”选择一种调度。每个横向选项会显示任务实现完美度与实现成本；点击左侧“详情”，可以查看当前界面语言对应的 Relay README。
3. 点击“检查并安装”。安装器会先预检目标；若发现其他 Relay，会说明多个调度的隐式路由可能互相冲突，并在获得确认后备份、移除已识别的旧调度，再完成安装。
4. 如需清理当前目标，点击“安装范围”底部的红色“移除当前目录的调度文件”按钮。确认框会列出将被移除的 Relay 和路径，确认后才执行。

> 安装器只处理配置中能够明确归属的 Skill 目录和 Agent 文件，不会删除未知自定义文件。切换或移除前的内容会保存到目标根目录的 `.relay-installer-backups`，便于恢复。

<details>
<summary><strong>配置检查与可执行文件打包</strong></summary>

只检查配置与所有 Relay 源文件：

```powershell
py -3 -B .\tools\relay-installer\relay_installer.py --check
```

安装 64 位 Python 3.11+ 与构建依赖后，可用仓库打包入口生成内置四套 Relay 的单文件 Win64 桌面程序。双击产物只会打开 Relay Installer 窗口，不创建命令行窗口，也不打开系统浏览器：

```powershell
python -m pip install -r .\tools\relay-installer\requirements-build.txt
.\packaging\build-win64.bat
```

BAT 从被 Git 忽略的 `packaging/version.txt` 读取版本号，在打包结束后检查桌面入口、包内内容、内置版本及 Windows 版本元数据，产物写入 `packaging/out/win64/relay-installer-v<版本号>.exe`。窗口标题和 Windows 文件属性都会显示该版本；桌面窗口使用系统的 Microsoft Edge WebView2 Runtime。完整的版本格式、配置字段、路径边界与高级打包参数见 **[Relay Installer 文档](../tools/relay-installer/README.md)**。

</details>

## 快速验证

先验证准备使用的源码包，再按对应 README 安装。四套 Skill 都支持隐式调用；同一个任务域应只选择一套主导策略，避免重叠规则同时抢占路由。

<details>
<summary><strong>验证 Poor Relay</strong></summary>

```powershell
Push-Location .\relay\poor-relay
.\scripts\verify.ps1
Pop-Location
```

</details>

<details>
<summary><strong>验证 Sol Explore Relay</strong></summary>

```powershell
Push-Location .\relay\sol-explore-relay
python -X utf8 skills\sol-explore-relay\scripts\validate_sol_explore_relay.py
Pop-Location
```

</details>

<details>
<summary><strong>验证 Sol Pair Relay</strong></summary>

```powershell
Push-Location .\relay\sol-pair-relay
.\scripts\verify.ps1
Pop-Location
```

</details>

<details>
<summary><strong>验证 Sol-led Relay</strong></summary>

```powershell
Push-Location .\relay\sol-led-relay
python -X utf8 skills\sol-led-relay\scripts\validate_sol_led_relay.py
Pop-Location
```

</details>

> 静态验证只能证明包内配置与契约自洽。安装后仍应开启一个新的 Codex task，确认实际发现的 Agent、模型、reasoning effort、有效 sandbox / approval policy 与可见工具；声明为只读的角色需要在目标项目内用可丢弃 fixture 验证实际隔离。

## 共同原则

- **委派必须有收益**：简单、明确的一步任务留在父会话中直接完成。
- **只启用所选边界**：成本分层、Explore-only、双 Sol 接力与全车道分流是四种不同策略，不应在同一任务域叠加解释。
- **返回证据，不转移权力**：子 Agent 提供文件、行号、来源、检查结果和风险；父级决定是否接受。
- **写入必须有明确所有者**：Sol Explore Relay 的写入只属于父级；其他 Relay 也必须为每个写入切片指定所有者。
- **上下文隔离必须真实**：Sol Pair Relay 的 Planner 与 Executor 必须是不同 Agent，临时 `plan.md` 是两个 Sol 之间唯一的持久接力物。
- **失败不会自动扩权**：超时、静默、证据不足或检查失败都不自动授权重试、升级或接管。
- **仓库治理始终优先**：Relay 不覆盖用户权限、项目规则、Git 流程或显式验收门槛。

## 仓库结构

```text
codex-relay/
├── relay/
│   ├── poor-relay/                 # 成本与风险感知的 5-profile 调度包
│   ├── sol-explore-relay/          # Explore-only、父级 Sol 实现的 4-profile 调度包
│   ├── sol-pair-relay/             # Luna / Terra 主对话、双 Sol 接力的 3-profile 调度包
│   └── sol-led-relay/              # 父级 Sol 控制三车道的 9-profile 调度包
├── packaging/
│   ├── build-win64.bat             # 单文件 Win64 打包与包内自检入口
│   ├── version.txt                 # 被 Git 忽略的本地版本号来源
│   └── out/win64/                  # 被 Git 忽略的生成产物
├── tools/
│   └── relay-installer/            # 支持桌面窗口、网页运行、安装、切换、移除与打包
├── README.md                       # 根目录英文 README
└── readme/
    ├── README.zh-CN.md             # 简体中文版本
    └── assets/                     # 根 README 的本地视觉资源
```

从这里进入完整文档：**[Poor Relay](../relay/poor-relay/README.md)** · **[Sol Explore Relay](../relay/sol-explore-relay/README.md)** · **[Sol Pair Relay](../relay/sol-pair-relay/README.md)** · **[Sol-led Relay](../relay/sol-led-relay/README.md)**
