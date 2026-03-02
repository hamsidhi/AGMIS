param(
  [switch]$NoReload,
  [int]$Port = 8001,
  [string]$BindHost = "127.0.0.1"
)

$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

$VenvActivate = Join-Path $Root ".venv\Scripts\Activate.ps1"
if (Test-Path $VenvActivate) {
  & $VenvActivate
} else {
  Write-Host "Warning: .venv not found. Using system Python." -ForegroundColor Yellow
}

if (Test-Path (Join-Path $Root "backend\requirements.txt")) {
  try {
    python -m pip install -r (Join-Path $Root "backend\requirements.txt") | Out-Null
  } catch {
    Write-Host "Warning: Failed to ensure requirements. Continuing..." -ForegroundColor Yellow
  }
}

$ReloadFlag = ""
if (-not $NoReload) { $ReloadFlag = "--reload" }

python -m uvicorn app.main:app --app-dir "$Root\backend" $ReloadFlag --host $BindHost --port $Port
