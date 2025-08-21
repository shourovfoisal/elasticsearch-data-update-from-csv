#!/bin/bash
python3 core/bootstrap.py
source venv/bin/activate
python3 -m core.main
