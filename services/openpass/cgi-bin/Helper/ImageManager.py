import os
import stat
import shutil
import glob
import time

class ImageManager:
    def __init__(self, folder_name, src='edge'):
        if src == 'local':
            self.userfiles_path = '/home/icicle/icicleEdge/openpasswebsite'
            self.zip_sublink = '/home/icicle/icicleEdge/openpasswebsite/'
            self.photo_sublink = f'/home/icicle/icicleEdge/openpasswebsite/{folder_name}/'
        else:
            self.userfiles_path = '/opt/bitnami/apache/htdocs/userfiles'
            self.zip_sublink = f'http://10.43.195.204:30080/cgi-bin/callms.py?ms=i54292openpass&port=54292&path=/userfiles/&state=user&code=None&page='
            self.photo_sublink = f'http://10.43.195.204:30080/cgi-bin/callms.py?ms=i54292openpass&port=54292&path=/userfiles/{folder_name}/&state=user&code=None&page='

        self.folder_name = folder_name
        self.folder_path = f'{self.userfiles_path}/{self.folder_name}'

    def getPath(self):
        return self.folder_path

    def reset(self):
        if os.path.exists(self.folder_path):
            self.remove_folder()
        if os.path.exists(f'{self.folder_path}.zip'):
            os.remove(f'{self.folder_path}.zip')

        try:
            # Create the folder (including intermediate directories if necessary)
            os.makedirs(self.folder_path, exist_ok=True)
            #print(f"<br>== Folder '{self.folder_path}' created or already exists ==")

            # Define the desired permissions (e.g., read/write/execute for owner, read/execute for group and others)
            permissions = stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO  # 0o777

            # Change the permissions of the folder
            os.chmod(self.folder_path, permissions)
            #print(f"<br>== Permissions for '{self.folder_path}' set to {oct(permissions)} ==")

        except Exception as e:
            print(f"An error occurred: {e}")

    def remove_folder(self):
        shutil.rmtree(self.folder_path)

    def display_image(self, filename):
        filepath = f'{self.photo_sublink}{filename}'
        result = f'<br>== Displaying Image {filename} =='
        result += f'<br><img src="{filepath}" alt="{filename}">'
    
        return result

    def display_all_images(self):
        pattern = os.path.join(self.folder_path, '*.jpg')
        jpg_files = glob.glob(pattern)
        
        result = ''
        for jpg_file in jpg_files:
            filename = os.path.basename(jpg_file)
            filepath = f'{self.photo_sublink}{filename}'
            result += f'<br>== Displaying Image {filename} =='
            result += f'<br><img src="{filepath}" alt="{filename}">'
        
        return result
            
    def link_download_zip(self, output_name):
        output_path = f'{self.userfiles_path}/{output_name}'
        shutil.make_archive(output_path, 'zip', self.folder_path)
        download_link = f'{self.zip_sublink}{output_name}'
        result = f'<br><br><a href="{download_link}.zip" download="{output_name}.zip">Click to Download Images</a>'

        return result

# Example usage:
if __name__ == "__main__":
    # Define the path for the new folder
    folder_name = 'TestFolder'
    folder_path = f'/home/icicle/icicleEdge/openpasswebsite/{folder_name}'

    # Create an instance of MissionImages
    mission_images = ImageManager(folder_name, src='local')
    shutil.copyfile('/home/icicle/icicleEdge/openpasswebsite/cgi-bin/Repo/testImage.jpg', f'{folder_path}/testImage.jpg')
    shutil.copyfile('/home/icicle/icicleEdge/openpasswebsite/cgi-bin/Repo/wooloo.jpg', f'{folder_path}/wooloo.jpg')
    time.sleep(1)
    print(mission_images.display_all_images())
    print(mission_images.link_download_zip('TestImages'))
    
