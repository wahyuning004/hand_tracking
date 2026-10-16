@echo off
title Trend Jari - Hand Tracking Launcher
cls
echo ================================================================
echo          TREND JARI - HAND TRACKING & REAL-TIME FILTERS
echo ================================================================
echo.
echo Pilih cara menjalankan aplikasi:
echo.
echo [1] VERSI BROWSER (INSTANT - Tanpa download/install lama)
echo     - Menggunakan MediaPipe Web resmi langsung di Google Chrome/Edge.
echo     - Hand tracking 60 FPS, deteksi Shaka, filter Thermal & Glitch.
echo.
echo [2] VERSI PYTHON (Desktop OpenCV)
echo     - Memeriksa OpenCV & MediaPipe di Python Laragon.
echo.
echo ================================================================
set /p PILIHAN="Masukkan pilihan (1 atau 2, default: 1): "

if "%PILIHAN%"=="2" goto JALANKAN_PYTHON
goto JALANKAN_WEB

:JALANKAN_WEB
echo.
echo [*] Membuka Versi Browser di browser default Anda...
start "" "web\index.html"
echo [OK] Aplikasi dibuka di browser!
pause
exit

:JALANKAN_PYTHON
set PYTHON_CMD=python
if exist "D:\laragon\bin\python\python-3.13\python.exe" (
    set PYTHON_CMD="D:\laragon\bin\python\python-3.13\python.exe"
)

echo.
echo [*] Menggunakan Python: %PYTHON_CMD%
%PYTHON_CMD% --version

:: Cek apakah cv2 sudah terpasang agar tidak download ulang terus-menerus
%PYTHON_CMD% -c "import cv2" 2>nul
if %errorlevel% neq 0 (
    echo [*] Mengunduh dependensi (hanya dilakukan sekali)...
    %PYTHON_CMD% -m pip install opencv-python numpy
    %PYTHON_CMD% -m pip install mediapipe --only-binary :all:
)

echo.
echo [*] Menjalankan program Trend Jari Python...
%PYTHON_CMD% main.py

pause
