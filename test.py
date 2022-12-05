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
from olympe.messages.camera import take_photo
from olympe.messages.skyctrl.CoPiloting import setPilotingSource
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

    # # testing
    max_height = max_alt
    min_height = 1.80
    #
    #config camera
    # config_camera(drone)
    #
    #Config obstacle avoidance
    config_oa(drone)
    #
    # #	# Config rth
    config_rth(drone, max_height, min_height)
    #
    # # get home altitude
    # drone_home = drone.get_state(GpsLocationChanged)
    # print(drone_home["latitude"], drone_home["longitude"], drone_home["altitude"])
    # #	take_off_altitute = drone_home["altitude"]
    take_off_altitude = elevation
    #
    # #	# Take-off
    take_off(drone)
    # #
    # #	#gps
    goto_gps(drone, max_height, min_height, take_off_altitude, gps_points)
    time.sleep(10)
    streamer.stop()


# drone.disconnect()


def take_off(drone):
    print("\n\n", drone.get_state(FlyingStateChanged)["state"], "\n\n")

    exp = drone(
        TakeOff()).wait()
    exp.explain()

    #    drone.disconnect()

    # drone(
    #     FlyingStateChanged(state="hovering", _policy="check")
    #     | FlyingStateChanged(state="flying", _policy="check")
    #     | FlyingStateChanged(state="landed", _policy="check")
    #     | (
    #             GPSFixStateChanged(fixed=1, _timeout=10, _policy="check_wait")
    #             >> (
    #                     TakeOff(_no_expect=True)
    #                     & FlyingStateChanged(state="hovering", _timeout=10, _policy="check_wait")
    #             )
    #     )
    # ).wait()


#	drone(
#
#	    TakeOff(_no_expect=True)
#	    & FlyingStateChanged(
#	        state="hovering", _timeout=10, _policy="check_wait")

#	).wait()

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
    exp = drone(
        ResetHome()
        >> set_ending_behavior(ending_behavior="hovering")
        # >> set_min_altitude(altitude = max_height)
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
    for i in range(4):
        print(i)
        drone(
            FlyingStateChanged(state="hovering", _policy="check_wait")
            # >> take_photo(cam_id=0)).wait(10).success()
            >> StartRecording(camera_id=0)
            # >> Photo(camera_id=0, type="taking_photo")
            # >> Photo(camera_id=0, type="stop", stop_reason="capture_done")
        ).wait(10).success()
        time.sleep(3)
        drone(StopRecording(camera_id=0)).wait()
        drone(
            moveBy(0, 0, 0, 2 * math.pi / 4)
            >> moveByChanged(status='DONE', _timeout=10)
        ).wait(10).success()

    drone(Landing()).wait().success()



if __name__ == "__main__":
    SKYCTRL_IP = "192.168.53.1"
    drone = olympe.Drone(SKYCTRL_IP)
    assert drone.connect()
    list_of_points = [[47.62185,-122.17840,50.000000]]
    max_alt = 5
    elevation = 50
    flight(drone, list_of_points, max_alt, elevation)
#     print("break")
#     streamer = videostream_button.OlympeStreaming(drone)
#     streamer.start()
#     drone(
#         TakeOff()
#         >> FlyingStateChanged(state="hovering", _timeout=10, _policy="check_wait")).wait().success()
#     time.sleep(5)
#     flight(drone, list_of_points, max_alt, elevation)
#     # time.sleep(5)
#     # config_camera(drone)
#     time.sleep(30)
#     # streamer.stop()
    drone.disconnect()

    # flight(drone, list_of_points, max_alt, elevation)


