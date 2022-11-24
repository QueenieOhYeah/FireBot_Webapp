import olympe
from olympe.messages.drone_manager import connection_state
from olympe.enums.drone_manager import connection_state as cs
from olympe.messages.common.Controller import PeerStateChanged
from olympe.enums.common.Controller import PeerStateChanged_State

olympe.log.update_config({"loggers": {"olympe": {"level": "ERROR"}}})


def check_drone_connection(drone):
    if drone.connection_state():
        return True
    return False


def connection(drone):
    drone_state = drone.get_state(connection_state)
    if drone_state["state"] == cs.connected:
        return True
    return False

# if __name__ == "__main__":
#     # Simulated
#     # DRONE_IP = os.environ.get("DRONE_IP", "10.202.0.1")
#
#     # controller
#     DRONE_IP = "192.168.53.1"
#     drone = olympe.Drone(DRONE_IP)
#     drone.connect(retry=3)
#
#     # print(check_drone_connection(drone))
#     # print(controller_connection(drone))
#     print(connection(drone))
