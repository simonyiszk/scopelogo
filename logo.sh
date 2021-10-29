#!/bin/sh
pipenv run python3 scopelogo.py $1 | aplay -f U8 -c2 -r192000