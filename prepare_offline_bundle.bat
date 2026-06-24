@echo off
setlocal
cd /d "%~dp0"

set "PYTHON_CMD="
where python >nul 2>&1
if not errorlevel 1 (
  set "PYTHON_CMD=python"
) else (
  where py >nul 2>&1
  if not errorlevel 1 (
    set "PYTHON_CMD=py -3"
  )
)

if not defined PYTHON_CMD (
  echo Fehler: Weder "python" noch "py" wurde gefunden.
  echo Bitte Python 3.10 oder neuer installieren und danach erneut starten.
  exit /b 1
)

if not exist "requirements.txt" (
  echo Fehler: Datei "requirements.txt" fehlt.
  exit /b 1
)

if not exist "wheelhouse" mkdir wheelhouse

%PYTHON_CMD% -m pip download --only-binary=:all: -r requirements.txt -d wheelhouse
if errorlevel 1 (
  echo Fehler: Wheels konnten nicht heruntergeladen werden.
  exit /b 1
)

echo Offline-Bundle erstellt: wheelhouse\
endlocal
