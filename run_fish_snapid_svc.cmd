@echo off
REM Manual extracts the IP Address using ipconfig. 
REM		- Look for the IPv4 Address under your laptop WiFi adapter (typically something like 192.168.x.x) 
REM Auto extracts the IP address using the for /f loop.
REM 	- Sets the extracted IP address to a variable IP.
REM 	- Echoes the IP address (optional for verification).
for /f "tokens=14" %%i in ('ipconfig ^| findstr /i "ipv4"') do set IP=%%i
echo Local IP: %IP%
REM Calls another program, passing the IP address as an argument.
cd C:\fyp\fish_snapid_svc\
@echo on
powershell.exe -ExecutionPolicy Bypass python manage.py runserver %IP%:8000
pause...