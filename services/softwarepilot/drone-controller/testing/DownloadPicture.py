from AnafiController import AnafiController
import time

drone = AnafiController()

drone.connect()
drone.camera.media.setup_stream()

drone.camera.media.start_stream()

time.sleep(1000)

drone.camera.media.stop_stream()

drone.disconnect()


