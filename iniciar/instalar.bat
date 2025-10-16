@echo off
title Instalacao DGTECH GESTAO

echo =========================================================
echo   INSTALACAO - DGTECH GESTAO Sistema de Vendas
echo =========================================================
echo.
echo Este script ira:
echo 1. Criar ambiente virtual Python
echo 2. Instalar todas as dependencias
echo 3. Preparar o sistema para uso
echo.
echo =========================================================
echo.
pause

echo.
echo [1/3] Criando ambiente virtual...
python -m venv .venv
if errorlevel 1 (
    echo.
    echo ERRO: Nao foi possivel criar o ambiente virtual!
    echo Verifique se o Python esta instalado corretamente.
    pause
    exit /b 1
)
echo OK - Ambiente virtual criado!

echo.
echo [2/3] Ativando ambiente virtual...
call .venv\Scripts\activate.bat

echo.
echo [3/3] Instalando dependencias (pode levar alguns minutos)...
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ERRO: Falha ao instalar dependencias!
    pause
    exit /b 1
)

echo.
echo =========================================================
echo   INSTALACAO CONCLUIDA COM SUCESSO!
echo =========================================================
echo.
echo Para iniciar o sistema, execute:
echo   - DGTECH_GESTAO.bat (mais rapido)
echo   - iniciar.bat (com informacoes)
echo   - python main.py (manual)
echo.
echo =========================================================
pause
