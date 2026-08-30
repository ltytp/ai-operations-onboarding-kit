[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$PackagePath
)

$ErrorActionPreference = "Stop"
& python (Join-Path $PSScriptRoot "diagnose.py") validate --package (Resolve-Path -LiteralPath $PackagePath).Path
if ($LASTEXITCODE -ne 0) {
    throw "Package検証に失敗しました (exit code: $LASTEXITCODE)"
}
