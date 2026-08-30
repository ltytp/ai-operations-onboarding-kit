[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$TargetPath,

    [string]$SystemName,

    [string]$OutputRoot = (Join-Path $PSScriptRoot "runs"),

    [string]$ProfilePath = (Join-Path $PSScriptRoot "profiles\default-profile.json")
)

$ErrorActionPreference = "Stop"
$resolvedTarget = (Resolve-Path -LiteralPath $TargetPath).Path
if ([string]::IsNullOrWhiteSpace($SystemName)) {
    $SystemName = Split-Path -Leaf $resolvedTarget
}
New-Item -ItemType Directory -Path $OutputRoot -Force | Out-Null

& python (Join-Path $PSScriptRoot "diagnose.py") scan `
    --target $resolvedTarget `
    --system-name $SystemName `
    --output-root $OutputRoot `
    --profile $ProfilePath

if ($LASTEXITCODE -ne 0) {
    throw "導入前診断に失敗しました (exit code: $LASTEXITCODE)"
}
