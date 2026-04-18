#!/bin/bash
export PYTHONHOME=/opt/anaconda3
/opt/anaconda3/bin/python3 -m uvicorn main:app --reload --port 8000
