# Import PyTorch module
import os
import torch
import shutil
import subprocess
import pandas as pd

import Helper.globals as globals

class PhoneYolo:
    def __init__(self, weights='yolov5n.pt', default_label=None):
        # Download model from github
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path=weights)
        self.weights = weights
        self.default_label = default_label

    def Inference(self, src_folder=None):
        print(src_folder)
        if src_folder:
            source_path = f'{globals.repo_path}/{src_folder}'
        else:
            source_path = globals.repo_path
        download_path = f"{globals.result_path}/predictions.csv"
        print(source_path)
        print(download_path)
        
        #cache_dir = torch.hub.get_dir()
        cache_dir = '/.cache/torch/hub'
        yolov5_dir = os.path.join(cache_dir, "ultralytics_yolov5_master")
        detect_script = os.path.join(yolov5_dir, "detect.py")
        
        exp_dir = os.path.join(yolov5_dir, 'runs/detect/exp')
        if os.path.exists(exp_dir):
            shutil.rmtree(exp_dir)

        print("\n\n== Running inference with detect.py ==")
        # Run detect.py
        subprocess.run([
            "python3", detect_script,
            "--weights", self.weights,
            "--img", "416",
            "--conf", "0.4",
            "--source", source_path,
            "--save-csv"
        ])
        print('\n\n==Inference finished==')

        csv_file = os.path.join(exp_dir, 'predictions.csv')
        if os.path.exists(csv_file):
            shutil.copy(csv_file, download_path)
            os.chmod(download_path, 0o777)
            print("\n\n== Copying results to user accessible directory ==")
        else:
            print("\n\n== Results not found ==")
        
        results_df = pd.read_csv(download_path) #, names=['file_name', 'label', 'confidence'])
        
        if self.default_label:
            print('\n\n== Populating default values For empty detections ==')
            images_with_detections = results_df['Image Name'].tolist()
            all_images = os.listdir(source_path)
            images_without_detections = [f for f in all_images if f not in images_with_detections]

            #No Detections = nd
            nd_names = images_without_detections
            nd_labels = [self.default_label]*len(nd_names)

            nd_rows = pd.DataFrame({'Image Name': nd_names, 'Prediction': nd_labels})

            results_df = pd.concat([results_df, nd_rows], ignore_index=True)
        
        #print(results_df)
        results_df.to_csv(download_path)

        response = {}
        print('\n\n== Reading detections ==')
        for index, row in results_df.iterrows():
            image_name = row['Image Name']
            label = row['Prediction']
            confidence = row['Confidence']
            
            response[image_name] = {'Prediction': label, 'Confidence': confidence}

        print()
        print(response)

        return response