@echo off
REM ============================================
REM Git Initial Setup Script
REM Run this once to configure git for your repository
REM ============================================

echo.
echo ========================================
echo Git Setup Utility
echo ========================================
echo.

REM Navigate to the repository directory
cd /d "%~dp0"

echo This script will help you set up git for this repository.
echo.

REM Check if git is installed
git --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Git is not installed!
    echo Please install Git from https://git-scm.com/
    pause
    exit /b 1
)

REM Set up user name and email if not already configured
echo Checking git configuration...
echo.

for /f "delims=" %%i in ('git config --global user.name 2^>nul') do set git_name=%%i
for /f "delims=" %%i in ('git config --global user.email 2^>nul') do set git_email=%%i

if "%git_name%"=="" (
    set /p git_name="Enter your name: "
    git config --global user.name "%git_name%"
    echo User name set to: %git_name%
) else (
    echo User name already set: %git_name%
)

if "%git_email%"=="" (
    set /p git_email="Enter your email: "
    git config --global user.email "%git_email%"
    echo Email set to: %git_email%
) else (
    echo Email already set: %git_email%
)

echo.
echo Checking remote repository...
git remote -v

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo You can now use push-changes.bat to push updates.
echo.

pause

