import os
import time
import urllib.request
from urllib.error import HTTPError

def getDecodedResponse(url):
  set_response = urllib.request.urlopen(url)
  data = set_response.read()
  decoded_data = data.decode('utf-8') 
  return decoded_data

def pullFile(src_url, dst_path):
  old_file_size, new_file_size = 0, 0

  while (not os.path.exists(dst_path)) or (old_file_size == 0) or (old_file_size < new_file_size):
    try:
      file, _ = urllib.request.urlretrieve(src_url, dst_path)
      old_file_size = new_file_size
      new_file_size = os.path.getsize(dst_path)
      time.sleep(1)
    except HTTPError as e:
      time.sleep(1)
