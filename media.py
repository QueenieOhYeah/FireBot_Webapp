# Example program to download/delete images from drone.
# Media Not Yet Indexed error means usb still connected.
# http://192.168.42.1/data/media/100000040004.JPG

import olympe
import os
import re
import requests
import shutil
import tempfile
import xml.etree.ElementTree as ET


# Drone IP
def download():
	ANAFI_IP = "10.202.0.1"
	SKYCTRL_IP = "192.168.53.1"
	DRONE_IP = "192.168.42.1"
	# Drone web server URL
	ANAFI_URL = "http://{}/".format(DRONE_IP)
	# Drone media web API URL
	ANAFI_MEDIA_API_URL = ANAFI_URL + "api/v1/media/medias"

	# download the photos associated with this media id
	media_info_response = requests.get(ANAFI_MEDIA_API_URL)
	print("id : ", ANAFI_MEDIA_API_URL)
	media_info_response.raise_for_status() #check for error, should be in try except block?
	download_dir = 'static/images/'


	# media_info_response.json() is a list of media_id_dict
	# media_id_dict is a dict containing general info about that media_id as well as 'resources' dict which contains info on each image.
	# resource is a dict inside of the media
	for media_id_dict in media_info_response.json():
		for resource in media_id_dict["resources"]:
			print("Downloading ", ANAFI_URL + resource["url"])
			image_response = requests.get(ANAFI_URL + resource["url"], stream=True)
			image_response.raise_for_status()
			download_path = os.path.join(download_dir, resource["resource_id"])
			with open(download_path, "wb") as image_file:
				shutil.copyfileobj(image_response.raw, image_file)


			# print("Deleting ", ANAFI_URL + resource["url"])
			# ######### trying to delete returns HTTPerror: 400 bad request for url. ###############
			# image_response = requests.delete(ANAFI_MEDIA_API_URL + '/'+resource["media_id"], stream=True)
			# image_response.raise_for_status()

def metadata(download_path):
	ANAFI_IP = "10.202.0.1"
	SKYCTRL_IP = "192.168.53.1"
	DRONE_IP = "192.168.42.1"
	# Drone web server URL
	ANAFI_URL = "http://{}/".format(DRONE_IP)
	# Drone media web API URL
	ANAFI_MEDIA_API_URL = ANAFI_URL + "api/v1/media/medias"

	# download the photos associated with this media id
	media_info_response = requests.get(ANAFI_MEDIA_API_URL)
	print("id : ", ANAFI_MEDIA_API_URL)
	media_info_response.raise_for_status()  # check for error, should be in try except block?
	download_dir = 'static/images/'

	XMP_TAGS_OF_INTEREST = (
		"CameraRollDegree",
		"CameraPitchDegree",
		"CameraYawDegree",
		"CaptureTsUs",
		# NOTE: GPS metadata is only present if the drone has a GPS fix
		# (i.e. they won't be present indoor)
		"GPSLatitude",
		"GPSLongitude",
		"GPSAltitude",
	)

	with open(download_path, "rb") as image_file:
		image_data = image_file.read()
		image_xmp_start = image_data.find(b"<x:xmpmeta")
		image_xmp_end = image_data.find(b"</x:xmpmeta")
		image_xmp = ET.fromstring(image_data[image_xmp_start: image_xmp_end + 12])
		for image_meta in image_xmp[0][0]:
			xmp_tag = re.sub(r"{[^}]*}", "", image_meta.tag)
			xmp_value = image_meta.text
			# only print the XMP tags we are interested in
			if xmp_tag in XMP_TAGS_OF_INTEREST:
				print(resource["resource_id"], xmp_tag, xmp_value)