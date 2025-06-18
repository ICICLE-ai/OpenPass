#!/usr/bin/python3

import sys
from ImgManager import ImgManager

try:
    src = sys.argv[1]    
except:
    src = 'edge'

img_manager = ImgManager(src)
img_manager.startStream()
