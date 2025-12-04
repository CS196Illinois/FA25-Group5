@echo off
REM Quick start script for Schedule Generator Backend (Windows)

echo ==========================================
echo Schedule Generator Backend - Quick Start
echo ==========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created
) else (
    echo Virtual environment already exists
)

REM Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt --quiet
echo Dependencies installed

REM Create data directory if it doesn't exist
if not exist "data" (
    echo.
    echo Creating data directory...
    mkdir data
    echo Data directory created
)

REM Check if data file exists
if not exist "data\cleaned_courses.pkl" (
    echo.
    echo Warning: No data file found at data\cleaned_courses.pkl
    echo The server will use sample data for demonstration
)

REM Start the server
echo.
echo ==========================================
echo Starting server...
echo ==========================================
echo.
python app.py

pause
