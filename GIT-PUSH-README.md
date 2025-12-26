# Git Push Mechanism for Statistical-Calculator

This repository includes automated scripts to make pushing updates to GitHub easier.

## 📁 Available Scripts

### 1. **push-changes.bat** (Recommended for Quick Use)
Simple batch file that guides you through pushing changes.

**How to use:**
1. Double-click `push-changes.bat`
2. Enter your commit message when prompted
3. The script will automatically:
   - Add all changes
   - Commit with your message
   - Push to GitHub

### 2. **push-changes.ps1** (Advanced PowerShell Version)
Enhanced PowerShell script with more features and better error handling.

**How to use:**

**Option A: Double-click** (will prompt for commit message)
```
Just double-click the file
```

**Option B: Command line with message**
```powershell
.\push-changes.ps1 -Message "Your commit message here"
```

**Option C: Show help**
```powershell
.\push-changes.ps1 -Help
```

**Features:**
- ✅ Color-coded output
- ✅ Automatic pull before push (avoids conflicts)
- ✅ Detailed status information
- ✅ Timestamps in default commit messages
- ✅ Force push option (use carefully!)

### 3. **git-setup.bat** (One-Time Setup)
Configure git settings for your repository.

**How to use:**
1. Run this once if you're setting up git for the first time
2. It will ask for your name and email if not already configured

## 🚀 Quick Start Guide

### First Time Setup:
1. Run `git-setup.bat` (only needed once)
2. Make your changes to any HTML files
3. Run `push-changes.bat` to push updates

### Regular Use:
1. Make changes to your calculator files
2. Double-click `push-changes.bat`
3. Enter a descriptive commit message
4. Done! Your changes are on GitHub

## 📝 Tips

- **Commit Message Ideas:**
  - "Fixed calculator bug in Normal Distribution"
  - "Added new Chi-Square calculator"
  - "Updated styling for all calculators"
  - "Fixed mobile responsiveness"

- **When to Push:**
  - After completing a feature
  - After fixing a bug
  - At the end of your work session
  - Before switching computers

## ⚠️ Important Notes

1. **Always review changes** before pushing
2. The scripts will show you what's being pushed
3. If push fails, check:
   - Internet connection
   - GitHub credentials
   - Merge conflicts

## 🔗 Repository

GitHub: https://github.com/avibenita/Statistical-Calculator

---

**Need Help?** Check git status with:
```bash
git status
```

**Undo last commit (before push):**
```bash
git reset --soft HEAD~1
```

