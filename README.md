# Leaderboard-to-csv
It's a python script that can import data from the leaderboard to a csv file.
The script will automatically get the world record and the laptime of the player you specified on the .ini file.
## Installation:
- install Python.

https://www.python.org/downloads/
- Launch the cmd, go to the repository of your choice and clone the git repository:
```
git clone https://github.com/MatBlanchard/rre-leaderboard_to_csv.git
```
- Go to the repository you cloned :
```
cd rre-leaderboard_to_csv
```
- Modify the raceroom.ini file with your parameters:
```
save_directory: [The directory you want to save the data]
car_id_list: [The ids of the cars you want to save]
player: [The player name that made the laptimes you want to save]
header: [The header of your csv file]
```
- Launch the script using or double-click on the raceroom.bat file:
```
raceroom
```
