# Run AGMIS backend - MUST run from E:\Projects\agmis\backend
Set-Location $PSScriptRoot

if (Test-Path ".\venv\Scripts\Activate.ps1") {
    .\venv\Scripts\Activate.ps1
}

# Use port 8001 so we don't conflict with anything else on 8000
$port = 8001
Write-Host "Starting AGMIS at http://127.0.0.1:$port" -ForegroundColor Green
Write-Host "Open that URL in your browser. Press Ctrl+C to stop." -ForegroundColor Gray
uvicorn app.main:app --reload --host 127.0.0.1 --port $port
