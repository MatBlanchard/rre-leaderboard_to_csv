if not exist env (py -m venv env)
call env\scripts\activate
pip install -r requirements.txt
py raceroom.py
pause