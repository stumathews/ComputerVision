# Pull in imread from sk-image
from skimage.io import imread
from skimage.color import rgb2gray
from skimage.util import invert
# Pull in pyploy from matplotlib
import matplotlib.pyplot as plot
from skimage import data
from numpy.linalg import norm
import numpy as np
from scipy.ndimage import convolve
from skimage import io, color, img_as_float, img_as_ubyte
from skimage import io, color, filters
import math

cat = data.chelsea()
cat = color.rgb2gray(cat)

kx = 0.5 * np.array([-1, 0, 1]).reshape(3, 1)
ky = 0.5 * np.array([-1, 0, 1]).reshape(1, 3)

img_x = convolve(cat, kx)
img_y = convolve(cat, ky)

# Pair corresponding derivatives from x and y axis
img_grad = np.array(list(zip(img_x.flatten(), img_y.flatten())))

# Get image gradient magnitude, which is basically a combination of both derivatives
magnitude = np.array([math.sqrt(x*x + y*y) for x, y in img_grad]).reshape(cat.shape)

fig, ax = plot.subplots(1, 3, figsize=(14, 4))

ax[0].set_title('Derivative along x-axis')
ax[1].set_title('Derivative along y-axis')
ax[2].set_title('Image gradient')

ax[0].imshow(img_x, cmap='gray')
ax[1].imshow(img_y, cmap='gray')
ax[2].imshow(magnitude, cmap='gray')

plot.show()


# import math
# tens = [10, 20, 30, 40, 50]
# units = [1, 2, 3, 4, 5]
#
# zipped = list(zip(units, tens))
# ##zipped = [ ( x*x, y*y) for x, y in zipped]
# zipped = [ [math.sqrt(x*x + y*y)] for x, y in zipped]
# list_list = list(map(list, zipped))
# i = np.array(list_list)
# print(i.flatten())
# ##x_axis = i[:, 0]
# ##y_axis = i[:, 1]
# ##print(f'x_axis = {x_axis}, y-axis={y_axis}')