@echo off
REM VMM-FRC Documentation Development Server
REM This script starts a local development server for documentation preview

setlocal enabledelayedexpansion

echo ============================================
echo VMM-FRC Documentation Server
echo ============================================
echo.

REM Change to docs directory
cd /d "%~dp0"

REM Check if node_modules exists
if not exist "node_modules" (
    echo [INFO] Installing npm dependencies...
    call npm install
    if errorlevel 1 (
        echo [ERROR] Failed to install npm dependencies
        exit /b 1
    )
)

echo Starting development server...
echo Press Ctrl+C to stop
echo.

call npm start

endlocal
