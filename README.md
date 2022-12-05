# Introduction
This is a prototype of a drone-based data collection system that focuses on collecting vegetation types under forest canopies. 
Considering that such data collections are conducted in scenarios without internet connection, this project provides a local web app as the user interface and the backend services are linked 
to the drone autonomy.

## Dependencies
The drone model used in the project for autonomy is Parrot Anafi AI. Therefore the code needs to be run together with this drone model and its controller.
The operating system requirement for Parrot SDKs(Olympe) is Ubuntu 20.04 or higher. The web app is built upon Flask framework.
<br />
<br />
Language: Python 3<br />
Installations on Olympe and its dependencies in a virtual enviroment: https://developer.parrot.com/docs/olympe/installation.html<br />
Installations on Flask: https://flask.palletsprojects.com/en/2.2.x/installation/<br />
Other dependencies: OpenCV<br />

## How to run
1. Turn on the drone and the controller.
2. Connect the controller to PC by USB and confirm the PC is connected to the controller through Ethernet.
3. Navigate to the project folder and do ```flask run``` in CLI.
4. Open the local web address.

## Notice
1. The drone functions with GPS signals so that do not run indoor.
2. Make sure your mission is well created based on your location before starting it.
3. Do safety check on your drone before taking off. 
