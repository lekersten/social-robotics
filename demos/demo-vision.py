from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep
import cv2 as cv # the OpenCV library (computer vision)
import numpy as np

def vision(frame):
	# This function is called each time the robot sees a change in the camera

	frame_single = frame["data"]["body.head.eyes"] # collecting the data from the stream
	image_np = np.frombuffer(frame_single, np.uint8) # read the information from the single frame
	img_np = cv.imdecode(image_np, cv.IMREAD_COLOR) # decodes the image using the OpenCV library
	# print(frame_single)
	cv.imshow('frame', img_np) # send it to the display
	cv.waitKey(1)


@inlineCallbacks
def main(session, details):
	frames = yield session.call("rom.sensor.sight.read")
	frame_single = frames[0]["data"]
	print("Current sight:") # just checking what the robot sees in numbers....
	print("single=",frame_single["body.head.eyes"])
	print("frame=",frames)
	print("")

	# Here we subscribe the camera (sight) stream to the system in the function vision(stream)
	yield session.subscribe(vision, "rom.sensor.sight.stream")
	# and call the stream
	yield session.call("rom.sensor.sight.stream")


	# session.leave() # Close the connection with the robot



wamp = Component(
	transports=[{
		"url": "ws://wamp.robotsindeklas.nl",
		"serializers": ["msgpack"],
		"max_retries": 0
	}],
	realm="rie.65e85addd9eb6cfb396e548c",
)

wamp.on_join(main)

if __name__ == "__main__":
	run([wamp])