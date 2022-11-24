import olympe
from olympe.messages.battery import capacity

olympe.log.update_config({"loggers": {"olympe": {"level": "ERROR"}}})


def battery_level(drone):
    battery = drone.get_state(capacity)
    full_capacity = battery["full_charge"]
    remaining = battery["remaining"]
    return int(round(remaining/full_capacity,2) * 100)


# if __name__ == "__main__":
# #     # Simulated
# #     # DRONE_IP = os.environ.get("DRONE_IP", "10.202.0.1")
# #
#     # controller
#     DRONE_IP = "192.168.53.1"
#     drone = olympe.Drone(DRONE_IP)
#     drone.connect(retry=3)
#     battery_level(drone)
# #
#     # print(check_drone_connection(drone))
#     # print(controller_connection(drone))
#     print(connection(drone))
