from skimage import io, img_as_float, img_as_ubyte
import matplotlib.pyplot as plt
import numpy as np
from skimage import io, color, filters
import numpy as np
from skimage import color, img_as_float, img_as_ubyte
from numpy import where
# load in the picture
img = io.imread('OnTheBeach.png')

# Get rid of some of the detail
img = img_as_ubyte(filters.gaussian(img, sigma=1))
rows, cols, _ = img.shape

# Segmentation map
img_seg = np.ndarray([rows, cols])

for r in range(rows):
    for c in range(cols):
        red = img[r][c][0]
        green = img[r][c][1]
        blue = img[r][c][2]
        img_seg[r, c] = 1 if red > 155 and 180 > green > 100 and blue < 140 else 0


fig, ax = plt.subplots(1, 2)

ax[0].imshow(img)
ax[1].imshow(img_seg, cmap='gray')
plt.show()
