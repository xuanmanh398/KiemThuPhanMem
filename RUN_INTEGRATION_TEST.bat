@echo off
chcp 65001 >nul
title PetCare PRO - Integration Test Automation (70 Test Cases)

echo ============================================================
echo   PETCARE PRO - INTEGRATION TEST AUTOMATION (70 TEST CASES)
echo ============================================================
echo.

cd /d "%~dp0test-automation"
powershell -NoProfile -ExecutionPolicy Bypass -File "run_tests.ps1" -Suite "integration"

pause
