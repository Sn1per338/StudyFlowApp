@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
  echo Fehler: .venv fehlt oder ist unvollstaendig. Bitte zuerst install.bat ausfuehren.
  exit /b 1
)

for %%F in ("app.py" "data\studiengang.csv" "data\studienmodule.csv") do (
  if not exist "%%~F" (
    echo Fehler: Datei "%%~F" fehlt.
    exit /b 1
  )
  type "%%~F" >nul 2>&1
  if errorlevel 1 (
    echo Fehler: Datei "%%~F" ist nicht lesbar.
    exit /b 1
  )
)

set "STREAMLIT_BROWSER_GATHER_USAGE_STATS=false"
".venv\Scripts\python.exe" -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501
endlocal
