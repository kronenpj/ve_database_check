#!/usr/bin/env bash

if [ -x /usr/bin/python3.10 ];then
  PY=python3.10
else
  PY=python3
fi

/usr/bin/${PY} -m venv .venv --clear --prompt VEdbcheck
source .venv/bin/activate
#pip install poetry
pip install -r requirements.txt -r requirements-test.txt
#poetry install --no-root
