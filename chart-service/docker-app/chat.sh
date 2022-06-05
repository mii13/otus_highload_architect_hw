#!/bin/bash

python db_migrate.py && opentelemetry-instrument uvicorn main:app --port 8088 --host "0.0.0.0" --reload