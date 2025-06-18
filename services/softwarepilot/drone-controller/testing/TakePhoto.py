from AnafiController import AnafiController
import time

drone = AnafiController()

drone.connect()
drone.camera.media.setup_photo()

drone.camera.media.take_photo()
drone.camera.media.download_last_media()
drone.camera.media.take_photo()
drone.camera.media.download_last_media()
drone.camera.media.take_photo()
drone.camera.media.download_last_media()
drone.camera.media.take_photo()
drone.camera.media.download_last_media()

drone.disconnect()


