[CmdletBinding()]
param(
    [ValidateSet("onedir", "onefile")]
    [string]$Mode = "onedir",
    [string]$ConfigPath,
    [string]$PythonExecutable,
    [string]$OutputDirectory,
    [switch]$RequireWin64,
    [string]$VersionFile,
    [switch]$VerifyPackage
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

$resolvedVersionPath = if ([string]::IsNullOrWhiteSpace($VersionFile)) {
    Join-Path $repositoryRoot "packaging\version.txt"
} elseif ([IO.Path]::IsPathRooted($VersionFile)) {
    [IO.Path]::GetFullPath($VersionFile)
} else {
    [IO.Path]::GetFullPath((Join-Path $repositoryRoot $VersionFile))
}
if (-not (Test-Path -LiteralPath $resolvedVersionPath -PathType Leaf)) {
    throw "Version file was not found: $resolvedVersionPath"
}

$packageVersion = [IO.File]::ReadAllText(
    $resolvedVersionPath,
    [Text.Encoding]::UTF8
).Trim()
$versionMatch = [regex]::Match(
    $packageVersion,
    "^(?<major>0|[1-9]\d*)\.(?<minor>0|[1-9]\d*)\.(?<patch>0|[1-9]\d*)(?:\.(?<build>0|[1-9]\d*))?$"
)
if (-not $versionMatch.Success) {
    throw (
        "Version must use MAJOR.MINOR.PATCH or MAJOR.MINOR.PATCH.BUILD " +
        "with non-negative integers: $packageVersion"
    )
}

try {
    $versionMajor = [int]$versionMatch.Groups["major"].Value
    $versionMinor = [int]$versionMatch.Groups["minor"].Value
    $versionPatch = [int]$versionMatch.Groups["patch"].Value
    $versionBuild = if ($versionMatch.Groups["build"].Success) {
        [int]$versionMatch.Groups["build"].Value
    } else {
        0
    }
} catch {
    throw "Version components must be integers from 0 through 65535: $packageVersion"
}

foreach ($component in @($versionMajor, $versionMinor, $versionPatch, $versionBuild)) {
    if ($component -gt 65535) {
        throw "Version components must be integers from 0 through 65535: $packageVersion"
    }
}

$fileVersion = "$versionMajor.$versionMinor.$versionPatch.$versionBuild"
$artifactBaseName = "relay-installer-v$packageVersion"

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

& $PythonExecutable -c "import importlib.util, sys; sys.exit(0 if importlib.util.find_spec('webview') else 1)"
if ($LASTEXITCODE -ne 0) {
    throw (
        "pywebview is not available in the selected Python environment. " +
        "Install the build requirements with: python -m pip install -r " +
        "tools\relay-installer\requirements-build.txt"
    )
}

$configDirectory = Split-Path -Parent $resolvedConfigPath
$configJson = [IO.File]::ReadAllText(
    $resolvedConfigPath,
    [Text.Encoding]::UTF8
)
$bundleConfig = $configJson | ConvertFrom-Json
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
$stagedMetadataDirectory = Join-Path $buildRoot "metadata"
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
[void](New-Item -ItemType Directory -Path $stagedMetadataDirectory -Force)
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

$stagedRuntimeVersionPath = Join-Path $stagedMetadataDirectory "relay-installer.version"
[IO.File]::WriteAllText(
    $stagedRuntimeVersionPath,
    $packageVersion + [Environment]::NewLine,
    [Text.UTF8Encoding]::new($false)
)
$dataArguments.Add("--add-data")
$dataArguments.Add("$stagedRuntimeVersionPath;.")

$pyInstallerVersionPath = Join-Path $stagedMetadataDirectory "relay-installer-version-info.txt"
$pyInstallerVersionText = @"
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=($versionMajor, $versionMinor, $versionPatch, $versionBuild),
    prodvers=($versionMajor, $versionMinor, $versionPatch, $versionBuild),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo([
      StringTable(
        '040904B0',
        [
          StringStruct('CompanyName', 'Codex Relay'),
          StringStruct('FileDescription', 'Relay Installer'),
          StringStruct('FileVersion', '$fileVersion'),
          StringStruct('InternalName', 'relay-installer'),
          StringStruct('OriginalFilename', '$artifactBaseName.exe'),
          StringStruct('ProductName', 'Relay Installer'),
          StringStruct('ProductVersion', '$packageVersion')
        ]
      )
    ]),
    VarFileInfo([VarStruct('Translation', [1033, 1200])])
  ]
)
"@
[IO.File]::WriteAllText(
    $pyInstallerVersionPath,
    $pyInstallerVersionText + [Environment]::NewLine,
    [Text.UTF8Encoding]::new($false)
)

