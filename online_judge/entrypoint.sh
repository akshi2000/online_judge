#!/bin/sh

## Uncomment this to remove all data from database at each start
# python3 manage.py flush --no-input

## Uncomment these to makemigrations ans migrate changes to database at each start
# python3 manage.py makemigrations
# python3 manage.py migrate

## Uncomment this to collect static files at each start
#python3 manage.py collectstatic --no-input --clear

# Executes the remaining commands (if any)
exec "$@"
