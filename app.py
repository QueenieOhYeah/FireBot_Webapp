
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, request, render_template
# import droneMapper
import json
import olympe
import os
import landing
import videostream
import videostream_button
import flight
import connection
import battery
import read_missions
import media
import test

app = Flask(__name__)
_threadpool_cpus = int(os.cpu_count()/2)
EXECUTOR = ThreadPoolExecutor(max_workers=max(_threadpool_cpus, 2))

# DRONE_IP = os.environ.get("DRONE_IP", "10.202.0.1")
# #
# # # controller
drone = None
DRONE_IP = os.environ.get("DRONE_IP", "192.168.53.1")
# # DRONE_IP = "192.168.42.1"
drone = olympe.Drone(DRONE_IP)
# drone.connect(retry=3)
# Simulated
# DRONE_IP = os.environ.get("DRONE_IP", "10.202.0.1")
#
# # controller
# # DRONE_IP = "192.168.53.1"
# drone = olympe.Drone(DRONE_IP)
# drone.connect(retry=3)
# drone.connect()
# videostream.test_streaming(drone)

# DRONE_IP = os.environ.get("DRONE_IP", "10.202.0.1")
#
# # controller
# # DRONE_IP = "192.168.53.1"
# drone = olympe.Drone(DRONE_IP)
# drone.connect(retry=3)
# videostream.test_streaming(drone)

@app.route('/')
def display_html_page():
    with open('templates/index.html') as file:
        page = file.read()
    return page

@app.route('/connectDrone')
def connect_to_drone():
    future = EXECUTOR.submit(connect_to_drone_thread)
    result = future.result()
    return result

def connect_to_drone_thread():
    global drone

    # drone.connect()
    drone.connect(retry=3)
    if connection.check_drone_connection(drone):
        return "success"
    return "failure"

@app.route('/startVideo')
def start_video():
    # global drone
    # global streamer
    # # if not streamer:
    # #     print("streamer is none")
    # # streamer = videostream_button.OlympeStreaming(drone)
    # print(streamer)
    # streamer.start()
    return "start Video"


# @app.route('/stopVideo')
# def stop_video():
#     global streamer
#     # streamer = videostream_button.OlympeStreaming(drone)
#     streamer.stop()
#     return "start Video"


@app.route('/land')
def land():
    landing.test_landing(drone)
    return "landings"


@app.route('/fly', methods=["POST"])
def fly():
    EXECUTOR.submit(send_fly())
    return render_template('index.html')


def send_fly():
    global missions
    global drone
    # DRONE_IP = os.environ.get("DRONE_IP", "192.168.53.1")
    # # DRONE_IP = "192.168.42.1"
    # drone = olympe.Drone(DRONE_IP)
    # drone.connect(retry=3)
    mission = request.form.get('missionOptions')
    max_alt = request.form.get('maxAlt')
    elevation = request.form.get('takeOffEle')
    print(missions[mission])
    print(max_alt)
    print(elevation)
    gps_points = missions[mission]
    flight.flight(drone, gps_points, eval(max_alt), eval(elevation))
    # test.flight(drone, gps_points, eval(max_alt), eval(elevation))
    drone.disconnect()


# CONNECTION = False


@app.route('/connect')
def connect_status():
    future = EXECUTOR.submit(connect_status_thread)
    result = future.result()
    if result:
        return "connected"
    return "disconnected"


def connect_status_thread():
    global drone
    if connection.check_drone_connection(drone):
        return True


@app.route('/battery')
def get_battery_level():
    global bat
    future = EXECUTOR.submit(battery_thread)
    result = future.result()
    return result


def battery_thread():
    global drone
    global bat
    response = battery.battery_level(drone)
    return str(response)


@app.route('/loadMissions', methods=["POST"])
def load_mission():
    global missions
    # Write Co-ordinates to file
    data_dict = read_missions.read_missions()
    if (missions != data_dict):
        missions = data_dict
    # print(missions)
    # print("here")
    data = []
    for mission in data_dict:
        data.append({mission:data_dict[mission]})
        # data.append({mission})
    # print(data)
    return data


@app.route('/createMission/')
def createMission():
    return render_template('map.html')


@app.route('/createMission/saveCoords', methods=["POST"])
def save_mission():
    # Write Co-ordinates to file
    req = request
    content = json.loads(req.data)
    name = "missions/" + content['mission'] + ".txt";
    with open(name, "w+") as file:
        for coord in content['coordinates']:
            file.write("{} {} {}".format(coord['lat'], coord['lng'], coord['alt']))
            file.write('\n')
        # file.write(content['altitude'])
    # run drone script
    # droneMapper.main()
    return content


@app.route('/data/')
def get_data():
    return render_template('images.html')


@app.route('/data/images')
def get_images():
    images_urls = {}
    count = 0
    path_to_images = 'static/images/'
    for entry in os.listdir(path_to_images):
        if os.path.isfile(os.path.join(path_to_images, entry)):
            images_urls[count] = entry
            count += 1
    return images_urls


@app.route('/data/download')
def download_data():
    # EXECUTOR.submit(download_data_thread)
    print("download")
    return "DONE"


def download_data_thread():
    media.download()
    return "DONE"

# streamer = None
# streamer.start()
# streamer = videostream_button.OlympeStreaming(drone)



# two videostreams use only one
# videostream.test_streaming(drone)
# test_video.streaming(drone)
missions = None

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)