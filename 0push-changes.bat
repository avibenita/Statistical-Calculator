@echo off
setlocal

REM ============================
REM Configuration
REM ============================
set REPO_BRANCH=main
set COMMIT_MSG=Update calculators

REM ============================
REM Go to script directory
REM ============================
cd /d "%~dp0"

echo.
echo ============================
echo Statistico Git Push Script
echo ============================
echo.

REM ============================
REM Check git availability
REM ============================
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed or not in PATH.
    pause
    exit /b 1
)

REM ============================
REM Show status
REM ============================
echo Current git status:
git status
echo.

REM ============================
REM Stage changes
REM ============================
echo Adding files...
git add *.html
git add *.bat

REM ============================
REM Commit (only if needed)
REM ============================
git diff --cached --quiet
if %errorlevel%==0 (
    echo No changes to commit.
) else (
    echo Committing changes...
    git commit -m "%COMMIT_MSG%"
)

REM ============================
REM Push to GitHub
REM ============================
echo.
echo Pushing to GitHub...
git push origin %REPO_BRANCH%

REM ============================
REM Done
REM ============================
echo.
echo Push completed.
pause
endlocal
