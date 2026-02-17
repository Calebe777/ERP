@echo off
setlocal

REM Resolve a raiz do projeto mesmo quando executado por duplo clique
set "SCRIPT_DIR=%~dp0"
for %%I in ("%SCRIPT_DIR%..") do set "PROJECT_ROOT=%%~fI"

cd /d "%PROJECT_ROOT%"

if not exist ".venv\Scripts\python.exe" (
  echo Ambiente virtual nao encontrado. Executando setup inicial...
  call "%PROJECT_ROOT%\scripts\setup_venv.bat"
  if errorlevel 1 (
    echo ERRO: falha ao preparar o ambiente virtual.
    pause
    exit /b 1
  )
)

call .venv\Scripts\activate
if errorlevel 1 (
  echo ERRO: nao foi possivel ativar o ambiente virtual.
  pause
  exit /b 1
)

python -m app.main
if errorlevel 1 (
  echo ERRO: a aplicacao foi encerrada com falha.
  pause
  exit /b 1
)

endlocal
