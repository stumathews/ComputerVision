# Pull in imread from sk-image
from skimage.io import imread
from skimage.color import rgb2gray
from skimage.util import invert
# Pull in pyploy from matplotlib
import matplotlib.pyplot as plot
from skimage import data
from numpy.linalg import norm
import numpy as np


print('1) Reading Peppers.jpg')
# read with imread, note this results in a matrix of intensities for each pixel in the image
peppers = imread('Peppers.jpg')
print(f'2) The resultant matrix shape is {peppers.shape}, which is 777rowsx1024cols with each item consisting of a '
      f'3-tuple colour in range 0-255')
print(f'3) The matrix contains items of type: {peppers.dtype}')

plot.imshow(peppers)
plot.show()

# Lets produce a negative image:
print('4) Produce a negative image by subtracting each elements intensity from the max intensity of 255')
neg_image = 255 - peppers
plot.imshow(neg_image)
plot.show()

# Lets set the Red and blue channels to 0
print('5) Performing a vector-vector multiplication which multiples element for element, masking red and green values')
change = peppers[:, :]
p = change[:, :] * [0, 1, 0]  # This does a vector multiplication, element-wise
print(p.shape)
plot.imshow(p)
plot.show()

print('5) Alternative way to reduce to colors to just red values ie not [r,g,b] but just [r]')
img_r = peppers[:, :, 0]  # seems to just bring back the first element for all row and cols
print(img_r.shape)
fig, ax = plot.subplots(1, 2)
ax[0].imshow(img_r, cmap='gray')
ax[1].imshow(img_r + 100, cmap='gray')
plot.show()

print('6) Gray scale an image using rgb2gray. This turns of the datatype into float and scales it in range[0,1].'
      ' It also reduces the channels from 3 to 1')
grey_img = rgb2gray(peppers)
plot.imshow(grey_img, cmap='gray')
plot.show()

print('7) Iterating through the image manually')
copy_peppers = peppers.copy()
[rows, cols, depth] = copy_peppers.shape
for row in range(rows):
    for col in range(cols):
        copy_peppers[row][col][0] = 0  # Set the red channel to 0, leave blue and green as-is
plot.imshow(copy_peppers)
plot.show()

print('8) access to contents directly without iterating, here we are setting the'
      ' first and 2nd element of the 3-tuple channel to 123! Amazing!')
copy_peppers[:, :, [0, 1]] = 123
plot.imshow(copy_peppers)
plot.show()

print('9) You can use utils functions too, you know: invert')
copy_peppers = peppers.copy()
neg_peppers = invert(copy_peppers)
plot.imshow(neg_peppers)
plot.show()

print('10) Swap the blue and red channels, leaving the green unchanged')
copy_peppers = peppers.copy()
swap_candidate_channels = copy_peppers[:, :, [1, 2]]
copy_peppers[:, :, [1, 2]] = swap_candidate_channels[:, :, [1, 0]]
plot.imshow(copy_peppers)
plot.show()

print('11) add a vignette')
cat = data.chelsea()
cat_vign = cat.copy()

# Change intensity of pixel colour, depending on the distance the pixel is from the centre of the image
import math
from scipy.interpolate import interp1d

[rows, cols, depth] = cat_vign.shape
center_x = cols / 2
center_y = rows / 2
max_distance = math.sqrt(center_x + center_y)
m = interp1d([0, max_distance], [0, 255])

v_center = [center_x, center_y, 0]

def brightness(r, image_width):
    return math.exp(-r / image_width)


for y in range(rows):
    for x in range(cols):
        # determine distance from center
        me = np.array([x, y, 0])
        #p = np.array([x, center_x])
        #q = np.array([center_x, y])
        #hyp = q - p
        dist = np.linalg.norm(v_center - me)
        #distance = norm(hyp) #math.sqrt(center_x - x) + (center_y - y)
        cat_vign[y][x] = brightness(dist, cols)
plot.imshow(cat)
plot.show()
