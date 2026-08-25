<p align="right">
  <strong>简体中文</strong> · <a href="./README.en.md">English</a>
</p>

<p align="center">
  <img src="./assets/readme/hero.svg" width="100%" alt="Sol-led Relay：由父级 Sol 控制、沿 Explorer、Executor 与 Reviewer 三条回路分流任务的 Codex 多 Agent 调度包">
</p>

<p align="center">
  <strong>让 Sol 保留决策权，让复杂任务沿边界清晰的回路流动。</strong><br>
  面向项目级 Codex 工作的窄职责多 Agent 调度包：按需探索、有限执行、独立复核，最终仍由父会话集成与交付。
</p>

## 它解决什么

复杂任务需要分工，但分工不该稀释责任。Sol-led Relay 将可隔离的工作交给 9 个专用 profile，同时把需求澄清、架构决策、共享文件协调、最终验证和对外交付留在父级 Sol。

- **按收益委派**：只有上下文隔离、并行调查或独立复核确有价值时才启动子 Agent；小而明确的任务直接完成。
- **按边界路由**：Explorer 只取证，Executor 只写已冻结的范围，Reviewer 只审查真实 diff 或验收证据。
- **按契约交接**：每次 dispatch 都必须写明 outcome、sources、scope、checks、stop condition 与 return contract。
- **失败时收紧**：超时只是一次轮询结果；没有文件变化不等于没有进展；静默、证据不足或检查失败都不会自动授权升级、重试或接管。

## 路由面板

<p align="center">
  <img src="./assets/readme/routing-board.svg" width="100%" alt="Sol-led Relay 路由图：父级 Sol 根据任务需要把有界工作分流到四个 Explorer、三个 Executor 或两个 Reviewer，再接收结果并完成最终验证与集成">
</p>

| 回路 | 适合处理 | Profiles | 默认权限 |
| --- | --- | --- | --- |
| **Explore ×4** | 代码路径、外部文档、单点运行证据、初始即跨系统或证据矛盾的问题 | `code_explorer` · `docs_researcher` · `runtime_investigator` · `runtime_investigator_deep` | read-only |
| **Execute ×3** | 精确机械修改、已确认根因的最小修复、接口与验收条件已冻结的功能切片 | `mechanical_executor` · `minimal_fixer` · `bounded_executor` | workspace-write |
| **Review ×2** | 真实实现的正确性/回归审查、逐项验收证据核对 | `code_reviewer` · `verification_reviewer` | read-only |

所有 profile 均使用 `model_reasoning_effort = "max"`。`runtime_investigator_deep`、`code_reviewer` 与 `verification_reviewer` 使用 `gpt-5.6-terra`；其余 profile 使用 `gpt-5.6-luna`。

> `runtime_investigator_deep` 只接受任务开始时就跨系统或已有证据明显矛盾的调查；它不是普通调查无结论后的自动升级通道。

## 一次完整接力

1. **父级判断是否值得委派**：未解决的产品、架构、安全、权限和跨系统决策不下放。
2. **选择最小角色集合**：最多并行三个只读 Agent；同一时刻只允许一个写入 Agent，并明确文件所有权。
3. **发送有界 packet**：固定目标、来源、范围、检查、停止条件和返回格式；子 Agent 不得继续派生后代。
4. **接收证据而非结论权**：父级检查实际文件、diff、产物和验证输出，再决定是否接受。
5. **由父级完成闭环**：集成、Git 操作、构建、发布、外部写入和最终回复始终属于父会话。

## 安装到项目

标准安装面只有两处：

```text
<target-project>/
├── .codex/agents/*.toml
└── .agents/skills/sol-led-relay/**
```

下面的 PowerShell 示例会在发现同名 Agent 或 Skill 时停止，不覆盖来源不明的现有文件：

```powershell
$relaySource = "D:\path\to\codex-relay\relay\sol-led-relay"
$targetProject = "D:\path\to\target-project"
$agentTarget = Join-Path $targetProject ".codex\agents"
$skillTarget = Join-Path $targetProject ".agents\skills\sol-led-relay"

$profileNames = Get-ChildItem (Join-Path $relaySource "agents\*.toml") | Select-Object -ExpandProperty Name
$conflicts = $profileNames | Where-Object { Test-Path (Join-Path $agentTarget $_) }
if ($conflicts -or (Test-Path $skillTarget)) {
    throw "发现同名 Agent 或 Skill；请先确认来源：$($conflicts -join ', ')"
}

New-Item -ItemType Directory -Force $agentTarget, $skillTarget | Out-Null
Copy-Item (Join-Path $relaySource "agents\*.toml") $agentTarget
Copy-Item (Join-Path $relaySource "skills\sol-led-relay\*") $skillTarget -Recurse
```

如果目标项目已有自己的 Skill 安装器或 Junction 约定，请把 `skills/sol-led-relay` 作为唯一源目录接入现有流程，不要另建一份来源不明的副本。

## 验证

先在 `sol-led-relay` 包根目录运行静态验证：

```powershell
python -X utf8 skills\sol-led-relay\scripts\validate_sol_led_relay.py
```

验证器会检查：9 个 profile 是否齐全、模型与 `max` 推理强度、sandbox 默认值、隐式 Skill 路由、dispatch 契约，以及存活/超时/中断的 fail-closed 规则。

配置文件通过不等于运行时已经生效。安装后还需要开启一个**新的 Codex task**，逐个确认实际发现的 Agent 名称、模型、reasoning effort、有效 sandbox / approval policy 与可见工具。若权限隔离是验收条件，请只在目标项目内的可丢弃 fixture 上执行写入探针；只读角色能够产生变更时应记录为 `NOT_ENFORCED`。

## 包结构

```text
sol-led-relay/
├── agents/                         # 安装到目标项目 .codex/agents/
│   ├── code_explorer.toml
│   ├── docs_researcher.toml
│   ├── runtime_investigator*.toml
│   ├── *_executor.toml
│   └── *_reviewer.toml
├── skills/sol-led-relay/           # 安装到目标项目 .agents/skills/
│   ├── SKILL.md                    # 激活、路由、并发与失败边界
│   ├── agents/openai.yaml          # 展示信息与隐式调用策略
│   ├── references/                 # dispatch、路由与评估契约
│   └── scripts/                    # 静态验证器
├── README.en.md
└── README.md
```

没有 `default.toml`：这个包不会用一个宽泛的默认角色吞掉所有任务。`agents/` 与 Skill 也保持分开分发——前者声明运行 profile，后者决定何时委派、如何路由，以及哪些权力必须留在父会话。

## 设计边界

| 子 Agent 可以做 | 父级 Sol 保留 |
| --- | --- |
| 在明确来源和范围内调查 | 需求、产品、架构、安全与权限决策 |
| 修改唯一归属的文件切片 | 共享文件协调与跨切片集成 |
| 执行分配的确定性检查 | 接受或拒绝子 Agent 结果 |
| 返回证据、风险与最小下一步 | Git、远程构建、发布、外部写入与最终交付 |

完整行为约束见 [`skills/sol-led-relay/SKILL.md`](./skills/sol-led-relay/SKILL.md)，细分契约见 [`contracts.md`](./skills/sol-led-relay/references/contracts.md)、[`routing.md`](./skills/sol-led-relay/references/routing.md) 与 [`evaluation.md`](./skills/sol-led-relay/references/evaluation.md)。
