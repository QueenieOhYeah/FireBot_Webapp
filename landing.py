import olympe
import os
import time
import logging
import olympe.log
import pprint
from olympe.messages.ardrone3.Piloting import TakeOff, Landing
from olympe.messages.ardrone3.PilotingState import FlyingStateChanged
from olympe.messages.ardrone3.GPSSettingsState import GPSFixStateChanged

#DRONE_IP = os.environ.get("DRONE_IP", "192.168.42.1")
# Simulated drone
# DRONE_IP = os.environ.get("DRONE_IP", "10.202.0.1")

def test_landing(drone):
    # drone = olympe.Drone(DRONE_IP)
    # assert drone.connect().wait().success()
    assert drone(Landing()).wait().success()
    # drone.disconnect()

#def main()

# if __name__ == "__main__":
#    test_landing()
