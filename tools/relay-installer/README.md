# Relay Installer

这是一个配置驱动的 Relay 安装器。源码入口以本地网页方式运行；打包后的 Win64 EXE 会把同一套界面嵌入独立的 Windows 桌面窗口，不创建命令行窗口，也不打开系统浏览器。实际目录选择、冲突检查、备份和文件复制由只监听 127.0.0.1 的 Python 本地服务完成。关闭桌面窗口时，该服务会一并退出。支持中文与英文切换，并提供浅色、夜间两套主题。

## 直接运行

要求 Python 3.11 或更高版本，不需要安装第三方运行时依赖。

~~~powershell
.\tools\relay-installer\start.ps1
~~~

也可以直接运行入口：

~~~powershell
py -3 -B .\tools\relay-installer\relay_installer.py
~~~

只检查配置与所有 Relay 源文件：

~~~powershell
py -3 -B .\tools\relay-installer\relay_installer.py --check
~~~

## 界面与语言

- 桌面窗口在宽度至少 1100px、高度至少 700px 时使用居中的 16:9 工作台，最大尺寸为 1600 × 900；安装范围、Relay 类型、预检摘要与安装按钮会同时显示在一屏内。
- Relay 类型使用纵向排列的横向长条；每个名称下方显示“任务实现完美度 / 实现成本”相对估值，默认值与仓库根目录 README 的对比表一致。每条左侧的“详情”按钮独立于单选区域，打开与当前界面语言对应的 README 抽屉，不会改变已选择的 Relay。
- “安装范围”底部提供红色“移除当前目录的调度文件”按钮。安装器会先只读识别当前全局或项目目标中的已知 Relay，再通过确认框列出 Relay、状态、目标目录和具体路径；用户确认后才会移除。
- 较窄窗口、低高度窗口和移动设备自动切换为可滚动布局，不会产生横向溢出。
- 顶栏的“中文 / EN”切换会立即更新静态文案、Relay 说明、安装结果、预检状态和冲突确认框；没有已保存偏好时默认使用英文，手动选择后保存在当前浏览器中。
- 夜间模式选择同样会保存在当前浏览器中，并保留可见键盘焦点与系统“减少动态效果”偏好。

## 安装边界

- “全局”表示当前 Windows 用户目录，不是整台机器，也不会请求管理员权限。
- “项目”要求目标根目录已经存在。浏览按钮通过本地后端打开原生目录选择器。
- 每种 Relay 只写入配置声明的 Skill 目录和 Agent 文件。
- 安装前会扫描同一目标根目录。发现任意其他已配置 Relay 时，接口返回冲突，网页必须由用户明确选择“移除其他调度并安装”。
- 确认切换后，其他 Relay 会从活动位置移走，并保存在目标根目录的 .relay-installer-backups 目录中。新安装校验失败时会自动回滚。
- 单独移除调度时同样会先写入 .relay-installer-backups 可恢复备份；只移动能够归属到配置中 Relay 的 Skill 目录和 Agent 文件，不删除未知文件，也不清理 .agents/skills 或 .codex/agents 父目录。
- 如果同名 Agent 文件无法归属到任一已配置 Relay，安装器会停止，不会把自定义文件当作 Relay 自动删除。

多个调度 Skill 同时存在时，隐式路由规则可能竞争同一个任务；Poor Relay 与 Sol Pair Relay 还共享 tm_explorer、tm_planner、tm_executor 文件名，会进一步产生覆盖。因此本安装器把“同一范围只保留一种主调度”作为默认安全边界。

## 配置 Relay 路径

默认配置是 relay-installer.config.json；在本仓库中，它把 `sourceRoot` 指向根目录下的 `relay/`。sourceRoot 相对配置文件所在目录解析，每个 relay.sourcePath 再相对 sourceRoot 解析。Skill 和 Agent 的源路径相对该 Relay 目录解析，目标路径必须相对安装根目录，不能包含跳出根目录的路径。

