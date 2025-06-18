from Models.Yolo import Yolo

model = Yolo('corn_best.pt')

bounding_box, offset_x, offset_y, img_shape = model.objectInference('TestImages/corn2.jpg', 'TestImages/result_corn.jpg')

print(bounding_box)

print(f'{offset_x}   {offset_y}')

print(img_shape)