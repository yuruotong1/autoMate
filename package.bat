cd server
call .\.venv\Scripts\activate
pip install -r requirements.txt
call echo y | pyinstaller main.spec
xcopy .\.venv\Lib\site-packages\litellm\*.json .\dist\autoMateServer\_internal\litellm\  /E /H /F /I /Y

cd ..\app
set "target_dir=.\dist"
del /f /q "%target_dir%\*.*"
for /d %%i in ("%target_dir%\*") do rmdir /s /q "%%i"
call npm run build:win