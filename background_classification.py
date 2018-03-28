from skimage import color
from skimage import io
from skimage.util.dtype import dtype_range
from skimage import exposure
from skimage.color import rgb2lab, lab2lch

import cv2

colors = []
colors.append((70.96, -2.35, 55.16))
colors.append((78.09, -5.51, 64.32))
colors.append((82.47, -29.6, 61.83))
colors.append((72.71, -22.28, 60.315))

#definimos el lab de los colores de la tabla de forma manual para sistemas de prueba
#los colores de la tabla estan el el espacio de color LAB
#color1 = (70.96, -2.35, 55.16)
#color2 = (78.09, -5.51, 64.32)
#color3 = (82.47, -29.6, 61.83)
#color4 = (72.71, -22.28, 60.315)

import numpy as np

def distancia_color(imagen_lab, color_id):
  return color.deltaE_ciede2000(imagen_lab,colors[color_id])

def analisis_distancia(matriz,dimensiones,largo, mask):
  elementos = 0
  for j in range(0,largo):
    for x in range(0,dimensiones):
      elementos = elementos + matriz[j][x]*mask[j][x]
  elementos = elementos / (largo * dimensiones)
  return elementos

def similitud_color(imagen, mask):
  imagen_lab = rgb2lab(imagen)
  dimensiones = len(imagen[0])
  distancia = []
  for i in range(len(colors)):
    matriz = distancia_color(imagen_lab, i)
    largo = len(matriz)
    distancia.append(analisis_distancia(matriz,dimensiones,largo, mask))
  return distancia

def establecer_color(distancia):
  deltaE    = 100
  resultado = -1
  for i in range(0,len(colors)):
    if distancia[i] < deltaE :
      deltaE = distancia[i]
  for i in range(0,len(colors)):
    if distancia[i] == deltaE:
      resultado = i
  return resultado

def getClassFromURL(url):
  imagen = io.imread(url)
  distancias = similitud_color(imagen)
  clase = establecer_color(distancias)
  return clase

def getClassFromImage(image, mask):
  mask = np.divide(mask, 255)
  distancias = similitud_color(image, mask)
  clase = establecer_color(distancias)
  return clase

def classify_color(color):
  [[color]] = rgb2lab([[color/255]])
  distancia = []
  for i in range(len(colors)):
    distancia.append(distancia_color(color, i))
  min_val = min(distancia)
  idx = distancia.index(min_val)
  return(get_color_class(idx))

def classify_color_rgb(color):
  colors = []
  colors.append((192, 173, 67))
  colors.append((209, 194, 63))
  colors.append((176, 219, 78))
  colors.append((163, 189, 55))
  distancia = []
  for i in range(len(colors)):
    d = np.linalg.norm(colors[i]-color)
    distancia.append(d)
  min_val = min(distancia)
  idx = distancia.index(min_val)
  return(get_color_class(idx))

color_list = {
  0: 'Crema',
  1: 'Amarillo',
  2: 'Verde',
  3: 'Verde crema'
}

def get_color_class(idx):
  return color_list[idx]

if __name__ == "__main__":
  clase = getClassFromURL("1.jpg")
  print("La imagen corresponde a la clase ", clase+1)
