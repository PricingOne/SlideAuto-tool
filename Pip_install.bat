@echo off
echo Checking if Python is already installed...

:: Check if Python exists in the PATH
python --version >nul 2>&1
set PYTHON_VERSION=3.13.1  
set PYTHON_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/python-%PYTHON_VERSION%-amd64.exe
set PYTHON_INSTALLER=python-3.13.1-amd64.exe
if %errorlevel% equ 0 (
    echo Python is already installed.
    echo Checking if pip is installed...
    python -m pip --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo Pip not found. Installing pip...
        python -m ensurepip
        python -m pip install --upgrade pip
    ) else (
        echo Pip is already installed.
    )
) else (
    echo Python is not installed.

    :: Set the Python version and download URL
    set PYTHON_VERSION=3.13.1  
    set PYTHON_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/python-%PYTHON_VERSION%-amd64.exe
    set PYTHON_INSTALLER=python-3.13.1-amd64.exe
    echo Current Directory: %CD%\%PYTHON_INSTALLER%
    pushd "%~dp0"
    echo After Change: %CD% 
    :: Check if the installer already exists
    if not exist "%PYTHON_INSTALLER%" (
        echo Downloading Python installer...
        powershell -Command "Invoke-WebRequest -Uri 'www.python.org/ftp/python/3.13.1/python-3.13.1-amd64.exe' -OutFile 'python-3.13.1-amd64.exe'"
    ) else (
        echo Python installer already downloaded.
    )
    echo Current Directory22: %CD%\%PYTHON_INSTALLER%
    :: Check if the installer was downloaded successfully
    if exist "%PYTHON_INSTALLER%" (
        echo Installing Python...
        start "" "%~dp0%PYTHON_INSTALLER%" 
        echo Waiting for Python installation to complete...
        timeout /t 10
    ) else (
        echo Failed to download Python installer. Please check your internet connection.
        pause
        exit /b 1
    )
)

:: Verify Python installation
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Installing Python packages from requirements.txt...
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
    echo Python and requirements installed successfully!
) else (
    echo Python installation failed. Please install Python manually.
)

pause