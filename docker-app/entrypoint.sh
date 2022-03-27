#!/bin/bash

sleep 5  # wait db

python db_migrate.py

# uvicorn main:app --reload --port 8088 --host "0.0.0.0"
echo "start back"
uvicorn main:app --port 8088 --host "0.0.0.0" --workers 4