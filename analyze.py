import numpy as np
import cv2
from matplotlib import pyplot as plt
import argparse
from background_classification import *
from intensity_classification import *
from dominant_color import *

parser = argparse.ArgumentParser(description='Histogram backprojection according to: https://docs.opencv.org/3.3.1/dc/df6/tutorial_py_histogram_backprojection.html.')
parser.add_argument('--image', '-i', help='Image to process.')
parser.add_argument('--reference', '-r', help='Image to use as color reference.')
args = parser.parse_args()

target_image    = args.image
reference_image = args.reference

roi = cv2.imread(reference_image)
hsv = cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)

target = cv2.imread(target_image)
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

print('Color de Cubrimiento: {0:.2f} % del área'.format(white/total*100))

#bacgkround_category = getClassFromImage(cv2.cvtColor(green_area, cv2.COLOR_BGR2RGB), cv2.bitwise_not(original_thresh))
#print('Categoría del Fondo: {} '.format(bacgkround_category))

#get_dominant_color(green_area)
import kmeans_colors as km
print('Análisis de color de fondo:')
(hist, colors, bar) = km.get_dominant_colors(green_area)
for idx, color in enumerate(colors):
  #print(classify_color(color))
  print(idx, hist[idx], classify_color_rgb(color), color)

#get_foreground_intensity(cv2.cvtColor(red_area, cv2.COLOR_BGR2RGB))

print('Análisis de color de cubrimiento:')
(hist_red, colors_red, bar_red) = km.get_dominant_colors(red_area)
for idx, color in enumerate(colors_red):
  print(idx, hist_red[idx], classify_color_intensity_rgb(color[0], color[1], color[2]), color)

# Show color bar
#plt.figure()
#plt.axis("off")
#plt.imshow(bar)
#plt.show()

#plt.axis("off")
#plt.imshow(cv2.cvtColor(stacked, cv2.COLOR_BGR2RGB))
#plt.show()

plt.subplot(3, 1, 1)
plt.title('Resultados del análisis')
plt.imshow(cv2.cvtColor(stacked, cv2.COLOR_BGR2RGB))
plt.subplot(3, 1, 2)
plt.axis('off')
plt.imshow(bar)
plt.subplot(3, 1, 3)
plt.axis('off')
plt.imshow(bar_red)
plt.show()
