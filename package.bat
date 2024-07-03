cd app
call npm run build:win
move .\dist\win-unpacked\resources\app.asar.unpacked\resources\icon.png .\dist\win-unpacked\resources
cd ..
cd server
call .\.venv\Scripts\activate
call echo y | pyinstaller main.spec
xcopy .\.venv\Lib\site-packages\litellm\*.json .\dist\autoMateServer\_internal\litellm\  /E /H /F /I /Y
xcopy .\dist\autoMateServer\* ..\app\dist\win-unpacked\ /E /H /F /I /Y
cd ..\app\dist
REN win-unpacked autoMate
call del autoMate.zip
powershell Compress-Archive -Path autoMate -DestinationPath autoMate.zip
