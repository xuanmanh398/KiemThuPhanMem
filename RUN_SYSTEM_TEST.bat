@echo off
chcp 65001 >nul
title PetCare PRO - System Test Automation (100 Test Cases)

echo ============================================================
echo   PETCARE PRO - SYSTEM / E2E TEST AUTOMATION (100 TEST CASES)
echo ============================================================
echo.

cd /d "%~dp0test-automation"
powershell -NoProfile -ExecutionPolicy Bypass -File "run_tests.ps1" -Suite "system"

pause
