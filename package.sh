#!/usr/bin/env bash
cd server
. ./.venv/bin/activate
pip install -r requirements.txt
echo y | pyinstaller main.spec
mkdir -p ./dist/autoMateServer/_internal/litellm
# cp ./.venv/lib/python*/site-packages/litellm/*.json ./dist/autoMateServer/_internal/litellm
cp "$(find ./.venv/lib -maxdepth 1 -type d -name 'python*' | head -n 1)"/site-packages/litellm/*.json ./dist/autoMateServer/_internal/litellm

cd ../app
target_dir=./dist
rm -rf $target_dir/*.*
npm run build:linux
npm run build:mac