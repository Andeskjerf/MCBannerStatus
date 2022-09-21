#!/bin/bash

python -m venv env
source env/bin/activate
pip install -r requirements.txt
cp sample/conf.py.sample src/conf.py
