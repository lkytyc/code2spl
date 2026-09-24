# Run the Experiment 1 configs that produced the paper's ClassEval table.
#
#   .\run_paper.ps1                      # every model
#   .\run_paper.ps1 -Model claude-opus-5 # one model
#   .\run_paper.ps1 -EvaluateOnly        # score the outputs already on disk
#
# Credentials and the endpoint come from the package's `.env`.

param(
    [string]$Model = "",
    [switch]$EvaluateOnly
)

$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..\..\..")).Path
Set-Location $root

$configs = Get-ChildItem (Join-Path $root "data\RQ1\settings\configs") -Filter "full100_*.json" |
    Where-Object { $_.Name -notlike "*_spl_structure_ablation.json" } |
    Where-Object { $Model -eq "" -or $_.Name -eq "full100_$Model.json" } |
    Sort-Object Name

if (-not $configs) { throw "no config matched -Model '$Model'" }

foreach ($config in $configs) {
    Write-Host "== $($config.Name)"
    if (-not $EvaluateOnly) {
        python (Join-Path $root "code\RQ1\run.py") --config $config.FullName
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    }
    python (Join-Path $root "code\RQ1\evaluate.py") --config $config.FullName
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
exit 0
