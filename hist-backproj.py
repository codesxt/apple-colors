import numpy as np
import cv2
from matplotlib import pyplot as plt
import argparse

parser = argparse.ArgumentParser(description='Histogram backprojection according to: https://docs.opencv.org/3.3.1/dc/df6/tutorial_py_histogram_backprojection.html.')
parser.add_argument('--image', '-i', help='Image to process.')
parser.add_argument('--reference', '-r', help='Image to use as color reference.')
args = parser.parse_args()

target_image    = args.image
reference_image = args.reference

roi = cv2.imread(reference_image)
hsv = cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)

#plt.axis("off")
#plt.imshow(cv2.cvtColor(roi, cv2.COLOR_BGR2RGB))
#plt.show()

target = cv2.imread(target_image)
hsvt   = cv2.cvtColor(target,cv2.COLOR_BGR2HSV)

# calculating object histogram
roihist = cv2.calcHist([hsv],[0, 1], None, [180, 256], [0, 180, 0, 256])
# normalize histogram and apply backprojection
cv2.normalize(roihist,roihist,0,255,cv2.NORM_MINMAX)
dst = cv2.calcBackProject([hsvt],[0,1],roihist,[0,180,0,256],1)

#plt.axis("off")
#plt.imshow(cv2.merge((dst,dst,dst)))
#plt.show()

# Now convolute with circular disc
disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
cv2.filter2D(dst,-1,disc,dst)
# threshold and binary AND
ret,thresh = cv2.threshold(dst,50,255,0)
thresh = cv2.merge((thresh,thresh,thresh))

#plt.axis("off")
#plt.imshow(thresh)
#plt.show()

red_area = cv2.bitwise_and(target, thresh)
green_area = cv2.bitwise_and(target, cv2.bitwise_not(thresh))

#plt.axis("off")
#plt.imshow(cv2.cvtColor(red_area, cv2.COLOR_BGR2RGB))
#plt.show()

dst = cv2.merge((dst, dst, dst))
stacked = np.hstack((target, thresh, red_area, green_area))

plt.axis("off")
plt.imshow(cv2.cvtColor(stacked, cv2.COLOR_BGR2RGB))
plt.show()
