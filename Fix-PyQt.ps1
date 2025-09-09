# CS2 Tool Login - PyQt6 DLL Fix Utility (PowerShell Version)

Write-Host "CS2 Tool Login - PyQt6 DLL Fix Utility" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "This script will attempt to fix PyQt6 DLL loading issues by:"
Write-Host "1. Uninstalling current PyQt6 packages"
Write-Host "2. Installing specific compatible versions"
Write-Host "3. Checking for Visual C++ Redistributable"
Write-Host ""

$continue = Read-Host "Do you want to continue? (Y/N)"
if ($continue -ne "Y" -and $continue -ne "y") { exit }

Write-Host ""
Write-Host "Step 1: Uninstalling current PyQt6 packages..." -ForegroundColor Yellow
pip uninstall -y PyQt6 PyQt6-Qt6 PyQt6-sip

Write-Host ""
Write-Host "Step 2: Installing specific compatible versions..." -ForegroundColor Yellow
pip install PyQt6==6.4.0 PyQt6-Qt6==6.4.0 PyQt6-sip==13.4.0

Write-Host ""
Write-Host "Step 3: Checking for Visual C++ Redistributable..." -ForegroundColor Yellow

try {
    $vcRedist = Get-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\x64" -Name Version -ErrorAction Stop
    Write-Host "Visual C++ Redistributable is installed." -ForegroundColor Green
} catch {
    Write-Host "WARNING: Visual C++ Redistributable might not be installed." -ForegroundColor Red
    Write-Host "This is required for PyQt6 to work properly." -ForegroundColor Red
    Write-Host ""
    
    $installVcRedist = Read-Host "Do you want to download Visual C++ Redistributable now? (Y/N)"
    if ($installVcRedist -eq "Y" -or $installVcRedist -eq "y") {
        Start-Process "https://aka.ms/vs/17/release/vc_redist.x64.exe"
        Write-Host "Please run this application again after installing Visual C++ Redistributable." -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "Fix completed! Try running the application again with:" -ForegroundColor Green
Write-Host "python main.py" -ForegroundColor Cyan
Write-Host ""

Read-Host "Press Enter to exit"