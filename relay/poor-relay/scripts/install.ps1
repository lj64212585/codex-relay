[CmdletBinding(SupportsShouldProcess = $true, ConfirmImpact = "Medium")]
param(
    [switch]$Force
)

$ErrorActionPreference = "Stop"
$packageRoot = Split-Path -Parent $PSScriptRoot
$sourceSkill = Join-Path $packageRoot "skills\poor-relay"
$sourceAgents = Join-Path $packageRoot "agents"
$agentNames = @(
    "tm_planner.toml",
    "tm_explorer.toml",
    "tm_executor.toml",
    "tm_reviewer.toml",
    "tm_integrator.toml"
)

& (Join-Path $PSScriptRoot "verify.ps1")

$userProfilePath = [Environment]::GetFolderPath("UserProfile")
if ([string]::IsNullOrWhiteSpace($userProfilePath)) {
    throw "Unable to resolve the current user profile."
}

$skillParent = Join-Path $userProfilePath ".agents\skills"
$agentParent = Join-Path $userProfilePath ".codex\agents"
$targetSkill = Join-Path $skillParent "poor-relay"
$targetAgents = @($agentNames | ForEach-Object { Join-Path $agentParent $_ })

function Assert-PathUnderRoot {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$Root
    )

    $fullPath = [IO.Path]::GetFullPath($Path)
    $fullRoot = [IO.Path]::GetFullPath($Root).TrimEnd(
        [IO.Path]::DirectorySeparatorChar,
        [IO.Path]::AltDirectorySeparatorChar
    ) + [IO.Path]::DirectorySeparatorChar

    if (-not $fullPath.StartsWith($fullRoot, [StringComparison]::OrdinalIgnoreCase)) {
        throw "Refusing path outside intended install root: $fullPath"
    }
}

Assert-PathUnderRoot -Path $targetSkill -Root $skillParent
foreach ($targetAgent in $targetAgents) {
    Assert-PathUnderRoot -Path $targetAgent -Root $agentParent
}

$conflicts = [System.Collections.Generic.List[string]]::new()
if (Test-Path -LiteralPath $targetSkill) {
    $conflicts.Add($targetSkill)
}
foreach ($targetAgent in $targetAgents) {
    if (Test-Path -LiteralPath $targetAgent) {
        $conflicts.Add($targetAgent)
    }
}

if ($conflicts.Count -gt 0 -and -not $Force) {
    throw (
        "Existing targets were found. Nothing was installed. " +
        "Inspect them first or rerun with -Force:" +
        [Environment]::NewLine +
        ($conflicts -join [Environment]::NewLine)
    )
}

if (-not $PSCmdlet.ShouldProcess($userProfilePath, "Install Poor Relay user Skill and Agent profiles")) {
    return
}

if ($Force) {
    if (Test-Path -LiteralPath $targetSkill) {
        Remove-Item -LiteralPath $targetSkill -Recurse -Force
    }
    foreach ($targetAgent in $targetAgents) {
        if (Test-Path -LiteralPath $targetAgent) {
            Remove-Item -LiteralPath $targetAgent -Force
        }
    }
}

[void](New-Item -ItemType Directory -Path $skillParent -Force)
[void](New-Item -ItemType Directory -Path $agentParent -Force)
Copy-Item -LiteralPath $sourceSkill -Destination $targetSkill -Recurse

foreach ($agentName in $agentNames) {
    Copy-Item -LiteralPath (Join-Path $sourceAgents $agentName) -Destination (Join-Path $agentParent $agentName)
}

Write-Host "[OK] Installed Skill: $targetSkill"
Write-Host "[OK] Installed Agent profiles: $($agentNames.Count)"
Write-Host "[NEXT] Start a new Codex task and verify runtime discovery and effective sandbox behavior."
