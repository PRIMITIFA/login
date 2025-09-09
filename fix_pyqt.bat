@echo off
echo CS2 Tool Login - PyQt6 DLL Fix Utility
echo =====================================
echo.

echo This script will attempt to fix PyQt6 DLL loading issues by:
echo 1. Uninstalling current PyQt6 packages
echo 2. Installing specific compatible versions
echo 3. Checking for Visual C++ Redistributable
echo.

set /p continue=Do you want to continue? (Y/N): 
if /i "%continue%" NEQ "Y" exit /b

echo.
echo Step 1: Uninstalling current PyQt6 packages...
pip uninstall -y PyQt6 PyQt6-Qt6 PyQt6-sip

echo.
echo Step 2: Installing specific compatible versions...
pip install PyQt6==6.4.0 PyQt6-Qt6==6.4.0 PyQt6-sip==13.4.0

echo.
echo Step 3: Checking for Visual C++ Redistributable...
reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\x64" /v Version >nul 2>&1
if %errorlevel% equ 0 (
    echo Visual C++ Redistributable is installed.
) else (
    reg query "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\VisualStudio\14.0\VC\Runtimes\x64" /v Version >nul 2>&1
    if %errorlevel% equ 0 (
        echo Visual C++ Redistributable is installed.
    ) else (
        echo WARNING: Visual C++ Redistributable might not be installed.
        echo This is required for PyQt6 to work properly.
        echo.
        set /p install_vcredist=Do you want to download Visual C++ Redistributable now? (Y/N): 
        if /i "%install_vcredist%"=="Y" (
            start https://aka.ms/vs/17/release/vc_redist.x64.exe
            echo Please run this application again after installing Visual C++ Redistributable.
        )
    )
)

echo.
echo Fix completed! Try running the application again with:
echo python main.py
echo.

pause