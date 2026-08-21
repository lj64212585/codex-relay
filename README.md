<p align="right">
  <strong>简体中文</strong> · <a href="./readme/README.en.md">English</a>
</p>

<p align="center">
  <img src="./readme/assets/hero.svg" width="100%" alt="Codex Relay：在成本优先与 Sol 控制优先的两种多 Agent 调度线路之间选择">
</p>

<p align="center">
  <strong>两种调度哲学，一套清晰边界。</strong><br>
  为 Codex 复杂任务选择成本感知的渐进升级，或由父级 Sol 控制的专用分流。
</p>

<p align="center">
  <a href="#选择适合你的-relay">选择 Relay</a> ·
  <a href="#快速验证">快速验证</a> ·
  <a href="#共同原则">共同原则</a> ·
  <a href="#仓库结构">仓库结构</a>
</p>

## 选择适合你的 Relay

`codex-relay` 收录了两个取舍不同的 Codex 多 Agent 调度包。它们都由 Skill 与 custom Agent profile 组成，不引入新的 Runner 或常驻服务；区别在于你最想守住的是**模型成本**，还是**父级决策权与执行边界**。

| | [Poor Relay](./poor-relay/README.md) | [Sol-led Relay](./sol-led-relay/README.md) |
| --- | --- | --- |
| 优先目标 | 让 Luna 承担大多数工作，只在风险或价值足够高时升级 | 让父级 Sol 保留决策、集成与交付权 |
| 控制方式 | Coordinator 选择最短且足够的调度路径 | 父级 Sol 将有界任务分流到专用回路 |
| Agent 结构 | 5 个 profile：Luna 主力、Terra 审核、Sol 按需介入 | 9 个 profile：Explore ×4、Execute ×3、Review ×2 |
| 安装方式 | Windows PowerShell 脚本，默认安装到当前用户 | 将 Agent 与 Skill 安装到目标项目的 `.codex/` 与 `.agents/` |
| 适合场景 | 日常项目工作、预算敏感、希望减少高成本推理 | 复杂项目、强调角色隔离、证据交接与父级控制 |

### Poor Relay — 成本优先

让 Luna 完成高上下文调查、常规实现和自检；只有自动化证据不能覆盖关键风险时才让 Terra 审核，并把多步骤规划、失败升级和最终技术集成保留给 Sol。

**继续阅读：[poor-relay/README.md](./poor-relay/README.md)**

### Sol-led Relay — 控制优先

父级 Sol 始终负责需求、架构、共享文件协调、结果接纳和最终交付；Explorer、Executor 与 Reviewer 只接收来源、范围、检查和停止条件都明确的任务包。

**继续阅读：[sol-led-relay/README.md](./sol-led-relay/README.md)**

## 快速验证

先验证你准备使用的源码包，再按对应 README 完成安装。

<details>
<summary><strong>验证 Poor Relay</strong></summary>

```powershell
Push-Location .\poor-relay
.\scripts\verify.ps1
Pop-Location
```

</details>

<details>
<summary><strong>验证 Sol-led Relay</strong></summary>

```powershell
Push-Location .\sol-led-relay
python -X utf8 skills\sol-led-relay\scripts\validate_sol_led_relay.py
Pop-Location
```

</details>

> 静态验证只能证明包内配置与契约自洽。安装后仍应开启一个新的 Codex task，确认实际发现的 Agent、模型、推理强度、sandbox、approval policy 与可见工具；权限隔离需要用目标项目内的可丢弃 fixture 做真实验证。

## 共同原则

- **委派必须有收益**：简单、明确的一步任务留在父会话中直接完成。
- **写入必须有归属**：执行者只修改明确拥有的文件切片，共享边界由父级协调。
- **返回证据，不转移权力**：子 Agent 提供文件、diff、检查结果和风险；父级决定是否接受。
- **失败不会自动扩权**：超时、静默、证据不足或检查失败都不自动授权重试、升级或接管。
- **仓库治理始终优先**：Relay 不覆盖用户权限、项目规则、Git 流程或显式验收门槛。

## 仓库结构

```text
codex-relay/
├── poor-relay/                     # 成本与风险感知的 5-profile 调度包
│   └── README.md                    # 完整安装、策略、验证与许可证说明
├── sol-led-relay/                  # 父级 Sol 控制的 9-profile 调度包
│   └── README.md                    # 完整路由、契约、安装与验证说明
└── readme/
    ├── README.en.md                # 根 README 的英文版本
    └── assets/                     # 根 README 的本地视觉资源
```

从这里进入完整文档：**[Poor Relay](./poor-relay/README.md)** · **[Sol-led Relay](./sol-led-relay/README.md)**
