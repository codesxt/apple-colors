from sklearn.cluster import KMeans
#import matplotlib.pyplot as plt
import argparse
import cv2
import numpy as np

N_CLUSTERS = 3
def centroid_histogram(clt):
  # grab the number of different clusters and create a histogram
  # based on the number of pixels assigned to each cluster
  numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
  (hist, _) = np.histogram(clt.labels_, bins = numLabels)
  # normalize the histogram, such that it sums to one
  hist = hist.astype("float")
  hist /= hist.sum()
  # return the histogram
  return hist

def plot_colors(hist, centroids):
  # initialize the bar chart representing the relative frequency
  # of each of the colors
  bar = np.zeros((50, 300, 3), dtype = "uint8")
  startX = 0
  # loop over the percentage of each cluster and the color of
  # each cluster
  for (percent, color) in zip(hist, centroids):
    # plot the relative percentage of each cluster
    endX = startX + (percent * 300)
    cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
      color.astype("uint8").tolist(), -1)
    startX = endX
  # return the bar chart
  return bar

def filter_colors(hist, centroids):
  # Filter black from histogram
  new_hist = []
  new_centroids = []
  for (percent, color) in zip(hist, centroids):
    if(color[0]>50 or color[1]>50 or color[2]>50):
      new_hist.append(percent)
      new_centroids.append(color)
  new_hist = [x / sum(new_hist) for x in new_hist]
  return(new_hist, new_centroids)

def get_dominant_colors(image):
  image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  #plt.figure()
  #plt.axis("off")
  #plt.imshow(image)
  #plt.show()
  image = image.reshape((image.shape[0] * image.shape[1], 3))
  clt = KMeans(n_clusters = N_CLUSTERS)
  clt.fit(image)
  # build a histogram of clusters and then create a figure
  # representing the number of pixels labeled to each color
  hist = centroid_histogram(clt)
  (hist, colors) = filter_colors(hist, clt.cluster_centers_)
  bar = plot_colors(hist, colors)
  return(hist, colors, bar)
