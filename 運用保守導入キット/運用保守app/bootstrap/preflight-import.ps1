[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$PackagePath,
    [string]$DiagnosisToolRoot,
    [string]$TargetPath
)

$ErrorActionPreference = "Stop"
$operationsRoot = (Resolve-Path -LiteralPath (Split-Path $PSScriptRoot -Parent)).Path
if ([string]::IsNullOrWhiteSpace($DiagnosisToolRoot)) {
    $DiagnosisToolRoot = Join-Path (Split-Path $operationsRoot -Parent) "導入前診断"
}
$arguments = @(
    (Join-Path $PSScriptRoot "bootstrap_import.py"), "preflight",
    "--package", (Resolve-Path -LiteralPath $PackagePath).Path,
    "--diagnosis-root", (Resolve-Path -LiteralPath $DiagnosisToolRoot).Path,
    "--operations-root", $operationsRoot
)
if (-not [string]::IsNullOrWhiteSpace($TargetPath)) {
    $arguments += @("--target", (Resolve-Path -LiteralPath $TargetPath).Path)
}
& python @arguments
if ($LASTEXITCODE -ne 0) {
    throw "Import事前検証に失敗しました (exit code: $LASTEXITCODE)"
}
