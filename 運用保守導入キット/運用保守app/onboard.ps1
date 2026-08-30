[CmdletBinding()]
param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Arguments
)

$ErrorActionPreference = "Stop"
& python (Join-Path $PSScriptRoot "workspace_onboard.py") @Arguments
if ($LASTEXITCODE -ne 0) {
    throw "Workspace onboardingに失敗しました (exit code: $LASTEXITCODE)"
}
