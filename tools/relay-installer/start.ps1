[CmdletBinding()]
param(
    [string]$ConfigPath,
    [int]$Port = 0,
    [switch]$NoBrowser,
    [switch]$VerboseHttp
)

$ErrorActionPreference = "Stop"
$installerRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$entryPoint = Join-Path $installerRoot "relay_installer.py"

$launchers = [System.Collections.Generic.List[object]]::new()
if (-not [string]::IsNullOrWhiteSpace($env:RELAY_INSTALLER_PYTHON)) {
    $launchers.Add([pscustomobject]@{
        Command = $env:RELAY_INSTALLER_PYTHON
        Prefix = @()
    })
}

$pyLauncher = Get-Command "py.exe" -ErrorAction SilentlyContinue
if ($null -ne $pyLauncher) {
    $launchers.Add([pscustomobject]@{
        Command = $pyLauncher.Source
        Prefix = @("-3")
    })
}

$pythonLauncher = Get-Command "python.exe" -ErrorAction SilentlyContinue
if ($null -ne $pythonLauncher) {
    $launchers.Add([pscustomobject]@{
        Command = $pythonLauncher.Source
        Prefix = @()
    })
}

if ($launchers.Count -eq 0) {
    throw "Python 3 was not found. Set RELAY_INSTALLER_PYTHON to a Python 3 executable."
}

$launcher = $launchers[0]
$launcherArguments = [System.Collections.Generic.List[string]]::new()
foreach ($argument in $launcher.Prefix) {
    $launcherArguments.Add($argument)
}
$launcherArguments.Add("-B")
$launcherArguments.Add("-X")
$launcherArguments.Add("utf8")
$launcherArguments.Add($entryPoint)
$launcherArguments.Add("--port")
$launcherArguments.Add([string]$Port)

if (-not [string]::IsNullOrWhiteSpace($ConfigPath)) {
    $launcherArguments.Add("--config")
    $launcherArguments.Add([IO.Path]::GetFullPath($ConfigPath))
}
if ($NoBrowser) {
    $launcherArguments.Add("--no-browser")
}
if ($VerboseHttp) {
    $launcherArguments.Add("--verbose")
}

& $launcher.Command @launcherArguments
exit $LASTEXITCODE
