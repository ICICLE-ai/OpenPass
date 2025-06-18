#!/usr/bin/python3

import sys
from Helper.IpAddress import getIpAddress

src = 'i43210asu'
try:
    src = sys.argv[1]    
except:
    pass

ip_address = getIpAddress(src)

print(ip_address)