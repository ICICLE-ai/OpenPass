#!/usr/bin/python3

import sys
from ImgManager import ImgManager

try:
    src = sys.argv[1]    
except:
    src = 'edge'

img_manager = ImgManager(src)

data0 = "{'time':0, 'coordinates':[500.0, 500.0, 500.0], 'path':repo/testImage.jpg}"
data1 = "{'time':1, 'coordinates':[500.0, 500.0, 500.0], 'path':repo/testImage.jpg}"


img_manager.updatePhotoFile(0, data0)
img_manager.updatePhotoFile(1, data1)

