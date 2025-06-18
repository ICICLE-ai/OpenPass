# Import PyTorch module
import torch
import cv2
import math

import Helper.globals as globals

class Yolo:
    def __init__(self, weights='yolov5n.pt', draw=True):
        # Download model from github
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path=weights)
        self.draw = draw

    def Inference(self, target_label=None, offset='True', correction_alt=None):
        img_path = globals.in_path
        download_path = globals.out_path
        print(img_path)
        print(download_path)
        
        img, data_frame = self.inferenceHelper(img_path)

        response = self.resultHelper(img, data_frame, target_label, offset, correction_alt)

        cv2.imwrite(download_path, img)

        return response

    def inferenceHelper(self, img_path):
        img = cv2.imread(img_path)

        if img is None:
            raise Exception('Image path invalid')

        # Perform detection on image
        result = self.model(img)
    
        # Convert detected result to pandas data frame
        data_frame = result.pandas().xyxy[0]
        
        print('result: ', result)
        print('data_frame:')
        print(data_frame)

        return img, data_frame

    def resultHelper(self, img, data_frame, target_label, offset, correction_alt):
        indexes = data_frame.index
        img_shape = img.shape[:-1]

        detections = []
        if target_label is None:
            for index in indexes:
                
                detection = {
                    'label': data_frame['name'][index],
                    'confidence': data_frame['confidence'][index],
                }

                bounding_box = Yolo.boundObject(img, data_frame, index, self.draw)
                detection['bounding_box'] = bounding_box

                if offset=='True':
                    offset_x, offset_y = Yolo.calculatePixelOffset(img, bounding_box, img_shape, self.draw)
                    detection['offset'] = (offset_x, offset_y)
                
                    if correction_alt is not None:
                        meter_correction = Yolo.calculateMeterCorrection(offset_x, offset_y, img_shape, float(correction_alt))
                        detection['meter_correction'] = meter_correction
        
                detections.append(detection)
        
        response = {
            'result': True,
            'values': detections
        }

        return response

    '''
    def boundHelper(img, data_frame, target_label, offset):
        indexes = data_frame.index
        
        if target_label is None:
            if offset == 'True':
                img_shape = img.shape[:-1]
                for index in indexes:
                    bounding_box = Yolo.boundObject(img, data_frame, index)
                    Yolo.calculatePixelOffset(img, bounding_box, img_shape)
            else:
                for index in indexes:
                    Yolo.boundObject(img, data_frame, index)
        else:    
            if offset == 'True':
                img_shape = img.shape[:-1]
                for index in indexes:
                    label = data_frame['name'][index]
                    if label == target_label:
                        bounding_box = Yolo.boundObject(img, data_frame, index)
                        offset_x, offset_y = Yolo.calculatePixelOffset(img, bounding_box, img_shape)
                        break
                
                result = {
                    'bounding_box': bounding_box,
                    'offset': (offset_x, offset_y)
                }
                return result

            else:
                for index in indexes:
                    label = data_frame['name'][index]
                    if label == target_label:
                        bounding_box = Yolo.boundObject(img, data_frame, index)
                        break
                
                result = {
                    'bounding_box': bounding_box
                }
                return result
            
        return None
    '''

    # Returns inference on objects in the image
    def objectInference(self, img_path, download_path, target_label=None):
        img = cv2.imread(img_path)

        if img is None:
            print('Invalid path:', img_path)
        else:
            img_shape = img.shape[:-1]

            # Perform detection on image
            result = self.model(img)
            print('result: ', result)

            # Convert detected result to pandas data frame
            data_frame = result.pandas().xyxy[0]
            print('data_frame:')
            print(data_frame)

            # Bound all objects or the target object
            indexes = data_frame.index
            if target_label is None:
                for index in indexes:
                    bounding_box = Yolo.boundObject(img, data_frame, index)
                    Yolo.calculatePixelOffset(img, bounding_box, img_shape, self.draw)
                cv2.imwrite(download_path, img)
                return None, None, None, img_shape
            
            else:
                for index in indexes:
                    label = data_frame['name'][index]
                    if label == target_label:
                        bounding_box = Yolo.boundObject(img, data_frame, index)
                        offset_x, offset_y = Yolo.calculatePixelOffset(img, bounding_box, img_shape, self.draw)
                        break

                cv2.imwrite(download_path, img)
                return bounding_box, offset_x, offset_y, img_shape
            
            #cv2.imshow('IMAGE', img)
            #cv2.waitKey(0)

    # Calculates a bounding box around the object
    def boundObject(img, data_frame, index, draw):

        # Find the coordinate of top left corner of bounding box
        x1 = int(data_frame['xmin'][index])
        y1 = int(data_frame['ymin'][index])
        # Find the coordinate of right bottom corner of bounding box
        x2 = int(data_frame['xmax'][index])
        y2 = int(data_frame['ymax'][index ])

        if draw:
            # Find confidance score of the model
            conf = data_frame['confidence'][index]
            
            label = data_frame['name'][index]
            text = label + ' ' + str(conf.round(decimals= 2))

            # Draw bounding box and prediction around each object
            cv2.rectangle(img, (x1,y1), (x2,y2), (255,255,0), 2)
            cv2.putText(img, text, (x1,y1-5), cv2.FONT_HERSHEY_PLAIN, 2,
                        (255,255,0), 2)
        
        bounding_box = (x1, y1, x2, y2)
        return bounding_box

    # Calculates the object's pixel offset from the center of the image
    def calculatePixelOffset(img, bounding_box, img_shape, draw=True):
        (x1, y1, x2, y2) = bounding_box

        #Calculate object center
        width = x2-x1
        height= y2-y1
        obj_center_x = x1+width//2
        obj_center_y = y1+height//2
        
        #Calculate image center
        img_center_x = img_shape[1]//2
        img_center_y = img_shape[0]//2

        #Calculate offset
        offset_x = obj_center_x - img_center_x
        offset_y = obj_center_y - img_center_y

        if draw:
            #Draw object center
            cv2.rectangle(img, (obj_center_x-25, obj_center_y), (obj_center_x+25, obj_center_y), (255,0,0), 2)
            cv2.rectangle(img, (obj_center_x, obj_center_y-25), (obj_center_x, obj_center_y+25), (255,0,0), 2)       

            #Draw image center
            cv2.rectangle(img, (img_center_x-25, img_center_y), (img_center_x+25, img_center_y), (0,0,255), 2)
            cv2.rectangle(img, (img_center_x, img_center_y-25), (img_center_x, img_center_y+25), (0,0,255), 2)

            #Draw object offset
            cv2.rectangle(img, (obj_center_x, obj_center_y), (img_center_x, obj_center_y), (0,255,0), 2)
            cv2.rectangle(img, (img_center_x, obj_center_y), (img_center_x, img_center_y), (0,255,0), 2)

        return offset_x, offset_y

    # Calculates the necesary correction in meters to center the object (assumes bird's eye view)
    def calculateMeterCorrection(offset_x, offset_y, shape, altitude):
        LENGTH_ANGLE = math.radians(75)
        WIDTH_ANGLE = math.radians(30)

        x_max = 2 * altitude * math.tan(LENGTH_ANGLE/2)
        y_max = 2 * altitude * math.tan(WIDTH_ANGLE/2)
        
        x_mpp = x_max/shape[1]
        y_mpp = y_max/shape[0]
        
        x_meter_correction = offset_x * x_mpp
        y_meter_correction = offset_y * y_mpp

        # Convert to drone format (swap x and y, invert x)
        # Image: Top Left is 0, 0 | x is side to side | y is top to bottom
        # Drone: Drone is 0, 0 | x is forwards and backwards | y is side to side
        correction_x = y_meter_correction
        correction_y = -1*x_meter_correction

        return correction_x, correction_y
