@echo off
REM =================================================================
REM N2P-CRM01 - ISP Management System
REM Automatic Installation Script for Windows
REM =================================================================
REM Author: Net2Point Engineering Team
REM Repository: https://github.com/ppez33/N2P-CRM01
REM License: Commercial
REM IMPORTANT: Run as Administrator!
REM =================================================================

setlocal enabledelayedexpansion

REM Configuration
set APP_NAME=N2P-CRM01
set VERSION=1.0.0
set INSTALL_DIR=C:\N2P-CRM01
set LOG_FILE=%TEMP%\n2p-install.log

REM Colors (using escape sequences for Windows 10+)
set "RED=[91m"
set "GREEN=[92m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "CYAN=[96m"
set "WHITE=[97m"
set "NC=[0m"

REM Check Administrator privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo %RED%[ERROR]%NC% This script must be run as Administrator!
    echo Right-click on install.bat and select "Run as administrator"
    pause
    exit /b 1
)

REM Print banner
cls
echo %CYAN%=================================================================
echo   _   _ ____  ____       ____ ____  __  __  ___  _ 
echo  ^| \ ^| ^|___ \^|  _ \     / ___^|  _ \^|  \/  ^|/ _ \/ ^|
echo  ^|  \^| ^| __) ^| ^|_) ^|   ^| ^|   ^| ^|_) ^| ^|\/^| ^| ^| ^| ^| ^|
echo  ^| ^|\  ^|/ __/^|  __/    ^| ^|___^|  _ ^^^| ^|  ^| ^| ^|_^| ^| ^|
echo  ^|_^| \_^|_____^|_^|        \____^|_^| \_\_^|  ^|_^|\___/^|_^|
echo.
echo         ISP Management System v%VERSION%
echo      Automatic Installation Script for Windows
echo =================================================================%NC%
echo.

echo %BLUE%[INFO]%NC% Starting N2P-CRM01 installation...
echo [%date% %time%] Starting installation > "%LOG_FILE%"

REM Check system requirements
echo %BLUE%[INFO]%NC% Checking system requirements...

REM Check Windows version
for /f "tokens=4-5 delims=. " %%i in ('ver') do set VERSION=%%i.%%j
if %VERSION% LSS 10.0 (
    echo %RED%[ERROR]%NC% Windows 10 or later required!
    pause
    exit /b 1
)

REM Check available disk space (requires at least 50GB)
for /f "tokens=3" %%a in ('dir /-c %SystemDrive%\ ^| find "bytes free"') do set FREESPACE=%%a
set /a FREESPACE_GB=FREESPACE/1073741824
if %FREESPACE_GB% LSS 50 (
    echo %YELLOW%[WARNING]%NC% Low disk space: %FREESPACE_GB%GB available, 50GB+ recommended
)

echo %GREEN%[SUCCESS]%NC% System requirements check passed

REM Create installation directory
echo %BLUE%[INFO]%NC% Creating installation directory...
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
echo %GREEN%[SUCCESS]%NC% Directory created: %INSTALL_DIR%

REM Check for existing installations
if exist "%INSTALL_DIR%\.git" (
    echo %BLUE%[INFO]%NC% Existing installation detected, updating...
    cd /d "%INSTALL_DIR%"
    git pull
) else (
    REM Download application
    echo %BLUE%[INFO]%NC% Downloading N2P-CRM01...
    
    REM Check if git is installed
    git --version >nul 2>&1
    if %errorLevel% neq 0 (
        echo %YELLOW%[WARNING]%NC% Git not found, installing Git for Windows...
        
        REM Download Git installer
        powershell -Command "Invoke-WebRequest -Uri 'https://github.com/git-for-windows/git/releases/latest/download/Git-2.42.0-64-bit.exe' -OutFile '%TEMP%\Git-installer.exe'"
        
        REM Install Git silently
        "%TEMP%\Git-installer.exe" /VERYSILENT /NORESTART
        
        REM Add Git to PATH
        setx PATH "%PATH%;C:\Program Files\Git\bin" /M
        set "PATH=%PATH%;C:\Program Files\Git\bin"
        
        echo %GREEN%[SUCCESS]%NC% Git installed
    )
    
    REM Clone repository
    cd /d "%INSTALL_DIR%"
    git clone https://github.com/ppez33/N2P-CRM01.git .
    
    if %errorLevel% neq 0 (
        echo %RED%[ERROR]%NC% Failed to download application
        pause
        exit /b 1
    )
)

echo %GREEN%[SUCCESS]%NC% Application downloaded

REM Check for Docker Desktop
echo %BLUE%[INFO]%NC% Checking for Docker Desktop...
docker --version >nul 2>&1
if %errorLevel% neq 0 (
    echo %YELLOW%[WARNING]%NC% Docker Desktop not found
    echo Installing Docker Desktop...
    
    REM Download Docker Desktop installer
    powershell -Command "Invoke-WebRequest -Uri 'https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe' -OutFile '%TEMP%\Docker-Desktop-Installer.exe'"
    
    REM Install Docker Desktop
    "%TEMP