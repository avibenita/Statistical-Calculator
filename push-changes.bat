@echo off
REM ============================================
REM Git Push Script for Statistical-Calculator
REM ============================================

echo.
echo ========================================
echo Git Push Utility
echo ========================================
echo.

REM Navigate to the repository directory
cd /d "%~dp0"

REM Show current status
echo Checking repository status...
git status
echo.

REM Ask for commit message
set /p commit_msg="Enter commit message (or press Enter for default): "
if "%commit_msg%"=="" set commit_msg=Update files

echo.
echo Adding all changes...
git add -A

echo.
echo Committing with message: "%commit_msg%"
git commit -m "%commit_msg%"

echo.
echo Pushing to GitHub...
git push origin main

echo.
if %ERRORLEVEL% EQU 0 (
    echo ========================================
    echo SUCCESS: Changes pushed to GitHub!
    echo ========================================
) else (
    echo ========================================
    echo ERROR: Push failed! Check the error above.
    echo ========================================
)

echo.
pause

