import numpy as np
import cv2
from background_classification import *
from intensity_classification import *

def limit_resolution(image):
  limit_h = 480
  limit_w = 640
  img_h = image.shape[0]
  img_w = image.shape[1]
  if(img_h > img_w):
    scale = limit_h/img_h
  else:
    scale = limit_w/img_w
  image = cv2.resize(image, None, fx=scale, fy=scale, interpolation = cv2.INTER_LINEAR)
  return image

def analyze_apples(image_file, image_template):
  target_image    = image_file
  reference_image = image_template

  roi = cv2.imread(reference_image)
  hsv = cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)

  target = cv2.imread(target_image)
  target = limit_resolution(target)
  hsvt   = cv2.cvtColor(target,cv2.COLOR_BGR2HSV)

  # calculating object histogram
  roihist = cv2.calcHist([hsv],[0, 1], None, [180, 256], [0, 180, 0, 256])
  # normalize histogram and apply backprojection
  cv2.normalize(roihist,roihist,0,255,cv2.NORM_MINMAX)
  dst = cv2.calcBackProject([hsvt],[0,1],roihist,[0,180,0,256],1)

  # Now convolute with circular disc
  disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
  cv2.filter2D(dst,-1,disc,dst)
  # threshold and binary AND
  ret,thresh = cv2.threshold(dst,50,255,0)
  original_thresh = thresh
  thresh = cv2.merge((thresh,thresh,thresh))

  red_area = cv2.bitwise_and(target, thresh)
  green_area = cv2.bitwise_and(target, cv2.bitwise_not(thresh))

  dst = cv2.merge((dst, dst, dst))
  stacked = np.hstack((target, thresh, red_area, green_area))

  white = original_thresh.ravel().sum()/255
  total = original_thresh.ravel().shape[0]

  result = {}
  result['coverage_area'] = '{0:.2f}'.format(white/total*100)
  result['background_colors'] = []
  result['foreground_colors'] = []

  print('Color de Cubrimiento: {0:.2f} % del área'.format(white/total*100))

  import kmeans_colors as km
  print('Análisis de color de fondo:')
  (hist, colors, bar) = km.get_dominant_colors(green_area)
  for idx, color in enumerate(colors):
    print(idx, hist[idx], classify_color_rgb(color), color)
    result['background_colors'].append(
        {
            'percentage': hist[idx],
            'class': classify_color_rgb(color),
            'color': color
        }
    )

  print('Análisis de color de cubrimiento:')
  (hist_red, colors_red, bar_red) = km.get_dominant_colors(red_area)
  for idx, color in enumerate(colors_red):
    print(idx, hist_red[idx], classify_color_intensity_rgb(color[0], color[1], color[2]), color)
    result['foreground_colors'].append(
        {
            'percentage': hist_red[idx],
            'score': classify_color_intensity_rgb(color[0], color[1], color[2]),
            'color': color
        }
    )

  return(result)
