

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

app = Flask(__name__)

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
    global drone
    global streamer
    global is_stream

    # drone.connect()
    drone.connect()
    if connection.check_drone_connection(drone):
    # #     print("connect to drone")
    # #
    #     # if not streamer:
    #     if streamer:
    #         streamer.stop()
    #     streamer = videostream_button.OlympeStreaming(drone)
    #     ''' Decide when to start video streaming'''
    #     print(streamer)
    #     streamer.start()

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
    global missions
    global drone
    mission = request.form.get('missionOptions')
    max_alt = request.form.get('maxAlt')
    elevation = request.form.get('takeOffEle')
    print(missions[mission])
    print(max_alt)
    print(elevation)
    gps_points = missions[mission]
    flight.flight(drone, gps_points, eval(max_alt), eval(elevation))
    return render_template('index.html')


@app.route('/connect')
def connect_status():
    global drone
    print(drone)
    print(connection.check_drone_connection(drone))
    if connection.check_drone_connection(drone):
        print("success")
        return "connected"
    return "disconnected"


@app.route('/battery')
def get_battery_level():
    global drone
    print(drone)
    print("drone")
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


DRONE_IP = os.environ.get("DRONE_IP", "10.202.0.1")
# #
# # # controller
# DRONE_IP = os.environ.get("DRONE_IP", "192.168.53.1")
# DRONE_IP = "192.168.42.1"
drone = olympe.Drone(DRONE_IP)
drone.connect(retry=3)
# streamer = None
# streamer.start()
# streamer = videostream_button.OlympeStreaming(drone)


import threading


# two videostreams use only one
# videostream.test_streaming(drone)
# test_video.streaming(drone)
missions = None

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)