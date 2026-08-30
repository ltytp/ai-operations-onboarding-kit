[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$PackagePath,
    [Parameter(Mandatory = $true)][string]$Id,
    [Parameter(Mandatory = $true)][string]$Title,
    [Parameter(Mandatory = $true)][string]$EvidencePath,
    [Parameter(Mandatory = $true)][string[]]$AcceptanceCriteria,
    [Parameter(Mandatory = $true)][string]$Actor
)

$ErrorActionPreference = "Stop"
$arguments = @(
    (Join-Path $PSScriptRoot "diagnose.py"), "set-golden",
    "--package", (Resolve-Path -LiteralPath $PackagePath).Path,
    "--id", $Id,
    "--title", $Title,
    "--evidence-path", $EvidencePath,
    "--actor", $Actor
)
foreach ($criterion in $AcceptanceCriteria) {
    $arguments += @("--criterion", $criterion)
}
& python @arguments
if ($LASTEXITCODE -ne 0) {
    throw "Golden Work Item更新に失敗しました (exit code: $LASTEXITCODE)"
}
