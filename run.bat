@echo off
setlocal
set ROOT=%~dp0
cd /d "%ROOT%"

if exist ".venv\Scripts\activate.bat" (
  call ".venv\Scripts\activate.bat"
) else (
  echo Warning: .venv not found. Using system Python.
)

:: Navigate to backend and run the server
cd backend
uvicorn app.main:app --reload --host 127.0.0.1 --port 8001

endlocal
