param(
    [ValidateSet("flash", "pro", "both")]
    [string]$Model = "both",
    [switch]$SkipPrepare,
    [switch]$SkipRun
)

$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..\..\..")).Path
Set-Location $root
$configs = @()
if ($Model -in @("flash", "both")) {
    $configs += "$PROJECT_ROOT/data/RQ1/settings/configs/full100_deepseek-v4-flash.json"
}
if ($Model -in @("pro", "both")) {
    $configs += "$PROJECT_ROOT/data/RQ1/settings/configs/full100_deepseek-v4-pro.json"
}
foreach ($config in $configs) {
    $arguments = @(
        "$PROJECT_ROOT/code/RQ1/scripts/run_full100_model.py",
        "--config", $config
    )
    if ($SkipPrepare) { $arguments += "--skip-prepare" }
    if ($SkipRun) { $arguments += "--skip-run" }
    python @arguments
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
python $PROJECT_ROOT/code/RQ1/scripts/summarize_full100_models.py
exit $LASTEXITCODE
