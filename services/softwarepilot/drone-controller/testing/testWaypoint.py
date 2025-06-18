from AnafiController import AnafiController
import time

drone = AnafiController()

drone.connect()
drone.piloting.takeoff()

drone.piloting.move_to(40.00934600000012, -83.01677883333323, 5, "NONE", 0, True)
#drone.piloting.move_to(40.00934600000012, -83.01677883333323, 5)

drone.disconnect()


