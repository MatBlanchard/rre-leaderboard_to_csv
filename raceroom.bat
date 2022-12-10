if exist env (rd /s /q env)
py -m venv env
call env\scripts\activate
pip install -r requirements.txt
py raceroom.py
rd /s /q env