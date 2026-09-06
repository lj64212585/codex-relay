# Relay 指令审计与 Win64 构建验证

审计日期：2026-09-06（Asia/Shanghai）。基线为本轮开始时的暂存区，包含用户已有的 Relay 更名和安装器修改；本轮改动留在工作区，未提交、推送或安装到用户配置目录。

## 官方依据与适用范围

已实时搜索并读取 [GPT-6 Astra 官方模型指导](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-6-astra) 的提示词最佳实践和迁移说明。此次采用其中关于自主完成、指令冲突、明确委派条件、简洁沟通和适度验证的建议。以下路由和恢复规则是结合本仓库职责边界作出的设计选择，不是官方提供的 Relay 配置。

[官方 Skills 文档](https://developers.openai.com/codex/skills/)说明按需加载以及简短、清晰的触发描述；据此缩短入口和必读交接内容。[官方 Subagents 文档](https://developers.openai.com/codex/subagents/)用于核对专用角色配置、模型／推理设置、上下文和并发配置的职责。

[Astra 模型页](https://developers.openai.com/api/docs/models/gpt-6-astra)列出的推理强度包含 `xhigh`。模型指导建议先保留现有有效推理强度，因此两个 Budget Astra 角色继续使用 `gpt-6-astra` / `xhigh`，没有凭名称将其改成 `max` 或 `ultra`。Explore／Implementation 的 Luna、Terra 型号、推理强度、权限类型和角色名保持原有分工。API 的异步调用、缓存等功能不属于这些 Skill／TOML 的配置表面，本次未添加无法兑现的 API 设置。

## 审计发现与处理

| 发现 | 调整及保留的边界 |
| --- | --- |
| 入口、routing、contracts 多次描述相同职责，派单需要填写大量固定字段 | 入口保留目的、路由、所有权和完成要求；交接改为简短自然语言，标签和不适用字段可省略，预算仅在实际存在时传递 |
| 缺少明确的自主推进规则，容易将模板缺项当成阻塞 | 从上下文完成常规选择；只有实质影响正确性、范围或授权的缺口才请求决策，同时继续独立工作 |
| 要求精确角色却没有角色不可用时的继续路径 | 保留精确角色名；缺少所需角色时父代理直接继续，不臆造等价代理 |
| 固定最多三个只读代理，Implementation 固定只能一个写者 | 使用宿主容量和用户预算；并行写者必须满足文件不相交、接口稳定、生成产物及运行资源独立，冲突资源仍串行 |
| 普通 runtime 一轮无结论即停止，deep 禁止接收前序调查的新证据 | 允许在范围内沿新增证据推进；父代理可根据实际发现提出跨系统问题，禁止仅因无结论而原样升级重跑 |
| Implementation 写者第二次检查失败必停 | 在所有权和预算内继续有证据支持的相关修正；重复同一失败且无进展、契约冲突或预算耗尽仍返回父代理 |
| 审查前要求全部检查通过，审查者只准追踪一跳依赖 | 允许审查注明状态的部分 diff 和失败检查；按证据检查必要依赖，保持指定风险范围 |
| Planner 负责架构规划，却可能因没有预先给定架构选择而 BLOCKED | 允许在委派授权内选择技术方案；真实产品／权限／兼容性等未决事项仍返回 Coordinator；只写指定 plan.md |
| Integrator 早期升级仍要求已有 diff、plan、state，Final 只能修一个阻塞缺陷 | 允许直接检查源码完成早期技术任务；Final 在分配所有权内解决相关阻塞缺陷，再运行匹配检查 |
| Budget 模板只展示 PLAN_READY，与真实阻塞的角色输出冲突 | 模板明确仅可执行计划返回 PLAN_READY，并保留 BLOCKED 与部分计划交接；同步精简入口派单说明和 Final 单数措辞 |
| 静态验证器用固定句子、标题和重试次数证明提示词行为 | 改验实际配置、唯一角色、路由引用、必需引用链接、本地链接和隐式调用元数据；行为另做情境评估 |

对应入口为 [Explore Skill](../relay/explore-relay/skills/explore-relay/SKILL.md)、[Implementation Skill](../relay/implementation-relay/skills/implementation-relay/SKILL.md)、[tm_planner](../relay/budget-relay/agents/tm_planner.toml) 和 [tm_integrator](../relay/budget-relay/agents/tm_integrator.toml)。为消除运行时矛盾，同步修改了两个包中 7 个相关子代理指令、引用文件和双语说明。

Explore 仍只委派证据收集，所有写入和验收判断由父代理完成。Implementation 仍把需要持续判断的复杂状态、持久化、并发、安全和核心交互交给父代理；文件少或接口固定并不自动代表实现简单。两者都保留证据新鲜度、限定负面搜索范围、停止确认和写入权交接。

Budget 的低成本 `tm_executor` 原有有限重试与升级策略仍保留；不能把 Implementation 新的修正策略套用到 Budget executor。

## 指令体量

按 LF 归一化后的 Unicode 字符计数，比较本轮开始的暂存版本与当前工作区。不是模型 token 计费或性能数据。

| 表面 | 修改前 | 修改后 | 变化 |
| --- | ---: | ---: | ---: |
| Explore SKILL.md | 7,376 | 4,947 | −32.9% |
| Explore 入口 + contracts + routing | 12,718 | 8,495 | −33.2% |
| Implementation SKILL.md | 9,044 | 6,835 | −24.4% |
| Implementation 入口 + contracts + routing | 15,810 | 11,885 | −24.8% |

两个 Astra 角色增加了必要的授权内判断、早期升级和真实完成要求，文件本身没有按字符数缩短。精简目标是减少重复流程和人为停止规则，同时补齐会造成停工或错误完成的契约。

## 验证证据

| 验证层 | 实际结果 |
| --- | --- |
| 修改前基线 | 三个包的原验证器均通过 |
| 当前静态包验证 | Explore、Implementation、Budget 均通过；18 个角色的模型、推理强度和声明权限符合各包预期 |
| Skill Creator quick_validate.py | 三个 Skill 均通过 |
| 隔离配置回归 | [test_relay_packages.py](../tools/tests/test_relay_packages.py) 的 6 个测试方法、20 个临时目录用例通过：源／安装布局、错误模型／推理／只读权限、缺文件、损坏链接、未知路由等 |
| 安装器现有测试 | 24 项通过；配置 `--check` 识别当前 3 种 Relay |
| 独立情境评估 | 10 个场景完成提示词解释与模拟下一步，发现的 Budget 输出／派单措辞冲突已修正 |
| 工作区差异 | `git diff --check` 通过；保留原有暂存改动 |

独立评估覆盖：角色缺失时继续、新证据支持的 deep 调查、共享生成产物的写入串行、第二次有新证据的修正、失败检查下的审查、授权内缓存规划、无历史产物的早期升级、多个 Final 阻塞修复、停止未确认的所有权保护，以及单测不能替代浏览器交互。评估者读到了包含相近预期场景的 evaluation 引用，因此本轮是**有限情境评估，不是完全盲测**，也没有实际调用这些已安装自定义角色执行场景。

真实任务质量／耗时／全部代理 token 的 A/B、已安装角色发现、有效模型／工具设置和沙箱拒写探针均为 **NOT_EVALUATED**。文本缩短和配置测试通过不能证明已经最大化 Astra 性能；新的 evaluation 引用保留了可复用的实测场景。

复现静态检查（仓库根目录）：

```powershell
python -B -X utf8 relay/explore-relay/skills/explore-relay/scripts/validate_explore_relay.py
python -B -X utf8 relay/implementation-relay/skills/implementation-relay/scripts/validate_implementation_relay.py
python -B -X utf8 relay/budget-relay/skills/budget-relay/scripts/validate_budget_relay.py
python -B -X utf8 -m unittest discover -s tools/tests -v
$env:PYTHONPATH = (Resolve-Path tools/relay-installer).Path
python -B -X utf8 -m unittest discover -s tools/relay-installer/tests -v
python -B -X utf8 tools/relay-installer/relay_installer.py --check
```

## Win64 构建与 SHA-256

用户追加要求已落实到 [build-win64.bat](../packaging/build-win64.bat) 和 [build.ps1](../tools/relay-installer/build.ps1)：BAT 传入 `-VersionedOutput -WriteChecksums`，后端使用已校验版本拼接输出目录，验证 EXE 后写入无 BOM、LF 结尾的标准 SHA-256 清单。直接调用后端时这两个开关是可选的，`WriteChecksums` 要求 `onefile` 模式，以覆盖整个便携包。

当前 version.txt 为 `2.0.0`，实际成功产物：

- [relay-installer-v2.0.0.exe](../packaging/out/win64/2.0.0/relay-installer-v2.0.0.exe)，22,657,286 bytes。
- [SHA256SUMS.txt](../packaging/out/win64/2.0.0/SHA256SUMS.txt)。

```text
d5db21be359b77f1366b4f766ad16c21d193b54426240eb582d7930d58a24296  relay-installer-v2.0.0.exe
```

Windows PowerShell 实际调用 BAT 成功；EXE 的 `--check`、内置版本输出和 Windows 版本元数据均通过。使用独立 Python hashlib 核对清单的哈希、文件名、两空格格式和换行；PyInstaller archive 中 56 个 Relay 文件与当前源码逐字节一致。非法版本路径以及 `onedir + WriteChecksums` 均在构建前被拒绝。

首次构建的 EXE 验证已通过，但宿主 Windows PowerShell 无法找到 `Get-FileHash`；已改用 .NET SHA256 流式计算并重新执行完整 BAT 成功。生成新 EXE 前会清除同目录旧清单，防止失败重建留下过期校验文件。

原平铺输出未移动或删除。`packaging/` 及 BAT 仍按仓库现有 `.gitignore` 被忽略；本地修改和新版产物已存在，后端构建脚本及说明属于可跟踪改动。本次没有打开安装器 GUI、写入安装目标或发布安装包。