$modeArgument = if ($Mode -eq "onefile") { "--onefile" } else { "--onedir" }
$pyInstallerArguments = [System.Collections.Generic.List[string]]::new()
$pyInstallerArguments.Add("-m")
$pyInstallerArguments.Add("PyInstaller")
$pyInstallerArguments.Add("--noconfirm")
$pyInstallerArguments.Add("--clean")
$pyInstallerArguments.Add($modeArgument)
$pyInstallerArguments.Add("--windowed")
$pyInstallerArguments.Add("--name")
$pyInstallerArguments.Add($artifactBaseName)
$pyInstallerArguments.Add("--version-file")
$pyInstallerArguments.Add($pyInstallerVersionPath)
$pyInstallerArguments.Add("--distpath")
$pyInstallerArguments.Add($distDirectory)
$pyInstallerArguments.Add("--workpath")
$pyInstallerArguments.Add($workDirectory)
$pyInstallerArguments.Add("--specpath")
$pyInstallerArguments.Add($specDirectory)
foreach ($argument in $dataArguments) {
    $pyInstallerArguments.Add($argument)
}
$pyInstallerArguments.Add((Join-Path $installerRoot "relay_installer_desktop.py"))

& $PythonExecutable @pyInstallerArguments
if ($LASTEXITCODE -ne 0) {
    throw "PyInstaller build failed with exit code $LASTEXITCODE."
}

$artifactPath = if ($Mode -eq "onefile") {
    Join-Path $distDirectory "$artifactBaseName.exe"
} else {
    Join-Path $distDirectory $artifactBaseName
}
if (-not (Test-Path -LiteralPath $artifactPath)) {
    throw "PyInstaller completed without the expected artifact: $artifactPath"
}

if ($VerifyPackage) {
    $executablePath = if ($Mode -eq "onefile") {
        $artifactPath
    } else {
        Join-Path $artifactPath "$artifactBaseName.exe"
    }
    if (-not (Test-Path -LiteralPath $executablePath -PathType Leaf)) {
        throw "Packaged executable was not found: $executablePath"
    }

    $checkProcess = Start-Process `
        -FilePath $executablePath `
        -ArgumentList @("--check") `
        -WindowStyle Hidden `
        -Wait `
        -PassThru
    if ($checkProcess.ExitCode -ne 0) {
        throw "Packaged executable content validation failed with exit code $($checkProcess.ExitCode)."
    }

    $versionReportPath = Join-Path $stagedMetadataDirectory "packaged-version.txt"
    $quotedVersionReportPath = '"' + $versionReportPath.Replace('"', '""') + '"'
    $versionProcess = Start-Process `
        -FilePath $executablePath `
        -ArgumentList @("--write-version", $quotedVersionReportPath) `
        -WindowStyle Hidden `
        -Wait `
        -PassThru
    if (
        $versionProcess.ExitCode -ne 0 -or
        -not (Test-Path -LiteralPath $versionReportPath -PathType Leaf)
    ) {
        throw "Packaged executable could not report its embedded version."
    }
    $reportedVersion = [IO.File]::ReadAllText(
        $versionReportPath,
        [Text.Encoding]::UTF8
    ).Trim()
    if ($reportedVersion -ne $packageVersion) {
        throw "Packaged executable did not report version $packageVersion."
    }

    $windowsVersion = (Get-Item -LiteralPath $executablePath).VersionInfo
    if (
        $windowsVersion.FileVersion -ne $fileVersion -or
        $windowsVersion.ProductVersion -ne $packageVersion
    ) {
        throw (
            "Packaged executable version metadata did not match. " +
            "FileVersion=$($windowsVersion.FileVersion), " +
            "ProductVersion=$($windowsVersion.ProductVersion)"
        )
    }
    Write-Host "[OK] Packaged desktop executable, content, and version metadata validated."
}

Write-Host "[OK] Relay Installer package created: $artifactPath"
Write-Host "[INFO] Package version: $packageVersion"
Write-Host "[INFO] Bundled Relay source root: relay-packages"
Write-Host "[INFO] Repository root used for this build: $repositoryRoot"
