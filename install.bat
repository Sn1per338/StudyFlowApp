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

%PYTHON_CMD% -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)"
if errorlevel 1 (
  echo Fehler: Python 3.10 oder neuer ist erforderlich.
  exit /b 1
)

for %%F in ("app.py" "requirements.txt" "data\studiengang.csv" "data\studienmodule.csv") do (
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

if not exist "wheelhouse" (
  echo Fehler: Ordner "wheelhouse" fehlt.
  echo Bitte auf einem Build-Rechner mit Internet zuerst prepare_offline_bundle.bat ausfuehren.
  exit /b 1
)

dir /b "wheelhouse\*.whl" >nul 2>&1
if errorlevel 1 (
  echo Fehler: Keine Wheel-Dateien im Ordner "wheelhouse" gefunden.
  echo Bitte auf einem Build-Rechner mit Internet zuerst prepare_offline_bundle.bat ausfuehren.
  exit /b 1
)

%PYTHON_CMD% -m venv .venv
if errorlevel 1 (
  echo Fehler: Virtuelle Umgebung konnte nicht erstellt werden.
  exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
  echo Fehler: Die Python-Umgebung wurde nicht korrekt erstellt.
  exit /b 1
)

.venv\Scripts\python.exe -m pip install --no-index --find-links wheelhouse -r requirements.txt
if errorlevel 1 (
  echo Fehler: Abhaengigkeiten konnten nicht installiert werden.
  echo Stelle sicher, dass wheelhouse fuer diese Python-Version und Architektur erstellt wurde.
  exit /b 1
)

echo Offline-Installation abgeschlossen.
endlocal
