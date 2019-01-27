#!/bin/sh

mkdir -p build/aegir
cp -r aegir contrib postgres requirements.txt docker-compose.yaml Dockerfile setup.py build/aegir
cd build/
tar czf aegir.tar.gz aegir

scp aegir.tar.gz ${USER}@${HOST}:~
ssh ${USER}@${HOST} <<EOF
    apt update
    apt -y install docker docker-compose
    rm -rf aegir/
    tar xvf aegir.tar.gz
    cd aegir/
    docker-compose up -d
    docker-compose run api python -m aegir db create
EOF

rm -rf build
