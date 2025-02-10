@echo off
REM
REM ABOUT 
REM
REM ngrok: https://dashboard.ngrok.com/get-started/setup/windows
REM ngrok is your app’s front door—a globally distributed reverse proxy that secures,
REM protects and accelerates your applications and network services, no matter where you run them.
REM 

REM
REM INSTALLATION
REM
REM Sign up at: 
REM		https://ngrok.com/
REM Install ngrok via Chocolatey with the following command:
REM 	choco install ngrok
REM Run the following command to add your authtoken to the default ngrok.yml configuration file.
REM		ngrok config add-authtoken 2hK5T0zqPeIbKudFfFb1tdpvo1K_5emFuWs342ySvLB6pNEs5
REM		Note: this token will be provided after sign-up.

REM
REM CLI USAGE
REM
REM When ngrok is installed;
REM 	- Auto extracts the IP address using the for /f loop.
REM 	- Sets the extracted IP address to a variable IP.
REM 	- Echoes the IP address (optional for verification).
REM		- Use the ngrok command to start the tunnel.
for /f "tokens=14" %%i in ('ipconfig ^| findstr /i "ipv4"') do set IP=%%i
echo Local IP: %IP%
@echo on
ngrok http http://%IP%:8000/
pause...