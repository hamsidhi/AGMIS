$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

$VenvActivate = Join-Path $Root ".venv\Scripts\Activate.ps1"
if (Test-Path $VenvActivate) {
  & $VenvActivate
} else {
  Write-Host "Warning: .venv not found. Using system Python." -ForegroundColor Yellow
}

# Navigate to backend and run the server
Set-Location (Join-Path $Root "backend")
uvicorn app.main:app --reload --host 127.0.0.1 --port 8001
