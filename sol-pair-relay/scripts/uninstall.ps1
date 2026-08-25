[CmdletBinding(SupportsShouldProcess = $true, ConfirmImpact = "High")]
param()

$ErrorActionPreference = "Stop"
$userProfilePath = [Environment]::GetFolderPath("UserProfile")
if ([string]::IsNullOrWhiteSpace($userProfilePath)) {
    throw "Unable to resolve the current user profile."
}

$skillParent = Join-Path $userProfilePath ".agents\skills"
$agentParent = Join-Path $userProfilePath ".codex\agents"
$targetSkill = Join-Path $skillParent "sol-pair-relay"
$agentNames = @(
    "tm_explorer.toml",
    "tm_planner.toml",
    "tm_executor.toml"
)
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

foreach ($targetAgent in $targetAgents) {
    if (Test-Path -LiteralPath $targetAgent -PathType Leaf) {
        $profileText = Get-Content -LiteralPath $targetAgent -Raw
        if ($profileText -notmatch "Sol Pair Relay") {
            throw "Refusing to remove a same-named Agent that is not owned by Sol Pair Relay: $targetAgent"
        }
    }
}

$installedTargets = [System.Collections.Generic.List[string]]::new()
if (Test-Path -LiteralPath $targetSkill) {
    $installedTargets.Add($targetSkill)
}
foreach ($targetAgent in $targetAgents) {
    if (Test-Path -LiteralPath $targetAgent) {
        $installedTargets.Add($targetAgent)
    }
}

if ($installedTargets.Count -eq 0) {
    Write-Host "[OK] Sol Pair Relay is not installed for this user."
    return
}

if (-not $PSCmdlet.ShouldProcess(
    ($installedTargets -join ", "),
    "Remove only the Sol Pair Relay Skill and three owned Agent profiles"
)) {
    return
}

if (Test-Path -LiteralPath $targetSkill) {
    Remove-Item -LiteralPath $targetSkill -Recurse -Force
}
foreach ($targetAgent in $targetAgents) {
    if (Test-Path -LiteralPath $targetAgent) {
        Remove-Item -LiteralPath $targetAgent -Force
    }
}

Write-Host "[OK] Removed Sol Pair Relay user Skill and owned Agent profiles."
Write-Host "[NOTE] Parent .agents and .codex directories were preserved."
