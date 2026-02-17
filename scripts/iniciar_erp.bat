@echo off
setlocal

REM Diretório do script e raiz do projeto
set "SCRIPT_DIR=%~dp0"
for %%I in ("%SCRIPT_DIR%..") do set "PROJECT_ROOT=%%~fI"

cd /d "%PROJECT_ROOT%"

echo ==========================================
echo   ERP Desktop Offline - Inicializador
echo ==========================================

if not exist ".venv\Scripts\python.exe" (
  echo [1/4] Ambiente virtual nao encontrado. Criando .venv...
  python -m venv .venv
  if errorlevel 1 (
    echo ERRO: nao foi possivel criar o ambiente virtual.
    pause
    exit /b 1
  )

  echo [2/4] Instalando dependencias...
  call .venv\Scripts\activate
  python -m pip install --upgrade pip
  pip install -e .
  if errorlevel 1 (
    echo ERRO: falha ao instalar dependencias.
    pause
    exit /b 1
  )
) else (
  echo [1/4] Ambiente virtual encontrado.
  call .venv\Scripts\activate
)

echo [3/4] Aplicando migrations do banco...
alembic upgrade head
if errorlevel 1 (
  echo ERRO: falha ao aplicar migrations.
  pause
  exit /b 1
)

echo [4/4] Iniciando ERP...
python -m app.main

endlocal
