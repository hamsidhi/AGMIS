@echo off
setlocal
set ROOT=%~dp0
cd /d "%ROOT%"
if exist ".venv\Scripts\activate.bat" (
  call ".venv\Scripts\activate.bat"
) else (
  echo Warning: .venv not found. Using system Python.
)
if exist "backend\requirements.txt" (
  python -m pip install -r backend\requirements.txt >NUL 2>&1
)
python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8001 %*
endlocal
