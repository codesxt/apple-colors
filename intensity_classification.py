import cv2
import numpy as np
from sklearn import linear_model

# #824f3d [130, 79, 61]
# #d56f87 [213, 111, 135]
# #c22e44 [194, 46, 68]

def get_foreground_intensity(image):
  image_hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
  h, s, v = cv2.split(image_hsv)
  h = h[np.nonzero(h)]
  s = s[np.nonzero(s)]
  v = v[np.nonzero(v)]
  hue = np.average(h)
  saturation = np.average(s)
  value = np.average(v)
  print(hue, saturation, value)
  classify_color_intensity(hue, saturation, value)

def classify_color_intensity(hue, saturation, value):
  red_x = [[15.65, 36.13, 37.45], [345.88, 47.89, 83.53], [351.08, 61.67, 47.06]]
  red_y = [0, 0.5, 1]
  regr = linear_model.LinearRegression()
  regr.fit(red_x, red_y)
  red_x_pred = [[hue, saturation, value]]
  print(regr.predict(red_x_pred))

def classify_color_intensity_rgb(r, g, b):
  red_x = [[231, 149, 134], [176, 52, 64]]
  red_y = [0, 1]
  regr = linear_model.LinearRegression()
  regr.fit(red_x, red_y)
  red_x_pred = [[r, g, b]]
  return(regr.predict(red_x_pred)[0])
