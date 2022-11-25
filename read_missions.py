import os

# def read_missions():
#     missions = []
#     path_to_missions = 'missions/'
#     mission_name = None
#     for entry in os.listdir(path_to_missions):
#         mission_name = entry[:-4]
#         file = open(path_to_missions+entry, "r+")
#
#         raw_coords = [line.rstrip('\n') for line in file]
#         process_coords = []
#         for coords in raw_coords:
#             int_coords = [float(x) for x in coords.split()]
#             process_coords.append(int_coords)
#         missions.append({mission_name : process_coords})
#     print(missions)
#     return missions

def read_missions():
    missions = {}
    path_to_missions = 'missions/'
    mission_name = None
    for entry in os.listdir(path_to_missions):
        mission_name = entry[:-4]
        file = open(path_to_missions+entry, "r+")

        raw_coords = [line.rstrip('\n') for line in file]
        process_coords = []
        for coords in raw_coords:
            int_coords = [float(x) for x in coords.split()]
            process_coords.append(int_coords)
        missions[mission_name] = process_coords
    print(missions)
    return missions


#
#
# if __name__ == "__main__":
#     read_missions()
