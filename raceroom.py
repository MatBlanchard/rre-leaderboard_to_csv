import requests
import csv
import json

save_directory = "c:/Users/matbl.DESKTOP-SE0KTRR/OneDrive/Bureau/RRE/" #Change - the directory you want to save your data
car_class = 5818 #Change - the car you want to save
driver_name = 'Mathieu Blanchard' #Change - the pilot you want to save
header = ["id", "track_name", "wr", "lap_time"]


def get_lap_time_sec(lap_time):
    if len(lap_time) == 2:
        return str(float(lap_time[0])*60 + float(lap_time[1])).replace('.', ',')
    else:
        return str(float(lap_time[0])).replace('.', ',')


def get_data(track_id, car_id):
    url = "https://game.raceroom.com/leaderboard/listing/0?track=" + str(track_id) + "&car_class=" + str(car_id)
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
        return [wr, lap_time]


def save_data(car_id):
    tracks = get_all_tracks()
    with open(save_directory + get_car_name(car_id) + ".csv", "w+", encoding="utf-16", newline="") as file:
        writer = csv.writer(file, delimiter="\t")
        writer.writerow(header)
        n = 1
        for t in tracks:
            data = [n] + [t[0]] + get_data(t[1], car_id)
            if len(data) == 4:
                writer.writerow(data)
                print(t[0] + " data saved")
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


save_data(car_class)