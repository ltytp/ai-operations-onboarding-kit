[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$PackagePath,
    [Parameter(Mandatory = $true)]
    [ValidateSet("SCANNER_VALIDATED", "OWNER_REVIEWED", "SECURITY_REVIEWED", "ONBOARDING_APPROVED")]
    [string]$State,
    [Parameter(Mandatory = $true)][string]$Actor,
    [Parameter(Mandatory = $true)]
    [ValidateSet("scanner-operator", "system-owner", "security-reviewer", "onboarding-approver")]
    [string]$Role,
    [Parameter(Mandatory = $true)][string]$Evidence
)

$ErrorActionPreference = "Stop"
& python (Join-Path $PSScriptRoot "diagnose.py") signoff `
    --package (Resolve-Path -LiteralPath $PackagePath).Path `
    --state $State `
    --actor $Actor `
    --role $Role `
    --evidence $Evidence
if ($LASTEXITCODE -ne 0) {
    throw "Sign-off更新に失敗しました (exit code: $LASTEXITCODE)"
}
