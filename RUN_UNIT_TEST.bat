@echo off
chcp 65001 >nul
title PetCare PRO - Unit Test Automation (70 Test Cases)

echo ============================================================
echo   PETCARE PRO - UNIT TEST AUTOMATION (70 TEST CASES)
echo ============================================================
echo.

cd /d "%~dp0test-automation"
powershell -NoProfile -ExecutionPolicy Bypass -File "run_tests.ps1" -Suite "unit"

pause
