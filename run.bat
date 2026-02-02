@echo off
setlocal enabledelayedexpansion
title Typer TUI Launcher

echo ========================================================
echo   Typer TUI Launcher
echo ========================================================

:: 1. Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in your PATH.
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

:: 2. Priority Check: Global Dependencies
:: Check if 'textual' is available in the current (system) environment.
python -c "import textual" >nul 2>&1
if %errorlevel% equ 0 (
    echo [INFO] Dependencies found globally. skipping virtual environment.
    goto :LAUNCH_APP
)

:: 3. Check for Virtual Environment (Fallback)
if exist venv\Scripts\activate.bat (
    echo [INFO] Dependencies not found globally. Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo [INFO] No 'venv' found and global deps missing. Will attempt install.
)

:: 4. Final Dependency Check & Install
python -c "import textual" >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Required dependency 'textual' not found.
    echo [INFO] Attempting to install from requirements.txt...
    if exist requirements.txt (
        pip install -r requirements.txt
        if !errorlevel! neq 0 (
            echo [ERROR] Failed to install dependencies.
            pause
            exit /b 1
        )
        echo [SUCCESS] Dependencies installed.
    ) else (
        echo [ERROR] 'requirements.txt' not found. Cannot install dependencies.
        pause
        exit /b 1
    )
)

:LAUNCH_APP
echo [INFO] Starting application...
echo --------------------------------------------------------
python main.py
set APP_EXIT_CODE=%errorlevel%

echo --------------------------------------------------------
if %APP_EXIT_CODE% neq 0 (
    echo [ERROR] Application exited with code %APP_EXIT_CODE%
    pause
) else (
    echo [SUCCESS] Application exited gracefully.
    timeout /t 3 >nul
)
