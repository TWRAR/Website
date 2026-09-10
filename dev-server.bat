@echo off
REM TWRAR Website - Local dev server (Windows)
REM Usage: dev-server.bat [port] [--no-dev-mode]
REM   port            default: 8000
REM   --no-dev-mode   serve pages untouched, matching production
REM
REM DEV_MODE is forced ON for every run of this script - every page gets a
REM dev banner injected so it's obvious you're looking at a local build.
REM Pass --no-dev-mode to test the site as it behaves in production instead.
setlocal
set "DIR=%~dp0"

where python >nul 2>nul
if errorlevel 1 (
    where py >nul 2>nul
    if errorlevel 1 (
        echo Python 3 is required to run dev-server.py
        exit /b 1
    )
    py "%DIR%dev-server.py" %*
) else (
    python "%DIR%dev-server.py" %*
)
