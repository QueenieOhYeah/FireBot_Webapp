import math
import olympe
from olympe.messages.ardrone3.Piloting import TakeOff, moveBy, Landing, moveTo, Circle, PCMD
from olympe.messages.move import extended_move_by, extended_move_to
from olympe.messages.ardrone3.PilotingState import moveToChanged, FlyingStateChanged, PositionChanged, AttitudeChanged, \
    moveByChanged
from olympe.messages.ardrone3.GPSSettingsState import GPSFixStateChanged, ReturnHomeMinAltitudeChanged
from olympe.messages.ardrone3.GPSSettings import ReturnHomeMinAltitude, ResetHome
from olympe.messages.ardrone3.PilotingState import GpsLocationChanged
from olympe.enums.ardrone3.Piloting import MoveTo_Orientation_mode
from olympe.messages.camera2.Command import Configure, StartPhoto, StartRecording, StopRecording
from olympe.messages.camera2.Event import Photo
from olympe.messages.rth import set_min_altitude, set_ending_hovering_altitude, set_ending_behavior, return_to_home, \
    state, rth_auto_trigger
from olympe.messages.obstacle_avoidance import set_mode, status, alert_timer
import videostream_button
import time
olympe.log.update_config({"loggers": {"olympe": {"level": "ERROR"}}})


def flight(drone, gps_points, max_alt, elevation):
    # real drone
    #	drone = olympe.Drone("192.168.42.1")
    #	drone.connect()

    #	 simulated drone
    # drone = olympe.Drone("10.202.0.1")
    # drone.connect()

    # skycontroller
    # SKYCTRL_IP = "192.168.53.1"
    # drone = olympe.Drone(SKYCTRL_IP)
    # assert drone.connect()

    streamer = videostream_button.OlympeStreaming(drone)
    streamer.start()

    # testing
    max_height = max_alt
    min_height = 1.80

    # # config camera
    # config_camera(drone)

    # Config obstacle avoidance
    config_oa(drone)

	# Config rth
    config_rth(drone, max_height, min_height)

    # get home altitude
    drone_home = drone.get_state(GpsLocationChanged)
    print(drone_home["latitude"], drone_home["longitude"], drone_home["altitude"])
    #	take_off_altitute = drone_home["altitude"]
    take_off_altitude = elevation

    #	# Take-off
    take_off(drone)

    #	#gps
    goto_gps(drone, max_height, min_height, take_off_altitude, gps_points)
    time.sleep(60)
    streamer.stop()


# drone.disconnect()


def take_off(drone):
    print("\n\n", drone.get_state(FlyingStateChanged)["state"], "\n\n")

    assert drone(
        FlyingStateChanged(state="hovering", _policy="check")
        | FlyingStateChanged(state="flying", _policy="check")
        | (
                GPSFixStateChanged(fixed=1, _timeout=10, _policy="check_wait")
                >> (
                        TakeOff(_no_expect=True)
                        & FlyingStateChanged(
                    state="hovering", _timeout=10, _policy="check_wait")
                )
        )
    ).wait()


def config_camera(drone):
    assert drone(
        Configure(camera_id=0,
                  config=dict(
                      camera_mode="photo",
                      photo_mode="single",
                      photo_format="full_frame",
                      photo_file_format="jpeg",
                      photo_dynamic_range="standard",
                      exposure_mode="automatic",
                      white_balance_mode="automatic",
                      ev_compensation="0_00", ))).wait(10).success()


def config_rth(drone, max_height, min_height):
    #	max_height = 10
    #	min_height = 1.83
    exp = drone(
        ResetHome()
        >> set_ending_behavior(ending_behavior="hovering")
        #	    >> set_min_altitude(altitude = max_height)
        #	    #auto tigger at low battery
        #	    >> rth_auto_trigger(reason = 1)
    )
    assert exp.wait(10), exp.explain()

    drone(
        # landing
        ReturnHomeMinAltitude(value=max_height)
        >> ReturnHomeMinAltitudeChanged(value=max_height)
        # auto tigger at low battery
        #	    >> rth_auto_trigger(reason = 1)
    ).wait().success()


