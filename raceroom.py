import ast
import requests
import csv
import json
import configparser
config = configparser.RawConfigParser()
config.read('raceroom.ini', encoding='utf-8')

save_directory = config.get('RRE', 'save_directory')
car_class = ast.literal_eval(config.get('RRE', 'car_id_list'))
driver_name = config.get('RRE', 'player')
header = ast.literal_eval(config.get('RRE', 'header'))


def get_lap_time_sec(lap_time):
    if len(lap_time) == 2:
        return '{:.3f}'.format(float(lap_time[0])*60 + float(lap_time[1])).replace('.', ',')
    else:
        return '{:.3f}'.format(float(lap_time[0])).replace('.', ',')


def get_data(track_id, car_id):
    url = "https://game.raceroom.com/leaderboard/listing/0?start=0&count=200&track=" + str(track_id) + "&car_class=" + str(car_id)
    page = requests.get(url, headers={"X-Requested-With": "XMLHttpRequest"})
    if page.ok:
        file = json.loads(page.text)
        context = file['context']['c']['results']
        if len(context) == 0:
            return []
        wr = context[0]['laptime']
        wr = wr.split('s')[0].split('m ')
        wr = get_lap_time_sec(wr)
        lap_time = ""
        for c in context:
            if c['driver']['name'] == driver_name:
                lap_time = c['laptime'].split('s')[0].split('m ')
                lap_time = get_lap_time_sec(lap_time)
                break
        return [wr, lap_time]


def save_data(car_id):
    car_name = get_car_name(car_id)
    with open(save_directory + car_name + ".csv", "w+", encoding="utf-16", newline="") as file:
        writer = csv.writer(file, delimiter="\t")
        writer.writerow(header)
        n = 1
        for t in tracks:
            data = [n] + [t[0]] + get_data(t[1], car_id)
            if len(data) == 4:
                writer.writerow(data)
                print("Car: " + car_name + " | Track: " + t[0] + " saved successfully")
                n += 1


def get_all_tracks():
    page = requests.get("https://raw.githubusercontent.com/sector3studios/r3e-spectator-overlay/master/r3e-data.json")
    if page.ok:
        results = {}
        file = json.loads(page.text)
        tracks = file["tracks"]
        for i in tracks:
            track_name = tracks[i]['Name']
            for j in tracks[i]['layouts']:
                results.update({track_name + " - " + j['Name']: j['Id']})
        return sorted(results.items(), key=lambda t: t[0])


def get_car_name(car_id):
    url = "https://game.raceroom.com/leaderboard/listing/0?car_class=" + str(car_id)
    page = requests.get(url, headers={"X-Requested-With": "XMLHttpRequest"})
    if page.ok:
        file = json.loads(page.text)
        return file['context']['c']['results'][0]['car_class']['car']['name']


def get_pilot_by_id(pilot_id):
    url = "https://game.raceroom.com/utils/user-info/" + str(pilot_id)
    page = requests.get(url)
    if page.ok:
        file = json.loads(page.text)
        return file['name']


def get_pilot_by_username(pilot_username):
    url = "https://game.raceroom.com/utils/user-info/" + pilot_username
    page = requests.get(url)
    if page.ok:
        file = json.loads(page.text)
        return file['name']


if __name__ == "__main__":
    tracks = get_all_tracks()
    try:
        for car in car_class:
            save_data(car)
    except KeyboardInterrupt:
        print("\nProgram interrupted")
