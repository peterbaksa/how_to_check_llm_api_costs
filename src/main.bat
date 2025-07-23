@echo off
title OpenAI model pricing

COLOR E

pushd ..

set /p environment_name=<_conda_env_name.ini
echo Setting up environment: %environment_name%

call activate %environment_name%

if %errorlevel% neq 0 (
    echo.
    echo Error: Unable to run conda environment: %environment_name%.
    echo.
    pause
    goto end
)

echo Running Python script: src/main.py
python -m src.main

if %errorlevel% neq 0 (
    echo.
    echo Error: Python script ends with an error.
    echo.
    pause
    goto end
)

echo Skript successfully done.
pause

:end
