#!/bin/bash

export FLASK_APP=manage.py
export FLASK_ENV=development

test -f "temp/TestDatabase.db" || sqlite3 temp/TestDatabase.db

flask db upgrade