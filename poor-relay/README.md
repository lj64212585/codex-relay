# Poor Relay

Poor Relay 是一个面向 Codex Desk 单会话的低成本多 Agent 调度包。它让主会话主要维护用户意图、任务生命周期和简短结果包，把高上下文调查与常规实现交给 Luna，仅在规划、独立判断、疑难升级和最终集成真正需要时使用 Terra 或 Sol。

它不是新的多 Agent 工具，也不会安装外部 Runner。它由一个可隐式触发的 Skill、五个 custom Agent profile、两个临时状态模板和本地安装脚本组成。

## 设计目标

- 一个 Codex task 接收一次任务并编排到底；
- Luna Max 作为推荐 Coordinator，不让 Sol 常驻；
- Luna 承担调查和有界实现，Terra 只做有价值的独立 Reviewer；
- Sol 只负责复杂规划、失败升级和最终技术集成；
- Agent 数量保持克制，技术专长优先通过 Skill 提供；
- 规划和状态只写入临时运行目录，完成后清理；
- 不引入 OpenSpec、强制 worktree、每 Task commit 或固定全量 Review。

若用户或仓库本身要求 OpenSpec、特定 Git 流程或其他治理规则，应继续服从那些规则；Poor Relay 不会删除、替换或绕过既有治理文件。

## 架构

~~~text
用户
  |
  v
Codex Desk 单一主会话
Luna Max Coordinator（推荐）
  |
  +-- tm_explorer   Luna Medium  调查 / 搜索 / 代码探索
  +-- tm_planner    Sol xHigh     架构 / 多步骤计划
  +-- tm_executor   Luna High     有界实现 / 自测
  +-- tm_reviewer   Terra Medium  按风险触发的独立审核
  └-- tm_integrator Sol xHigh     疑难升级 / 最终集成
~~~

Coordinator 保留用户意图、权限、调度、共享文件协调和最终交付。Planner 与 Integrator 可以作技术判断，但不能扩大用户授权，也不能代替用户验收。

## 目录

~~~text
poor-relay/
├── README.md
├── LICENSE
├── THIRD_PARTY_NOTICES.md
├── agents/
│   ├── tm_planner.toml
│   ├── tm_explorer.toml
│   ├── tm_executor.toml
│   ├── tm_reviewer.toml
│   └── tm_integrator.toml
├── skills/
│   └── poor-relay/
│       ├── SKILL.md
│       ├── agents/openai.yaml
│       ├── references/
│       │   ├── execution-plan.md
│       │   └── runtime-state.md
│       └── scripts/validate_poor_relay.py
└── scripts/
    ├── install.ps1
    ├── uninstall.ps1
    └── verify.ps1
~~~

根级 agents 与 Skill 源目录分离，沿用 sol-led-relay 的分发形状；角色数量和行为则按 Poor Relay 的轻量方案收窄。

## Profiles

| Profile | 模型 | 推理强度 | 默认 sandbox | 用途 |
|---|---|---|---|---|
| tm_planner | gpt-5.6-sol | xhigh | workspace-write | 写临时执行计划 |
| tm_explorer | gpt-5.6-luna | medium | read-only | 收集压缩证据 |
| tm_executor | gpt-5.6-luna | high | workspace-write | 实现一个有界 Task |
| tm_reviewer | gpt-5.6-terra | medium | read-only | 审核一个明确 blocking risk |
| tm_integrator | gpt-5.6-sol | xhigh | workspace-write | 升级修复或最终集成 |

没有 default.toml。每次 dispatch 必须显式指定 agent_type，避免覆盖用户级默认 Agent 并影响其他 Codex 工作流。

## 安装

在 poor-relay 目录执行：

~~~powershell
.\scripts\verify.ps1
.\scripts\install.ps1
~~~

默认安装到当前 Windows 用户：

~~~text
%USERPROFILE%\.agents\skills\poor-relay\
%USERPROFILE%\.codex\agents\tm_planner.toml
%USERPROFILE%\.codex\agents\tm_explorer.toml
%USERPROFILE%\.codex\agents\tm_executor.toml
%USERPROFILE%\.codex\agents\tm_reviewer.toml
%USERPROFILE%\.codex\agents\tm_integrator.toml
~~~

安装器会先检查所有目标。只要 Skill 或任一同名 Agent 已存在，默认就停止，不覆盖来源不明的用户配置。确认这些目标应由本包替换时，才显式使用：

~~~powershell
.\scripts\install.ps1 -Force
~~~

安装或更新 custom Agent 后，启动一个新的 Codex task，再检查实际发现到的 Agent 名称、模型、reasoning effort、sandbox 和工具。静态解析 TOML 不能证明运行时配置已经生效。

## 验证

验证源码包：

~~~powershell
.\scripts\verify.ps1
~~~

验证已安装副本：

~~~powershell
.\scripts\verify.ps1 -Installed
~~~

验证内容包括 Skill frontmatter、UI 元数据、两个 Reference、五个 Agent 的精确模型/推理强度/sandbox、角色安全边界、命名残留、安装脚本语法和 default.toml 缺失。

read-only 是 profile 请求的默认 sandbox，不等于已证明的技术隔离。若隔离是验收条件，应在新的 Codex task 中使用一次性 fixture 做真实写入拒绝测试；不要对生产文件、凭据或外部系统做权限探测。

## 使用方式

可以显式调用：

~~~text
Use $poor-relay to complete this multi-step project task.
~~~

Skill 允许隐式触发，但会先判断是否值得委派。简单的一步回答或修改仍由主会话直接完成。

复杂任务的最小流程：

1. 需要大量未知上下文时，使用 tm_explorer；
2. 多步骤或架构型任务使用 tm_planner 写临时 plan.md；
3. Coordinator 维护极简 state.md；
4. 每个有界 Task 使用 tm_executor 实现并自测；
5. 只有风险无法被机械验证完全覆盖时才使用 tm_reviewer；
6. 一次定向修复仍失败时，直接交给 tm_integrator；
7. 所有 Task 完成后，tm_integrator 做一次最终集成检查；
8. Coordinator 核对实际 diff 和证据，清理当前任务的临时目录并交付。

## 临时状态

多步骤任务临时创建：

~~~text
<ProjectRoot>/.codex-team/runtime/<task-id>/
├── plan.md
└── state.md
~~~

这些文件用于 context compaction 和中断恢复，不是项目文档，不得 stage 或 commit。只有整个用户任务真正完成时才删除当前 task-id 的目录；任务被阻塞或中断时保留，以便同一任务恢复。不得借清理 Poor Relay 状态删除仓库原有的 OpenSpec、计划、归档或其他项目资料。

## Reviewer 与升级规则

机械改名、单文件低风险修改、强自动化覆盖可以跳过 Reviewer。业务逻辑、多文件协作、状态变化、持久化、API contract、边界逻辑或难以被测试完全证明的行为才使用 Terra。

Executor 对直接相关的检查失败最多做一次定向修正。Reviewer FAIL 后，Coordinator 最多再派 Luna 定向修一次；仍失败就直接由 Sol Integrator 接管，不让 Terra 变成执行者，也不建立反复换模型的长链。

## 来源和许可证

Poor Relay 的文本和脚本为重新编写，设计上吸收了 codex-team-mode、wshobson/agents、agency-agents 与 Superpowers 的部分工作流思想。项目本身采用 MIT License；上游版权、具体来源文件和改编边界见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
