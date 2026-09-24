# Run the Experiment 2 configs that produced the paper's core-reasoning table.
#
#   .\run_paper.ps1                  # the tagged-SPL run and the rule check
#   .\run_paper.ps1 -IncludeSummary  # also the untagged-summary control
#   .\run_paper.ps1 -EvaluateOnly    # score the outputs already on disk
#
# Credentials and the endpoint come from the package's `.env`.

param(
    [switch]$IncludeSummary,
    [switch]$EvaluateOnly
)

$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..\..\..")).Path
Set-Location $root

$names = @("full341_deepseek-v4-pro.json", "verify_rules_deepseek-v4-pro.json")
if ($IncludeSummary) { $names += "full341_deepseek-v4-pro_unstructured_summary.json" }

foreach ($name in $names) {
    $config = Join-Path $root "data\RQ2\settings\configs\$name"
    Write-Host "== $name"
    if (-not $EvaluateOnly) {
        python (Join-Path $root "code\RQ2\run.py") --config $config
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    }
    python (Join-Path $root "code\RQ2\evaluate.py") --config $config
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
exit 0
