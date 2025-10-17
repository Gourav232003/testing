@echo off
echo Installing MongoDB Community Server...
echo.

REM Download MongoDB Community Server
echo Downloading MongoDB Community Server...
powershell -Command "Invoke-WebRequest -Uri 'https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-7.0.4-signed.msi' -OutFile 'mongodb-installer.msi'"

echo.
echo Installing MongoDB...
msiexec /i mongodb-installer.msi /quiet /norestart

echo.
echo Creating MongoDB data directory...
mkdir "C:\data\db" 2>nul

echo.
echo Starting MongoDB service...
net start MongoDB

echo.
echo MongoDB installation completed!
echo MongoDB should now be running on localhost:27017
echo.
echo To test the connection, run:
echo mongo
echo.
pause






