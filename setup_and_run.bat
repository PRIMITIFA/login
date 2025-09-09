@echo off
echo Setting up CS2 Tool Login Application...
echo.
echo Note: If running in PowerShell, use .\setup_and_run.bat instead of setup_and_run.bat
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Check for Visual C++ Redistributable
echo Checking for Visual C++ Redistributable...
reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\x64" /v Version >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: Visual C++ Redistributable might not be installed.
    echo This is required for PyQt6 to work properly.
    echo Please download and install from: https://aka.ms/vs/17/release/vc_redist.x64.exe
    set /p continue_setup=Do you want to continue with setup anyway? (Y/N): 
    if /i "%continue_setup%"=="N" (
        start https://aka.ms/vs/17/release/vc_redist.x64.exe
        echo Please run this setup again after installing Visual C++ Redistributable.
        pause
        exit /b 1
    )
    echo Continuing setup without Visual C++ Redistributable...
    echo.
)

REM Check if .env file exists
if not exist .env (
    echo Creating example .env file...
    copy .env.example .env
    echo Please edit the .env file with your Supabase credentials before running the application.
    notepad .env
)

REM Install dependencies
echo Installing dependencies...

REM Check if user wants to use specific versions to avoid DLL issues
set /p specific_versions=Do you want to install specific PyQt6 versions to avoid DLL issues? (Y/N): 
if /i "%specific_versions%"=="Y" (
    echo Installing specific versions from requirements-dev.txt...
    pip install -r requirements-dev.txt
) else (
    echo Installing dependencies from requirements.txt...
    pip install -r requirements.txt
)

echo Setup complete!
echo.

REM Ask if user wants to run the application
set /p run_app=Do you want to run the application now? (Y/N): 
if /i "%run_app%"=="Y" (
    echo Starting CS2 Tool Login Application...
    python main.py
    
    REM Check if application failed to start due to DLL error
    if %errorlevel% neq 0 (
        echo.
        echo ERROR: Application failed to start. This might be due to missing Visual C++ Redistributable.
        echo Please check the TROUBLESHOOTING.md file for solutions.
        start TROUBLESHOOTING.md
    )
) else (
    echo You can run the application later using 'python main.py' or by packaging it with 'pyinstaller cs2_login.spec'
    echo If you encounter any issues, please refer to TROUBLESHOOTING.md
)

pause