#!/bin/sh
export FLASK_APP=web_interface/web_interface
export FLASK_ENV=development
source venv/bin/activate
./web_interface/run_server.sh
