pyinstaller -D -w main.py --add-data=pages/*.ui:pages --add-data=source/*:source
move dist/main/_internal/pages dist/main/pages
move dist/main/_internal/source dist/main/source