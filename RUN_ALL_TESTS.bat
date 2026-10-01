@echo off
chcp 65001 >nul
title PetCare PRO - Complete Full Test Automation (240 Test Cases)

echo ============================================================
echo   PETCARE PRO - FULL TEST AUTOMATION (240 TEST CASES)
echo   [70 Unit Tests + 70 Integration Tests + 100 System Tests]
echo ============================================================
echo.

cd /d "%~dp0test-automation"
powershell -NoProfile -ExecutionPolicy Bypass -File "run_tests.ps1" -Suite "all"

pause
