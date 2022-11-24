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


@app.route('/run', methods=["POST"])
def run_drone_mapper():
    # Write Co-ordinates to file
    req = request
    content = json.loads(req.data)
    with open("Coordinates.txt", "w+") as file:
        for coord in content['coordinates']:
            file.write("({},{})".format(coord['lat'], coord['lng']))
            file.write('\n')
        file.write(content['altitude'])
    # run drone script
    # droneMapper.main()
    return content


@app.route('/startVideo')
def start_video():
    streamer.start()
    return "start Video"


@app.route('/stopVideo')
def stop_video():
    streamer.stop()
    return "start Video"


@app.route('/land')
def land():
    landing.test_landing(drone)
    return "landings"


@app.route('/fly')
def fly():
    flight.flight(drone)
    return "fly"


@app.route('/connect')
def connect_status():
    if connection.check_drone_connection(drone):
        print("success")
        return "connected"
    return "disconnected"


@app.route('/battery')
def get_battery_level():
    response = battery.battery_level(drone)
    return str(response)


@app.route('/images')
def get_images():
    images_urls = {}
    count = 0
    path_to_images = 'static/images/'
    for entry in os.listdir(path_to_images):
        if os.path.isfile(os.path.join(path_to_images, entry)):
            print(entry)
            images_urls[count] = entry
            count += 1
    return images_urls


@app.route('/createMission/')
def createMission():
    return render_template('map.html')


# DRONE_IP = os.environ.get("DRONE_IP", "10.202.0.1")
#
# # controller
# # DRONE_IP = os.environ.get("DRONE_IP", "192.168.53.1")
# # DRONE_IP = "192.168.53.1"
# drone = olympe.Drone(DRONE_IP)
# drone.connect(retry=3)
# streamer = videostream_button.OlympeStreaming(drone)

# two videostreams use only one
# videostream.test_streaming(drone)
# test_video.streaming(drone)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)

