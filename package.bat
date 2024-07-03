cd app
call npm run build:win
move .\dist\win-unpacked\resources\app.asar.unpacked\resources\icon.png .\dist\win-unpacked\resources
cd ..
cd server
call .\.venv\Scripts\activate
call echo y | pyinstaller main.spec
xcopy .\.venv\Lib\site-packages\litellm\*.json .\dist\autoMateServer\_internal\litellm\  /E /H /F /I /Y


REM 设置要清空的目录路径
set "target_dir=..\app\dist"
REM 删除目标目录中的所有文件
del /f /q "%target_dir%\*.*"
REM 删除目标目录中的所有子目录
for /d %%i in ("%target_dir%\*") do rmdir /s /q

xcopy .\dist\autoMateServer\* ..\app\dist\win-unpacked\ /E /H /F /I /Y
cd ..\app\dist
REN win-unpacked autoMate
powershell Compress-Archive -Path autoMate -DestinationPath autoMate.zip
