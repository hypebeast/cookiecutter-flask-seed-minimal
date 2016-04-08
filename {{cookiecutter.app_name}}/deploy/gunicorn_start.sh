#!/bin/bash

NAME="{{ cookiecutter.app_name }}"
FLASKDIR=/opt/$NAME
VENVDIR=$FLASKDIR/env
SOCKFILE=$FLASKDIR/sock
NUM_WORKERS=1
HOST=127.0.0.1
PORT=8000

echo "Starting $NAME"

# activate the virtualenv
cd $VENVDIR
source bin/activate

export PYTHONPATH=$FLASKDIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your unicorn
exec gunicorn {{ cookiecutter.app_name }}.app:create_app\(\) -b $HOST:$PORT \
  --name $NAME \
  --workers $NUM_WORKERS \
  --log-level=warn \
  --bind=unix:$SOCKFILE
