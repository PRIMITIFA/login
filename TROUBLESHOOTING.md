# Troubleshooting Guide

## PyQt6 DLL Loading Error

If you encounter the following error when running the application:

```
ImportError: DLL load failed while importing QtCore: The specified procedure could not be found.
```

This is typically caused by missing or incompatible Visual C++ Redistributable packages. Follow these steps to resolve the issue:

### Solution 1: Install Visual C++ Redistributable

1. Download and install the latest Visual C++ Redistributable for Visual Studio 2019 from the official Microsoft website:
   - [Microsoft Visual C++ Redistributable for Visual Studio 2019](https://aka.ms/vs/17/release/vc_redist.x64.exe) (64-bit)
   - [Microsoft Visual C++ Redistributable for Visual Studio 2019](https://aka.ms/vs/17/release/vc_redist.x86.exe) (32-bit)

2. Restart your computer after installation

3. Try running the application again

### Solution 2: Use the Fix Script

We've included a fix script that will automatically reinstall PyQt6 with compatible versions without requiring PowerShell execution policy changes:

```bash
RunPyQtFix.bat
```

This script will:
1. Uninstall current PyQt6 packages
2. Install specific compatible versions
3. Check for Visual C++ Redistributable and provide download link if needed

### Solution 3: Manually Reinstall PyQt6

If the fix script doesn't work, try manually reinstalling PyQt6 with specific versions:

```bash
pip uninstall PyQt6 PyQt6-Qt6 PyQt6-sip
pip install PyQt6==6.4.0 PyQt6-Qt6==6.4.0 PyQt6-sip==13.4.0
```

### Solution 4: Use a Virtual Environment

Create a clean virtual environment and install dependencies there:

```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Solution 5: Check Python Architecture

Ensure you're using the correct Python architecture (32-bit or 64-bit) that matches your system:

```bash
python -c "import platform; print(platform.architecture())"
```

If you're using 32-bit Python on a 64-bit system, consider switching to 64-bit Python.

## Other Common Issues

### Supabase Connection Issues

If you encounter issues connecting to Supabase:

1. Verify your `.env` file contains the correct Supabase URL and key
2. Check your internet connection
3. Ensure your Supabase project is active and the service is running

### Application Crashes on Startup

If the application crashes immediately:

1. Run from the command line to see error messages
2. Check if all dependencies are installed correctly
3. Verify that the required assets exist in the correct directories

### Packaging Issues

If you encounter issues when packaging with PyInstaller:

1. Make sure you have the latest version of PyInstaller
2. Try using the `--clean` flag to clear PyInstaller cache
3. Check if all dependencies are correctly specified in the spec file

```bash
pip install --upgrade pyinstaller
pyinstaller --clean cs2_login.spec
```

If you continue to experience issues, please open an issue on the project repository with detailed information about your system and the exact error messages you're encountering.