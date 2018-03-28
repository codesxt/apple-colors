import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import itemfreq

def get_dominant_color(img):
  average_color = [img[:, :, i].mean() for i in range(img.shape[-1])]

  arr = np.float32(img)
  pixels = arr.reshape((-1, 3))

  n_colors = 5
  criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
  flags = cv2.KMEANS_RANDOM_CENTERS
  _, labels, centroids = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)

  palette = np.uint8(centroids)
  quantized = palette[labels.flatten()]
  quantized = quantized.reshape(img.shape)

  dominant_color = palette[np.argmax(itemfreq(labels)[:, -2])]

  color = (dominant_color[2], dominant_color[1], dominant_color[0])
  print(centroids)
  print(color)

  plt.imshow([[color]])
  plt.show()

  plt.imshow(cv2.cvtColor(quantized, cv2.COLOR_BGR2RGB))
  plt.show()
