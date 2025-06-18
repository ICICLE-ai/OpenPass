#!/usr/bin/python3

import sys

from BaseMission import BaseMission

sys.path.append('/opt/bitnami/apache/cgi-bin')
from Helper.AIManager import AIManager

mission = BaseMission()

def fullMission():
    #image_folder = 'flyYoloImg'
    #model_name = 'Yolo'
    image_folder = sys.argv[2]
    model_name = sys.argv[4]
    model_weights = sys.argv[5]

    mission.writef('<br><br>== Setup ==')
    ai = AIManager(image_folder)
    mission.writef(ai.Setup(model_name, model_weights))

    mission.baseStart(takeoff=False)

    # == Inference ==
    mission.writef('<br><br>== Running Inference ==')
    result, file, header = ai.Inference('start.jpg', 'inference.jpg')
    mission.writef(result)
    mission.writef(mission.timed(mission.images.display_image, ['inference.jpg']))
    #for i in range(10):
    #    mission.writef(f'<br><br>== Downloading Image {i} ==')
    #    mission.download_and_display_image(f'stream_{i}.jpg', wait=False)
    #    time.sleep(1)
    # == Inference ==

    mission.baseEnd(takeoff=False)
    if mission.enableDigitalAgriculture():
        parameters = mission.enableDigitalAgriculture()
        mission.upload_folder(parameters[1], parameters[2], parameters[3])

#fullMission()
mission.run(fullMission)