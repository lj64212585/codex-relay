[CmdletBinding()]
param(
    [switch]$Installed
)

$ErrorActionPreference = "Stop"
$packageRoot = Split-Path -Parent $PSScriptRoot
$userProfilePath = [Environment]::GetFolderPath("UserProfile")

if ([string]::IsNullOrWhiteSpace($userProfilePath)) {
    throw "Unable to resolve the current user profile."
}

if ($Installed) {
    $validatorPath = Join-Path $userProfilePath ".agents\skills\sol-pair-relay\scripts\validate_sol_pair_relay.py"
}
else {
    $validatorPath = Join-Path $packageRoot "skills\sol-pair-relay\scripts\validate_sol_pair_relay.py"
}

if (-not (Test-Path -LiteralPath $validatorPath -PathType Leaf)) {
    throw "Validator not found: $validatorPath"
}

$parseFailures = [System.Collections.Generic.List[string]]::new()
foreach ($scriptPath in Get-ChildItem -LiteralPath $PSScriptRoot -Filter "*.ps1" -File) {
    $tokens = $null
    $errors = $null
    [void][System.Management.Automation.Language.Parser]::ParseFile(
        $scriptPath.FullName,
        [ref]$tokens,
        [ref]$errors
    )
    foreach ($parseError in $errors) {
        $parseFailures.Add(("{0}: {1}" -f $scriptPath.Name, $parseError.Message))
    }
}

if ($parseFailures.Count -gt 0) {
    throw (
        "PowerShell syntax validation failed:" +
        [Environment]::NewLine +
        ($parseFailures -join [Environment]::NewLine)
    )
}

$pythonCommand = Get-Command "python" -ErrorAction SilentlyContinue
$pythonArguments = @("-X", "utf8", $validatorPath)

if ($null -eq $pythonCommand) {
    $pythonCommand = Get-Command "py" -ErrorAction SilentlyContinue
    $pythonArguments = @("-3", "-X", "utf8", $validatorPath)
}

if ($null -eq $pythonCommand) {
    throw "Python 3.11 or newer is required to parse Agent TOML files."
}

& $pythonCommand.Path @pythonArguments
if ($LASTEXITCODE -ne 0) {
    throw "Sol Pair Relay validation failed with exit code $LASTEXITCODE."
}

Write-Host "[OK] PowerShell scripts parsed successfully."
if ($Installed) {
    Write-Host "[OK] Installed Sol Pair Relay files passed static validation."
}
else {
    Write-Host "[OK] Sol Pair Relay source package passed static validation."
}
