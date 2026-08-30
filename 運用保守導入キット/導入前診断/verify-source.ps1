[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$PackagePath,
    [string]$TargetPath
)

$ErrorActionPreference = "Stop"
$arguments = @(
    (Join-Path $PSScriptRoot "diagnose.py"), "verify-source",
    "--package", (Resolve-Path -LiteralPath $PackagePath).Path
)
if (-not [string]::IsNullOrWhiteSpace($TargetPath)) {
    $arguments += @("--target", (Resolve-Path -LiteralPath $TargetPath).Path)
}
& python @arguments
if ($LASTEXITCODE -ne 0) {
    throw "Source fingerprintが一致しません、または検証に失敗しました (exit code: $LASTEXITCODE)"
}
