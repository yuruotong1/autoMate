echo Y | pyinstaller -D -w --add-data=pages/*.ui:pages  --add-data=source/*:source -i source/logo.ico  --hidden-import=tiktoken_ext.openai_public --hidden-import=tiktoken_ext --name=autoMate  main.py 
mkdir dist/autoMate/_internal/self_utils
@REM move dist/autoMate/_internal/pages dist/autoMate/pages
@REM move dist/autoMate/_internal/source dist/autoMate/source
copy "config_tmp.yaml" "dist/autoMate/_internal/config.yaml"

cd dist
del "autoMate.zip"
powershell Compress-Archive -Path autoMate -DestinationPath autoMate.zip
cd ..

