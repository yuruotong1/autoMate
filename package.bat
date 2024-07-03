@REM cd app
@REM @REM call npm run build:win
@REM @REM move .\dist\win-unpacked\resources\app.asar.unpacked\resources\icon.png .\dist\win-unpacked\resources
@REM cd ..
cd server
@REM call .\.venv\Scripts\activate
call echo y | pyinstaller main.spec
xcopy .\.venv\Lib\site-packages\litellm\*.json .\dist\autoMateServer\_internal\litellm\  /H /F /I /Y
xcopy .\dist\autoMateServer\* ..\app\dist\win-unpacked\ /E /H /F /I /Y

