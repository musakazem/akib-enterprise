@echo off
REM Change to your virtual environment directory if you are using one
cd "E:\Abbu\Invoice manager\.env\Scripts"
if %errorlevel% neq 0 (
    echo Failed to navigate to the virtual environment directory.
    pause
    exit /b %errorlevel%
)

REM Activate the virtual environment
call activate
if %errorlevel% neq 0 (
    echo Failed to activate the virtual environment.
    pause
    exit /b %errorlevel%
)

REM Change to your Django project directory
cd "E:\Abbu\Invoice manager\invoice_manager"
if %errorlevel% neq 0 (
    echo Failed to navigate to the Django project directory.
    pause
    exit /b %errorlevel%
)

REM Run the Django server
start "" cmd /c "python manage.py runserver"
if %errorlevel% neq 0 (
    echo Failed to start the Django server.
    pause
    exit /b %errorlevel%
)

start "" http://localhost:8000/admin

pause
