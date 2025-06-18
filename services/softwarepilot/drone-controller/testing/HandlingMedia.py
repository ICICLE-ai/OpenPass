import cv2
import numpy as np
import math
import time
import queue
import olympe
import os
from AnafiController import AnafiController


class RedTracker:
	def __init__(self, drone):
		self.drone = drone
		self.media = drone.camera.media
		
	def yuv_frame_processing(self):
		while self.media.running:
			try:
				yuv_frame = self.media.frame_queue.get(timeout=0.1)
				self.media.frame_counter += 1
				'''
				if (self.media.frame_counter % 20) == 0:
					# the VideoFrame.info() dictionary contains some useful information
					# such as the video resolution
					info = yuv_frame.info()

					height, width = (  # noqa
					    info["raw"]["frame"]["info"]["height"],
					    info["raw"]["frame"]["info"]["width"],
					)

					# yuv_frame.vmeta() returns a dictionary that contains additional
					# metadata from the drone (GPS coordinates, battery percentage, ...)

					# convert pdraw YUV flag to OpenCV YUV flag
					cv2_cvt_color_flag = {
						olympe.VDEF_I420: cv2.COLOR_YUV2BGR_I420,
						olympe.VDEF_NV12: cv2.COLOR_YUV2BGR_NV12,
					}[yuv_frame.format()]

					cv2frame = cv2.cvtColor(yuv_frame.as_ndarray(), cv2_cvt_color_flag)
					#cv2.imwrite(os.path.join(self.drone.download_dir, "test{}.jpg".format(self.media.frame_counter)), cv2frame)
				'''
			except queue.Empty:
				continue
		
			# You should process your frames here and release (unref) them when you're done.
			# Don't hold a reference on your frames for too long to avoid memory leaks and/or memory
			# pool exhaustion.
			yuv_frame.unref()	
	
if __name__ == "__main__":
	
	drone = AnafiController(1, "None")
	redTracker = RedTracker(drone)
	drone.connect()
	
	drone.camera.media.setup_stream(yuv_frame_processing = redTracker.yuv_frame_processing)
	
	#drone.piloting.takeoff()
	
	drone.camera.media.start_stream()
	
	time.sleep(1000)
	
	drone.camera.media.stop_stream()
	
	#drone.piloting.land()
	
	drone.disconnect()