启动时可换用另一份配置：

~~~powershell
.\tools\relay-installer\start.ps1 -ConfigPath D:\relay-bundle\installer.json
~~~

新增 Relay 时，在 relays 数组增加一项，并明确列出：

- 稳定且唯一的 id、界面名称、说明与标签；
- 必填的 metrics 对象，其中 taskPerfectionPercent 与 implementationCostPercent 必须是非负整数；二者以单个 Sol 独立完成为 100% 基准，因此允许高于 100；
- 可选的 translations 对象；每个语言条目必须同时提供 name、badge、description。当前界面的英文键为 en，缺少对应翻译时会回退到默认字段；
- 可选的 readmes 对象；语言键对应 Relay 根目录内的 README 相对路径，例如 zh-CN 指向 README.md、en 指向 README.en.md。路径不能跳出 Relay 目录；缺少当前语言条目时，该语言下的详情按钮会禁用；
- Relay 源目录；
- 一个 Skill 源目录及其安装目标；
- Agent 源目录、安装目标目录与允许复制的文件名清单。

安装器启动时会验证每个 Skill 都有 SKILL.md，且配置列出的 Agent 文件全部存在。路径和文件名不会由网页临时拼接。

## 打包

仓库级 Win64 打包入口会从 `packaging/version.txt` 读取版本号，把桌面窗口、网页工具、配置与当前配置列出的四套 Relay 全部固化进一个 EXE，并在构建后检查桌面入口、包内内容、内置版本和 Windows 版本元数据：

~~~powershell
python -m pip install -r .\tools\relay-installer\requirements-build.txt
.\packaging\build-win64.bat
~~~

版本文件只写一行 `MAJOR.MINOR.PATCH` 或 `MAJOR.MINOR.PATCH.BUILD`，例如 `1.0.0`；每段必须在 0—65535 之间。它以及 `packaging/` 下的其他内容都由该目录的 `.gitignore` 忽略，不进入 Git。产物名为 `packaging/out/win64/relay-installer-v<版本号>.exe`；版本同时显示在窗口标题与 Windows 文件属性中。

桌面窗口使用系统的 Microsoft Edge WebView2 Runtime。当前 Windows 10/11 通常已经包含该运行时；如果目标机器缺少它，程序会显示明确错误，而不是静默退出或改为打开浏览器。

需要直接控制底层构建时，可调用 build.ps1。它默认读取 `packaging/version.txt`，使用 onedir 并写入 `tools/relay-installer/dist`；也接受自定义版本文件、输出目录、Win64 检查与产物验证：

~~~powershell
.\tools\relay-installer\build.ps1
.\tools\relay-installer\build.ps1 -Mode onefile
.\tools\relay-installer\build.ps1 -Mode onefile -OutputDirectory packaging\out\win64 -RequireWin64 -VersionFile packaging\version.txt -VerifyPackage
~~~

构建脚本不会自动安装 PyInstaller 或 pywebview；二者都由 `requirements-build.txt` 声明。包内配置把 sourceRoot 改为 relay-packages，入口在冻结环境中会优先读取可执行文件旁的外部配置，其次读取包内配置。因此既可以使用固化进可执行文件的 Relay，也可以在 EXE 旁放置同名配置，改用外部 Relay 目录。

## 验证

运行标准库单元测试：

~~~powershell
$env:PYTHONPATH = (Resolve-Path .\tools\relay-installer)
py -3 -B -m unittest discover -s .\tools\relay-installer\tests -v
~~~

测试覆盖项目安装、同类型更新备份、不同 Relay 冲突确认、切换删除、独立移除的识别/备份/未知文件保护/空目标幂等、无共享文件时仍提示多调度冲突、未知同名文件保护、指标公开与校验、翻译配置公开与完整性校验、README 语言读取与本地图像内嵌，以及目标和 README 路径越界拒绝。
