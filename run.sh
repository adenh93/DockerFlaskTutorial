#!/bin/bash

source /env/bin/activate

export FLASK_APP=manage.py
export FLASK_ENV=development

flask run