[CmdletBinding()]
param(
    [switch]$AgentsOnly
)

$ErrorActionPreference = 'Stop'
$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent (Split-Path -Parent $scriptRoot)
$agentConfig = '$PROJECT_ROOT/data/RQ3/settings/configs/random218_full_semantic_summary/full_semantic_summary_218_config.json'
$evalConfig = '$PROJECT_ROOT/data/RQ3/settings/configs/random218_full_semantic_summary/full_semantic_summary_218_evaluation_config.json'
$runDir = Join-Path $scriptRoot 'results\reproduced_runs\semantic_matched\full_semantic_summary_218_agent_runs'
$logDir = Join-Path $runDir 'pipeline_logs'
New-Item -ItemType Directory -Force -Path $logDir | Out-Null

function Invoke-Logged([string]$label, [string[]]$command) {
    $stamp = Get-Date -Format 'yyyyMMdd_HHmmss'
    $log = Join-Path $logDir "$label`_$stamp.log"
    $stdout = "$log.stdout"
    $stderr = "$log.stderr"
    # Capture stderr as a file rather than merging it into the PowerShell
    # pipeline.  This avoids promotion of harmless Python warnings to
    # NativeCommandError while preserving both streams in the stage log.
    $process = Start-Process -FilePath $command[0] `
        -ArgumentList @($command[1..($command.Length - 1)]) `
        -WorkingDirectory $projectRoot -NoNewWindow -Wait -PassThru `
        -RedirectStandardOutput $stdout -RedirectStandardError $stderr
    if (Test-Path -LiteralPath $stdout) { Get-Content -LiteralPath $stdout | Tee-Object -FilePath $log }
    if (Test-Path -LiteralPath $stderr) { Get-Content -LiteralPath $stderr | Tee-Object -FilePath $log -Append }
    if ($process.ExitCode -ne 0) {
        throw "$label failed with exit code $($process.ExitCode). See $log"
    }
}

Set-Location $projectRoot
Invoke-Logged 'preflight' @('python', '$PROJECT_ROOT/code/RQ3/supplement_2026-09-16_full_semantic_218/prepare_full_semantic_summary_218.py')

& docker version --format '{{.Server.Version}}' | Out-Null
if ($LASTEXITCODE -ne 0) {
    $desktop = 'C:\Program Files\Docker\Docker\Docker Desktop.exe'
    if (Test-Path -LiteralPath $desktop) {
        Start-Process -FilePath $desktop -WindowStyle Hidden
    }
    $ready = $false
    foreach ($attempt in 1..24) {
        Start-Sleep -Seconds 5
        & docker version --format '{{.Server.Version}}' | Out-Null
        if ($LASTEXITCODE -eq 0) { $ready = $true; break }
    }
    if (-not $ready) { throw 'Docker Linux engine did not become ready.' }
}

$env:EXP6_FORCE_RESUME_EXISTING_CONDITIONS = '1'
Invoke-Logged 'agent_generation' @('python', '$PROJECT_ROOT/code/RQ3/supplement_2026-09-16_full_semantic_218/run_full_semantic_summary.py', '--config', $agentConfig)

$marker = [ordered]@{
    stage = 'agent_generation_complete'
    completed_at = (Get-Date).ToString('o')
    next_stage = if ($AgentsOnly) { 'manual_evaluation' } else { 'official_swebench_evaluation' }
} | ConvertTo-Json
Set-Content -LiteralPath (Join-Path $runDir 'AGENT_GENERATION_COMPLETE.json') -Value $marker -Encoding utf8

if ($AgentsOnly) { exit 0 }

# Stage 2 starts only after all 218 agent runs have returned.  It never shares
# Docker capacity with stage 1, so patch generation remains the fast first step.
Invoke-Logged 'official_evaluation' @('python', '$PROJECT_ROOT/code/RQ3/evaluate.py', '--config', $evalConfig)
Invoke-Logged 'comparison_summary' @('python', '$PROJECT_ROOT/code/RQ3/supplement_2026-09-16_full_semantic_218/summarize_full_semantic_summary_218.py', '--config', $evalConfig)

$finalMarker = [ordered]@{
    stage = 'pipeline_complete'
    completed_at = (Get-Date).ToString('o')
    results = 'ORIGINAL_VS_FULL_SEMANTIC_218_REPORT.md'
} | ConvertTo-Json
Set-Content -LiteralPath (Join-Path $runDir 'PIPELINE_COMPLETE.json') -Value $finalMarker -Encoding utf8
