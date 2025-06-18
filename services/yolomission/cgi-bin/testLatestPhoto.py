#!/usr/bin/python3

import sys
from Helper.ImgManager import ImgManager

try:
    src = sys.argv[1]    
except:
    src = 'edge'

img_manager = ImgManager(src, reset=True)
img_manager.getLatestStream(1, "test")
img_manager.getLatestStream(2, "wack")

