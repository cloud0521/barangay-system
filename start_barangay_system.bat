@echo off
REM Batch file to start the Barangay Django System
echo Starting Barangay System Launcher...
echo.

REM --- IMPORTANT: Set your project parent path here ---
SET "PROJECT_PARENT_PATH=C:\Users\cloud\"
echo Project Parent Path set to: "%PROJECT_PARENT_PATH%"

REM --- (Optional) Set your virtual environment activation script path ---
REM Make sure it's the activate.bat inside the "Scripts" folder of your venv.
REM Example: SET "VENV_ACTIVATE_PATH=%PROJECT_PARENT_PATH%\brgy\myenv\Scripts\activate.bat"
REM SET "VENV_ACTIVATE_PATH=%PROJECT_PARENT_PATH%\brgy\venv\Scripts\activate.bat"

REM --- Verify project directory exists ---
IF NOT EXIST "%PROJECT_PARENT_PATH%\brgy\" (
    echo ERROR: Project directory not found at "%PROJECT_PARENT_PATH%\brgy\"
    echo Please check the PROJECT_PARENT_PATH in this batch file.
    pause
    exit /b
)
IF NOT EXIST "%PROJECT_PARENT_PATH%\brgy\manage.py" (
    echo ERROR: manage.py not found in "%PROJECT_PARENT_PATH%\brgy\"
    echo Please ensure PROJECT_PARENT_PATH is the folder *containing* your 'brgy' project folder.
    pause
    exit /b
)
echo Project directory and manage.py found.
echo.

REM --- Change to your project directory ---
echo Changing directory to project...
cd /d "%PROJECT_PARENT_PATH%\brgy"
IF %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to change directory to "%PROJECT_PARENT_PATH%\brgy".
    pause
    exit /b
)
echo Current directory: %CD%
echo.

REM --- (Optional) Activate virtual environment ---
IF DEFINED VENV_ACTIVATE_PATH (
    IF NOT EXIST "%VENV_ACTIVATE_PATH%" (
        echo ERROR: Virtual environment activate script not found at "%VENV_ACTIVATE_PATH%".
        echo Please check the VENV_ACTIVATE_PATH setting.
        pause
        exit /b
    )
    echo Activating virtual environment from "%VENV_ACTIVATE_PATH%"...
    call "%VENV_ACTIVATE_PATH%"
    IF %ERRORLEVEL% NEQ 0 (
        echo ERROR: Failed to activate virtual environment.
        pause
        exit /b
    )
    echo Virtual environment activated.
) ELSE (
    echo Skipping virtual environment activation (VENV_ACTIVATE_PATH not set in script).
    echo WARNING: If your project uses a virtual environment, it may not run correctly.
)
echo.

REM --- Start the Django development server in a new window ---
echo Starting Django development server...
REM The cmd /k keeps the server window open so you can see its output and stop it with Ctrl+C
start "Barangay Django Server" cmd /k "python manage.py runserver"

REM --- Wait for a few seconds for the server to start ---
echo Waiting 5 seconds for the server to initialize...
timeout /t 5 /nobreak >nul

REM --- Open Chrome to the specified URL ---
echo Opening application in Chrome...
start chrome "http://127.0.0.1:8000/accounts/login/?next=/residents/"

echo.
echo Batch file finished. The Django server should be running in a separate window.
echo You can close this initial window.
echo.
REM pause