def config_oa(drone):
    if drone(status(mode='disabled', _policy="check")).wait().success():
        assert drone(set_mode(mode='standard')).wait().success()


def goto_gps(drone, max_height, min_height, take_off_altitute, gps_points):
    # ascend to height
    exp = drone(
        moveBy(0, 0, -max_height, 0)
        >> PCMD(1, 0, 0, 0, 0, 0)
        >> FlyingStateChanged(state="hovering", _timeout=5, _policy="check_wait")
    ).wait().success()
    #	assert exp.wait(10), exp.explain()
    print("ascent")

    #	list_of_points = [[48.878924,2.367782,2.000000], [48.878928,2.367782,3.000000]]
    # list_of_points = [[48.878924,2.367782,0.000000]]
    list_of_points = gps_points
    #	list_of_points = [[47.60521,-122.16413,25.298400], [47.60581,-122.16360,33.528000]]
    #	list_of_points = [[47.62185,-122.17840,50.000000], [47.62192,-122.17847,50.000000]]

    # Move 10m
    # a = list_of_points[0]

    for point in list_of_points:
        print(point)
        drone(
            extended_move_to(point[0], point[1], point[2] - take_off_altitute + max_height, MoveTo_Orientation_mode.TO_TARGET,
                   0.0, 4.0, 4.0, 30.0)
            >> moveToChanged(status='DONE', _timeout=10, _policy="check_wait")
        ).wait().success()
        drone_curr = drone.get_state(GpsLocationChanged)
        print(point[2] - take_off_altitute + max_height)
        print(drone_curr["latitude"], drone_curr["longitude"], drone_curr["altitude"])
        drone(
            #moveTo(point[0],  point[1], point[2] - take_off_altitute + min_height, MoveTo_Orientation_mode.TO_TARGET, 0.0)
            extended_move_to(point[0], point[1], point[2] - take_off_altitute + min_height,
                             MoveTo_Orientation_mode.TO_TARGET, 0.0, 4.0, 4.0, 30.0)
            >> moveTo(point[0], point[1], point[2] - take_off_altitute + min_height,
                      MoveTo_Orientation_mode.HEADING_START, 0.0)
            >> moveToChanged(status='DONE', _timeout=10, _policy="check_wait")
        ).wait().success()
        for i in range(4):
            print(i)
            drone(
                FlyingStateChanged(state="hovering", _policy="check_wait")
                # >> take_photo(cam_id=0)).wait(10).success()
                >> StartRecording(camera_id=0)
                # >> StartPhoto(camera_id=0)
                # >> Photo(camera_id=0, type="taking_photo")
                # >> Photo(camera_id=0, type="stop", stop_reason="capture_done")
            ).wait(10).success()
            drone(StopRecording(camera_id=0)).wait()
            drone(
                moveBy(0, 0, 0, 2 * math.pi / 4)
                >> moveByChanged(status='DONE', _timeout=10)
            ).wait(10).success()

        drone(
            moveTo(point[0], point[1], point[2] + max_height, MoveTo_Orientation_mode.TO_TARGET, 0.0)
            >> moveToChanged(status='DONE', _timeout=10)
            >> FlyingStateChanged(state="hovering", _timeout=5)
        ).wait().success()

    # Go back home
    drone(
        return_to_home()
        >> state(state="in_progress")
        >> FlyingStateChanged(state="hovering", _policy="check_wait")
    ).wait().success()


# if __name__ == "__main__":
#     SKYCTRL_IP = "192.168.53.1"
#     drone = olympe.Drone(SKYCTRL_IP)
#     assert drone.connect()
#     list_of_points = [[47.62185,-122.17840,50.000000]]
#     max_alt = 5
#     elevation = 50
#     flight(drone, list_of_points, max_alt, elevation)
#

