@echo off
setlocal

REM Check if Python 3.12.7 is installed using py launcher
for /f "tokens=2 delims= " %%i in ('py -V 2^>nul') do (
    if "%%i"=="3.12.7" (
        echo Python 3.12.7 is already installed.
        goto install_libraries
    )
)

echo Python 3.12.7 not found. Downloading and installing...

REM Set download URL for Python 3.12.7
set PYTHON_VERSION=3.12.7
set PYTHON_INSTALLER=python-%PYTHON_VERSION%-amd64.exe
set DOWNLOAD_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/%PYTHON_INSTALLER%

REM Use PowerShell to download the installer
echo Downloading Python %PYTHON_VERSION% installer with PowerShell...
powershell -Command "Invoke-WebRequest -Uri '%DOWNLOAD_URL%' -OutFile '%PYTHON_INSTALLER%'"

REM Check if download was successful
if not exist %PYTHON_INSTALLER% (
    echo Failed to download Python installer. Exiting...
    exit /b 1
)

REM Silent install Python
echo Installing Python %PYTHON_VERSION%...
start /wait "" %PYTHON_INSTALLER% /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

REM Verify installation
for /f "tokens=2 delims= " %%i in ('py -V 2^>nul') do (
    if "%%i"=="3.12.7" (
        echo Python 3.12.7 successfully installed.
        goto install_libraries
    )
)

echo Python installation failed.
exit /b 1

:install_libraries
echo Installing required Python libraries...

REM Upgrade pip to the latest version
py -m ensurepip --upgrade
py -m pip install --upgrade pip

REM List of libraries to install (add or remove libraries as needed)
set LIBRARIES=clipboard pyinstaller

REM Check if libraries are installed, and install if not
for %%L in (%LIBRARIES%) do (
    py -m pip show %%L >nul 2>&1
    if errorlevel 1 (
        echo %%L is not installed. Installing %%L...
        py -m pip install %%L
    ) else (
        echo %%L is already installed.
    )
)

echo Python libraries installation complete.
exit /b 0
