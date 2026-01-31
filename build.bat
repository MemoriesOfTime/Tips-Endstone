@echo off
setlocal enabledelayedexpansion
REM Tips-Endstone Build Script (Windows)
REM Uses uv for dependency management

echo [Build] Tips-Endstone Build Script
echo ==============================

REM Check if uv is installed
where uv >nul 2>nul
if !ERRORLEVEL! neq 0 (
    echo [Error] uv is not installed. Installing...
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    set "PATH=%USERPROFILE%\.local\bin;!PATH!"
)

echo.
echo [Info] uv version:
uv --version

REM Sync dependencies
echo.
echo [Info] Installing dependencies...
uv sync
if !ERRORLEVEL! neq 0 (
    echo [Error] Failed to install dependencies
    exit /b 1
)

REM Build wheel
echo.
echo [Info] Building wheel...
uv build --wheel
if !ERRORLEVEL! neq 0 (
    echo [Error] Build failed
    exit /b 1
)

echo.
echo [Done] Build complete!
echo [Info] Output: dist\
dir dist\*.whl 2>nul
