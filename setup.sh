#!/bin/bash

export PYTHON_VERSION=$(python -c 'import sys; version=sys.version_info[:3]; print("{0}.{1}.{2}".format(*version))')
MAJ="$(cut -d'.' -f1 <<<$PYTHON_VERSION)"
MIN="$(cut -d'.' -f2 <<<$PYTHON_VERSION)"

PYTHON_VALID=false
if [ $MAJ -eq 3 ] && [ $MIN -gt 9 ]; then
    PYTHON_VALID=true
fi

if [ $PYTHON_VALID = false ]; then
    echo "Python version $PYTHON_VERSION is not supported. Please use Python 3.10 or higher."
    exit 1
fi

python -m venv env
source env/bin/activate
pip install -r requirements.txt
cp sample/conf.py.sample src/conf.py
cp sample/run.sh.sample run.sh
chmod +x run.sh
