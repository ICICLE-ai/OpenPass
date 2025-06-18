base_path = '/opt/bitnami/apache'
htdocs_path = f'{base_path}/htdocs'
cgi_path = f'{base_path}/cgi-bin'
userfiles_path = f'{htdocs_path}/userfiles'
mscopy_path = f'{htdocs_path}/mscopy'

repo_path = f'{htdocs_path}/repo'
result_path = f'{htdocs_path}/result'
zipDir_path = f'{htdocs_path}/zipDir'

in_file = 'model_in.jpg'
out_file = 'model_out.jpg'
in_path = f'{repo_path}/{in_file}'
out_path = f'{result_path}/{out_file}'

supported_ms = {
    'openpass': {'port': 54292, 'name': 'i54292openpass'},
    'phone': {'port': 4242, 'name': 'i4242phonehub', 'path': '/opt/bitnami/apache/htdocs/userfiles/result'}
}

test_images_path = '/home/icicle/icicleEdgeOld/aimissions/TestImages'
wooloo_path = f'{test_images_path}/wooloo.jpg' 
people_path = f'{test_images_path}/people.jpg'

flask_pid_path = f'{cgi_path}/Flask.pid'