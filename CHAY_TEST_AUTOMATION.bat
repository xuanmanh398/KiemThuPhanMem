@echo off
chcp 65001 >nul
title PetCare PRO - Test Automation Launcher

echo ============================================================
echo   PETCARE PRO - AUTOMATION TEST RUNNER (240 TEST CASES)
echo ============================================================
echo.
echo   [1] Chạy toàn bộ 240 Test Cases (Full Suite)
echo   [2] Chạy 70 Unit Test Cases (Kiểm thử Đơn vị)
echo   [3] Chạy 70 Integration Test Cases (Kiểm thử Tích hợp)
echo   [4] Chạy 100 System Test Cases (Kiểm thử Hệ thống E2E)
echo.
set /p opt="Nhap lua chon [1-4] (Mac dinh 1): "

if "%opt%"=="2" goto run_unit
if "%opt%"=="3" goto run_int
if "%opt%"=="4" goto run_sys
goto run_all

:run_unit
cd /d "%~dp0test-automation"
powershell -NoProfile -ExecutionPolicy Bypass -File "run_tests.ps1" -Suite "unit"
goto end

:run_int
cd /d "%~dp0test-automation"
powershell -NoProfile -ExecutionPolicy Bypass -File "run_tests.ps1" -Suite "integration"
goto end

:run_sys
cd /d "%~dp0test-automation"
powershell -NoProfile -ExecutionPolicy Bypass -File "run_tests.ps1" -Suite "system"
goto end

:run_all
cd /d "%~dp0test-automation"
powershell -NoProfile -ExecutionPolicy Bypass -File "run_tests.ps1" -Suite "all"
goto end

:end
pause
