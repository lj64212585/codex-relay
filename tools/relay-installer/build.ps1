[CmdletBinding()]
param(
    [ValidateSet("onedir", "onefile")]
    [string]$Mode = "onedir",
    [string]$ConfigPath,
    [string]$PythonExecutable,
    [string]$OutputDirectory,
    [switch]$RequireWin64
)

$ErrorActionPreference = "Stop"
$installerRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$repositoryRoot = [IO.Path]::GetFullPath((Join-Path $installerRoot "..\.."))
$resolvedConfigPath = if ([string]::IsNullOrWhiteSpace($ConfigPath)) {
    Join-Path $installerRoot "relay-installer.config.json"
} else {
    [IO.Path]::GetFullPath($ConfigPath)
}

if (-not (Test-Path -LiteralPath $resolvedConfigPath -PathType Leaf)) {
    throw "Config file was not found: $resolvedConfigPath"
}

if ([string]::IsNullOrWhiteSpace($PythonExecutable)) {
    if (-not [string]::IsNullOrWhiteSpace($env:RELAY_INSTALLER_PYTHON)) {
        $PythonExecutable = $env:RELAY_INSTALLER_PYTHON
    } else {
        $pythonCommand = Get-Command "python.exe" -ErrorAction SilentlyContinue
        if ($null -eq $pythonCommand) {
            throw "Python 3 was not found. Pass -PythonExecutable or set RELAY_INSTALLER_PYTHON."
        }
        $PythonExecutable = $pythonCommand.Source
    }
}

if ($RequireWin64) {
    if ([Environment]::OSVersion.Platform -ne [PlatformID]::Win32NT) {
        throw "The win64 package must be built on Windows."
    }

    & $PythonExecutable -c "import struct, sys; sys.exit(0 if sys.platform == 'win32' and struct.calcsize('P') * 8 == 64 else 1)"
    if ($LASTEXITCODE -ne 0) {
        throw "The selected Python runtime is not 64-bit Windows Python."
    }
}

& $PythonExecutable -B (Join-Path $installerRoot "relay_installer.py") --check --config $resolvedConfigPath
if ($LASTEXITCODE -ne 0) {
    throw "Relay Installer config validation failed with exit code $LASTEXITCODE."
}

& $PythonExecutable -c "import importlib.util, sys; sys.exit(0 if importlib.util.find_spec('PyInstaller') else 1)"
if ($LASTEXITCODE -ne 0) {
    throw "PyInstaller is not available in the selected Python environment."
}

$configDirectory = Split-Path -Parent $resolvedConfigPath
$bundleConfig = Get-Content -LiteralPath $resolvedConfigPath -Raw | ConvertFrom-Json
$configuredSourceRoot = [Environment]::ExpandEnvironmentVariables(
    [string]$bundleConfig.sourceRoot
)
if ([IO.Path]::IsPathRooted($configuredSourceRoot)) {
    $sourceRoot = [IO.Path]::GetFullPath($configuredSourceRoot)
} else {
    $sourceRoot = [IO.Path]::GetFullPath((Join-Path $configDirectory $configuredSourceRoot))
}

$buildRoot = Join-Path $installerRoot ".build"
$stagedConfigDirectory = Join-Path $buildRoot "package-config"
$workDirectory = Join-Path $buildRoot "pyinstaller"
$specDirectory = Join-Path $buildRoot "spec"
$distDirectory = if ([string]::IsNullOrWhiteSpace($OutputDirectory)) {
    Join-Path $installerRoot "dist"
} elseif ([IO.Path]::IsPathRooted($OutputDirectory)) {
    [IO.Path]::GetFullPath($OutputDirectory)
} else {
    [IO.Path]::GetFullPath((Join-Path $repositoryRoot $OutputDirectory))
}

if (Test-Path -LiteralPath $distDirectory -PathType Leaf) {
    throw "Output directory points to a file: $distDirectory"
}

