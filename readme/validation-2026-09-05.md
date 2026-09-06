# 调度模式调整验证

本次以 `fa492da` 为旧版迁移基线，修改仓库源码，不更新用户目录中的已安装副本。

| 检查 | 结果 |
|---|---|
| Explore / Implementation / Budget 专用校验器 | PASS |
| 三套 Skill 的 `skill-creator quick_validate.py`（UTF-8） | PASS |
| Budget 安装、卸载和验证脚本语法 | PASS |
| 安装器配置检查 | PASS，3 个可安装模式 |
| 安装器 unittest | PASS，24 项；包含旧版切换、备份、回滚、自定义文件保护和路径边界 |
| 从基线重建四个旧包，在临时目录切换到 Explore | PASS，含旧 Led 与已移除的 Pair；旧目标移入备份 |
| 更正后从四个旧包切换到 Implementation | PASS，安装 1 个 Skill 和 9 个 Agent，旧目标移入备份 |
| 浏览器中英文 README | PASS，6 份正文及图片正常加载 |
| 浏览器界面 | PASS，3 个模式，无估算百分比，0 个页面错误，390px 无横向溢出 |
| 本地 Markdown 相对链接、Agent 名称、包内检索工具耦合 | PASS |

复现安装器测试：

```powershell
Push-Location tools/relay-installer
python -m unittest discover -s tests
Pop-Location
```

更名和模型赋值是两个独立维度：原 `gpt-5.6-sol` 配置改为 `gpt-6-astra`，保留原推理强度；Luna / Terra 配置不变。模型指导来源为 [OpenAI 官方模型指南](https://developers.openai.com/api/docs/guides/latest-model)，未据此推断调度质量提升比例。

新任务中的真实 Agent 发现、有效 sandbox 隔离、预算退出等调度行为前向测试，以及全 Agent 成本和质量对照实验均为 **NOT_EVALUATED**。Explore 的 [evaluation.md](../relay/explore-relay/skills/explore-relay/references/evaluation.md) 列出了待运行场景。静态校验和浏览器安装器检查不能替代这些证据。

未构建新的 Win64 EXE；现有产物需要重新打包才会包含本次修改。旧版自动识别仅覆盖迁移基线的文件指纹；其他版本或自定义内容应先人工核对。

用户更正后：删除 Pair（含临时名称 `plan-execute-relay`），恢复 Led 并改为 `implementation-relay`；九个角色保留 Luna / Terra Max 配置，父会话推荐 Astra。移除检索工具耦合、补充不确定性检查、证据版本、预算退出及写入交接检查。
