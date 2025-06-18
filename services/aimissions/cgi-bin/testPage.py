import urllib.request

from Helper.PodAddress import getPodAddress

i1212aimissions_ipaddr = getPodAddress('i1212aimissions')

img_name = 'people2.jpg'
download_name = 'test.jpg'
target_label = 'person'
offset = 'True'
correction_alt = '2.0'

#target = 'teddy%20bear'

response = urllib.request.urlopen(f'http://{i1212aimissions_ipaddr}:1212/cgi-bin/runYolo.py?&p1={img_name}&p2={download_name}&p3={target_label}&p4={offset}&p5={correction_alt}')


data = response.read()
decoded_data = data.decode('utf-8') 

print(decoded_data)
