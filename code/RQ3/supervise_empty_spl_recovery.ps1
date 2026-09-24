param(
    [Parameter(Mandatory = $true)]
    [string]$RunRoot,

    [Parameter(Mandatory = $true)]
    [string]$PlanPath,

    [string]$PythonPath = "C:\conda\python.exe",

    [int]$PollSeconds = 1800,

    [int]$MaxRestarts = 10
)

$ErrorActionPreference = "SilentlyContinue"
$runPath = (Resolve-Path -LiteralPath $RunRoot).Path
$plan = (Resolve-Path -LiteralPath $PlanPath).Path
$workspace = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "../..")).Path
$recoveryScript = Join-Path $workspace "$PROJECT_ROOT/code/RQ3/recover_empty_spl_wave.py"
$workPath = Join-Path $runPath "plan/empty_spl_recovery_20260730"
$statePath = Join-Path $workPath "state.json"
$stopPath = Join-Path $runPath "plan/execution/STOP_REQUESTED"
$supervisorLog = Join-Path $workPath "supervisor_status.jsonl"
$restartCount = 0

New-Item -ItemType Directory -Force -Path $workPath | Out-Null

function Write-Status([string]$Event, $RecoveryProcess = $null) {
    $state = $null
    if (Test-Path -LiteralPath $statePath) {
        try { $state = Get-Content -LiteralPath $statePath -Raw | ConvertFrom-Json } catch {}
    }
    $entry = [ordered]@{
        observed_at = (Get-Date).ToString("o")
        event = $Event
        recovery_pid = if ($RecoveryProcess) { $RecoveryProcess.ProcessId } else { $null }
        restart_count = $restartCount
        prepared = if ($state -and $state.prepared) { @($state.prepared.PSObject.Properties).Count } else { 0 }
        rerun = if ($state -and $state.rerun) { @($state.rerun.PSObject.Properties).Count } else { 0 }
        evaluated = if ($state -and $state.evaluated) { @($state.evaluated.PSObject.Properties).Count } else { 0 }
        complete = if ($state) { [bool]$state.complete } else { $false }
    }
    ($entry | ConvertTo-Json -Compress) | Add-Content -LiteralPath $supervisorLog -Encoding UTF8
}

function Get-RecoveryProcess {
    @(
        Get-CimInstance Win32_Process |
            Where-Object {
                $_.CommandLine -like "*recover_empty_spl_wave.py*" -and
                $_.CommandLine -like "*$plan*"
            }
    ) | Select-Object -First 1
}

while ($true) {
    if (Test-Path -LiteralPath $stopPath) {
        Write-Status "stop_requested"
        exit 0
    }

    if (Test-Path -LiteralPath $statePath) {
        try {
            $state = Get-Content -LiteralPath $statePath -Raw | ConvertFrom-Json
            if ($state.complete) {
                Write-Status "complete"
                exit 0
            }
        } catch {}
    }

    $recovery = Get-RecoveryProcess
    if ($recovery) {
        Write-Status "recovery_alive" $recovery
        Start-Sleep -Seconds $PollSeconds
        continue
    }

    docker info *> $null
    if ($LASTEXITCODE -ne 0) {
        Write-Status "docker_unavailable"
        Start-Sleep -Seconds $PollSeconds
        continue
    }

    if ($restartCount -ge $MaxRestarts) {
        Write-Status "restart_limit_reached"
        exit 2
    }

    $restartCount += 1
    $stamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $stdout = Join-Path $workPath "launcher.$stamp.stdout.log"
    $stderr = Join-Path $workPath "launcher.$stamp.stderr.log"
    $arguments = @(
        "-u",
        $recoveryScript,
        "--plan", $plan,
        "--prepare-workers", "4",
        "--prepare-attempts", "3",
        "--prepare-timeout-seconds", "21600",
        "--pull-attempts", "3",
        "--min-free-gb", "80",
        "--min-free-memory-gb", "2.0"
    )
    $started = Start-Process -FilePath $PythonPath -ArgumentList $arguments `
        -WorkingDirectory $workspace -WindowStyle Hidden `
        -RedirectStandardOutput $stdout -RedirectStandardError $stderr -PassThru
    Write-Status "recovery_started" $started
    Start-Sleep -Seconds $PollSeconds
}
