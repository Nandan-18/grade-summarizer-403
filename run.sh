#!/usr/bin/env bash

if [[ -f .env ]]; then
    source .env
fi

python3 main.py "$USERNAME" "$PASSWORD" cmput303.txt > output.txt