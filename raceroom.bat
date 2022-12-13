@echo off
color 2
if not exist env (py -m venv env)
call env\scripts\activate
py -m pip install --upgrade pip
pip install -r requirements.txt
py raceroom.py
pause