@echo off
title DGTECH GESTAO - Sistema de Vendas

echo ========================================
echo   DGTECH GESTAO - Sistema de Vendas
echo ========================================
echo.

REM Executar o sistema diretamente
.venv\Scripts\python.exe main.py

REM Manter a janela aberta em caso de erro
if errorlevel 1 (
    echo.
    echo ERRO ao executar o sistema!
    pause
)
