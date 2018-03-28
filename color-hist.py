import numpy as np
import cv2
from matplotlib import pyplot as plt
import argparse

parser = argparse.ArgumentParser(description='Display color histograms of an image.')
parser.add_argument('--image', '-i', help='Image to process.')
args = parser.parse_args()

image_file = args.image

image   = cv2.imread(image_file)
hsv     = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

color = ('B','G','R')
plt.subplot(2, 1, 1)
plt.title('Histogramas del archivo: ' + image_file)
for i,col in enumerate(color):
  histr = cv2.calcHist([image], [i], None, [256], [0,256])
  plt.plot(histr, color = col, label = col)
  plt.xlim([0,256])
plt.legend()
plt.ylabel('Frecuencia')
plt.xlabel('Valor R/G/B')

plt.subplot(2, 1, 2)
hsv_colors = ('red','goldenrod','cadetblue')
labels = ['H', 'S', 'V']
for i,col in enumerate(hsv_colors):
  histr = cv2.calcHist([hsv], [i], None, [256], [0,256])
  plt.plot(histr, color = col, label = labels[i])
  plt.xlim([0,256])
plt.legend()
plt.ylabel('Frecuencia')
plt.xlabel('Valor H/S/V')
plt.show()

#cv2.imshow('Imagen', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
