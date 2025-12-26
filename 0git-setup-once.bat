@echo off
setlocal

REM ============================
REM CONFIGURATION (EDIT IF NEEDED)
REM ============================
set GITHUB_REPO_URL=https://github.com/avibenita/Statistical-Calculator.git
set BRANCH=main

REM ============================
REM GO TO THIS FOLDER
REM ============================
cd /d "%~dp0"

echo Initializing Git repository...
git init

echo.
echo Adding remote origin...
git remote add origin %GITHUB_REPO_URL%

echo.
echo Setting branch to %BRANCH%...
git branch -M %BRANCH%

echo.
echo Adding files...
git add .

echo.
echo First commit...
git commit -m "Initial commit of Statistico calculators"

echo.
echo Pushing to GitHub...
git push -u origin %BRANCH%

echo.
echo ======================================
echo Git setup complete. You can now use
echo push-changes.bat for future updates.
echo ======================================
pause
endlocal
