@echo off
setlocal

REM ============================
REM CONFIG
REM ============================
set BRANCH=main
set COMMIT_MSG=Update calculators

REM ============================
REM GO TO SCRIPT FOLDER
REM ============================
cd /d "%~dp0"

echo ===============================
echo Statistico Git Push Script
echo ===============================
echo.

REM ============================
REM CHECK GIT
REM ============================
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed or not in PATH.
    pause
    exit /b 1
)

REM ============================
REM SHOW STATUS
REM ============================
git status
echo.

REM ============================
REM STAGE FILES
REM ============================
git add .

REM ============================
REM COMMIT IF NEEDED
REM ============================
git diff --cached --quiet
if %errorlevel%==0 (
    echo No changes to commit.
) else (
    git commit -m "%COMMIT_MSG%"
)

REM ============================
REM SYNC WITH GITHUB (IMPORTANT)
REM ============================
echo.
echo Pulling latest changes from GitHub...
git pull --rebase origin %BRANCH%
if errorlevel 1 (
    echo.
    echo ERROR: Pull failed. Resolve conflicts, then rerun.
    pause
    exit /b 1
)

REM ============================
REM PUSH
REM ============================
echo.
echo Pushing to GitHub...
git push origin %BRANCH%
if errorlevel 1 (
    echo.
    echo ERROR: Push failed.
    pause
    exit /b 1
)

echo.
echo Push completed successfully.
pause
endlocal
