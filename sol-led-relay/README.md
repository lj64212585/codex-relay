# Sol-led Relay

这是一个由父级 Sol Agent 主导的项目级 Codex 多 Agent 调度包。它采用根级 Agent profiles 与独立 Skill 源目录的布局，把 Explorer、Executor 和 Reviewer 细分为 9 个窄职责 profile，并保持隐式 Skill 路由。

## 结构

```text
sol-led-relay/
├── agents/                         # 安装到目标项目 .codex/agents/
├── skills/sol-led-relay/            # 安装到目标项目 .agents/skills/
├── tests/
└── README.md
```

`agents/` 与 Skill 分开分发。Skill 负责判断是否值得委派、选择 profile、构造有界 dispatch packet，以及保留父会话决策和验收权；TOML profile 负责具体模型、推理强度、sandbox 默认值和角色行为。

## Profiles

| 类别 | Profile | 模型 | 默认 sandbox |
|---|---|---|---|
| Explorer | `code_explorer` | `gpt-5.6-luna` / max | read-only |
| Explorer | `docs_researcher` | `gpt-5.6-luna` / max | read-only |
| Explorer | `runtime_investigator` | `gpt-5.6-luna` / max | read-only |
| Explorer | `runtime_investigator_deep` | `gpt-5.6-terra` / max | read-only |
| Executor | `mechanical_executor` | `gpt-5.6-luna` / max | workspace-write |
| Executor | `minimal_fixer` | `gpt-5.6-luna` / max | workspace-write |
| Executor | `bounded_executor` | `gpt-5.6-luna` / max | workspace-write |
| Reviewer | `code_reviewer` | `gpt-5.6-terra` / max | read-only |
| Reviewer | `verification_reviewer` | `gpt-5.6-terra` / max | read-only |

没有 `default.toml`。`runtime_investigator_deep` 只用于任务初始即跨系统或输入证据已经矛盾的情况；普通 Luna 调查一轮仍无结论时直接交还父会话，不升级 Terra。

## 安装到项目

标准 Codex 项目安装面：

```text
<target-project>/.codex/agents/*.toml
<target-project>/.agents/skills/sol-led-relay/**
```

复制前先检查目标项目是否已有同名 Agent 或 Skill；不要覆盖无法确认来源的文件。配置新增后，在新的 Codex task 中验证实际发现、模型、reasoning effort、sandbox 和可见工具。

如果目标项目使用自己的 Skill 安装器或 Junction 约定，应将 `skills/sol-led-relay` 作为唯一源目录接入该安装流程；不要覆盖或复制来源不明的现有 Junction。

## 验证

在本仓库根目录运行：

```powershell
python -X utf8 skills/sol-led-relay/scripts/validate_sol_led_relay.py
python -m unittest discover -s tests -p "test_*.py" -v
```

静态通过不等于有效只读隔离。安装后仍需在目标项目的隔离 fixture 中执行 `skills/sol-led-relay/references/evaluation.md` 规定的 fresh-session 权限探针；若 read-only profile 可以产生写入，结果必须记录为 `NOT_ENFORCED`。
