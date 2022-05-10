#!/bin/bash

sleep 5  # wait db

if [ "$1" = 'run_web' ]; then
  python db_migrate.py
  # uvicorn main:app --reload --port 8088 --host "0.0.0.0"
  echo "start web"
  uvicorn main:app --port 8088 --host "0.0.0.0" --reload
elif [ "$1" = 'run_consumer' ]; then
  echo "start consumer"
  python run_consumer.py
else
  exec "$@"
fi
