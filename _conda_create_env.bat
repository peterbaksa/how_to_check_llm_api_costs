@echo off
title Create Conda Environment

COLOR 6

REM Ensure conda is initialized
call conda init >nul 2>&1

REM Check if config file exists
if not exist _conda_env_name.ini (
    echo [ERROR] _conda_env_name.ini file not found!
    pause
    exit /b 1
)

REM Read environment name
set /p environment_name=<_conda_env_name.ini
echo [INFO] Environment name read from file: %environment_name%

REM Check if environment exists (exact match)
set "env_exists=0"
for /f "tokens=1" %%e in ('conda env list ^| findstr /R "^[a-zA-Z0-9\._-]*"') do (
    if /i "%%e"=="%environment_name%" (
        set "env_exists=1"
    )
)

if %env_exists%==1 (
    echo [INFO] Conda environment '%environment_name%' already exists.
    pause
    exit /b 0
)

REM Create new environment
echo [INFO] Creating conda environment '%environment_name%' with Python 3.12...
call conda create -n %environment_name% python=3.12 -y

if %errorlevel% neq 0 (
    echo [ERROR] Conda environment creation failed!
    pause
    exit /b 1
)

echo [SUCCESS] Conda environment '%environment_name%' successfully created.
pause
