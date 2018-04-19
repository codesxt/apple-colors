import numpy as np
import cv2
from matplotlib import pyplot as plt
import argparse

def build_red_mask(image_hsv):
    h, s, v = cv2.split(image_hsv)
    ret, mh = cv2.threshold(h, 325/2, 255, cv2.THRESH_BINARY)       # Mayor al primer valor
    ret, mn = cv2.threshold(h, 360/2, 255, cv2.THRESH_BINARY_INV)   # Menor al segundo valor
    mh      = cv2.bitwise_and(mh, mn)
    ret, mh2= cv2.threshold(h, 0/2, 255, cv2.THRESH_BINARY)       # Mayor al primer valor
    ret, mn2= cv2.threshold(h, 10/2, 255, cv2.THRESH_BINARY_INV)   # Menor al segundo valor
    mh2     = cv2.bitwise_and(mh2, mn2)
    mh      = cv2.bitwise_or(mh, mh2)
    mask    = cv2.merge((mh,mh,mh))
    return mask

parser = argparse.ArgumentParser(description='Threshold color channels of an image.')
parser.add_argument('--image', '-i', help='Image to process.')
args = parser.parse_args()

image_file = args.image

image_o = cv2.imread(image_file)
hsv     = cv2.cvtColor(image_o, cv2.COLOR_BGR2HSV)

mask = build_red_mask(hsv)
# Now convolute with circular disc
disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
cv2.filter2D(mask,-1,disc,mask)

image_r = cv2.bitwise_and(image_o, mask)

plt.subplot(221)
plt.axis('off')
plt.imshow(cv2.cvtColor(image_o, cv2.COLOR_BGR2RGB))
plt.title('Imagen Original')

plt.subplot(222)
plt.axis('off')
plt.imshow(mask, 'gray')
plt.title('Máscara')

plt.subplot(223)
plt.axis('off')
plt.imshow(cv2.cvtColor(image_r, cv2.COLOR_BGR2RGB))
plt.title('Imagen Resultante')

image_g = cv2.bitwise_and(image_o, cv2.bitwise_not(mask))
plt.subplot(224)
plt.axis('off')
plt.imshow(cv2.cvtColor(image_g, cv2.COLOR_BGR2RGB))
plt.title('Imagen Resultante Invertida')



plt.show()
