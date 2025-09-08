@echo off
setlocal EnableDelayedExpansion
echo Checking if Python is already installed...

:: Check if Python exists in the PATH
python --version >nul 2>&1
set PYTHON_VERSION=3.13.1
set PYTHON_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/python-%PYTHON_VERSION%-amd64.exe
set PYTHON_INSTALLER=python-%PYTHON_VERSION%-amd64.exe

:: If Python is installed
if %errorlevel% equ 0 (
    echo Python is already installed.
    echo Checking Python version...

    for /f "tokens=*" %%a in ('where python') do (
    set PYTHON_PATH1=%%a
    echo Python found at: %%a 
    for /f "tokens=2 delims= " %%i in ('python --version 2^>^&1') do set CURRENT_PYTHON_VERSION=%%i
    echo Current Python Version: !CURRENT_PYTHON_VERSION!
    )


    :: Check if the current version is different from the desired version
    if not !CURRENT_PYTHON_VERSION!==!PYTHON_VERSION! (
        echo Updating Python to version %PYTHON_VERSION%...
        :: Download and install the new version
        call :InstallPython
    ) else (
        echo Python is up to date.
    )

) else (
    echo Python is not installed.
    echo Installing Python version %PYTHON_VERSION%...
    call :InstallPython
)

:: Check if pip is installed
echo Checking if pip is installed...
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Pip not found. Installing pip...
    python -m ensurepip
    python -m pip install --upgrade pip
) else (
    echo Pip is already installed.
)

:: Install Python packages from requirements.txt
echo Installing Python packages from requirements.txt...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
echo Python and packages installed successfully!

:: Pause to view the output
pause

:: Function to download and install Python
:InstallPython
echo Downloading Python installer...
powershell -Command "Invoke-WebRequest -Uri '%PYTHON_URL%' -OutFile '%PYTHON_INSTALLER%'"

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
exit /b


