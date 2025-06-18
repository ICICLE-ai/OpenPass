import cv2
import numpy as np

def getGLI(image_path):
  # Read Image
  image = cv2.imread(image_path)
  # Separate Color Channels
  image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  # Calculate GLI
  R, G, B = cv2.split(image_rgb)
  R, G, B = np.mean(R), np.mean(G), np.mean(B)
  denominator = ((2 * G) + R + B)
  gli = np.where(denominator != 0, ((2 * G) - R - B) / denominator, 0)
  # Take the mean accross the image
  mean_gli = np.mean(gli)

  return mean_gli