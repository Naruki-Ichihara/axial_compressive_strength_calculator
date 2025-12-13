@echo off
REM VMM-FRC Documentation Build Script
REM This script generates API documentation and builds the Docusaurus site

setlocal enabledelayedexpansion

echo ============================================
echo VMM-FRC Documentation Builder
echo ============================================
echo.

REM Change to docs directory
cd /d "%~dp0"

REM Check if pydoc-markdown is installed
python -c "import pydoc_markdown" 2>nul
if errorlevel 1 (
    echo [INFO] Installing pydoc-markdown...
    pip install pydoc-markdown[novella]
    if errorlevel 1 (
        echo [ERROR] Failed to install pydoc-markdown
        exit /b 1
    )
)

REM Check if node_modules exists
if not exist "node_modules" (
    echo [INFO] Installing npm dependencies...
    call npm install
    if errorlevel 1 (
        echo [ERROR] Failed to install npm dependencies
        exit /b 1
    )
)

REM Generate API documentation
echo.
echo [STEP 1] Generating API documentation from Python docstrings...
echo.

REM Clean old generated API docs
if exist "docs\api\reference" (
    echo Cleaning old API reference...
    rmdir /s /q "docs\api\reference"
)

REM Run pydoc-markdown
python -m pydoc_markdown
if errorlevel 1 (
    echo [WARNING] pydoc-markdown encountered issues, continuing...
)

echo.
echo [STEP 2] Building Docusaurus site...
echo.

REM Build the site
call npm run build
if errorlevel 1 (
    echo [ERROR] Failed to build Docusaurus site
    exit /b 1
)

echo.
echo ============================================
echo Documentation build complete!
echo Output: docs\build\
echo ============================================
echo.
echo To preview locally, run: npm start
echo.

endlocal
