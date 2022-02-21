#!/bin/sh
export FLASK_APP=web_interface/web_interface
export FLASK_ENV=development
flask run --host=0.0.0.0
