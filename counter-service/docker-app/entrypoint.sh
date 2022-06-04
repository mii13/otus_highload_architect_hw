#!/bin/sh

set -e
set -o nounset

if [ "$1" = 'runserver' ]; then
    alembic upgrade head
    uvicorn main:app --host 0.0.0.0 --port 8088 --reload
else
   exec sh -c "$@"
fi