$resolvedBuildRoot = [IO.Path]::GetFullPath($buildRoot)
$resolvedInstallerRoot = [IO.Path]::GetFullPath($installerRoot)
if (-not $resolvedBuildRoot.StartsWith(
    $resolvedInstallerRoot + [IO.Path]::DirectorySeparatorChar,
    [StringComparison]::OrdinalIgnoreCase
)) {
    throw "Refusing build directory outside installer root: $resolvedBuildRoot"
}

if (Test-Path -LiteralPath $buildRoot) {
    Remove-Item -LiteralPath $buildRoot -Recurse -Force
}
[void](New-Item -ItemType Directory -Path $stagedConfigDirectory -Force)
[void](New-Item -ItemType Directory -Path $workDirectory -Force)
[void](New-Item -ItemType Directory -Path $specDirectory -Force)
[void](New-Item -ItemType Directory -Path $distDirectory -Force)

$bundleConfig.sourceRoot = "relay-packages"
$dataArguments = [System.Collections.Generic.List[string]]::new()
$webSource = Join-Path $installerRoot "web"
$dataArguments.Add("--add-data")
$dataArguments.Add("$webSource;web")

foreach ($relay in $bundleConfig.relays) {
    $originalSourcePath = [string]$relay.sourcePath
    $relaySource = [IO.Path]::GetFullPath((Join-Path $sourceRoot $originalSourcePath))
    if (-not (Test-Path -LiteralPath $relaySource -PathType Container)) {
        throw "Relay source directory was not found: $relaySource"
    }
    $relay.sourcePath = [string]$relay.id
    $dataArguments.Add("--add-data")
    $dataArguments.Add("$relaySource;relay-packages\$($relay.id)")
}

$stagedConfigPath = Join-Path $stagedConfigDirectory "relay-installer.config.json"
$stagedConfigJson = $bundleConfig | ConvertTo-Json -Depth 12
[IO.File]::WriteAllText(
    $stagedConfigPath,
    $stagedConfigJson + [Environment]::NewLine,
    [Text.UTF8Encoding]::new($false)
)
$dataArguments.Add("--add-data")
$dataArguments.Add("$stagedConfigPath;.")

$modeArgument = if ($Mode -eq "onefile") { "--onefile" } else { "--onedir" }
$pyInstallerArguments = [System.Collections.Generic.List[string]]::new()
$pyInstallerArguments.Add("-m")
$pyInstallerArguments.Add("PyInstaller")
$pyInstallerArguments.Add("--noconfirm")
$pyInstallerArguments.Add("--clean")
$pyInstallerArguments.Add($modeArgument)
$pyInstallerArguments.Add("--name")
$pyInstallerArguments.Add("relay-installer")
$pyInstallerArguments.Add("--distpath")
$pyInstallerArguments.Add($distDirectory)
$pyInstallerArguments.Add("--workpath")
$pyInstallerArguments.Add($workDirectory)
$pyInstallerArguments.Add("--specpath")
$pyInstallerArguments.Add($specDirectory)
foreach ($argument in $dataArguments) {
    $pyInstallerArguments.Add($argument)
}
$pyInstallerArguments.Add((Join-Path $installerRoot "relay_installer.py"))

& $PythonExecutable @pyInstallerArguments
if ($LASTEXITCODE -ne 0) {
    throw "PyInstaller build failed with exit code $LASTEXITCODE."
}

$artifactPath = if ($Mode -eq "onefile") {
    Join-Path $distDirectory "relay-installer.exe"
} else {
    Join-Path $distDirectory "relay-installer"
}
if (-not (Test-Path -LiteralPath $artifactPath)) {
    throw "PyInstaller completed without the expected artifact: $artifactPath"
}

Write-Host "[OK] Relay Installer package created: $artifactPath"
Write-Host "[INFO] Bundled Relay source root: relay-packages"
Write-Host "[INFO] Repository root used for this build: $repositoryRoot"
