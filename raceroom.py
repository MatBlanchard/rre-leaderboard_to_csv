import ast
import requests
import csv
import json
import configparser
from exceptions import TooManyErrorsException

config = configparser.RawConfigParser()
config.read('raceroom.ini', encoding='utf-8')

raceroom_directory = config.get('RRE', 'raceroom_directory')
save_directory = config.get('RRE', 'save_directory')
car_ids = ast.literal_eval(config.get('RRE', 'car_id_list'))
driver_name = config.get('RRE', 'player')
header = ast.literal_eval(config.get('RRE', 'header'))
finished_classes = []
count = 1500
max_errors = 10


def get_json_file():
    with open(raceroom_directory + 'Game/GameData/General/r3e-data.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def get_lap_time_sec(lap_time):
    if len(lap_time) == 2:
        return '{:.3f}'.format(float(lap_time[0]) * 60 + float(lap_time[1])).replace('.', ',')
    else:
        return '{:.3f}'.format(float(lap_time[0])).replace('.', ',')


def get_data(track_id, car_id):
    wr, lap_time, rank, i = None, None, None, 0
    errors = 0
    while True:
        if errors >= max_errors:
            raise TooManyErrorsException
        url = "https://game.raceroom.com/leaderboard/listing/0?start=0&count=" + \
              str(count) + "&track=" + str(track_id) + "&car_class=" + str(car_id)
        page = requests.get(url, headers={"X-Requested-With": "XMLHttpRequest"})
        if not page.ok:
            errors += 1
            continue
        file = json.loads(page.text)
        context = file['context']['c']['results']
        if len(context) == 0:
            if car_id in finished_classes and track_id != 10274:
                errors += 1
                continue
            else:
                return []
        wr = context[0]['laptime']
        wr = wr.split('s')[0].split('m ')
        wr = get_lap_time_sec(wr)
        for c in context:
            i += 1
            if c['driver']['name'] == driver_name:
                lap_time = c['laptime'].split('s')[0].split('m ')
                lap_time = get_lap_time_sec(lap_time)
                rank = i
        if car_id in finished_classes:
            if not wr or not lap_time or not rank or not i:
                errors += 1
                continue
        break
    if not wr or not lap_time or not rank or not i:
        return []
    return [wr, lap_time, rank, i]


def save_data(json_file, car_id):
    car_name = get_car_name(json_file, car_id)
    with open(save_directory + car_name + ".csv", "w+", encoding="utf-16", newline="") as file:
        writer = csv.writer(file, delimiter="\t")
        writer.writerow(header)
        n = 1
        for t in tracks:
            data = [n] + [t[0]] + get_data(t[1], car_id)
            if len(data) == len(header):
                writer.writerow(data)
                print("Car: " + car_name + " | Track: " + t[0] + " saved successfully")
                n += 1


def get_all_tracks(json_file):
    results = {}
    track_list = json_file["tracks"]
    for i in track_list:
        track_name = track_list[i]['Name']
        for j in track_list[i]['layouts']:
            results.update({track_name + " - " + j['Name']: j['Id']})
    return sorted(results.items(), key=lambda t: t[0])


def get_car_name(json_file, car_id):
    if type(car_id) == str:
        car_id = car_id.split("class-")[1]
        return json_file['classes'][car_id]['Name']
    else:
        return json_file['cars'][str(car_id)]['Name']


if __name__ == "__main__":
    jf = get_json_file()
    tracks = get_all_tracks(jf)
    try:
        for car in car_ids:
            save_data(jf, car)
        print("\nAll data has been saved successfully\n")
    except KeyboardInterrupt:
        print("\nProgram interrupted\n")
    except PermissionError as e:
        print("\nError: " + e.filename + " already opened, please close it and retry\n")
    except TooManyErrorsException:
        print("\nError: exceeding max number of try ("
              + str(max_errors) + " tries max) while getting the data\n")
